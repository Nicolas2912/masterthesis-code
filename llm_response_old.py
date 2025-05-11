# llm_response.py
# Standard library imports
import time
import pickle
from pathlib import Path
from typing import Dict, List, Literal, Optional, Tuple

# Third party imports
import torch
from sentence_transformers import CrossEncoder
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    pipeline,
)

# Local application imports
from data_models import Chunk, ImageMetadata, RAGResponse
from document_retrieval import DocumentRetriever

class EnhancedRetriever:
    """Enhanced retriever that combines vector search with Qwen processing"""
    def __init__(
            self,
            index_dir: str,
            document_name: str,
            model_name: str = "microsoft/phi-4",
            cross_encoder_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2",
            # unified parameters
            max_context_tokens: int = 30000,
            max_text_tokens: int = None,
            max_image_references: int = None,
            device: str = None,
            rerank: bool = True,
        ):
        # Set instance variables
        self.rerank = rerank
        self.document_name = document_name
        self.index_dir = index_dir
        # alias max_text_tokens → max_context_tokens
        if max_text_tokens is not None:
            self.max_context_tokens = max_text_tokens
        else:
            self.max_context_tokens = max_context_tokens
        # accept but ignore image limit for text‐only
        self.max_image_references = max_image_references
        self.retrieval_time = 0
        self.generation_time = 0

        # Setup device
        if device is None:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            self.device = device
        print(f"Using device: {self.device}")
        torch.random.manual_seed(0)
        torch.cuda.empty_cache()

        # Load image descriptions
        self.image_descriptions = self._load_image_descriptions()

        # Initialize base retriever
        self.base_retriever = DocumentRetriever(self.index_dir, document_name=self.document_name, model_name="intfloat/multilingual-e5-large-instruct")

        # Load model and tokenizer
        print(f"Loading model {model_name}...")
        try:
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                torch_dtype=torch.float16,  # Explicitly set to float16 for better efficiency with AWQ
                device_map="auto",
                trust_remote_code=True
            )
        except ImportError as e:
            print(f"Warning: Import error occurred ({str(e)}). Falling back to standard loading...")
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                device_map="auto",
                trust_remote_code=True,
            )
        
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)

        # Initialize cross-encoder (if rerank is True)
        if self.rerank:
            print(f"Loading cross-encoder {cross_encoder_name}...")
            self.cross_encoder = CrossEncoder(
                cross_encoder_name,
                device="cpu"
            )
        # Initialize pipeline
        self.pipe = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            device_map="auto",
            framework="pt"
        )

    def _load_image_descriptions(self) -> Dict[int, List[Dict]]:
        """Load image descriptions from pickle file."""
        try:
            descriptions_path = Path(f'{self.index_dir}') / f"{self.document_name}_image_description.pkl"

            if not descriptions_path.exists():
                print(f"Warning: No image descriptions found at {descriptions_path}")
                return {}

            with open(descriptions_path, 'rb') as f:
                return pickle.load(f)
        except Exception as e:
            print(f"Error loading image descriptions: {str(e)}")
            return {}

    def _get_relevant_image_descriptions(self, chunks: List[Tuple[Chunk, float]]) -> Dict[int, List[Dict]]:
        """
        Get image descriptions for pages containing the top 5 chunks AND pages 
        within a +/- 2 range of those top chunks' pages, grouped by page.
        """
        relevant_descriptions_by_page: Dict[int, List[Dict]] = {}
        target_pages = set() # Use a set to store all pages to check (original + range)

        # 0. Sort chunks by score (descending) and select top 5
        sorted_chunks = sorted(chunks, key=lambda item: item[1], reverse=True)
        top_chunks = sorted_chunks[:3]
        print(f"  - Considering top {len(top_chunks)} chunks for image context.")

        # 1. Identify initial pages from the top chunks
        initial_pages = set()
        for chunk, score in top_chunks:
            page = chunk.metadata.get('page_number')
            if page is not None:
                initial_pages.add(page)
        
        if not initial_pages:
            print("  - No page numbers found in top retrieved chunks.")
            return {} # Return empty if no pages found in top chunks

        # 2. Expand the range for each initial page from top chunks
        print(f"  - Initial pages found in top chunks: {sorted(list(initial_pages))}")
        page_range = 2 # Define the range (e.g., 2 pages before and after)
        for page in initial_pages:
            for i in range(-page_range, page_range + 1):
                page_to_check = page + i
                # Add page to target set if it's a valid page number (e.g., > 0)
                if page_to_check > 0: 
                    target_pages.add(page_to_check)
        
        print(f"  - Checking for images on pages (based on top chunks, including +/- {page_range} range): {sorted(list(target_pages))}")

        # 3. Fetch descriptions for all target pages
        found_images = False
        for page in sorted(list(target_pages)): # Process pages in order
            # Check if descriptions exist for this page in the loaded data
            if page in self.image_descriptions:
                print(f"    - Found images on page {page}")
                page_descriptions = self.image_descriptions[page]
                
                # Store descriptions, ensuring figure number order if available
                # Make a copy to avoid modifying the original list if sorting is needed elsewhere
                sorted_descriptions = sorted(page_descriptions, key=lambda x: x.get('figure_number', 0)) 
                
                relevant_descriptions_by_page[page] = sorted_descriptions
                found_images = True
            # else: # Optional: uncomment to log pages checked but without images
            #     print(f"    - No images found on page {page}")
                
        if not found_images:
             print("  - No images found within the target page range.")


        # 4. Return the dictionary sorted by page number (already sorted due to iteration order)
        # No need to sort again as we iterate through sorted(list(target_pages))
        return relevant_descriptions_by_page

    def _format_image_descriptions(self, descriptions_by_page: Dict[int, List[Dict]]) -> str:
        """Format image descriptions grouped by page for inclusion in context."""
        if not descriptions_by_page:
            return ""

        formatted_text = "\n\n--- Relevant Visual Context ---\n"

        for page, descriptions in descriptions_by_page.items():
            if not descriptions: # Should not happen with current logic, but safe check
                continue
                
            # Add page header
            formatted_text += f"\n**Page {page} Images:**\n"

            for desc in descriptions:
                image_path = desc['image_path']
                image_name = image_path.split("/")[-1]
                description_text = desc['description']
                
                # Format each image entry clearly
                formatted_text += f"*   Image: [{image_name}] - {description_text}\n"
        
        formatted_text += "\n------------------------------\n" # Footer for the visual context block
        return formatted_text

    def _rerank_chunks(
            self,
            query: str,
            chunks: List[Tuple[Chunk, float]],
            top_k: int = 10
    ) -> List[Tuple[Chunk, float]]:
        """Rerank chunks using cross-encoder"""
        if not chunks:
            return []

        pairs = [(query, chunk[0].text) for chunk in chunks]
        scores = self.cross_encoder.predict(pairs)
        reranked = [(chunk[0], float(score)) for chunk, score in zip(chunks, scores)]
        reranked.sort(key=lambda x: x[1], reverse=True)

        return reranked[:top_k]

    def _format_context(self, chunks: List[Tuple[Chunk, float]]) -> str:
        """Formats context with text chunks followed by a grouped image description block."""
        
        # Format text chunks without explicit page numbers
        formatted_chunks = []
        current_tokens = 0
        pages_in_context = set()

        print("Formatting text context...")
        for chunk, score in chunks:
            # We no longer add the Page Number to the chunk text itself
            # page_number = chunk.metadata.get('page_number', 'Unknown') 
            # pages_in_context.add(page_number) # Keep track of pages for image retrieval

            formatted_chunk = (
                f"\n{chunk.text}\n" # Just the content
                f"{'=' * 40}"       # Separator
            )

            chunk_tokens = self._count_tokens(formatted_chunk)
            if current_tokens + chunk_tokens > self.max_context_tokens:
                print(f"Text content reached token limit ({self.max_context_tokens}). Stopping.")
                break
            
            # Add page number to set for fetching images later
            page_number = chunk.metadata.get('page_number')
            if page_number is not None:
                pages_in_context.add(page_number)

            formatted_chunks.append(formatted_chunk)
            current_tokens += chunk_tokens
            
        print(f"Formatted {len(formatted_chunks)} text chunks. Total text tokens: {current_tokens}")

        # Combine text context first
        combined_context = "\n".join(formatted_chunks)

        # Get and format image descriptions for the pages present in the text chunks
        print("Fetching and formatting image context...")
        # Pass only the chunks that made it into the context to avoid fetching unnecessary images
        final_chunks_for_images = chunks[:len(formatted_chunks)]
        image_descriptions_by_page = self._get_relevant_image_descriptions(final_chunks_for_images)
        
        if image_descriptions_by_page:
            image_context = self._format_image_descriptions(image_descriptions_by_page)
            image_tokens = self._count_tokens(image_context)
            
            print(f"\nImage Context Statistics:")
            print(f"  - Image context tokens: {image_tokens}")
            print(f"  - Current total tokens (text + image): {current_tokens + image_tokens}")
            print(f"  - Maximum allowed tokens: {self.max_context_tokens}")

            # Check if adding image context exceeds the *total* limit
            if current_tokens + image_tokens <= self.max_context_tokens:
                combined_context += image_context
                current_tokens += image_tokens # Update total token count
                print("  - Successfully added image context.")
            else:
                # Option: Could try truncating the *image_context* string here if needed, 
                # but for now, we just warn and omit it if it overflows.
                print("Warning: Adding image descriptions would exceed token limit. Omitting image context.")
                # Optionally return only text context: return combined_context 
        else:
            print("\nNo relevant image context found or generated.")
            
        print(f"Final context size: {current_tokens} tokens.")
        return combined_context

    def _create_system_message(self) -> str:
        """Create a system message for Phi-4."""
        return """
                **Instructions for Answer Generation:**

                **Guiding Principle:** Your primary goal is to provide accurate, context-based answers. Enhance these answers comprehensively by referencing **all** specific images from the context that directly illustrate or clarify key points, components, or steps mentioned in your text.

                1.  **Image Integration & Requirement**
                    *   If the context contains **one or more images** relevant to and supporting different parts of your explanation, **you must strive to include references to all such relevant images.** The goal is to provide good visual support where appropriate.
                    *   Use the exact syntax for each reference: `[Image: <image_reference.png>]`

                2.  **Image Placement**
                    *   Integrate **each** image reference naturally *within the sentence* where it provides the most value to the explanation for that specific point.
                    *   Avoid placing image references at the end of paragraphs or as standalone list items. Multiple relevant images might appear in close succession if they support closely related points in your text.

                3.  **Relevance & Selection**
                    *   **Actively seek opportunities** to link distinct parts of your textual answer to specific, relevant image references.
                    *   If **multiple images** illustrate different points, different steps, different components, or different aspects of the same concept, **incorporate references to each** where they add distinct value and clarity.
                    *   Prefer images that clearly illustrate or clarify. Avoid unrelated or purely decorative images. Ensure **each** referenced image directly supports the specific text it accompanies.

                4.  **Content Structure & Style**
                    *   Respond in clear and precise **markdown format**.
                    *   Structure your answer logically using headings, bullet points, or numbered lists where appropriate for clarity.
                    *   Keep explanations concise and directly related to the query and context.

                5.  **Handling Missing Context**
                    *   If the provided context is insufficient to construct a reliable answer or address the query accurately, respond *only* with:
                        > *"Based on the provided context, I am unable to provide a correct answer."*

                6.  **Truthfulness**
                    *   Do **not** invent or hallucinate facts, concepts, procedures, or image content not present in the provided context.
                    *   Base your response **strictly** on the information given.
                    *   Do **not** invent, assume, or infer information beyond what is explicitly stated in the context. Verify every statement against the provided text and image descriptions.
                """

    def _create_user_message(self, query: str, context: str) -> str:
        """Create a user message with query and context."""
        return f"""**Context:**
                {context}

                ---

                **Question:**
                {query}"""

    def _count_tokens(self, text: str) -> int:
        """Count tokens using model's tokenizer"""
        return len(self.tokenizer.encode(text))

    def _truncate_context(self, context: str) -> str:
        """Truncate context to fit within token limit"""
        tokens = self.tokenizer.encode(context)
        if len(tokens) > self.max_context_tokens:
            tokens = tokens[:self.max_context_tokens]
            context = self.tokenizer.decode(tokens, skip_special_tokens=True)
        return context

    def query(
            self,
            query: str,
            num_chunks: int = 8,
            rerank: bool = True
    ) -> RAGResponse:
        """Query the system with both retrieval and LLM processing"""
        try:
            # Clear cache before starting
            if torch.cuda.is_available():
                torch.cuda.empty_cache()

            # Get initial chunks
            start = time.time()
            chunks = self.base_retriever.search(query, k=num_chunks)
            self.retrieval_time = time.time() - start

            if hasattr(self.base_retriever, 'unload_embedding_model'):  # Check if method exists
                self.base_retriever.unload_embedding_model()
                print("Unload embedding model")
            else:
                print("No embedding model to unload")

            # Rerank if enabled
            if self.rerank:
                chunks = self._rerank_chunks(query, chunks)

            # Format and truncate context
            start = time.time()
            context = self._format_context(chunks)
            context = self._truncate_context(context)
            print(f"Context length: {self._count_tokens(context)} tokens")

            # print(f"Context: {context}")

            # Create messages for Phi's chat template
            messages = [
                {"role": "system", "content": self._create_system_message()},
                {"role": "user", "content": self._create_user_message(query, context)}
            ]
            
            # Apply chat template
            prompt = self.tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True
            )
            
            # Count tokens
            prompt_tokens = self._count_tokens(prompt)
            
            # Generate response with optimized settings
            start = time.time()
            with torch.inference_mode():
                if torch.cuda.is_available():
                    # Move prompt to GPU if needed
                    encoded_input = self.tokenizer(prompt, return_tensors="pt").to("cuda")

                response = self.pipe(
                    prompt,
                    max_new_tokens=1024,
                    do_sample=True,
                    temperature=0.09,
                    return_full_text=False,
                    pad_token_id=self.tokenizer.eos_token_id,
                    use_cache=True,
                )[0]["generated_text"].strip()
            
            self.generation_time = time.time() - start
            print(f"Generation time: {round(self.generation_time, 3)}s")
            print(f"Answer: {response}")

            # Calculate completion tokens
            completion_tokens = self._count_tokens(response)
            
            # Clear cache after generation
            if torch.cuda.is_available():
                torch.cuda.empty_cache()

            return RAGResponse(
                answer=response,
                source_chunks=chunks,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens
            )

        except Exception as e:
            print(f"Error during query processing: {str(e)}")
            # Print error memory stats
            if torch.cuda.is_available():
                print(f"Error GPU Memory allocated: {torch.cuda.memory_allocated() / 1e9:.2f}GB")
                print(f"Error GPU Memory reserved: {torch.cuda.memory_reserved() / 1e9:.2f}GB")
            raise
        
    def cleanup(self):
        """Release resources and clear memory"""
        try:
            # Unload base retriever
            if hasattr(self, 'base_retriever') and hasattr(self.base_retriever, 'unload_embedding_model'):
                self.base_retriever.unload_embedding_model()
            
            # Explicitly delete models to free memory
            if hasattr(self, 'model'):
                del self.model
            if hasattr(self, 'tokenizer'):
                del self.tokenizer
            if hasattr(self, 'cross_encoder'):
                del self.cross_encoder
            
            # Force garbage collection
            import gc
            gc.collect()
            
            # Clear CUDA cache
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
                
            print("Successfully cleaned up resources")
        except Exception as e:
            print(f"Error during cleanup: {str(e)}")

    def get_statistics(self) -> Dict[str, int]:
        """Get statistics about the system"""
        stats = self.base_retriever.get_statistics()
        stats.update({
            "max_context_tokens": self.max_context_tokens,
            "device": str(self.device)
        })
        return stats


if __name__ == "__main__":
    try:
        start = time.time()
        # Initialize the enhanced retriever
        retriever = EnhancedRetriever(
            index_dir="index",
            document_name="fanuc-crx-educational-cell-manual",
            model_name="Qwen/Qwen2.5-32B-Instruct-AWQ",
            rerank=False
        )

        # Get system statistics
        stats = retriever.get_statistics()
        print("\nSystem Statistics:")
        for key, value in stats.items():
            print(f"{key}: {value}")

        # Example query
        query = "What is the procedure of quick mastering?"

        # Get response
        response = retriever.query(query, num_chunks=4)

        # Print results
        print(f"\nQuery: {query}")
        print("\nAnswer:")
        print(response.answer)
        print(f"\nUsed {response.prompt_tokens} prompt tokens and {response.completion_tokens} completion tokens")
        
        verbose = False
        if verbose:
            for chunk, score in response.source_chunks[:2]:  # Show top 3 sources
                print(f"\nDocument: {chunk.doc_id}")
                print(f"Relevance Score: {score:.4f}")

        print(f"\nTime taken: {time.time() - start:.3f} seconds")

    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback

        traceback.print_exc()