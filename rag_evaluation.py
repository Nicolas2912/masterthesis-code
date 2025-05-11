# rag_evaluation.py
import json
import torch
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Union
from pathlib import Path
from tqdm import tqdm
import time
import gc # Import gc
import importlib, os
# dynamically pick text vs. VL implementation
_impl = os.getenv("RETRIEVER_IMPL","vl")
_mod  = "llm_response_old" if _impl=="text" else "llm_response"
EnhancedRetriever = importlib.import_module(_mod).EnhancedRetriever

# Import the updated EnhancedRetriever
from metrics import (
    Metric, AlphaSimilarity, QuestionAnswerRelevanceMetric,
    HallucinationMetric, FaithfulnessMetric,
    MultimodalAnswerRelevancyMetric, MultimodalFaithfulnessMetric
)
from dotenv import load_dotenv

class RAGEvaluator:
    """Evaluates RAG system performance using various metrics."""

    def __init__(
            self,
            index_dir: str,
            document_name: str,
            # Update default model to reflect potential usage, though it's overridden
            model_name: str = "unsloth/Qwen2.5-VL-32B-Instruct-unsloth-bnb-4bit",
            cross_encoder_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2",
            # Updated parameters for EnhancedRetriever
            max_text_tokens: int = 6000,
            max_image_references: int = 10,
            device: str = None,
            rerank: bool = True,
            metrics: Optional[List[Metric]] = None,
            num_chunks: int = 8,
            use_openai: bool = False,
            # enable_multimodal is implicitly True if using VL model
    ):
        """Initialize with updated parameters for the new EnhancedRetriever."""
        if use_openai:
            load_dotenv()

        # Initialize the RAG system using the updated EnhancedRetriever signature
        self.retriever = EnhancedRetriever(
            index_dir=index_dir,
            document_name=document_name,
            model_name=model_name, # This will be the VL model path
            cross_encoder_name=cross_encoder_name,
            max_text_tokens=max_text_tokens, # Changed parameter name
            max_image_references=max_image_references, # Added parameter
            device=device,
            rerank=rerank
        )

        # Initialize metrics if not provided (same metrics can be used)
        if metrics is None:
            metrics = [
                AlphaSimilarity(),
                QuestionAnswerRelevanceMetric(),
                HallucinationMetric(),
                FaithfulnessMetric(),
                MultimodalFaithfulnessMetric(),
                MultimodalAnswerRelevancyMetric()
            ]
        self.metrics = metrics

        self.document_name = document_name
        self.index_dir = index_dir
        self.num_chunks = num_chunks
        self.results = []

    # _load_images can stay the same - it loads images specified in the question JSON
    def _load_images(self, question: Dict) -> List[str]:
        # ... (keep existing implementation) ...
        """Load images for a question if any exist."""
        images = []
        if question.get("has_images", False):
            if "image" in question:
                image_path = question["image"]
                images.append(image_path)
            elif "found_images" in question:
                for img_info in question["found_images"]:
                    image_path = img_info.get("reference")
                    if image_path:
                        images.append(image_path)
        return images


    # Completely rewritten to use response.included_images
    def _get_image_paths_from_response(self, response) -> List[str]:
        """
        Extract image paths directly from the response.included_images attribute.

        Args:
            response: The RAGResponse object from the retriever.

        Returns:
            List of image file paths included in the prompt context.
        """
        image_paths = []
        # Check if the response object and the included_images attribute exist
        if hasattr(response, 'included_images') and response.included_images:
            print(f"Extracting image paths from response.included_images ({len(response.included_images)} found)...")
            for img_info in response.included_images:
                # Ensure the dictionary has the 'image_path' key
                if isinstance(img_info, dict) and 'image_path' in img_info:
                    img_path = img_info['image_path']
                    # Optional: Check if path exists here too, though EnhancedRetriever should handle this
                    if Path(img_path).exists():
                         image_paths.append(img_path)
                    else:
                         print(f"Warning: Image path from response does not exist: {img_path}")
                else:
                    print(f"Warning: Invalid format in response.included_images item: {img_info}")
        else:
            print("No 'included_images' found in the response object.")

        # No need for deduplication, response.included_images should already be the final list
        print(f"Returned {len(image_paths)} existing image paths from response.")
        if image_paths:
            print(f"Sample image paths: {image_paths[:5]}")

        return image_paths

    # load_questions remains the same
    def load_questions(self, questions_path: Union[str, Path]) -> List[Dict]:
        # ... (keep existing implementation) ...
        """Load questions from a JSON file."""
        try:
            questions_path = Path(questions_path)
            if not questions_path.exists():
                raise FileNotFoundError(f"Questions file not found: {questions_path}")

            print(f"Loading questions from: {questions_path}")
            with open(questions_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if "questions" not in data:
                print(f"ERROR: 'questions' key not found in {questions_path}")
                if isinstance(data, list):
                    print("Using the JSON array as questions list")
                    return data
                elif self.document_name in data:
                    print(f"Using '{self.document_name}' key as questions list")
                    return data[self.document_name]
                else:
                    possible_keys = [k for k in data.keys() if 'question' in k.lower()]
                    if possible_keys:
                        key = possible_keys[0]
                        print(f"Using '{key}' key as questions list")
                        return data[key]
                    raise ValueError(f"Could not find questions data in {questions_path}")

            return data["questions"]
        except Exception as e:
            print(f"Error loading questions from {questions_path}: {str(e)}")
            raise


    def evaluate_question(self, question: Dict, output_path: Optional[Union[str, Path]] = None) -> Dict:
        """Evaluate a single question with updated logic for VL retriever."""
        question_text = question["question"]
        reference_answer = question.get("answer")
        is_answerable = question.get("category", "UNKNOWN") != "UNANSWERABLE" and reference_answer is not None

        start_time = time.time()
        response = None # Initialize response to None
        rag_answer = "Error: Could not retrieve response." # Default error answer
        chunk_texts = []
        image_paths = []
        has_images = False
        page_numbers = []

        try:
            # 1. Generate answer using RAG
            print(f"\nProcessing Question ID: {question['id']}")
            response = self.retriever.query(question_text, num_chunks=self.num_chunks)
            rag_answer = response.answer

            # print(f"Raw Answer: {rag_answer[:200]}...") # Print start of answer

            # Extract source chunks (handle potential absence)
            chunk_texts = [chunk.text for chunk, _ in response.source_chunks] if hasattr(response, 'source_chunks') and response.source_chunks else []

            # Extract page numbers from source chunks
            if hasattr(response, 'source_chunks') and response.source_chunks:
                for chunk, _ in response.source_chunks:
                    if chunk.metadata and 'page_number' in chunk.metadata:
                        page_numbers.append(chunk.metadata['page_number'])
                    else:
                        # Handle cases where metadata or page_number might be missing
                        page_numbers.append(None) # Or some other placeholder

            # Extract image paths directly from the response object
            image_paths = self._get_image_paths_from_response(response)
            has_images = len(image_paths) > 0 # Determine if images were used

            result = {
                "id": question["id"],
                "question": question_text,
                "category": question.get("category", "UNKNOWN"),
                "answerable": is_answerable,
                "safety_critical": question.get("safety_critical", False),
                "answer": rag_answer,
                "reference_answer": reference_answer,
                "error": None,
                "retrieval_time": self.retriever.retrieval_time,
                "generation_time": self.retriever.generation_time,
                "generate_queries_time": getattr(self.retriever, 'generate_queries_time', 0),
                "processing_time": time.time() - start_time,
                "has_images": has_images, # Store whether images were part of the context
                "num_images_in_context": len(image_paths), # Store count
                "chunk_pages": page_numbers # Add the list of page numbers
            }

            # 2. Handle unanswerable questions (Save and Return)
            if not is_answerable:
                print(f"Question {question['id']} marked as unanswerable. Saving basic result.")
                # Add empty metric fields
                for metric in self.metrics:
                    result[metric.name] = None
                    result[f"{metric.name}_reasoning"] = "Question marked as unanswerable."
                if output_path is not None:
                    self.save_incremental_results(result, output_path)
                return result

            # 3. Calculate metrics for answerable questions
            print(f"Calculating metrics for answerable question {question['id']}...")
            # Prepare base kwargs for metrics
            kwargs = {
                'question': question_text,
                'context': chunk_texts,
                'retrieval_context': chunk_texts, # Often same as context for RAG eval
            }

            # Add image-related kwargs IF images were included in the prompt
            if has_images:
                # Define the base directory where figures for this document are stored
                # Assumes a structure like /base_path/extracted_figures/document_name/
                # You might need to adjust 'extracted_figures' if your structure differs
                figures_dir = str(self.retriever.index_dir.parent / "extracted_figures" / self.document_name)
                print(f"Setting figures_dir for metrics: {figures_dir}")

                kwargs.update({
                    'input_images': image_paths, # Pass the list of full paths
                    'document_name': self.document_name,
                    'figures_dir': figures_dir # Pass the directory containing these images
                })

            # Calculate all metrics
            for metric in self.metrics:
                metric_name = metric.name
                print(f"  - Calculating metric: {metric_name}...")
                try:
                    # Skip multimodal metrics if no images were actually included
                    is_multimodal_metric = metric_name in ["multimodal_answer_relevancy", "multimodal_faithfulness"]
                    if is_multimodal_metric and not has_images:
                        print(f"    Skipping {metric_name} (no images in context).")
                        result[metric_name] = None
                        result[f"{metric_name}_reasoning"] = "No images were included in the RAG context."
                        continue

                    # Calculate the metric
                    # Ensure calculate method can handle potential missing kwargs gracefully
                    metric_score = metric.calculate(rag_answer, reference_answer, **kwargs)
                    result[metric_name] = metric_score

                    # Get reasoning if available
                    reasoning = getattr(metric, 'last_reason', None)
                    if reasoning:
                        result[f"{metric_name}_reasoning"] = reasoning

                    print(f"    Result for {metric_name}: {metric_score}")
                    gc.collect() # Collect garbage after each metric calculation

                except Exception as e:
                    print(f"    Error calculating {metric_name}: {str(e)}")
                    result[metric_name] = None
                    result[f"{metric_name}_reasoning"] = f"Error: {str(e)}"
                    import traceback
                    traceback.print_exc() # Print traceback for metric errors


            # Save result for answerable question after all metrics
            if output_path is not None:
                self.save_incremental_results(result, output_path)

            return result

        except Exception as e:
            # Catch errors during the main RAG query or result preparation
            print(f"Critical error evaluating question {question['id']}: {str(e)}")
            import traceback
            traceback.print_exc()

            result = {
                "id": question["id"],
                "question": question_text,
                "category": question.get("category", "UNKNOWN"),
                "answerable": is_answerable,
                "safety_critical": question.get("safety_critical", False),
                "answer": f"Error during evaluation: {str(e)}",
                "reference_answer": reference_answer,
                "error": str(e),
                "retrieval_time": getattr(self.retriever, 'retrieval_time', 0),
                "generation_time": getattr(self.retriever, 'generation_time', 0),
                "processing_time": time.time() - start_time,
                "has_images": False, # Assume no images if error occurred before check
                "num_images_in_context": 0,
                "chunk_pages": [] # Add empty list for page numbers
            }
            # Add empty metric fields
            for metric in self.metrics:
                result[metric.name] = None
                result[f"{metric.name}_reasoning"] = "Evaluation failed before metric calculation."

            # Save error result
            if output_path is not None:
                self.save_incremental_results(result, output_path)

            return result


    # force_generation_for_unanswerable remains the same
    def force_generation_for_unanswerable(self, results_df: pd.DataFrame) -> pd.DataFrame:
        # ... (keep existing implementation) ...
        """
        Ensure all unanswerable questions have generated answers.
        This re-processes any unanswerable questions that have empty answers.
        """
        missing_answers = results_df[(results_df["answerable"] == False) &
                                (results_df["answer"].isna() | (results_df["answer"] == ""))]

        if len(missing_answers) == 0:
            print("All unanswerable questions already have answers.")
            return results_df

        print(f"Generating answers for {len(missing_answers)} unanswerable questions...")
        missing_indices = missing_answers.index

        for idx in tqdm(missing_indices, desc="Generating missing answers"):
            row = results_df.loc[idx] # Use .loc for safety
            question_text = row["question"]

            try:
                response = self.retriever.query(question_text, num_chunks=self.num_chunks)
                results_df.loc[idx, "answer"] = response.answer
                results_df.loc[idx, "error"] = None
                # Update timings if available
                results_df.loc[idx, "retrieval_time"] = getattr(self.retriever, 'retrieval_time', 0)
                results_df.loc[idx, "generation_time"] = getattr(self.retriever, 'generation_time', 0)

            except Exception as e:
                print(f"Error generating answer for unanswerable question {row['id']}: {str(e)}")
                results_df.loc[idx, "answer"] = f"Error during forced generation: {str(e)}"
                results_df.loc[idx, "error"] = str(e)

        return results_df


    # evaluate_all remains largely the same
    def evaluate_all(self, questions_path: Union[str, Path], output_path: Optional[Union[str, Path]] = None) -> pd.DataFrame:
        # ... (keep existing implementation, relies on updated evaluate_question) ...
        """
        Evaluate all questions in the provided file with incremental saving.

        Args:
            questions_path: Path to the questions JSON file
            output_path: Path where to save results incrementally

        Returns:
            DataFrame containing evaluation results
        """
        questions = self.load_questions(questions_path)
        print(f"Evaluating {len(questions)} questions for document '{self.document_name}'...")

        results = []
        for question in tqdm(questions, desc="Evaluating questions"):
            gc.collect()
            if torch.cuda.is_available():
                torch.cuda.empty_cache()

            result = self.evaluate_question(question, output_path)
            results.append(result) # Append result to list for final DataFrame
            # self.results = results # Update self.results if needed, but redundant if using local 'results'

        results_df = pd.DataFrame(results)

        # Ensure all unanswerable questions have generated answers if needed
        # results_df = self.force_generation_for_unanswerable(results_df)

        print(f"Total questions processed: {len(questions)}")
        print(f"Total results collected: {len(results)}")

        # Optionally save the complete DataFrame at the end (in addition to incremental saves)
        # if output_path:
        #     final_output_path = Path(output_path)
        #     self.save_results(final_output_path.parent / f"{final_output_path.stem}_complete.csv", results_df)

        self.results = results # Store final list in self.results
        return results_df


    # Simplified cleanup
    def cleanup(self):
        """Clean up resources after evaluation"""
        print("Starting resource cleanup...")

        # Rely on the retriever's own cleanup method
        if hasattr(self, 'retriever') and hasattr(self.retriever, 'cleanup'):
            print("Cleaning up retriever resources...")
            try:
                self.retriever.cleanup()
            except Exception as retriever_cleanup_error:
                 print(f"Error during retriever cleanup: {retriever_cleanup_error}")
        else:
            print("Retriever or its cleanup method not found.")

        # Clean up metrics
        if hasattr(self, 'metrics'):
            print("Cleaning up metrics...")
            for metric in self.metrics:
                if hasattr(metric, 'cleanup'):
                    try:
                        metric.cleanup()
                    except Exception as metric_cleanup_error:
                         print(f"Error during metric {metric.name} cleanup: {metric_cleanup_error}")

        # Force garbage collection
        print("Running final garbage collection...")
        gc.collect()

        # Clear CUDA cache if available
        if torch.cuda.is_available():
            print("Clearing CUDA cache...")
            torch.cuda.empty_cache()

        print("Resource cleanup complete.")


    # save_results remains the same
    def save_results(self, output_path: Union[str, Path], results: Optional[pd.DataFrame] = None):
        """
        Save evaluation results to CSV.

        Args:
            output_path: Path to save the results CSV
            results: DataFrame containing results (uses self.results if None)
        """
        if results is None:
            if not self.results:
                 print("Warning: No results available in self.results to save.")
                 return
            results = pd.DataFrame(self.results)

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Define the desired order of columns, including the new 'pages' column
        columns =['id', 'question', 'category', 'answerable', 'safety_critical', 'answer',
       'reference_answer', 'error', 'chunk_pages', 'retrieval_time', 'generation_time', 'generate_queries_time',
       'processing_time', 'has_images', 'alpha_similarity',
       'alpha_similarity_reasoning', 'question_answer_relevance',
       'question_answer_relevance_reasoning', 'hallucination',
       'hallucination_reasoning', 'faithfulness', 'faithfulness_reasoning']

        # Create DataFrame, ensuring all expected columns exist, even if empty for some rows
        results_df = pd.DataFrame(results)

        print(results_df["generate_queries_time"])

        # Reorder and select columns, filling missing ones with NaN
        # Create a set of existing columns for faster lookup
        existing_columns = set(results_df.columns)
        # Select only columns that exist in the DataFrame AND are in the desired list
        ordered_columns = [col for col in columns if col in existing_columns]
        # Add any columns from the desired list that were NOT in the DataFrame initially
        for col in columns:
            if col not in existing_columns:
                results_df[col] = np.nan # Add missing columns with NaN

        # Now reindex with the full desired column list
        results_df = results_df.reindex(columns=columns)


        try:
            results_df.to_csv(output_path, index=False, encoding='utf-8')
            print(f"Results saved successfully to {output_path}")
        except Exception as e:
            print(f"Error saving results to CSV: {e}")
            # Fallback: Save to a temporary file or print to console?
            # For now, just print the error. Consider more robust fallback.

    def save_incremental_results(self, result: Dict[str, Any], output_path: str) -> None:
        """
        Saves a single evaluation result incrementally to a CSV file.

        Args:
            result: Dictionary containing the evaluation result for a single question
            output_path: Path where to save/append the CSV file
        """
        if not result:
            print("No result provided to save.")
            return

        # Define the desired order of columns, including the new 'pages' column
        columns =['id', 'question', 'category', 'answerable', 'safety_critical', 'answer',
       'reference_answer', 'error', 'chunk_pages', 'retrieval_time', 'generation_time', 'generate_queries_time',
       'processing_time', 'has_images', 'alpha_similarity',
       'alpha_similarity_reasoning', 'question_answer_relevance',
       'question_answer_relevance_reasoning', 'hallucination',
       'hallucination_reasoning', 'faithfulness', 'faithfulness_reasoning']

        # Create DataFrame from the single result dictionary
        result_df = pd.DataFrame([result]) # Wrap the dict in a list

        # Ensure all expected columns exist and are in the correct order
        existing_columns = set(result_df.columns)
        ordered_columns = [col for col in columns if col in existing_columns]
        for col in columns:
            if col not in existing_columns:
                result_df[col] = np.nan
        result_df = result_df.reindex(columns=columns)


        # Check if file exists to determine if header should be written
        file_exists = os.path.exists(output_path)

        try:
            # Append to CSV without index, add header only if file is new
            result_df.to_csv(output_path, mode='a', header=not file_exists, index=False, encoding='utf-8')
            # print(f"Incremental result for ID {result.get('id', 'N/A')} saved to {output_path}") # Optional: less verbose logging
        except Exception as e:
            print(f"Error saving incremental result to CSV for ID {result.get('id', 'N/A')}: {e}")
            # Consider fallback saving mechanism here as well.

    def visualize_results(self, results_path: str) -> None:
        # ... (keep existing implementation) ...
         """
         Visualize evaluation results using all metrics for answerable questions only.

         Args:
             results_path: Path to the results CSV file
             output_dir: Directory to save visualization files
         """
         if results_path is None:
             print("No results path provided.")
             return

         results_df = pd.read_csv(results_path)

         if len(results_df) == 0:
             print("No results to visualize.")
             return

         answerable_results = results_df[results_df["answerable"] == True].copy() # Use .copy() to avoid SettingWithCopyWarning

         if len(answerable_results) == 0:
             print("No answerable questions found in results to visualize metrics for.")
             return

         total_questions = len(results_df)
         answerable_count = len(answerable_results)
         unanswerable_count = total_questions - answerable_count

         print(f"\n--- Overall Statistics ---")
         print(f"Total questions evaluated: {total_questions}")
         print(f"Answerable questions: {answerable_count} ({100 * answerable_count / total_questions:.1f}%)")
         print(f"Unanswerable questions: {unanswerable_count} ({100 * unanswerable_count / total_questions:.1f}%)")
         print(f"------------------------\n")


         print("--- Metric Visualization & Summary (for Answerable Questions) ---")
         for metric in self.metrics:
             metric_name = metric.name
             try:
                 # Ensure metric column exists before filtering
                 if metric_name not in answerable_results.columns:
                      print(f"Metric column '{metric_name}' not found in results. Skipping visualization.")
                      continue

                 metric_results = answerable_results[answerable_results[metric_name].notna()]

                 if len(metric_results) == 0:
                     print(f"\nNo valid results available for '{metric_name}' metric.")
                     continue

                 excluded_count = len(answerable_results) - len(metric_results)
                 print(f"\nVisualizing '{metric_name}' ({len(metric_results)} results used, {excluded_count} excluded due to N/A score)...")

                 # Call visualize if it exists
                 if hasattr(metric, 'visualize'):
                      metric.visualize(metric_results, results_path)

                 # Get and print summary statistics if summarize exists
                 if hasattr(metric, 'summarize'):
                      summary = metric.summarize(metric_results)
                      print(f"{metric_name.replace('_', ' ').title()} Summary:")
                      if 'mean' in summary and summary['mean'] is not None: print(f"  Average: {summary['mean']:.4f}")
                      if 'median' in summary and summary['median'] is not None: print(f"  Median: {summary['median']:.4f}")
                      if 'min' in summary and summary['min'] is not None: print(f"  Min: {summary['min']:.4f}")
                      if 'max' in summary and summary['max'] is not None: print(f"  Max: {summary['max']:.4f}")

                      # Check and print category summaries
                      if summary.get("by_category"): # Use .get() for safety
                           print(f"  By Category:")
                           for category, mean in summary["by_category"].items():
                               if mean is not None:
                                    print(f"    {category}: {mean:.4f}")
                               else:
                                    print(f"    {category}: N/A")
                 print("-" * (len(metric_name) + 20)) # Separator


             except Exception as e:
                 print(f"\nERROR visualizing/summarizing metric '{metric_name}': {str(e)}")
                 import traceback
                 traceback.print_exc()
         print("--- End of Visualization & Summary ---")

# ===========================================
# Example Usage (If running this file directly)
# ===========================================
if __name__ == "__main__":
    evaluator = None # Initialize for finally block
    try:
        start_main_time = time.time()

        # --- Configuration ---
        INDEX_DIR = "index"
        DOCUMENT_NAME = "fanuc-crx-educational-cell-manual" # Or another document
        # Path to your questions file
        QUESTIONS_PATH = f"questions/questions_{DOCUMENT_NAME}.json"
        # Output path for results CSV
        OUTPUT_CSV_PATH = f"results/evaluation_results_{DOCUMENT_NAME}_vl.csv"
        # Optional directory for visualization outputs
        VIS_OUTPUT_DIR = f"results/visualizations_{DOCUMENT_NAME}_vl"

        # Ensure output directories exist
        Path(OUTPUT_CSV_PATH).parent.mkdir(parents=True, exist_ok=True)
        if VIS_OUTPUT_DIR:
             Path(VIS_OUTPUT_DIR).mkdir(parents=True, exist_ok=True)


        # --- Initialize Evaluator ---
        evaluator = RAGEvaluator(
            index_dir=INDEX_DIR,
            document_name=DOCUMENT_NAME,
            # Ensure this matches the model used in llm_response.py
            model_name="unsloth/Qwen2.5-VL-32B-Instruct-unsloth-bnb-4bit",
            # Adjust params as needed, matching llm_response.py if possible
            max_text_tokens=6000,
            max_image_references=10,
            rerank=False,
            # metrics=None, # Use default metrics
            num_chunks=6
        )

        # --- Run Evaluation ---
        evaluation_results_df = evaluator.evaluate_all(QUESTIONS_PATH, OUTPUT_CSV_PATH)

        # --- Save Final Results (Optional, if evaluate_all doesn't save complete) ---
        # evaluator.save_results(OUTPUT_CSV_PATH, evaluation_results_df)

        # --- Visualize Results ---
        evaluator.visualize_results(evaluation_results_df, VIS_OUTPUT_DIR)

        print(f"\nEvaluation complete for {DOCUMENT_NAME}.")
        print(f"Total execution time: {time.time() - start_main_time:.2f} seconds")

    except FileNotFoundError as fnf_error:
         print(f"\nERROR: Required file not found: {fnf_error}")
    except Exception as main_error:
        print(f"\nAn error occurred during the main evaluation process: {main_error}")
        import traceback
        traceback.print_exc()
    finally:
        # --- Cleanup ---
        if evaluator:
            print("\nInitiating final cleanup...")
            evaluator.cleanup()
            print("Cleanup finished.")