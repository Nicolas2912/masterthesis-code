import os
from dataclasses import dataclass, field # Added field
from pathlib import Path
from typing import List, Tuple, Optional, Dict, Any, Union
import time
import pickle
import re
import logging
import gc # Import gc for garbage collection

import numpy as np
import torch
# Removed torchvision transforms not directly used now
# from PIL import Image # Keep PIL if needed elsewhere, but processor handles image loading
# from torchvision.transforms.functional import InterpolationMode # Removed

# Transformers and Qwen specific imports
from transformers import Qwen2_5_VLForConditionalGeneration, AutoProcessor
from qwen_vl_utils import process_vision_info

# SentenceTransformer import kept in case it's used elsewhere, but not for core generation
# from sentence_transformers import SentenceTransformer

# Removed lmdeploy imports
# from lmdeploy import pipeline, TurbomindEngineConfig, GenerationConfig
# from lmdeploy.vl import load_image

from tqdm import tqdm
from functools import cached_property
import fitz # PyMuPDF

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ImageConfig:
    """Configuration for image processing parameters. (May be less relevant with AutoProcessor)"""
    input_size: int = 448 # Note: Qwen's processor handles resizing implicitly
    max_num: int = 12
    min_num: int = 1
    use_thumbnail: bool = True
    # Imagenet stats might not be directly applied but kept for reference
    imagenet_mean: Tuple[float, float, float] = (0.485, 0.456, 0.406)
    imagenet_std: Tuple[float, float, float] = (0.229, 0.224, 0.225)


@dataclass
class ImageDescription:
    """Data class for storing image descriptions and metadata."""
    image_path: Path
    description: str
    embedding: Optional[np.ndarray] = None


@dataclass
class ModelConfig:
    """Configuration for model parameters."""
    # Updated model path for the official Qwen model
    model_path: str = "Qwen/Qwen2.5-VL-32B-Instruct"
    # Using "auto" lets transformers handle dtype based on availability/model config
    torch_dtype: Union[str, torch.dtype] = "auto" # Changed to "auto"
    device_map: str = "auto"
    # Removed parameters less relevant for standard from_pretrained or handled differently
    # low_cpu_mem_usage: bool = True
    # offload_folder: str = "model_offload"
    # use_flash_attn: bool = False # Set to True if enabling flash_attention_2
    attn_implementation: Optional[str] = None # Use "flash_attention_2" for optimization if installed

    # Simplified generation config, primarily max_new_tokens
    generation_config: Dict[str, Any] = field(default_factory=lambda: {
        'max_new_tokens': 256, # Reduced for short summary
        'do_sample': False,    # Often better for factual description/summary
        'temperature': 0.1,   # Low temperature for focused output
    })

    # post_init removed as generation_config now uses field(default_factory=...)


class InternVLChatModel: # Consider renaming class if only using Qwen now
    """
    A class implementing the Qwen2.5-VL model with image processing capabilities
    using Hugging Face Transformers.
    """

    def __init__(
            self,
            model_config: Optional[ModelConfig] = None,
            image_config: Optional[ImageConfig] = None, # Kept but less critical
            pdf_path: str = None,
            images_dir: str = None,
            context_pages_before: int = 2,
            context_pages_after: int = 2,
            save_dir_image_descriptions: str = None
    ):
        """Initialize with model loading"""
        self.model_config = model_config or ModelConfig()
        self.image_config = image_config or ImageConfig() # Kept for potential future use

        self.descriptions: List[ImageDescription] = [] # Initialize descriptions list

        # Store paths that can be updated per document
        self.pdf_path = pdf_path
        self.images_dir = images_dir
        self.save_dir_image_descriptions = save_dir_image_descriptions

        # Initialize the model and processor
        self._initialize_hf_model()

        # Initialize context extractor if paths are provided
        self.context_extractor = None
        if pdf_path and images_dir:
            self.context_extractor = PDFContextExtractor(
                pdf_path=pdf_path,
                images_dir=images_dir,
                context_pages_before=context_pages_before,
                context_pages_after=context_pages_after
            )

    # Removed load_image - processor handles it internally via paths/URLs
    # def load_image(self, image_path: Union[str, Path]) -> Any:
    #     return load_image(str(image_path))

    def _initialize_hf_model(self) -> None:
        """Initialize the Qwen model and processor using Transformers."""
        logger.info(f"Loading Qwen model from: {self.model_config.model_path}")
        try:
            self.model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
                self.model_config.model_path,
                torch_dtype=self.model_config.torch_dtype,
                device_map=self.model_config.device_map,
                attn_implementation=self.model_config.attn_implementation, # Pass attn_implementation
                trust_remote_code=True # Often needed for custom model code
            ).eval()

            logger.info(f"Loading processor from: {self.model_config.model_path}")
            self.processor = AutoProcessor.from_pretrained(
                self.model_config.model_path,
                trust_remote_code=True
            )
            logger.info("Model and processor loaded successfully.")
            # Log device placement
            try:
                logger.info(f"Model is on device: {self.model.device}")
            except Exception:
                 logger.warning("Could not determine model device automatically.")


        except Exception as e:
            logger.error(f"Failed to initialize model or processor: {str(e)}")
            raise RuntimeError(f"Failed to initialize model or processor: {str(e)}")


    # Removed _initialize_model, _initialize_transform (processor handles transform)
    # Removed chat (replaced by generate_image_description_qwen logic)

    def _create_base_prompt(self) -> str:
        """Create the base prompt for a short image summary."""
        # Changed prompt to request a short summary
        return "Provide a short and correct summary of this image, focusing on its main subject and purpose."


    def _enhance_prompt_with_context(self, image_path: str, base_prompt: str) -> str:
        """
        Enhance the base prompt with document context. (No changes needed here, logic is sound)
        """
        enhanced_prompt = base_prompt # Default to base if no context

        if not self.context_extractor:
            logger.warning("Context extractor not available, using base prompt.")
            return base_prompt

        try:
            image_filename = Path(image_path).name
            context = self.context_extractor.get_image_context(image_filename)

            if not context:
                logger.warning(f"No context found for {image_filename}, using base prompt.")
                return base_prompt

            # Constructing the context string - adjusted formatting slightly
            context_text = f"Surrounding Document Context:\n"
            if context.caption:
                 context_text += f"Figure Caption: {context.caption}\n\n"
            if context.before_context:
                context_text += f"Context Before Image (Previous Pages/Text):\n{context.before_context}\n\n"
            if context.current_page_context:
                context_text += f"Context on Image Page:\n{context.current_page_context}\n\n"
            if context.after_context:
                context_text += f"Context After Image (Following Pages/Text):\n{context.after_context}\n"

            # Combine context with the base prompt instruction
            enhanced_prompt = f"{context_text}\nBased on the image and the surrounding context, {base_prompt}"

        except Exception as e:
            logger.error(f"Failed to enhance prompt with context for {image_path}: {str(e)}. Using base prompt.")
            # Fallback to base prompt in case of error during context enhancement
            enhanced_prompt = base_prompt

        return enhanced_prompt

    # Renamed and completely rewritten for Qwen+Transformers
    def generate_image_description_qwen(self, image_path: Union[str, Path]) -> str:
        """
        Generate a short description for a single image using Qwen model.

        Args:
            image_path: Path to the image file

        Returns:
            Short description/summary of the image
        """
        try:
            image_path_str = str(image_path)
            logger.debug(f"Generating description for: {image_path_str}")

            # 1. Create the prompt (potentially enhanced with context)
            base_prompt = self._create_base_prompt()
            enhanced_prompt = self._enhance_prompt_with_context(image_path_str, base_prompt)

            # 2. Format messages for the processor
            # Using the local image path directly. process_vision_info should handle it.
            messages = [
                {
                    "role": "user",
                    "content": [
                        {"type": "image", "image": image_path_str},
                        {"type": "text", "text": enhanced_prompt},
                    ],
                }
            ]

            # 3. Prepare inputs using the processor
            text = self.processor.apply_chat_template(
                messages, tokenize=False, add_generation_prompt=True
            )
            logger.debug(f"Formatted text template: {text[:500]}...") # Log beginning of text

            image_inputs, video_inputs = process_vision_info(messages) # video_inputs will be None
            logger.debug(f"Processed vision info: {len(image_inputs)} images")

            inputs = self.processor(
                text=[text], # Note: text needs to be in a list
                images=image_inputs,
                videos=video_inputs,
                padding=True,
                return_tensors="pt",
            )

            # Move inputs to the same device as the model
            inputs = inputs.to(self.model.device)
            logger.debug(f"Inputs moved to device: {inputs.input_ids.device}")


            # 4. Generate response
            start = time.time()
            logger.debug("Starting model generation...")
            with torch.no_grad(): # Disable gradient calculation for inference
                 generated_ids = self.model.generate(
                     **inputs,
                     # Pass generation parameters from config
                     max_new_tokens=self.model_config.generation_config.get('max_new_tokens', 256),
                     do_sample=self.model_config.generation_config.get('do_sample', False),
                     temperature=self.model_config.generation_config.get('temperature', 0.1),
                     # Add other relevant parameters if needed (e.g., top_p, top_k)
                 )
            logger.debug("Model generation finished.")
            print(f"Time for response generation: {time.time() - start:.2f}s") # Changed log level


            # 5. Decode the output
            # Trim the input IDs from the generated IDs
            generated_ids_trimmed = [
                out_ids[len(in_ids):] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
            ]

            output_text = self.processor.batch_decode(
                generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
            )

            # Since we process one image at a time, output_text is a list with one element
            description = output_text[0] if output_text else ""
            logger.debug(f"Generated Description: {description}")

            return description

        except Exception as e:
            logger.error(f"Failed to generate description for {image_path}: {str(e)}")
            # Reraise to be caught by the processing loop, but log details here
            raise RuntimeError(f"Failed to generate description for {image_path}: {str(e)}")

    def process_directory(self, directory: Union[str, Path], save_path: Optional[Union[str, Path]] = None, batch_size: int = 10):
        # This method remains largely the same, just calls the new generation function
        directory = Path(directory)
        # Consider adding other common image extensions if needed
        image_paths = list(directory.glob("*.png")) + list(directory.glob("*.jpg")) + list(directory.glob("*.jpeg"))
        total_images = len(image_paths)

        if not image_paths:
            logger.warning(f"No images found in {directory}") # Changed to warning
            return [] # Return empty list if no images

        # Sort image paths for consistent processing order (optional but good practice)
        image_paths.sort()

        try:
            # Clear previous descriptions if processing a new directory with the same instance
            self.descriptions = []
            current_image_idx = 0 # Renamed for clarity

            # Process images - using batch_size conceptually for saving, but generating one by one
            # The original batching logic was mainly for saving, let's keep that structure
            for i in range(0, len(image_paths), batch_size):
                batch_paths = image_paths[i:i + batch_size]
                batch_processed_count = 0 # Track progress within the batch for saving

                for img_path in batch_paths:
                    current_image_idx += 1
                    print(f"\nProcessing image {current_image_idx}/{total_images}: {img_path.name}") # Use print for progress

                    try:
                        # Call the updated generation function
                        description = self.generate_image_description_qwen(img_path)

                        img_desc = ImageDescription(
                            image_path=img_path,
                            description=description
                            # Embedding generation would need a separate step if required
                        )
                        self.descriptions.append(img_desc)
                        batch_processed_count += 1

                    except Exception as e:
                        # Log error but continue with the next image
                        logger.error(f"Error processing image {img_path.name}: {str(e)}")
                        # Optionally add a placeholder or skip adding to descriptions
                        # self.descriptions.append(ImageDescription(image_path=img_path, description="Error during generation"))
                        continue
                    finally:
                         # Clear CUDA cache more frequently (after each image)
                         if torch.cuda.is_available():
                             torch.cuda.empty_cache()
                         gc.collect() # Force garbage collection

                # Save intermediate results after each conceptual batch
                if batch_processed_count > 0 and save_path: # Only save if something was processed in the batch and save_path is provided
                    try:
                        # Ensure save directory exists
                        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
                        self.store_descriptions_by_page(save_path)
                        logger.info(f"Saved intermediate results ({len(self.descriptions)} total) to {save_path}")
                    except Exception as e:
                        logger.error(f"Error saving intermediate results: {str(e)}")

                # Force garbage collection between batches
                gc.collect()
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()

            logger.info(f"Finished processing directory {directory}. Total descriptions generated: {len(self.descriptions)}")
            return self.descriptions

        except Exception as e:
            logger.error(f"Critical error during directory processing: {str(e)}")
             # Save what we have if there's an error and save_path is defined
            if len(self.descriptions) > 0 and save_path:
                try:
                    Path(save_path).parent.mkdir(parents=True, exist_ok=True)
                    self.store_descriptions_by_page(save_path)
                    logger.info(f"Saved partial results ({len(self.descriptions)} descriptions) before error to {save_path}")
                except Exception as save_error:
                    logger.error(f"Error saving partial results after critical error: {str(save_error)}")

            raise RuntimeError(f"Failed to process directory: {str(e)}")

        finally:
            # Final cleanup (optional, as __del__ should handle it too)
            gc.collect()
            if torch.cuda.is_available():
                torch.cuda.empty_cache()


    # store_descriptions_by_page remains the same - logic is independent of model
    def store_descriptions_by_page(self, save_path) -> None:
        """
        Store image descriptions in a dictionary organized by page number.
        The dictionary is saved using pickle with the document name.
        """
        try:
            page_descriptions = {}
            for desc in self.descriptions:
                image_name = Path(desc.image_path).name
                # Robust pattern matching for page/figure numbers
                match = re.match(r'page_(\d+)[_-]figure_(\d+)', image_name, re.IGNORECASE) # More flexible pattern
                if not match:
                    logger.warning(f"Could not extract page/figure number from {image_name}, skipping storage for this entry.")
                    continue

                page_num = int(match.group(1))
                figure_num = int(match.group(2))

                description_entry = {
                    'figure_number': figure_num,
                    'description': desc.description,
                    'image_path': str(desc.image_path)
                }

                if page_num not in page_descriptions:
                    page_descriptions[page_num] = []
                page_descriptions[page_num].append(description_entry)

            for page_num in page_descriptions:
                page_descriptions[page_num].sort(key=lambda x: x['figure_number'])

            # Ensure directory exists before saving
            Path(save_path).parent.mkdir(parents=True, exist_ok=True)
            with open(save_path, 'wb') as f:
                pickle.dump(page_descriptions, f)
            logger.info(f"Stored descriptions for {len(page_descriptions)} pages in {save_path}")

            total_descriptions = sum(len(descs) for descs in page_descriptions.values())
            if page_descriptions: # Avoid division by zero
                 avg_desc_per_page = total_descriptions / len(page_descriptions)
                 logger.info(f"Total descriptions stored: {total_descriptions}, Avg per page: {avg_desc_per_page:.2f}")
            else:
                 logger.info(f"Total descriptions stored: {total_descriptions}")


        except Exception as e:
            logger.error(f"Error storing descriptions: {str(e)}")
            raise # Re-raise to signal failure


    # save_index remains the same (doesn't depend on the model directly)
    def save_index(self, save_path: Union[str, Path]) -> None:
        """
        Save the index and descriptions as a pickle file.

        Args:
            save_path: Directory to save the index and metadata
        """
        save_path = Path(save_path)
        save_path.mkdir(parents=True, exist_ok=True)

        try:
            # Save descriptions (without embeddings to save space)
            descriptions_to_save = [
                ImageDescription(
                    image_path=desc.image_path,
                    description=desc.description
                )
                for desc in self.descriptions
            ]
            with open(save_path / "descriptions.pkl", "wb") as f:
                pickle.dump(descriptions_to_save, f)
            logger.info(f"Saved raw descriptions list to {save_path / 'descriptions.pkl'}")

        except Exception as e:
            logger.error(f"Failed to save index: {str(e)}")
            raise RuntimeError(f"Failed to save index: {str(e)}")

    def __del__(self):
        """Cleanup resources when the object is destroyed."""
        logger.info("Cleaning up Qwen model resources...")
        # Delete model and processor attributes
        if hasattr(self, 'model') and self.model is not None:
            try:
                del self.model
                logger.info("Model deleted.")
            except Exception as e:
                logger.warning(f"Warning: Failed to delete model attribute: {str(e)}")
        if hasattr(self, 'processor') and self.processor is not None:
            try:
                del self.processor
                logger.info("Processor deleted.")
            except Exception as e:
                 logger.warning(f"Warning: Failed to delete processor attribute: {str(e)}")

        # Explicitly clear CUDA cache and collect garbage
        if torch.cuda.is_available():
            logger.info("Clearing CUDA cache.")
            torch.cuda.empty_cache()
        gc.collect()
        logger.info("Cleanup finished.")


# ============================================
# PDFContextExtractor and related classes
# No changes needed in these classes as they
# are independent of the VL model implementation.
# ============================================
@dataclass
class ImageContext:
    """Data class to store image context information"""
    image_path: str
    page_number: int
    figure_number: int
    caption: Optional[str]  # Added caption field
    before_context: str
    current_page_context: str
    after_context: str

    @property
    def full_context(self) -> str:
        """Combine all context parts into a single string"""
        caption_text = f"\nCaption: {self.caption}" if self.caption else ""
        return f"""
        {caption_text}

        Previous Context:
        {self.before_context}

        Current Page Context:
        {self.current_page_context}

        Following Context:
        {self.after_context}
        """

class PDFContextExtractor:
    def __init__(
            self,
            pdf_path,
            images_dir: str,
            context_pages_before: int = 2,
            context_pages_after: int = 2
    ):
        self.pdf_path = Path(pdf_path)
        self.images_dir = Path(images_dir)
        self.context_pages_before = context_pages_before
        self.context_pages_after = context_pages_after

        if not self.pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        if not self.images_dir.exists():
            raise FileNotFoundError(f"Images directory not found: {images_dir}")

        self.doc = fitz.open(str(self.pdf_path))
        logger.info(f"Loaded PDF '{self.pdf_path.name}' with {len(self.doc)} pages")
        self._page_text_cache: Dict[int, str] = {}

    def __del__(self):
        if hasattr(self, 'doc') and self.doc:
            try:
                self.doc.close()
                logger.info(f"Closed PDF document '{self.pdf_path.name}'")
            except Exception as e:
                 logger.warning(f"Error closing PDF document {self.pdf_path.name}: {e}")


    def _clean_text(self, text: str) -> str:
        text = re.sub(r'Page \d+ of \d+', '', text)
        text = re.sub(r'^\s*\d+\s*$', '', text, flags=re.MULTILINE)
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'^\s+|\s+$', '', text, flags=re.MULTILINE)
        return text.strip()

    def _extract_page_text(self, page_number: int) -> str:
        if page_number in self._page_text_cache:
            return self._page_text_cache[page_number]
        if 0 <= page_number < len(self.doc):
            try:
                page = self.doc[page_number]
                text = page.get_text("text") # Specify text format
                cleaned_text = self._clean_text(text)
                self._page_text_cache[page_number] = cleaned_text
                return cleaned_text
            except Exception as e:
                 logger.error(f"Error extracting text from page {page_number+1} of {self.pdf_path.name}: {e}")
                 return "" # Return empty string on error
        return ""

    def _parse_image_filename(self, filename: str) -> Optional[Tuple[int, int]]:
        """Extract page number and figure number from image filename"""
        # Using the more flexible pattern from store_descriptions_by_page
        pattern = r'page_(\d+)[_-]figure_(\d+)'
        match = re.match(pattern, Path(filename).stem, re.IGNORECASE)
        if not match:
            logger.warning(f"Could not parse page/figure number from filename: {filename}")
            return None # Return None if parsing fails
        return int(match.group(1)), int(match.group(2))

    def _get_context_range(self, page_number: int) -> Tuple[int, int]:
        """Calculate the valid page range for context (0-based index)"""
        start_page = max(0, page_number - self.context_pages_before)
        end_page = min(len(self.doc) - 1, page_number + self.context_pages_after)
        return start_page, end_page

    def get_pages_from_extracted_images(self, images_dir: Union[str, Path]) -> Dict[int, List[str]]:
        """ Get page numbers (1-based) and filenames """
        images_dir = Path(images_dir)
        page_to_images = {}
        pattern = r'page_(\d+)[_-]figure_(\d+)\.(png|jpe?g|bmp|gif)' # More extensions

        try:
            for image_path in images_dir.glob("*.*"): # Check all files
                match = re.match(pattern, image_path.name, re.IGNORECASE)
                if match:
                    page_num = int(match.group(1)) # 1-based page number from filename
                    if page_num not in page_to_images:
                        page_to_images[page_num] = []
                    page_to_images[page_num].append(image_path.name)

            logger.info(f"Found images on {len(page_to_images)} pages in {images_dir.name}")
            return page_to_images

        except Exception as e:
            logger.error(f"Error getting pages from images in {images_dir.name}: {str(e)}")
            return {}

    def find_figure_captions(self, page_to_images: Dict[int, List[str]]) -> Dict[str, str]:
        """ Find captions only on pages where we have extracted images. """
        image_captions = {}
        try:
            for page_num in page_to_images.keys(): # page_num is 1-based here
                pdf_page_idx = page_num - 1 # Convert to 0-based index for PyMuPDF
                if not (0 <= pdf_page_idx < len(self.doc)):
                    logger.warning(f"Page number {page_num} from image filename is out of bounds for PDF {self.pdf_path.name}.")
                    continue

                page = self.doc[pdf_page_idx]
                text = page.get_text("text") # Use "text" for better layout preservation

                # Updated pattern for common figure captions (more robust)
                # Looks for "Fig.", "Figure", etc., followed by numbers/letters, optional colon, and text until newline
                pattern = r'(Fig(?:ure)?\.?\s+\d+(?:[\.\-]\d+)*\s*(?:\([a-zA-Z]\))?)\s*:?\s*([^\n]+)'

                matches = re.finditer(pattern, text, re.IGNORECASE)
                found_captions_on_page = {}
                for match in matches:
                    fig_identifier = match.group(1).strip() # e.g., "Fig. 1.2"
                    caption_text = match.group(2).strip()
                    # Simple normalization of identifier for matching (e.g., remove dots, spaces)
                    # normalized_id = re.sub(r'[.\s]+', '', fig_identifier)
                    found_captions_on_page[fig_identifier] = caption_text
                    logger.debug(f"Found potential caption on page {page_num}: '{fig_identifier}: {caption_text}'")


                # Associate captions with image filenames based on order or explicit number matching (simple order for now)
                sorted_images = sorted(
                    page_to_images[page_num],
                    key=lambda x: int(re.match(r'page_\d+.*[_-]figure_(\d+)', x, re.IGNORECASE).group(1))
                )

                # Convert found caption keys (like "Fig. 1.2") to simple numbers for matching figure number in filename
                # This is complex and error-prone. A simpler approach: assume order matches.
                # If captions are found, assign them sequentially to sorted images on that page.
                caption_texts = list(found_captions_on_page.values())

                for idx, img_file in enumerate(sorted_images):
                    if idx < len(caption_texts):
                         image_captions[img_file] = caption_texts[idx]
                         logger.info(f"Assigned caption to {img_file} on page {page_num}: '{caption_texts[idx]}'")
                    else:
                         logger.warning(f"Found image {img_file} on page {page_num} but no corresponding caption found/matched.")


            return image_captions

        except Exception as e:
            logger.error(f"Error finding captions for {self.pdf_path.name}: {str(e)}")
            return {}

    # extract_all_captions, find_image_references, enhance_prompt_with_context methods remain unchanged
    def extract_all_captions(self, images_dir: Union[str, Path]) -> Dict[str, str]:
        """ Main function to extract captions for all images in directory. """
        try:
            page_to_images = self.get_pages_from_extracted_images(images_dir)
            if not page_to_images:
                logger.warning(f"No images found in directory {images_dir}")
                return {}
            image_captions = self.find_figure_captions(page_to_images)
            logger.info(f"Found {len(image_captions)} captions for images in {images_dir.name}")
            return image_captions
        except Exception as e:
            logger.error(f"Error extracting captions from {images_dir.name}: {str(e)}")
            return {}

    def find_image_references(self, images_dir: Union[str, Path], context_words: int = 50) -> Dict[str, List[Dict[str, Any]]]:
        """ Find references to figures across the document. (Logic unchanged) """
        # ... (Keep existing implementation, ensure logging/error handling is robust) ...
        # Placeholder - Add the existing implementation here
        logger.warning("find_image_references implementation not fully shown, assuming it exists and works.")
        return {} # Placeholder return

    def get_image_context(self, image_filename: str) -> Optional[ImageContext]:
        """ Get the context for a specific image. """
        try:
            parsed_info = self._parse_image_filename(image_filename)
            if parsed_info is None:
                return None # Error already logged by parser
            page_number, figure_number = parsed_info # 1-based page number

            pdf_page_idx = page_number - 1 # 0-based index for PyMuPDF

            if not (0 <= pdf_page_idx < len(self.doc)):
                 logger.error(f"Page number {page_number} for image {image_filename} is out of PDF bounds ({len(self.doc)} pages).")
                 return None

            start_page_idx, end_page_idx = self._get_context_range(pdf_page_idx)

            # Get caption (more robustly)
            captions_on_page = self.find_figure_captions({page_number: [image_filename]})
            caption = captions_on_page.get(image_filename)

            before_context = "\n---\n".join( # Use separator for clarity
                self._extract_page_text(i)
                for i in range(start_page_idx, pdf_page_idx)
            )
            current_page_context = self._extract_page_text(pdf_page_idx)
            after_context = "\n---\n".join( # Use separator
                self._extract_page_text(i)
                for i in range(pdf_page_idx + 1, end_page_idx + 1)
            )

            # Basic filtering of context if it's identical to caption
            if caption and caption in current_page_context:
                 current_page_context = current_page_context.replace(caption, f"[Caption for Figure {figure_number}]", 1).strip()


            return ImageContext(
                image_path=str(self.images_dir / image_filename),
                page_number=page_number,
                figure_number=figure_number,
                caption=caption,
                before_context=before_context,
                current_page_context=current_page_context,
                after_context=after_context
            )

        except Exception as e:
            logger.error(f"Error extracting context for {image_filename}: {str(e)}")
            return None

    def process_all_images(self) -> Dict[str, ImageContext]:
        """ Process all images in the directory and extract their context. """
        results = {}
        pattern = r'page_(\d+)[_-]figure_(\d+)\.(png|jpe?g|bmp|gif)' # Match common image types
        image_files = [p for p in self.images_dir.glob("*.*") if re.match(pattern, p.name, re.IGNORECASE)]

        logger.info(f"Found {len(image_files)} image files to process for context in {self.images_dir.name}")

        for image_path in image_files:
            try:
                context = self.get_image_context(image_path.name)
                if context:
                    results[image_path.name] = context
            except Exception as e:
                logger.error(f"Error processing context for {image_path.name}: {str(e)}")
                continue # Continue with next image

        logger.info(f"Successfully extracted context for {len(results)} images in {self.images_dir.name}")
        return results

    def get_statistics(self) -> Dict[str, int]:
        """Get statistics about the processed documents"""
        # Count images more reliably
        pattern = r'page_(\d+)[_-]figure_(\d+)\.(png|jpe?g|bmp|gif)'
        total_images = len([p for p in self.images_dir.glob("*.*") if re.match(pattern, p.name, re.IGNORECASE)])

        return {
            "total_pages_in_pdf": len(self.doc),
            "cached_pages_text": len(self._page_text_cache),
            "total_images_in_dir": total_images
        }


# ============================================
# Main Execution Logic
# ============================================

def get_all_pdfs_in_directory(directory):
    all_pdfs_paths = []
    try:
        for file in os.listdir(directory):
            if file.lower().endswith(".pdf"): # Case-insensitive check
                list_of_pdfs = os.path.join(directory, file)
                all_pdfs_paths.append(list_of_pdfs)
        logger.info(f"Found {len(all_pdfs_paths)} PDF documents in {directory}")
    except FileNotFoundError:
         logger.error(f"PDF directory not found: {directory}")
         return []
    except Exception as e:
         logger.error(f"Error listing PDFs in {directory}: {e}")
         return []
    return all_pdfs_paths


def process_documents(pdf_dir: str, base_images_dir: str, base_save_dir: str):
    """
    Processes all PDF documents found in pdf_dir.
    Args:
        pdf_dir: Directory containing PDF files.
        base_images_dir: Base directory where extracted figures subdirectories are located.
        base_save_dir: Base directory to save the output pickle files.
    """
    all_pdfs = get_all_pdfs_in_directory(pdf_dir)
    if not all_pdfs:
        logger.error("No PDF documents found to process.")
        return

    logger.info(f"Found PDFs: {[Path(p).name for p in all_pdfs]}")

    # Create a single model instance outside the loop
    chat_model = None
    try:
        logger.info("Initializing Qwen VL model (this may take a while)...")
        # Consider adding flash attention if installed and GPU supports it
        # model_cfg = ModelConfig(attn_implementation="flash_attention_2")
        model_cfg = ModelConfig() # Use default config
        chat_model = InternVLChatModel(model_config=model_cfg)
        logger.info("Model initialized successfully.")

        # Optional: Prioritize or sort PDFs if needed
        # sorted_pdfs = sorted(all_pdfs,
        #             key=lambda x: 0 if Path(x).stem == priority_document else 1)
        sorted_pdfs = sorted(all_pdfs) # Simple alphabetical sort

        # Process each PDF
        for pdf_path in sorted_pdfs:
            document_name = Path(pdf_path).stem
            logger.info(f"===== Processing document: {document_name} =====")

            # Construct document-specific paths
            images_dir = os.path.join(base_images_dir, document_name)
            save_path = os.path.join(base_save_dir, f"{document_name}_image_description.pkl")

            # Check if images directory exists
            if not os.path.isdir(images_dir):
                logger.warning(f"Images directory not found for {document_name}, skipping: {images_dir}")
                continue

            # Ensure save directory exists
            os.makedirs(Path(save_path).parent, exist_ok=True)

            # Update model's document-specific attributes
            logger.info(f"Updating context extractor for: {document_name}")
            chat_model.pdf_path = pdf_path
            chat_model.images_dir = images_dir
            # Re-initialize context extractor for the new document
            try:
                 chat_model.context_extractor = PDFContextExtractor(
                    pdf_path=pdf_path,
                    images_dir=images_dir,
                    context_pages_before=1, # Keep context window small for efficiency
                    context_pages_after=1
                 )
                 logger.info("Context extractor updated.")
            except FileNotFoundError as fnf_error:
                 logger.error(f"Error initializing context extractor for {document_name}: {fnf_error}. Skipping document.")
                 # Clean up context extractor if partially initialized
                 if hasattr(chat_model, 'context_extractor'):
                      del chat_model.context_extractor
                 chat_model.context_extractor = None
                 continue # Skip to the next document


            # Process the document's images
            try:
                 logger.info(f"Starting image processing for {document_name}...")
                 # Process the directory and save directly using the method
                 descriptions = chat_model.process_directory(
                    images_dir,
                    save_path=save_path,
                    batch_size=10 # Batch size for saving frequency
                 )
                 logger.info(f"Finished processing for {document_name}. Generated {len(descriptions)} descriptions.")

            except Exception as doc_proc_error:
                 logger.error(f"Error processing document {document_name}: {doc_proc_error}")
                 # Error handling within process_directory should save partial results
                 # Continue to the next document

            finally:
                # Clean up document-specific resources (context extractor)
                if hasattr(chat_model, 'context_extractor') and chat_model.context_extractor:
                    del chat_model.context_extractor
                    chat_model.context_extractor = None
                    logger.info(f"Cleaned up context extractor for {document_name}.")

                # Force garbage collection between documents
                gc.collect()
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()
                logger.info("Performed cleanup between documents.")
            logger.info(f"===== Finished document: {document_name} =====")

    except Exception as e:
        logger.critical(f"A critical error occurred during model initialization or document loop: {str(e)}", exc_info=True)
        # raise # Optionally re-raise the exception
    finally:
        # Clean up model resources once all documents are processed or if an error occurs
        if chat_model is not None:
            logger.info("Deleting main chat model instance.")
            del chat_model
            chat_model = None # Ensure it's cleared
            # Final cleanup
            gc.collect()
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            logger.info("Final model cleanup complete.")


# Example usage
if __name__ == "__main__":
    # --- Configuration ---
    # Set Correct Paths for your environment (Linux example)
    pdf_dir_server = "/example/path/to/pdf"
    images_base_dir_server = "/example/path/to/images" # Base dir containing subdirs named after PDFs
    save_base_dir_server = "/example/path/to/save" # Base dir to save pickle files

    # Ensure save directory exists
    os.makedirs(save_base_dir_server, exist_ok=True)

    # --- Run Processing ---
    logger.info("Starting document processing script.")
    process_documents(pdf_dir_server, images_base_dir_server, save_base_dir_server)
    logger.info("Document processing script finished.")
