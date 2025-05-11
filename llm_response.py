# llm_response.py
# Standard library imports
import time
import pickle
from pathlib import Path
from typing import Dict, List, Literal, Optional, Tuple, Union # Added Union
import gc # Import gc for garbage collection

# Third party imports
import torch
from sentence_transformers import CrossEncoder
# Import specific classes for Qwen-VL
from transformers import (
    Qwen2_5_VLForConditionalGeneration, # Changed from AutoModelForCausalLM
    AutoProcessor,                     # Changed from AutoTokenizer
    BitsAndBytesConfig
)
# Import Qwen VL utils
from qwen_vl_utils import process_vision_info

# Local application imports
from data_models import Chunk, ImageMetadata, RAGResponse
from document_retrieval import DocumentRetriever # Assuming this remains the same

class EnhancedRetriever:
    """Enhanced retriever that combines vector search with Qwen-VL processing"""

    def __init__(
            self,
            index_dir: str,
            document_name: str,
            # Update default model name
            model_name: str = "unsloth/Qwen2.5-VL-32B-Instruct-unsloth-bnb-4bit",
            cross_encoder_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2",
            max_text_tokens: int = 8000,    # default text‐token limit
            max_image_references: int = 15, # default image limit
            max_context_tokens: int = None, # alias → max_text_tokens
            device: str = None,
            rerank: bool = False,
        ):
        # Set instance variables
        self.rerank = rerank
        self.document_name = document_name
        self.index_dir = Path(index_dir) # Use Path object
        self.max_text_tokens = max_text_tokens
        self.max_image_references = max_image_references
        # alias context limit if provided
        if max_context_tokens is not None:
            max_text_tokens = max_context_tokens
        # enforce defaults if None
        if max_text_tokens is None:
            max_text_tokens = 8000
        if max_image_references is None:
            max_image_references = 15
        # Set instance variables
        self.retrieval_time = 0
        self.generation_time = 0

        # Setup device
        if device is None:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            self.device = device
        print(f"Using device: {self.device}")
        torch.random.manual_seed(0)
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

        # Load image descriptions (still needed to map page/figure to paths)
        self.image_descriptions = self._load_image_descriptions()

        # Initialize base retriever
        self.base_retriever = DocumentRetriever(str(self.index_dir), document_name=self.document_name, model_name="intfloat/multilingual-e5-large-instruct")

        # --- Qwen-VL Model Loading ---
        print(f"Loading model {model_name}...")

        # Configure 4-bit quantization
        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4", # or "fp4" based on unsloth documentation/recommendation
            bnb_4bit_compute_dtype=torch.bfloat16, # Recommended compute dtype
            bnb_4bit_use_double_quant=True,
        )

        try:
            max_pixels = 512*28*28
            self.model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
                model_name,
                quantization_config=quantization_config,
                device_map="auto", # Handles placing layers on devices
                trust_remote_code=True
            ).eval() # Set to evaluation mode

            # Load the corresponding processor
            print(f"Loading processor for {model_name}...")
            self.processor = AutoProcessor.from_pretrained(model_name, trust_remote_code=True, max_pixels=max_pixels)

            print("VL Model and Processor loaded successfully.")
            # Log device placement if possible
            try:
                print(f"Model is mapped to devices: {self.model.hf_device_map}")
            except AttributeError:
                 print(f"Model device map info not readily available, likely using 'auto'.")


        except Exception as e:
            print(f"Error loading Qwen-VL model or processor: {str(e)}")
            raise # Re-raise the exception as it's critical

        # Initialize cross-encoder (if rerank is True) - Keep on CPU to save VRAM
        if self.rerank:
            print(f"Loading cross-encoder {cross_encoder_name}...")
            self.cross_encoder = CrossEncoder(
                cross_encoder_name,
                max_length=512, # Specify max_length
                device="cpu" # Keep on CPU
            )
            print("Cross-encoder loaded on CPU.")

        # Remove the text-generation pipeline initialization
        # self.pipe = pipeline(...)

    def _load_image_descriptions(self) -> Dict[int, List[Dict]]:
        """Load image descriptions from pickle file."""
        try:
            # Use Path object for joining
            descriptions_path = self.index_dir / f"{self.document_name}_image_description.pkl"

            if not descriptions_path.exists():
                print(f"Warning: No image descriptions found at {descriptions_path}")
                return {}

            with open(descriptions_path, 'rb') as f:
                data = pickle.load(f)
                print(f"Loaded image descriptions for {len(data)} pages from {descriptions_path}")
                return data # Should be Dict[int, List[Dict]]
        except Exception as e:
            print(f"Error loading image descriptions: {str(e)}")
            return {}

    # Renamed and modified to return paths and metadata
    def _get_relevant_image_paths(
        self,
        # Function needs all retrieved chunks with scores
        all_retrieved_chunks: List[Tuple[Chunk, float]],
        max_images: int,
        page_range: int = 1 # Add page_range parameter, default to 1
        ) -> List[Dict[str, Union[str, int, float]]]: # Return type includes score
        """
        Gets image paths, prioritizing based on the relevance score of chunks
        on the same page. Also considers images from adjacent pages (+/- page_range).
        Limits the total number of images based on score priority.

        Returns:
            List of dicts, each containing 'page_number', 'figure_number',
            'image_path', and 'relevance_score'.
            The list returned is initially sorted by relevance score (desc).
            The CALLER (_prepare_context_and_messages) will re-sort by page/figure
            for the final prompt text generation.
        """
        print(f"Selecting relevant images based on chunk relevance and +/- {page_range} page range...")

        if not all_retrieved_chunks:
            print("  - No chunks provided for image relevance calculation.")
            return []

        # 1. Map page numbers with DIRECT hits to their highest score
        page_max_scores: Dict[int, float] = {}
        direct_hit_pages = set()
        for chunk, score in all_retrieved_chunks:
            page = chunk.metadata.get('page_number')
            if page is not None:
                direct_hit_pages.add(page)
                try:
                    current_score = float(score)
                    page_max_scores[page] = max(page_max_scores.get(page, -float('inf')), current_score)
                except (ValueError, TypeError):
                    print(f"Warning: Could not convert score '{score}' to float for chunk on page {page}. Skipping score.")
                    if page not in page_max_scores: page_max_scores[page] = -float('inf') # Assign default if page is new

        if not page_max_scores:
            print("  - No valid page numbers found in retrieved chunks.")
            return []
        print(f"  - Direct hit pages with max scores: { {p: f'{s:.4f}' for p, s in sorted(page_max_scores.items())} }")

        # 2. Determine the full set of target pages (direct hits + range)
        target_pages = set(direct_hit_pages) # Start with direct hits
        print(f"  - Expanding range by +/- {page_range} page(s)...")
        for page in direct_hit_pages:
            for i in range(-page_range, page_range + 1):
                if i == 0: continue # Skip the page itself (already added)
                page_to_check = page + i
                if page_to_check > 0: # Ensure valid page number
                    target_pages.add(page_to_check)
        print(f"  - Final target pages to check for images: {sorted(list(target_pages))}")


        # 3. Gather all candidate images from ALL target pages.
        #    Assign actual score if page had a direct hit, else assign very low score.
        candidate_images_with_scores = []
        VERY_LOW_SCORE = -float('inf') # Score for images from adjacent-only pages

        for page_num in sorted(list(target_pages)): # Iterate through all target pages
            # Assign score: actual max score if direct hit, otherwise VERY_LOW_SCORE
            page_score = page_max_scores.get(page_num, VERY_LOW_SCORE)

            # Check if descriptions exist for this page
            if self.image_descriptions and page_num in self.image_descriptions:
                page_image_list = self.image_descriptions[page_num]
                for stored_img_data in page_image_list:
                    # Ensure required keys exist and figure number is usable
                    if ('image_path' in stored_img_data and
                        'figure_number' in stored_img_data and
                        isinstance(stored_img_data['figure_number'], (int, float))):

                        candidate_images_with_scores.append({
                            'page_number': page_num,
                            'figure_number': int(stored_img_data['figure_number']),
                            'image_path': str(stored_img_data['image_path']),
                            'relevance_score': page_score # Use actual score or VERY_LOW_SCORE
                        })
                    else:
                        print(f"Warning: Skipping image data due to missing keys or invalid figure_number on page {page_num}: {stored_img_data}")


        if not candidate_images_with_scores:
            print("  - No valid images found on any target pages.")
            return []
        print(f"  - Found {len(candidate_images_with_scores)} candidate images across target pages.")


        # 4. Sort primarily by relevance score (desc), then page/figure (asc) for stable limiting
        #    Images from adjacent-only pages (with VERY_LOW_SCORE) will naturally end up last.
        candidate_images_with_scores.sort(
            key=lambda x: (x['relevance_score'], -x['page_number'], -x['figure_number']), # Score desc, page/fig asc
            reverse=True
        )


        # 5. Limit the number of images based on this score priority
        selected_images_info_relevance_sorted = candidate_images_with_scores[:max_images]
        print(f"  - Selected top {len(selected_images_info_relevance_sorted)} images based on relevance score (incl. adjacent pages).")

        # --- Optional: Log which pages might have been excluded ---
        # (Keep the previous logging logic here if desired)
        if len(candidate_images_with_scores) > max_images:
            included_pages = {img['page_number'] for img in selected_images_info_relevance_sorted}
            potential_candidate_pages = {img['page_number'] for img in candidate_images_with_scores}
            excluded_pages = potential_candidate_pages - included_pages
            partially_included_pages = set()
            if excluded_pages or len(selected_images_info_relevance_sorted) < len(candidate_images_with_scores):
                scores_of_excluded = {img['relevance_score'] for img in candidate_images_with_scores[max_images:]}
                min_score_excluded = min(scores_of_excluded) if scores_of_excluded else -float('inf')
                last_included_score = selected_images_info_relevance_sorted[-1]['relevance_score'] if selected_images_info_relevance_sorted else -float('inf')

                for img in selected_images_info_relevance_sorted:
                    # Check if this included image's score is low enough that some images on the same page *might* have been cut
                    # Or if its score is the same as the lowest score that got excluded (meaning page was cut mid-way)
                    if img['relevance_score'] <= last_included_score :
                        partially_included_pages.add(img['page_number'])

            print(f"    - Pages with direct hits fully included: {included_pages.intersection(direct_hit_pages) - partially_included_pages}")
            print(f"    - Adjacent-only pages fully included: {included_pages - direct_hit_pages - partially_included_pages}")
            if partially_included_pages.intersection(direct_hit_pages): print(f"    - Pages with direct hits potentially partially included: {partially_included_pages.intersection(direct_hit_pages)}")
            if partially_included_pages - direct_hit_pages: print(f"    - Adjacent-only pages potentially partially included: {partially_included_pages - direct_hit_pages}")
            if excluded_pages: print(f"    - Pages fully excluded (due to lower relevance or limit): {excluded_pages}")
        # --- End optional logging ---


        # 6. Ensure image paths exist and prepare the final list (including scores)
        #    NO final sort by page/figure here - return sorted by relevance
        final_relevant_images = []
        windows = True
        for img_info in selected_images_info_relevance_sorted: # Use the relevance sorted list
            if windows:
                win_path = r"C:\Users\Anwender\Desktop\Nicolas\Dokumente\FH Bielefeld\Optimierung und Simulation\4. Semester\masterthesis\programming\extracted_figures_all"
                img_doc_name = Path(img_info['image_path']).relative_to("/home/operation/extracted_figures")
                img_path = win_path / img_doc_name
                if Path(img_path).exists():
                    # Include score in the returned dictionary
                    final_relevant_images.append({
                        'page_number': img_info['page_number'],
                        'figure_number': img_info['figure_number'],
                        'image_path': img_path,
                        'relevance_score': img_info['relevance_score'] # Keep the score
                    })
                else:
                    print(f"Warning: Selected image path does not exist, skipping final inclusion: {img_path}")
            else:
                img_path = img_info['image_path']
                if Path(img_path).exists():
                    # Include score in the returned dictionary
                    final_relevant_images.append({
                        'page_number': img_info['page_number'],
                        'figure_number': img_info['figure_number'],
                        'image_path': img_path,
                        'relevance_score': img_info['relevance_score'] # Keep the score
                    })
                else:
                    print(f"Warning: Selected image path does not exist, skipping final inclusion: {img_path}")

        print(f"  - Returning {len(final_relevant_images)} existing images, sorted by relevance score (desc).")
        # RETURN THE LIST SORTED BY RELEVANCE SCORE
        return final_relevant_images

    def _rerank_chunks(
            self,
            query: str,
            chunks: List[Tuple[Chunk, float]],
            top_k: int = 10
    ) -> List[Tuple[Chunk, float]]:
        """Rerank chunks using cross-encoder"""
        if not chunks or not self.rerank or not hasattr(self, 'cross_encoder'):
            print("Skipping reranking (disabled, no chunks, or no encoder).")
            return chunks # Return original chunks if reranking is skipped

        print(f"Reranking {len(chunks)} chunks...")
        start_rerank = time.time()
        pairs = [(query, chunk[0].text) for chunk in chunks]
        # Run prediction on CPU
        with torch.no_grad():
             scores = self.cross_encoder.predict(pairs, show_progress_bar=False) # Turn off progress bar
        
        reranked = [(chunk[0], float(score)) for chunk, score in zip(chunks, scores)]
        reranked.sort(key=lambda x: x[1], reverse=True)
        print(f"Reranking took {time.time() - start_rerank:.3f}s")

        return reranked[:top_k]

    # Renamed and heavily modified for Qwen-VL message format
    def _prepare_context_and_messages(
        self,
        query: str,
        chunks: List[Tuple[Chunk, float]]
        ) -> Tuple[List[Dict], List[Dict[str, Union[str, int]]]]:
        """
        Formats text context, identifies relevant images, looks up their descriptions,
        introduces them explicitly in the text prompt using the specified format,
        and constructs the 'messages' list for Qwen-VL.

        Returns:
            Tuple: (messages_list, included_image_info_list)
        """
        # 1. Format Text Chunks (respecting max_text_tokens)
        formatted_text_chunks = []
        current_text_tokens = 0
        final_chunks_in_context = []

        print("Formatting text context...")
        for chunk, score in chunks:
            # Ensure chunk text is string and handle potential None
            chunk_text = chunk.text if chunk.text is not None else ""
            formatted_chunk = f"\n{chunk_text}\n{'=' * 40}"
            chunk_tokens = self._count_tokens(formatted_chunk) # Count tokens for this chunk

            if current_text_tokens + chunk_tokens <= self.max_text_tokens:
                formatted_text_chunks.append(formatted_chunk)
                current_text_tokens += chunk_tokens
                final_chunks_in_context.append((chunk, score)) # Add chunk to the list of used ones
            else:
                print(f"Text context reached token limit ({self.max_text_tokens}). Stopping text inclusion.")
                break # Stop adding text chunks

        print(f"Formatted {len(formatted_text_chunks)} text chunks. Total text tokens: {current_text_tokens}")
        combined_text_context = "\n".join(formatted_text_chunks)


        # 2. Get Relevant Image Paths based on included chunks
        print("Fetching relevant image paths...")
        relevant_images_info = self._get_relevant_image_paths(
            final_chunks_in_context,
            max_images=self.max_image_references
        ) # List[Dict{'page_number', 'figure_number', 'image_path'}]


        # 3. Construct the Textual Introduction for Images (with Descriptions)
        image_introduction_text = ""
        image_paths_for_message = [] # Store paths in order for message construction
        if relevant_images_info:
            print(f"Constructing image introduction block for {len(relevant_images_info)} images with descriptions.")
            # Optional Header - adjust or remove if needed
            image_introduction_text += "**Image References:**\n"

            for i, img_info in enumerate(relevant_images_info):
                target_image_path = img_info['image_path']
                page_num = img_info['page_number']
                filename = Path(target_image_path).name

                # --- Find the description ---
                description = "Description not available." # Default fallback
                if self.image_descriptions and page_num in self.image_descriptions:
                    # Get the list of image dicts for the correct page
                    page_image_list = self.image_descriptions[page_num]
                    # Find the specific image dict by matching the path
                    found_desc = False
                    for stored_img_data in page_image_list:
                        # Ensure paths match (or use filename if paths might differ slightly)
                        if stored_img_data.get('image_path') == target_image_path:
                            description = stored_img_data.get('description', "Description not available.")
                            found_desc = True
                            break # Found the matching image on this page
                    if not found_desc:
                         print(f"Warning: Image path '{target_image_path}' not found in stored descriptions for page {page_num}.")

                else:
                     print(f"Warning: No stored image descriptions found for page {page_num}.")
                # -----------------------------

                # Construct the line in the desired format
                image_introduction_line = f"Image reference {i+1}: {filename}: {description}\n"
                image_introduction_text += image_introduction_line

                image_paths_for_message.append(target_image_path) # Add path for message construction

            image_introduction_text += "---\n" # Separator after image intros
        else:
            print("No relevant images identified to include in the prompt.")


        # 4. Construct the Final Text Prompt for the User Message
        # Combine image introductions, context, and query
        final_text_prompt = f"""{image_introduction_text}
                        **Relevant Document Context:**
                        {combined_text_context}

                        ---
                        **Question:**
                        {query}
                        """

        # 5. Construct the 'messages' list for Qwen-VL
        messages = []

        # -- System Message --
        messages.append({"role": "system", "content": self._create_system_message()})

        # -- User Message --
        user_content = []

        # Add image entries first (in the order they were introduced in the text)
        if image_paths_for_message:
            for img_path in image_paths_for_message:
                # Ensure path exists before adding
                if Path(img_path).exists():
                    # Convert to string so VL processor sees a native str, not a Path
                    user_content.append({"type": "image", "image": str(img_path)})
                else:
                     print(f"Error: Image path does not exist, cannot add to message: {img_path}")


        # Add the single text entry containing the structured prompt
        user_content.append({"type": "text", "text": final_text_prompt})

        messages.append({"role": "user", "content": user_content})

        print(f"Constructed messages list. User role has {len(user_content)} items ({len(image_paths_for_message)} actual image paths included, 1 text block).")
        # print(f"DEBUG: Final Text Prompt Part:\n{final_text_prompt[:1000]}...") # Optional: Print start of text prompt

        # Return messages and the structured image info list
        return messages, relevant_images_info

    def _create_system_message(self) -> str:
        """Create a system message tailored for Qwen-VL with image referencing."""
        # Make instructions even more explicit about using the filename.
        return """
                **Instructions for Answer Generation:**

                **Guiding Principle:** Your primary goal is to provide accurate, context-based answers derived *strictly* from the provided text context and the visual information in the referenced images. Enhance answers by referencing specific images using their filenames when they directly illustrate key points.

                1.  **Image References Provided:**
                    *   You have been given text context and potentially relevant images.
                    *   These images are introduced in the text with lines like: `Image N: reference: <filename>: [description]`.
                    *   The string immediately following `reference:` (e.g., `page_10_figure_1.png`) is the **exact filename** you must use for referencing.

                2.  **Image Referencing Requirement:**
                    *   When an image visually clarifies or demonstrates something mentioned in your text answer, **you MUST reference it using the specific filename identified above.**
                    *   **Correct Reference Format:** `[Image: <image_filename.png>]`
                    *   **Example:** If the text introduces `Image 3: reference: page_45_diagram_2.png: A flowchart...`, and you refer to it, you MUST write `[Image: page_45_diagram_2.png]`.
                    *   **Incorrect:** Do NOT use sequential labels like `Image 3` or `Image reference 3` in your final answer's references. Use the FILENAME.

                3.  **Image Placement:**
                    *   Integrate image references (using the filename format) naturally *within the sentence* it supports.
                    *   Avoid placing references at the end of paragraphs or as standalone items.

                4.  **Relevance & Grounding:**
                    *   Base your entire answer **only** on the provided text context and the visual information in the images whose references were provided.
                    *   Reference an image **only** if its visual content directly supports the specific point you are making. Use the information from the image description line and the image itself.

                5.  **Content Structure & Style:**
                    *   Respond in clear and precise **markdown format**.
                    *   Structure answers logically (headings, lists). Keep explanations concise.

                6.  **Handling Insufficient Information:**
                    *   If the text and images *together* are insufficient to answer accurately, respond *only* with:
                        > *"Based on the provided context and images, I am unable to provide a correct answer."*

                7.  **Truthfulness & Strict Grounding:**
                    *   **Do NOT** invent or hallucinate information, procedures, or visual details not present in the provided text or images/descriptions.
                    *   Verify every statement against the provided materials. **Strict adherence to the provided context (text, image references, and visual content) is mandatory.**
                """

    # Removed _create_user_message - handled by _prepare_context_and_messages

    def _count_tokens(self, text: str) -> int:
        """Count tokens using the processor's tokenizer"""
        # The processor object usually wraps the tokenizer
        if hasattr(self.processor, 'tokenizer'):
             return len(self.processor.tokenizer.encode(text))
        else:
             # Fallback if tokenizer is accessed differently or unavailable
             print("Warning: Could not access processor.tokenizer directly for token counting.")
             # Approximate by splitting, less accurate
             return len(text.split())


    # Removed _truncate_context - Text truncation happens during context building.
    # VL models often have large context windows, and processor handles combined input.

    def query(
            self,
            query: str,
            num_chunks: int = 8,
            # rerank parameter is now read from self.rerank during init
    ) -> RAGResponse:
        """Query the system using Qwen-VL, combining retrieval, optional reranking, and multimodal generation"""
        try:
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            gc.collect()

            # 1. Retrieve initial chunks
            print(f"\n--- Starting Query: '{query}' ---")
            start_retrieval = time.time()
            # Request slightly more chunks initially if reranking is enabled
            initial_k = num_chunks * 2 if self.rerank else num_chunks
            chunks = self.base_retriever.search(query, k=initial_k)
            self.retrieval_time = time.time() - start_retrieval
            print(f"Retrieved {len(chunks)} initial chunks in {self.retrieval_time:.3f}s")

            # Optionally unload embedding model *after* retrieval
            if hasattr(self.base_retriever, 'unload_embedding_model'):
                self.base_retriever.unload_embedding_model()
                print("Unload embedding model")
            else:
                print("No embedding model to unload")

            # 2. Rerank if enabled
            if self.rerank:
                chunks = self._rerank_chunks(query, chunks, top_k=num_chunks)
                print(f"Reranked to {len(chunks)} chunks.")

            if not chunks:
                 print("No relevant chunks found after retrieval/reranking.")
                 return RAGResponse(answer="No relevant information found in the document.", source_chunks=[], prompt_tokens=0, completion_tokens=0)

            # 3. Prepare context and messages list
            print("Preparing context and messages for VL model...")
            start_context = time.time()
            # Pass only the final desired number of chunks after potential reranking
            messages, included_images = self._prepare_context_and_messages(query, chunks)
            print(f"Context preparation took {time.time() - start_context:.3f}s")

            # 4. Process inputs for Qwen-VL model
            print("Processing inputs with AutoProcessor...")
            start_process = time.time()
            try:
                # Use processor to prepare text, images, and tokenize
                text_template = self.processor.apply_chat_template(
                    messages, tokenize=False, add_generation_prompt=True
                )
                # print("\n" + "="*20 + " Full Text Prompt Sent to Processor " + "="*20)
                # print(text_template)
                # print("="* (42 + len(" Full Text Prompt Sent to Processor ")) + "\n")   

                image_inputs, video_inputs = process_vision_info(messages) # video_inputs should be None

                inputs = self.processor(
                    text=[text_template], # Must be a list
                    images=image_inputs,
                    videos=video_inputs,
                    padding=True, # Pad to max length in batch (only 1 item here)
                    return_tensors="pt",
                )
                # Move inputs to the model's device (usually GPU handled by device_map)
                inputs = inputs.to(self.model.device)
                print(f"Input processing took {time.time() - start_process:.3f}s")
                # print(f"DEBUG: Input tensor shapes: { {k: v.shape for k, v in inputs.items()} }") # Optional debug
                # print(f"DEBUG: Input device: {inputs['input_ids'].device}") # Optional debug

            except Exception as proc_error:
                 print(f"Error during input processing: {proc_error}")
                 # Provide a fallback response or re-raise
                 raise RuntimeError(f"Failed during input processing: {proc_error}") from proc_error


            # Estimate prompt tokens from the processed inputs
            prompt_tokens = inputs['input_ids'].shape[1] if 'input_ids' in inputs else 0
            print(f"Estimated prompt tokens (including images): {prompt_tokens}")


            # 5. Generate response using model.generate
            print("Generating response with Qwen-VL model...")
            start_generate = time.time()
            try:
                 with torch.inference_mode(): # Use inference mode for efficiency
                      generated_ids = self.model.generate(
                          **inputs,
                          max_new_tokens=1024, # Or adjust as needed
                          do_sample=True,
                          temperature=0.1, # Lower temperature for more factual answers
                          top_p=0.9,
                          pad_token_id=self.processor.tokenizer.eos_token_id, # Use EOS for padding
                          eos_token_id=self.processor.tokenizer.eos_token_id, # Stop generation token
                          use_cache=True, # Enable KV caching
                          # Add other generation params if needed
                      )
            except Exception as gen_error:
                 print(f"Error during model generation: {gen_error}")
                 if torch.cuda.is_available():
                      print(f"GPU Memory allocated: {torch.cuda.memory_allocated() / 1e9:.2f}GB")
                      print(f"GPU Memory reserved: {torch.cuda.memory_reserved() / 1e9:.2f}GB")
                 raise RuntimeError(f"Failed during model generation: {gen_error}") from gen_error


            self.generation_time = time.time() - start_generate
            print(f"Generation took {self.generation_time:.3f}s")


            # 6. Decode the response
            # Trim the input prompt tokens from the generated output
            generated_ids_trimmed = generated_ids[:, inputs['input_ids'].shape[1]:]
            response_text = self.processor.batch_decode(
                generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
            )[0].strip() # Get the first (and only) response

            print("\n--- Generated Answer ---")
            print(response_text)
            print("------------------------")

            # Calculate completion tokens
            completion_tokens = generated_ids_trimmed.shape[1]

            # Clear cache after generation
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            gc.collect()

            # 7. Return RAGResponse
            # Add included image paths to the response object for traceability
            # source_chunks_data = [(c.to_dict(), s) for c, s in chunks] # Convert Chunk objects if needed
            
            return RAGResponse(
                answer=response_text,
                source_chunks=chunks, # Or pass original Chunk objects if serializable
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                included_images=included_images # Add the list of image dicts used
            )

        except Exception as e:
            print(f"Error during query processing: {str(e)}")
            # Print error memory stats
            if torch.cuda.is_available():
                print(f"Error GPU Memory allocated: {torch.cuda.memory_allocated() / 1e9:.2f}GB")
                print(f"Error GPU Memory reserved: {torch.cuda.memory_reserved() / 1e9:.2f}GB")
            import traceback
            traceback.print_exc()
            # Return a minimal error response
            return RAGResponse(answer=f"An error occurred: {e}", source_chunks=[], prompt_tokens=0, completion_tokens=0)


    def cleanup(self):
        """Release resources and clear memory"""
        print("Cleaning up resources...")
        try:
            # Unload base retriever's embedding model
            if hasattr(self, 'base_retriever') and hasattr(self.base_retriever, 'unload_embedding_model'):
                print("Unloading embedding model...")
                self.base_retriever.unload_embedding_model()

            # Explicitly delete models and processor to free memory
            print("Deleting models and processor...")
            if hasattr(self, 'model'):
                del self.model
                self.model = None
            if hasattr(self, 'processor'):
                del self.processor
                self.processor = None
            if hasattr(self, 'cross_encoder'):
                del self.cross_encoder
                self.cross_encoder = None

            # Force garbage collection
            print("Running garbage collection...")
            n = gc.collect()
            print(f"Garbage collector released {n} objects.")

            # Clear CUDA cache
            if torch.cuda.is_available():
                print("Clearing CUDA cache...")
                torch.cuda.empty_cache()

            print("Cleanup finished successfully.")
        except Exception as e:
            print(f"Error during cleanup: {str(e)}")

    def get_statistics(self) -> Dict[str, Union[int, str]]: # Allow string values for device
        """Get statistics about the system"""
        print("Gathering system statistics...") # Add a print statement for debugging
        try:
            # Initialize stats dictionary
            stats: Dict[str, Union[int, str]] = {}

            # Get base retriever stats safely
            if hasattr(self, 'base_retriever') and self.base_retriever is not None and \
               hasattr(self.base_retriever, 'get_statistics'):
                try:
                    base_stats = self.base_retriever.get_statistics()
                    if isinstance(base_stats, dict):
                        stats.update(base_stats)
                    else:
                        print("Warning: Base retriever get_statistics did not return a dict.")
                except Exception as br_stat_err:
                    print(f"Warning: Could not get stats from base_retriever: {br_stat_err}")
            else:
                 print("Info: Base retriever or its get_statistics method not available.")


            # Get VL model name safely
            model_name = "N/A"
            if hasattr(self, 'model') and self.model is not None and hasattr(self.model, 'config') and \
               hasattr(self.model.config, '_name_or_path'):
                model_name = self.model.config._name_or_path
            stats["vl_model_name"] = model_name

            # Get processor name safely (Corrected access)
            processor_name = "N/A"
            if hasattr(self, 'processor') and self.processor is not None and hasattr(self.processor, 'tokenizer') and \
               hasattr(self.processor.tokenizer, 'name_or_path'): # Processor often wraps a tokenizer
                 processor_name = self.processor.tokenizer.name_or_path # Get from underlying tokenizer
            elif hasattr(self, 'processor') and self.processor is not None and hasattr(self.processor, 'name_or_path'):
                 processor_name = self.processor.name_or_path # Fallback if processor itself has it
            stats["processor_name"] = processor_name


            # Get cross-encoder name safely
            cross_encoder_name = "N/A"
            # CrossEncoder might store name directly or in config depending on how it's loaded
            if hasattr(self, 'cross_encoder') and self.cross_encoder is not None:
                 if hasattr(self.cross_encoder, 'model_name'): # Direct attribute common in SentenceTransformer models
                      cross_encoder_name = self.cross_encoder.model_name
                 elif hasattr(self.cross_encoder, 'config') and hasattr(self.cross_encoder.config, '_name_or_path'): # If loaded via HF pipeline/model
                      cross_encoder_name = self.cross_encoder.config._name_or_path

            stats["cross_encoder_name"] = cross_encoder_name

            # Add other stats
            stats.update({
                "max_text_tokens": self.max_text_tokens,
                "max_image_references": self.max_image_references,
                "device": str(self.device)
            })

            print("Statistics gathered successfully.") # Confirmation
            return stats

        except Exception as e:
            print(f"Error getting statistics: {e}")
            import traceback
            traceback.print_exc() # Print full traceback for debugging
            return {"error": f"Error getting statistics: {str(e)}"} # Return error in dict


if __name__ == "__main__":
    retriever = None # Initialize outside try block for cleanup
    try:
        start_time = time.time()

        # --- Configuration ---
        INDEX_DIRECTORY = "index" # Your index directory path
        DOCUMENT_NAME = "fanuc-crx-educational-cell-manual" # Document name (without .pdf)
        # Use the specific Unsloth VL model name
        VL_MODEL_NAME = "unsloth/Qwen2.5-VL-32B-Instruct-unsloth-bnb-4bit"

        # Initialize the enhanced retriever with the VL model
        retriever = EnhancedRetriever(
            index_dir=INDEX_DIRECTORY,
            document_name=DOCUMENT_NAME,
            model_name=VL_MODEL_NAME,
            rerank=False, # Set to True to enable reranking (ensure sufficient CPU)
            max_text_tokens=6000, # Adjust based on typical context size needed
            max_image_references=5 # Limit images sent to model
        )

        # Get system statistics
        stats = retriever.get_statistics()
        print("\n--- System Statistics ---")
        for key, value in stats.items():
            print(f"- {key}: {value}")
        print("-------------------------\n")

        # Example query
        # query = "What is the procedure of quick mastering?"
        query = "Explain how to perform zero point mastering using the fixture." # Query more likely to involve images

        # Get response
        response = retriever.query(query, num_chunks=6) # Adjust num_chunks as needed

        # Print results
        print(f"\n--- Query ---")
        print(query)
        print("\n--- Final Answer ---")
        print(response.answer)
        print("--------------------\n")
        print(f"Prompt Tokens (text+image): {response.prompt_tokens}")
        print(f"Completion Tokens: {response.completion_tokens}")
        print(f"Retrieval Time: {retriever.retrieval_time:.3f}s")
        print(f"Generation Time: {retriever.generation_time:.3f}s")

        # if response.included_images:
        #      print("\n--- Images Included in Context ---")
        #      for img_info in response.included_images:
        #           img_path = Path(img_info['image_path'])
        #           print(f"- Page {img_info['page_number']}, Figure {img_info['figure_number']}: {img_path.name} ({'Exists' if img_path.exists() else 'MISSING!'})")
        # else:
        #      print("\n--- No images were included in the context for this query ---")


        # Optional: Verbose source chunk display
        verbose = False
        if verbose and response.source_chunks:
            print("\n--- Top Source Chunks ---")
            for i, (chunk_dict, score) in enumerate(response.source_chunks[:3]): # Show top 3
                print(f"\n{i+1}. Score: {score:.4f} (Page: {chunk_dict.get('metadata', {}).get('page_number', 'N/A')})")
                print(f"   Text: {chunk_dict.get('text', '')[:200]}...") # Show beginning of text
            print("-------------------------")


        total_time = time.time() - start_time
        print(f"\nTotal execution time: {total_time:.3f} seconds")

    except Exception as e:
        print(f"\nAn error occurred in the main execution block: {str(e)}")
        import traceback
        traceback.print_exc()

    finally:
        # Ensure cleanup happens even if errors occur
        if retriever:
            print("\n--- Initiating Cleanup ---")
            retriever.cleanup()
            print("------------------------")