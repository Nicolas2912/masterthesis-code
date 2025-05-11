# rag_fusion.py
from typing import List, Tuple, Dict, Optional, Union
from dataclasses import dataclass, field

import torch
import importlib, os

# dynamically pick text vs. VL implementation
_impl = os.getenv("RETRIEVER_IMPL","vl")
_mod  = "llm_response_old" if _impl=="text" else "llm_response"
EnhancedRetriever = importlib.import_module(_mod).EnhancedRetriever

from data_models import RAGResponse, ImageMetadata
import time
from pathlib import Path  # Add this import
import sys
import re
import os
import gc

from transformers import (
    Qwen2_5_VLForConditionalGeneration, 
    AutoProcessor, 
    BitsAndBytesConfig
)
# Import Qwen VL utils
from qwen_vl_utils import process_vision_info

@dataclass(frozen=True)
class Chunk:
    """Data class for storing document chunks with hashable properties."""
    text: str
    doc_id: str
    start_idx: int
    end_idx: int
    metadata: Optional[Dict] = None

    def __hash__(self):
        """Make Chunk hashable by using immutable attributes."""
        return hash((self.text, self.doc_id, self.start_idx, self.end_idx))

    def __eq__(self, other):
        """Define equality for Chunk objects."""
        if not isinstance(other, Chunk):
            return False
        return (self.text == other.text and
                self.doc_id == other.doc_id and
                self.start_idx == other.start_idx and
                self.end_idx == other.end_idx)

class FusionRetriever(EnhancedRetriever):
    """
    RAG-Fusion implementation that extends EnhancedRetriever with query generation
    and reciprocal rank fusion capabilities.
    """

    def __init__(
            self,
            index_dir: str,
            document_name: str,
            model_name: str = "microsoft/Phi-3.5-mini-instruct",
            cross_encoder_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2",
            max_context_tokens: int = 100000,
            device: str = None,
            rerank: bool = True,
            num_generated_queries: int = 3,
            rrf_k: float = 60.0  # RRF smoothing parameter
    ):

        super().__init__(
            index_dir=index_dir,
            document_name=document_name,
            model_name=model_name,
            cross_encoder_name=cross_encoder_name,
            max_text_tokens=max_context_tokens,
            device=device,
            rerank=rerank
        )
        self.num_generated_queries = num_generated_queries
        self.rrf_k = rrf_k
        self.retrieval_time = 0
        self.generation_time = 0
        self.fusion_time = 0
        self.generate_queries_time = 0

    def _generate_queries(self, original_query: str) -> List[str]:
        """Generate multiple search queries based on the original query."""
        # Create messages for Phi-4's chat template
        messages = [
            {"role": "system", "content": "You are a helpful assistant that generates search queries."},        
            {"role": "user", "content": f"""Generate {self.num_generated_queries} different search queries to help answer the following question. 
        Make each query explore a different aspect or perspective of the original question.
        Format your response as a simple list with one query per line, without any introductory text or numbering.

        Original question: {original_query}"""}
        ]

        # Generate queries using the model
        try:
            print(f"Generating queries for: {original_query}")

            VLM = True # Set this to True to use the Qwen model path

            if not VLM:
                # Use the pipeline with the messages array
                response = self.pipe(
                    messages,
                    max_new_tokens=300,
                    do_sample=True,
                    temperature=0.7,
                    top_p=0.9
                )[0]["generated_text"][-1]['content']  # Get the assistant's response

            else:
                # Use Qwen VLM to generate queries (Text-only generation)
                # Use inherited model and processor
                if not self.model or not self.processor:
                     raise RuntimeError("Qwen model or processor not initialized (expected inheritance).")

                # Prepare inputs for Qwen model
                text = self.processor.apply_chat_template(
                    messages, tokenize=False, add_generation_prompt=True
                )
                # No images or videos needed for this task
                inputs = self.processor(
                    text=[text],
                    # images=None, # No images
                    # videos=None, # No videos
                    padding=True,
                    return_tensors="pt",
                )
                # Move inputs to the same device as the model
                # Infer device from model if possible, otherwise default to cuda/cpu
                model_device = next(self.model.parameters()).device
                inputs = inputs.to(model_device)

                # Inference: Generation of the output
                # Adjust max_new_tokens as needed for query generation
                generated_ids = self.model.generate(**inputs, max_new_tokens=300, do_sample=True, temperature=0.7, top_p=0.9) 
                
                # Decode the generated IDs, excluding the input prompt tokens
                generated_ids_trimmed = [
                    out_ids[len(in_ids) :] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
                ]
                output_text = self.processor.batch_decode(
                    generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
                )
                
                response = output_text[0] if output_text else "" # Get the first response

            # --- Common Response Parsing Logic ---
            print(f"Raw response: {response}") # Print raw response for debugging

            if not response or len(response.strip()) == 0:
                print("Empty response from model, using only original query")
                return [original_query]
                
            # Parse response into list of queries (reuse existing logic)
            queries = [q.strip() for q in response.split('\n') if q.strip()]

            # If splitting by newlines didn't work, try other separators
            if not queries:
                # Try numbered format (1. Query)
                queries = re.findall(r'\d+\.\s*(.*?)(?=\d+\.|\Z|\n)', response, re.DOTALL)
                queries = [q.strip() for q in queries if q.strip()]
                
            cleaned_queries = []
            for q in queries:
                # Remove numbering pattern at the beginning (e.g., "1.", "2)")
                q = re.sub(r'^\s*\d+[\.\)]\s*', '', q)
                
                # Remove quotes around the entire query
                q = re.sub(r'^["\'](.*)["\']$', r'\1', q)
                
                # Remove hyphens or bullet points at the beginning
                q = q.lstrip('*- ').strip()
                
                if q:  # Only add non-empty queries
                    cleaned_queries.append(q)

            # Add original query to the list
            all_queries = [original_query] + cleaned_queries[:self.num_generated_queries]
            print(f"Generated {len(all_queries)} total queries (including original):")
            for i, q in enumerate(all_queries):
                 print(f"  {i}: {q}")
                
            return all_queries

        except Exception as e:
            print(f"Error generating queries: {str(e)}")
            import traceback
            traceback.print_exc()
            return [original_query]  # Fallback to original query

    def _calculate_rrf_scores(self, ranked_lists: List[List[Tuple[Chunk, float]]]) -> Dict[
        str, Dict[str, Union[Chunk, float]]]:
        """
        Calculate Reciprocal Rank Fusion scores for documents across all queries.
        Uses document content as key to handle duplicate chunks.
        """
        rrf_scores = {}

        for ranked_list in ranked_lists:
            for rank, (chunk, score) in enumerate(ranked_list):
                # Create a unique key for the chunk
                chunk_key = f"{chunk.doc_id}:{chunk.start_idx}:{chunk.end_idx}"

                if chunk_key not in rrf_scores:
                    rrf_scores[chunk_key] = {
                        'chunk': chunk,
                        'score': 0.0
                    }

                # Calculate RRF score for this document in this ranking
                rrf_score = 1 / (rank + self.rrf_k)
                rrf_scores[chunk_key]['score'] += rrf_score

        return rrf_scores

    def _fuse_chunks(self, ranked_lists: List[List[Tuple[Chunk, float]]], top_k: int = 10) -> List[Tuple[Chunk, float]]:
        """
        Fuse multiple ranked lists using Reciprocal Rank Fusion.
        """
        # Calculate RRF scores
        rrf_scores = self._calculate_rrf_scores(ranked_lists)

        # Convert scores back to (Chunk, score) format and sort
        fused_chunks = [
            (info['chunk'], info['score'])
            for info in rrf_scores.values()
        ]
        fused_chunks.sort(key=lambda x: x[1], reverse=True)

        return fused_chunks[:top_k]

    def query(
            self,
            query: str,
            num_chunks: int = 8,
            rerank: bool = True
    ) -> RAGResponse:
        """
        Enhanced query processing using RAG-Fusion approach.
        """
        try:
            if torch.cuda.is_available():
                torch.cuda.empty_cache()

            # Generate multiple queries
            start_generate_queries = time.time()
            queries = self._generate_queries(query)
            self.generate_queries_time = time.time() - start_generate_queries

            # Get chunks for each query
            start_retrieval = time.time()
            self.retrieval_time = 0
            all_ranked_lists = []
            for q in queries:
                chunks = self.base_retriever.search(q, k=num_chunks)
                self.retrieval_time += time.time() - start_retrieval
                if rerank:
                    chunks = self._rerank_chunks(q, chunks)
                all_ranked_lists.append(chunks)

            # Fuse results using RRF
            start_fusion = time.time()
            fused_chunks = self._fuse_chunks(all_ranked_lists)
            self.fusion_time = time.time() - start_fusion

            # Parameter to control whether to use VLM for RAG Fusion or not
            VLM = True
            if not VLM: 
                # Format context with all queries for better context
                context = self._format_context(fused_chunks)
                context = self._truncate_context(context)

                # Create messages for chat template (same as in EnhancedRetriever)
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
            
                prompt_tokens = self._count_tokens(prompt)
                
                start_generation = time.time()
                with torch.inference_mode():
                    response = self.pipe(
                        prompt,
                        max_new_tokens=1024,
                        do_sample=True,
                        temperature=0.1,
                        return_full_text=False,
                        pad_token_id=self.tokenizer.eos_token_id,
                        use_cache=True,
                    )[0]["generated_text"].strip()
                self.generation_time = time.time() - start_generation
                # print(f"Answer: {response}")

                completion_tokens = self._count_tokens(response)

                if torch.cuda.is_available():
                    torch.cuda.empty_cache()

                return RAGResponse(
                    answer=response,
                    source_chunks=fused_chunks,
                    prompt_tokens=prompt_tokens,
                    completion_tokens=completion_tokens,
                    included_images=None
                )
            
            else:
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()
                gc.collect()

                # 3. Prepare context and messages list
                print("Preparing context and messages for VL model...")
                start_context = time.time()
                # Pass only the final desired number of chunks after potential reranking
                messages, included_images = self._prepare_context_and_messages(query, fused_chunks)
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
                    source_chunks=fused_chunks, # Or pass original Chunk objects if serializable
                    prompt_tokens=prompt_tokens,
                    completion_tokens=completion_tokens,
                    included_images=included_images # Add the list of image dicts used
                )

        except Exception as e:
            print(f"Error during fusion query processing: {str(e)}")
            if torch.cuda.is_available():
                print(f"GPU Memory allocated: {torch.cuda.memory_allocated() / 1e9:.2f}GB")
            raise


if __name__ == "__main__":
    # Example usage
    fanuc_document = "fanuc-crx-educational-cell-manual"
    retriever = FusionRetriever(
        index_dir="index",
        document_name=fanuc_document,
        model_name="microsoft/Phi-3.5-mini-instruct",
        num_generated_queries=2
    )

    query = "What is an acceptable motion speed?"
    response = retriever.query(query, num_chunks=4)

    print("\nQuery:", query)
    print("\nAnswer:", response.answer)
    print(f"\nUsed {response.prompt_tokens} prompt tokens and {response.completion_tokens} completion tokens")