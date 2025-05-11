# run_evaluation.py with KG RAG support
import argparse
import json
import time
import os
import sys
# Early override of RETRIEVER_IMPL based on CLI flag, before any evaluator imports
_impl = "vl"
if "--retriever_impl" in sys.argv:
    idx = sys.argv.index("--retriever_impl")
    if idx + 1 < len(sys.argv) and sys.argv[idx + 1] in ("vl", "text"):
        _impl = sys.argv[idx + 1]
os.environ["RETRIEVER_IMPL"] = _impl
from pathlib import Path
import torch
from rag_evaluation import RAGEvaluator # Import the updated RAGEvaluator
# Assuming these other evaluators are separate and may or may not use VL models
from rag_fusion_evaluation import FusionRAGEvaluator
from kg_rag_evaluation import KGEnhancedRAGEvaluator
from metrics import (
    Metric, # Ensure Metric base class is imported if needed by type hints
    AlphaSimilarity,
    QuestionAnswerRelevanceMetric,
    HallucinationMetric,
    FaithfulnessMetric,
    MultimodalAnswerRelevancyMetric,
    MultimodalFaithfulnessMetric,
    GoogleVertexAI # Keep if used for DeepEval
)
import sys
from data_models import Chunk, RAGResponse, ImageMetadata # Ensure these are defined correctly
from dotenv import load_dotenv
import openai
import copy
from langchain_google_vertexai import (
    ChatVertexAI,
    HarmBlockThreshold,
    HarmCategory,
)
import logging
import traceback
import gc # Import gc

# Suppress excessive Google logging
logging.getLogger('google.api_core').setLevel(logging.WARNING)
logging.getLogger('google.auth').setLevel(logging.WARNING)
logging.getLogger('urllib3.connectionpool').setLevel(logging.WARNING) # Also suppress this common one


def find_questions_file(questions_dir: str, document_name: str) -> str:
    # ... (no changes needed) ...
    """Find the questions file for the specified document."""
    questions_dir = Path(questions_dir)
    patterns = [ f"{document_name}_questions.json", f"questions_{document_name}.json" ] # Added common pattern
    for pattern in patterns:
        file_path = questions_dir / pattern
        if file_path.exists():
            print(f"Found questions file: {file_path}")
            return str(file_path)
    for file_path in questions_dir.glob("*questions*.json"): # More flexible glob
        if document_name.lower() in file_path.stem.lower():
            print(f"Found questions file: {file_path}")
            return str(file_path)
    raise FileNotFoundError(f"No questions file found for document '{document_name}' in {questions_dir}")


def find_kg_file(kg_dir: str, document_name: str) -> str:
    # ... (no changes needed) ...
    """Find the knowledge graph file for the specified document."""
    kg_dir = Path(kg_dir)
    patterns = [ f"{document_name}_kg.txt", f"{document_name}_kg.json", f"{document_name.replace('-', '_')}_kg.txt", f"{document_name.replace('-', '_')}_kg.json", ]
    for pattern in patterns:
        file_path = kg_dir / pattern
        if file_path.exists():
            print(f"Found knowledge graph file: {file_path}")
            return str(file_path)
    for file_path in kg_dir.glob("*_kg.*"):
        if document_name.lower() in file_path.stem.lower():
            print(f"Found knowledge graph file: {file_path}")
            return str(file_path)
    raise FileNotFoundError(f"No knowledge graph file found for document '{document_name}' in {kg_dir}")


def find_image_descriptions(image_descriptions_dir: str, document_name: str) -> str:
    # ... (no changes needed) ...
     """Find the image descriptions file for the specified document."""
     if not image_descriptions_dir: return None
     image_descriptions_dir = Path(image_descriptions_dir)
     if not image_descriptions_dir.exists(): print(f"Image descriptions directory '{image_descriptions_dir}' does not exist"); return None
     patterns = [ f"{document_name}_image_description.pkl", f"{document_name}_image_descriptions.pkl", f"{document_name.replace('-', '_')}_image_description.pkl", f"{document_name.replace('-', '_')}_image_descriptions.pkl", ]
     for pattern in patterns:
         file_path = image_descriptions_dir / pattern
         if file_path.exists(): print(f"Found image descriptions file: {file_path}"); return str(file_path)
     for file_path in image_descriptions_dir.glob("*_image_description*.pkl"):
         if document_name.lower() in file_path.stem.lower(): print(f"Found image descriptions file: {file_path}"); return str(file_path)
     print(f"No image descriptions file found for document '{document_name}' in {image_descriptions_dir}")
     return None


def find_all_documents(index_dir: str) -> list:
    # ... (no changes needed) ...
    """Find all document directories in the index directory."""
    index_dir = Path(index_dir)
    documents = []
    try: # Add try-except for robustness
         for item in os.listdir(index_dir):
             item_path = index_dir / item
             # Check if it's a directory or a specific index file pattern
             if item_path.is_dir():
                 # Assuming directory name is the document name
                 documents.append(item)
             elif item.endswith(".bin") or item.endswith(".faiss"): # Common index extensions
                 # Extract name before potential suffixes
                 name = item.split("_faiss_index")[0].split("_index")[0].split(".bin")[0].split(".faiss")[0]
                 if name not in documents:
                      documents.append(name)
    except FileNotFoundError:
         print(f"Error: Index directory '{index_dir}' not found.")
         return []
    return documents


def evaluate_document(document: str, args, metrics: list) -> bool:
    """Evaluate a single document and return success status."""
    print(f"\n{'='*80}\nEvaluating document: {document} for approach: {'KG' if args.use_kg else ('Fusion' if args.use_fusion else 'Standard (VL)')}\n{'='*80}") # Updated label

    # Create document-specific output directory within the approach's base output dir
    output_dir = Path(args.output_dir)
    doc_output_dir = output_dir / document
    doc_output_dir.mkdir(parents=True, exist_ok=True)

    # Use standard _evaluation.csv suffix
    results_path = doc_output_dir / f"{document}_evaluation.csv"
    print(f"Results will be saved incrementally to: {results_path}")

    try:
        questions_file = find_questions_file(args.questions_dir, document)
    except FileNotFoundError as e:
        print(f"Error finding questions file: {str(e)}")
        return False

    start_time = time.time()
    is_using_openai_for_deepeval = (args.deepeval_llm == 'openai')
    evaluator = None # Initialize for finally block

    try:
        # Initialize the appropriate evaluator based on args
        if args.use_kg:
            # --- KG RAG Initialization ---
            print(f"Initializing Knowledge Graph Enhanced evaluator for document '{document}'...")
            if args.kg_file_path: kg_file_path = args.kg_file_path
            else:
                try: kg_file_path = find_kg_file(args.kg_dir, document)
                except FileNotFoundError as e: print(f"Error finding KG file: {str(e)}"); return False

            if args.image_descriptions_path: image_descriptions_path = args.image_descriptions_path
            else: image_descriptions_path = find_image_descriptions(args.image_descriptions_dir, document)

            if image_descriptions_path is None or not Path(image_descriptions_path).exists():
                print(f"Warning: No valid image descriptions file found for KG approach on document '{document}'")
                image_descriptions_path = None

            evaluator = KGEnhancedRAGEvaluator( # Assuming KGEnhancedRAGEvaluator exists and has similar signature
                index_dir=args.index_dir,
                document_name=document,
                kg_file_path=kg_file_path,
                image_descriptions_path=image_descriptions_path,
                model_name=args.model, # Specific LLM for KG
                metrics=copy.deepcopy(metrics), # Pass copy
                num_chunks=args.num_chunks,
                use_openai=is_using_openai_for_deepeval,
                enable_multimodal=(args.enable_all_metrics or args.enable_multimodal),
                cache_dir=args.cache_dir
            )

        elif args.use_fusion:
             # --- RAG Fusion Initialization ---
            print(f"Initializing Fusion evaluator for document '{document}'...")
            evaluator = FusionRAGEvaluator( # Assuming FusionRAGEvaluator exists and has similar signature
                index_dir=args.index_dir,
                document_name=document,
                model_name=args.model, # Use main RAG model
                metrics=copy.deepcopy(metrics), # Pass copy
                num_chunks=args.num_chunks,
                use_openai=is_using_openai_for_deepeval,
                enable_multimodal=(args.enable_all_metrics or args.enable_multimodal),
                num_generated_queries=args.num_generated_queries,
                rrf_k=args.rrf_k
            )

        else:
            # --- Standard RAG (VL Model) Initialization ---
            print(f"Initializing Standard RAG (VL) evaluator for document '{document}'...")
            # Correctly pass the VL-specific parameters
            evaluator = RAGEvaluator(
                index_dir=args.index_dir,
                document_name=document,
                model_name=args.model, # Use the main VL model specified
                cross_encoder_name=args.cross_encoder_name, # Pass cross-encoder if used
                max_text_tokens=args.max_text_tokens, # Pass VL text token limit
                max_image_references=args.max_image_references, # Pass VL image limit
                rerank=args.rerank, # Pass rerank flag
                metrics=copy.deepcopy(metrics), # Pass copy
                num_chunks=args.num_chunks,
                use_openai=is_using_openai_for_deepeval,
                # enable_multimodal is handled implicitly by using RAGEvaluator with a VL model
            )

        # Evaluate questions using the selected evaluator
        print(f"Starting evaluation using questions from: {questions_file}")
        results_df = evaluator.evaluate_all(questions_file, results_path) # Pass results_path for incremental save

        total_time = time.time() - start_time
        print(f"Evaluation for '{document}' completed in {total_time:.2f} seconds")

        # Visualize results
        print(f"\nGenerating visualizations for '{document}'...")
        # evaluator.visualize_results(results_df, doc_output_dir)

        # --- Save Summary ---
        # (Keep the summary generation logic, it's independent of evaluator type)
        # ... (summary generation code as before) ...
        summary = {
            "document": document,
            "evaluator_type": "kg_enhanced" if args.use_kg else ("fusion" if args.use_fusion else "standard_vl"), # Updated label
            # Use the same LLM for both RAG generation and KG transformation
            "llm_model": args.model,
            "total_questions": len(results_df),
            "answerable_questions": len(results_df[results_df["answerable"] == True]),
            "unanswerable_questions": len(results_df[results_df["answerable"] == False]),
            "safety_critical_questions": len(results_df[results_df["safety_critical"] == True]),
            "categories": dict(results_df["category"].value_counts().to_dict()),
            "execution_time": total_time,
            "metrics": {},
            "metrics_enabled": [metric.name for metric in metrics]
        }
        answerable_results = results_df[results_df["answerable"] == True].copy()
        for metric in metrics:
             if metric.name in answerable_results.columns: # Check if column exists
                  # Use .get() for safety, provide default if summarize doesn't exist
                  summarize_func = getattr(metric, 'summarize', lambda df: {})
                  try:
                     summary["metrics"][metric.name] = summarize_func(answerable_results)
                  except Exception as sum_err:
                     print(f"Warning: Error summarizing metric {metric.name}: {sum_err}")
                     summary["metrics"][metric.name] = {"error": str(sum_err)}
             else:
                  summary["metrics"][metric.name] = {"error": "Metric column not found in results"}


        # Add method-specific metrics/config to summary
        # ... (Keep KG and Fusion specific summary additions) ...
        if args.use_kg:
             # Use the same model for KG processing as for RAG generation
             kg_metrics = {"config": {"kg_file_path": kg_file_path,
                                           "image_descriptions_path": image_descriptions_path if image_descriptions_path else None,
                                           "llm_model_name": args.model }}
             # Add timings if columns exist
             for metric_name in ['extract_entities_time', 'relevant_kg_nodes_time', 'format_kg_time']:
                  if metric_name in answerable_results.columns:
                       valid_results = answerable_results[answerable_results[metric_name].notna()]
                       if len(valid_results) > 0: kg_metrics[metric_name] = { 'mean': float(valid_results[metric_name].mean()), 'median': float(valid_results[metric_name].median()), 'min': float(valid_results[metric_name].min()), 'max': float(valid_results[metric_name].max()) }
             summary['kg_metrics'] = kg_metrics
        elif args.use_fusion:
             fusion_metrics = {"config": {"num_generated_queries": args.num_generated_queries, "rrf_k": args.rrf_k }}
             # Add timings if columns exist
             for metric_name in ['generate_queries_time', 'fusion_time']:
                  if metric_name in answerable_results.columns:
                       valid_results = answerable_results[answerable_results[metric_name].notna()]
                       if len(valid_results) > 0: fusion_metrics[metric_name] = { 'mean': float(valid_results[metric_name].mean()), 'median': float(valid_results[metric_name].median()), 'min': float(valid_results[metric_name].min()), 'max': float(valid_results[metric_name].max()) }
             summary['fusion_metrics'] = fusion_metrics


        # Save summary to JSON
        summary_path = doc_output_dir / f"{document}_summary.json"
        try: # Add try-except for file saving
            with open(summary_path, "w", encoding='utf-8') as f:
                # Handle potential non-serializable numpy types
                def default_serializer(obj):
                     if isinstance(obj, (np.int_, np.intc, np.intp, np.int8, np.int16, np.int32, np.int64, np.uint8, np.uint16, np.uint32, np.uint64)): return int(obj)
                     elif isinstance(obj, (np.float_, np.float16, np.float32, np.float64)): return float(obj)
                     elif isinstance(obj, (np.ndarray,)): return obj.tolist() # Convert arrays to lists
                     elif isinstance(obj, Path): return str(obj) # Convert Path objects to strings
                     raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")
                json.dump(summary, f, indent=2, default=default_serializer)
            print(f"Evaluation summary for '{document}' saved to {summary_path}")
        except Exception as json_err:
             print(f"ERROR saving summary JSON for '{document}': {json_err}")


        print(f"Evaluation for '{document}' successful. Results saved to {doc_output_dir}")
        return True

    except Exception as doc_eval_err:
         print(f"\n--- ERROR during evaluation for document '{document}' ---")
         print(f"{doc_eval_err}")
         traceback.print_exc()
         print("--------------------------------------------------------\n")
         return False # Indicate failure for this document

    finally:
        # Ensure cleanup happens even if there are errors during evaluation
        if evaluator:
             print(f"Cleaning up resources for document '{document}'...")
             evaluator.cleanup()


def reset_cuda_device():
    # ... (no changes needed) ...
    """Perform a more aggressive CUDA memory cleanup."""
    if torch.cuda.is_available():
        print("Performing aggressive CUDA cleanup...")
        gc.collect()
        torch.cuda.empty_cache()
        try:
            if hasattr(torch.cuda, 'reset_accumulated_memory_stats'): torch.cuda.reset_accumulated_memory_stats()
            if hasattr(torch.cuda, 'reset_peak_memory_stats'): torch.cuda.reset_peak_memory_stats()
            print("CUDA device reset complete.")
        except Exception as e: print(f"Warning: advanced CUDA reset failed: {e}")


def document_already_evaluated(document: str, output_dir: Path) -> bool:
    # ... (no changes needed) ...
    """Check if a document has already been evaluated."""
    doc_output_dir = output_dir / document
    if not doc_output_dir.exists(): return False
    # Check for the specific evaluation CSV file
    results_file = doc_output_dir / f"{document}_evaluation.csv"
    summary_file = doc_output_dir / f"{document}_summary.json"
    # Consider evaluated if either the CSV or the summary JSON exists
    return results_file.exists() or summary_file.exists()


# run_evaluation_for_approach remains mostly the same, relying on evaluate_document
def run_evaluation_for_approach(base_args, documents_to_process, metrics, output_dir_base, use_fusion, use_kg):
    # ... (no changes needed, it calls the updated evaluate_document) ...
     """Runs the evaluation loop for a specific RAG approach."""
     if use_kg: approach_name = "Knowledge Graph Enhanced RAG"; output_dir_name = "results_kg_rag"
     elif use_fusion: approach_name = "RAG Fusion"; output_dir_name = "results_rag_fusion"
     else: approach_name = "Standard RAG (VL)"; output_dir_name = "results_rag_vl" # Changed default folder name

     final_output_dir_base = output_dir_base if output_dir_base else output_dir_name
     output_dir = Path(final_output_dir_base)
     output_dir.mkdir(parents=True, exist_ok=True)

     print(f"\n{'#'*80}")
     print(f"Starting evaluation for: {approach_name}")
     print(f"Output directory: {output_dir}")
     print(f"{'#'*80}\n")

     successful_documents = 0; failed_documents = 0; skipped_documents = 0
     start_time = time.time()

     for document in documents_to_process:
         if document_already_evaluated(document, output_dir):
             print(f"\n{'='*80}\nSkipping document: {document} for {approach_name} (already evaluated in {output_dir})\n{'='*80}")
             skipped_documents += 1
             continue

         current_args = copy.deepcopy(base_args)
         current_args.output_dir = str(output_dir)
         current_args.use_fusion = use_fusion
         current_args.use_kg = use_kg

         success = evaluate_document(document, current_args, metrics)
         if success: successful_documents += 1
         else: failed_documents += 1

         gc.collect()
         if torch.cuda.is_available():
             torch.cuda.empty_cache()
             reset_cuda_device() # Call reset between documents

     end_time = time.time()
     print(f"\n{'='*80}")
     print(f"Evaluation for {approach_name} completed in {end_time - start_time:.2f} seconds")
     print(f"Successful documents: {successful_documents}")
     print(f"Failed documents: {failed_documents}")
     print(f"Skipped documents: {skipped_documents}")
     print(f"Results saved to: {output_dir}")
     print(f"{'='*80}")

     return { "successful": successful_documents, "failed": failed_documents, "skipped": skipped_documents }


def main():
    import os 

    parser = argparse.ArgumentParser(description="Evaluate RAG system using various metrics")
    # --- Document Selection ---
    parser.add_argument("--document", help="Specific document name to evaluate")
    parser.add_argument("--documents", nargs="+", help="List of specific document names to evaluate")
    parser.add_argument("--all_documents", action="store_true", help="Evaluate all documents found in the index directory")
    parser.add_argument("--index_dir", default="index", help="Directory containing the document indices (subdirs or index files)")
    parser.add_argument("--questions_dir", default="data/questions_with_gemini_answers", help="Directory containing question JSON files")

    # --- Output ---
    parser.add_argument("--output_dir", default="results_rag_test", help="Base directory to save results (defaults to approach-specific dirs like results_rag_vl)")

    # --- Core RAG Model & Config ---
    # parser.add_argument("--model", default="microsoft/Phi-4-mini-instruct", help="LLM model name for RAG generation (Standard/Fusion)")
    # Default to the VL model
    parser.add_argument("--model", default="unsloth/Qwen2.5-VL-7B-Instruct-bnb-4bit", help="LLM model name for RAG generation (Standard/Fusion)")
    # VL Specific Params (passed to RAGEvaluator)
    parser.add_argument("--max_text_tokens", type=int, default=7000, help="Max text tokens for context (VL RAG only)")
    parser.add_argument("--max_image_references", type=int, default=12, help="Max images to include in context (VL RAG only)")
    parser.add_argument("--rerank", action=argparse.BooleanOptionalAction, default=False, help="Enable/disable cross-encoder reranking") # Use BooleanOptionalAction
    parser.add_argument("--cross_encoder_name", default="cross-encoder/ms-marco-MiniLM-L-6-v2", help="Cross-encoder model for reranking")
    parser.add_argument("--num_chunks", type=int, default=6, help="Number of chunks to retrieve/rerank for context")

    # --- Metrics Arguments ---
    parser.add_argument("--enable_all_metrics", action="store_true", help="Enable all available metrics (AlphaSim + all DeepEval)")
    parser.add_argument("--enable_all_text_metrics", action="store_true", help="Enable all text-based metrics (AlphaSim, Relevance, Hallucination, Faithfulness)") # New argument
    parser.add_argument("--enable_relevance", action="store_true", help="Enable question-answer relevance metric (DeepEval)")
    parser.add_argument("--enable_hallucination", action="store_true", help="Enable hallucination detection metric (DeepEval)")
    parser.add_argument("--enable_faithfulness", action="store_true", help="Enable faithfulness metric (DeepEval)")
    parser.add_argument("--enable_multimodal", action="store_true", help="Enable multimodal metrics (DeepEval)")
    parser.add_argument("--embedding_model", default="intfloat/multilingual-e5-large-instruct", help="Embedding model for alpha similarity") # Update default embedding

    # --- DeepEval LLM Configuration ---
    parser.add_argument("--deepeval_llm", default="openai", choices=["openai", "gemini"], help="LLM provider for DeepEval")
    parser.add_argument("--openai_model", default="gpt-4o-mini", help="OpenAI model for DeepEval (must support vision if multimodal enabled)")
    parser.add_argument("--gemini_model", default="gemini-2.0-flash", help="Gemini model for DeepEval (must support vision if multimodal enabled)") # Updated Gemini model
    parser.add_argument("--google_project_id", default=os.getenv("GOOGLE_PROJECT_ID"), help="GCP Project ID for Vertex AI")
    parser.add_argument("--google_location", default=os.getenv("GOOGLE_LOCATION"), help="GCP Location for Vertex AI")

    # --- RAG Approach Arguments ---
    retriever_group = parser.add_mutually_exclusive_group()
    retriever_group.add_argument("--use_fusion", action="store_true", help="Use RAG Fusion approach")
    retriever_group.add_argument("--use_kg", action="store_true", help="Use Knowledge Graph Enhanced RAG approach")
    retriever_group.add_argument("--run_all_approaches", action="store_true", help="Run Standard (VL), Fusion, and KG RAG sequentially")

    # RAG Fusion args
    parser.add_argument("--num_generated_queries", type=int, default=3, help="Num generated queries for fusion")
    parser.add_argument("--rrf_k", type=float, default=60.0, help="RRF smoothing parameter for fusion")
    
    # Choose approach
    parser.add_argument(
        "--retriever_impl",
        choices=["vl","text"],
        default="vl",
        help="Which retriever implementation to use: 'vl' (Vision+Language) or 'text' (LLM‐only)."
    )
    
    # KG RAG args
    parser.add_argument("--kg_file_path", help="Path to specific KG file (optional)")
    parser.add_argument("--kg_dir", default="knowledge_graphs", help="Directory containing KG files")
    parser.add_argument("--image_descriptions_path", help="Path to specific image descriptions file (optional)")
    parser.add_argument("--image_descriptions_dir", default="image_descriptions", help="Directory containing image description PKL files")
    # Removed separate KG transformation model: always use the main --model for KG processing
    parser.add_argument("--cache_dir", default="kg_cache", help="Directory for cached KG transformations")

    args = parser.parse_args()
    import os
    os.environ["RETRIEVER_IMPL"] = args.retriever_impl

    # --- Argument Validation ---
    if not args.document and not args.all_documents and not args.documents:
        print("Error: Specify --document <name>, --documents <name1> <name2>..., or --all_documents")
        sys.exit(1)
    if args.use_fusion and args.use_kg: # Should be caught by mutually_exclusive_group, but double-check
         print("Error: Cannot use --use_fusion and --use_kg simultaneously.")
         sys.exit(1)

    # Check if multimodal is enabled and warn if the DeepEval model might not support it
    multimodal_metrics_enabled = args.enable_all_metrics or args.enable_multimodal
    if multimodal_metrics_enabled:
         if args.deepeval_llm == 'openai' and ('vision' not in args.openai_model and '4o' not in args.openai_model): # Added 4o check
             print(f"Warning: Multimodal metrics enabled, but OpenAI model '{args.openai_model}' might not support vision. Consider 'gpt-4-vision-preview' or 'gpt-4o'/'gpt-4o-mini'.")
         elif args.deepeval_llm == 'gemini' and ('vision' not in args.gemini_model and 'flash' not in args.gemini_model and 'pro' not in args.gemini_model): # Needs better check for Gemini vision models
             print(f"Warning: Multimodal metrics enabled, but Gemini model '{args.gemini_model}' might not support vision. Ensure it's a multimodal variant like 'gemini-pro-vision' or 'gemini-1.5-flash-001'.") # Updated models

    # --- Load Environment Variables & Initialize DeepEval Model Placeholders ---
    text_deepeval_model_instance_or_name = None; text_model_description_for_log = "None"
    multimodal_deepeval_model_instance_or_name = None; multimodal_model_description_for_log = "None"
    gemini_setup_ok = False
    openai_setup_for_text_ok = False
    openai_setup_for_multimodal_ok = False

    # Determine if any deepeval metrics are requested at all
    any_deepeval_metric_requested = (args.enable_all_metrics or args.enable_relevance or args.enable_hallucination or args.enable_faithfulness or args.enable_multimodal or args.enable_all_text_metrics)

    if any_deepeval_metric_requested:
        load_dotenv(); print(f"DeepEval metrics requested, configuring LLM provider(s)...")

        if args.deepeval_llm == "openai":
            print(f"Configuring OpenAI ({args.openai_model}) for DeepEval metrics.")
            openai_api_key = os.getenv("OPENAI_API_KEY")
            if not openai_api_key:
                print("Warning: OPENAI_API_KEY not found. Cannot use OpenAI for DeepEval.")
            else:
                openai.timeout = 60.0
                text_deepeval_model_instance_or_name = args.openai_model
                text_model_description_for_log = f"OpenAI ({args.openai_model})"
                openai_setup_for_text_ok = True
                if multimodal_metrics_enabled: # Check if multimodal needed
                    multimodal_deepeval_model_instance_or_name = args.openai_model
                    multimodal_model_description_for_log = text_model_description_for_log
                    openai_setup_for_multimodal_ok = True

        elif args.deepeval_llm == "gemini":
            print(f"Configuring Gemini ({args.gemini_model}) for TEXT DeepEval metrics.")
            project_id = args.google_project_id
            location = args.google_location
            if not project_id or not location:
                print("Error: --google_project_id and --google_location required for --deepeval_llm gemini.")
            else:
                if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS") and not (Path.home() / ".config" / "gcloud" / "application_default_credentials.json").exists():
                    print("\nWarning: Google ADC likely missing for Gemini.\n")
                try:
                    safety_settings = { HarmCategory.HARM_CATEGORY_UNSPECIFIED: HarmBlockThreshold.BLOCK_NONE, HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE, HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE, HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE, HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE }
                    custom_model_gemini = ChatVertexAI(model_name=args.gemini_model, project=project_id, location=location, safety_settings=safety_settings, temperature=0.1)
                    text_deepeval_model_instance_or_name = GoogleVertexAI(model=custom_model_gemini)
                    text_model_description_for_log = text_deepeval_model_instance_or_name.get_model_name()
                    print(f"Successfully initialized Gemini model for TEXT metrics: {text_model_description_for_log}")
                    gemini_setup_ok = True
                except Exception as e:
                    print(f"\n--- Error Initializing Vertex AI Model for TEXT metrics ---\nFailed to initialize {args.gemini_model}: {e}"); traceback.print_exc(); print("TEXT-based DeepEval metrics using Gemini will be skipped.\n-------------------------------------------------------\n")
                    text_deepeval_model_instance_or_name = None # Explicitly set to None on failure

            # If multimodal is enabled, it MUST use OpenAI
            if multimodal_metrics_enabled:
                print(f"Configuring OpenAI ({args.openai_model}) for MULTIMODAL DeepEval metrics (required when multimodal enabled).")
                openai_api_key = os.getenv("OPENAI_API_KEY")
                if not openai_api_key:
                    print("Warning: OPENAI_API_KEY not found. MULTIMODAL metrics will fail.")
                else:
                    openai.timeout = 60.0
                    multimodal_deepeval_model_instance_or_name = args.openai_model
                    multimodal_model_description_for_log = f"OpenAI ({args.openai_model})"
                    openai_setup_for_multimodal_ok = True

    # --- Initialize Metrics List (Simplified Logic) ---
    metrics = []; print("\n--- Initializing Metrics ---")
    metrics.append(AlphaSimilarity(embedding_model=args.embedding_model)) # Always add AlphaSim

    # Flags to track requested metrics
    want_relevance = args.enable_relevance or args.enable_all_metrics or args.enable_all_text_metrics
    want_hallucination = args.enable_hallucination or args.enable_all_metrics or args.enable_all_text_metrics
    want_faithfulness = args.enable_faithfulness or args.enable_all_metrics or args.enable_all_text_metrics
    want_multimodal = args.enable_multimodal or args.enable_all_metrics

    # Check if provider setup was successful for the requested metrics
    text_provider_ready = (gemini_setup_ok or openai_setup_for_text_ok) and text_deepeval_model_instance_or_name is not None
    multimodal_provider_ready = openai_setup_for_multimodal_ok and multimodal_deepeval_model_instance_or_name is not None

    # Log which models are ready
    if text_provider_ready: print(f"- Text Metrics Ready: YES (Model: {text_model_description_for_log})")
    else: print(f"- Text Metrics Ready: NO (Setup failed or model not initialized)")
    if multimodal_provider_ready: print(f"- Multimodal Metrics Ready: YES (Model: {multimodal_model_description_for_log})")
    else: print(f"- Multimodal Metrics Ready: NO (Setup failed or model not initialized)")

    # Initialize Text Metrics (if requested and provider is ready)
    if text_provider_ready:
        text_metric_args = {"model": text_deepeval_model_instance_or_name}
        if want_relevance: metrics.append(QuestionAnswerRelevanceMetric(**text_metric_args))
        if want_hallucination: metrics.append(HallucinationMetric(**text_metric_args))
        if want_faithfulness: metrics.append(FaithfulnessMetric(**text_metric_args))
    elif want_relevance or want_hallucination or want_faithfulness:
        print("Warning: Skipping requested text-based DeepEval metrics because provider setup failed.")

    # Initialize Multimodal Metrics (if requested and provider is ready)
    if multimodal_provider_ready:
        multimodal_metric_args = {"model": multimodal_deepeval_model_instance_or_name}
        if want_multimodal:
            metrics.append(MultimodalAnswerRelevancyMetric(**multimodal_metric_args))
            metrics.append(MultimodalFaithfulnessMetric(**multimodal_metric_args))
    elif want_multimodal:
        print("Warning: Skipping requested multimodal DeepEval metrics because provider setup failed.")

    # Print final list
    print(f"Metrics initialized: {[m.name for m in metrics]}")
    print("--------------------------\n")

    overall_start_time = time.time()

    # Determine documents to process
    # ... (Keep document finding logic as before) ...
    documents_to_process = []
    if args.all_documents:
        documents_to_process = find_all_documents(args.index_dir)
        if not documents_to_process: print(f"Error: No documents found in index directory '{args.index_dir}'"); sys.exit(1)
        print(f"Found {len(documents_to_process)} documents to evaluate: {documents_to_process}")
    elif args.documents:
        documents_to_process = args.documents
        print(f"Processing {len(documents_to_process)} specified documents: {documents_to_process}")
    elif args.document:
        documents_to_process = [args.document]
        print(f"Processing single document: {args.document}")
    else: # Should be caught by initial validation, but defensive check
        print("Error: No documents specified for evaluation."); sys.exit(1)


    # --- Run evaluation based on flags ---
    # ... (Keep the main run logic using run_evaluation_for_approach as before) ...
    total_successful = 0; total_failed = 0; total_skipped = 0
    if args.run_all_approaches:
        print("Running all approaches sequentially: Standard RAG (VL) -> RAG Fusion -> KG RAG")
        approaches = [
            {"name": "standard_vl", "output_dir_default": "results_rag_vl", "use_fusion": False, "use_kg": False},
            {"name": "fusion", "output_dir_default": "results_rag_fusion", "use_fusion": True, "use_kg": False},
            {"name": "kg", "output_dir_default": "results_kg_rag", "use_fusion": False, "use_kg": True}, ]
        for approach in approaches:
            output_dir_for_approach = args.output_dir if args.output_dir else approach["output_dir_default"]
            print(f"\n--- Running Approach: {approach['name']} ---")
            results = run_evaluation_for_approach( base_args=args, documents_to_process=documents_to_process, metrics=metrics, output_dir_base=output_dir_for_approach, use_fusion=approach["use_fusion"], use_kg=approach["use_kg"] )
            total_successful += results["successful"]; total_failed += results["failed"]; total_skipped += results["skipped"]
    else:
        output_dir_base = args.output_dir
        use_fusion = args.use_fusion; use_kg = args.use_kg
        if output_dir_base is None:
             if use_fusion: output_dir_base = "results_rag_fusion"
             elif use_kg: output_dir_base = "results_kg_rag"
             else: output_dir_base = "results_rag_vl" # Updated default
        print(f"\n--- Running Single Approach ({'KG' if use_kg else 'Fusion' if use_fusion else 'Standard (VL)'}) ---") # Updated label
        results = run_evaluation_for_approach( base_args=args, documents_to_process=documents_to_process, metrics=metrics, output_dir_base=output_dir_base, use_fusion=use_fusion, use_kg=use_kg )
        total_successful += results["successful"]; total_failed += results["failed"]; total_skipped += results["skipped"]

    # Report overall results
    # ... (Keep overall summary report as before) ...
    overall_time = time.time() - overall_start_time
    print(f"\n{'#'*80}")
    print(f"Overall evaluation run completed in {overall_time:.2f} seconds")
    if args.run_all_approaches: print("Summary across all approaches:")
    print(f"Total successful document evaluations: {total_successful}")
    print(f"Total failed document evaluations: {total_failed}")
    print(f"Total skipped document evaluations (due to prior results): {total_skipped}")
    print(f"Check respective output directories for detailed results.")
    print(f"{'#'*80}")


if __name__ == "__main__":
    main()