# Standard library imports
import os
import pickle
import random
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field # Use field for default_factory
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union, Any

# Third-party imports
import fitz  # PyMuPDF
from rapidfuzz import fuzz
import faiss
import nltk
import numpy as np
import matplotlib.pyplot as plt
import torch # Added for torch.cuda checks
from llama_index.core.node_parser import MarkdownNodeParser
from llama_index.core import Document
# from llama_index.core.schema import TextNode # Not directly used
# from nltk.tokenize import sent_tokenize # Not directly used, nltk.download needed though
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
import pandas as pd

# Download necessary NLTK data - moved here for clarity
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    print("NLTK 'punkt' tokenizer not found. Downloading...")
    nltk.download('punkt', quiet=True) # Download quietly

# --- Data Classes ---

@dataclass
class Chunk:
    """
    Represents a segment of text extracted from a document.

    Attributes:
        text: The actual text content of the chunk.
        doc_id: Unique identifier of the document this chunk belongs to.
        start_idx: Starting character index of this chunk in the original document text.
        end_idx: Ending character index of this chunk in the original document text.
        metadata: Dictionary containing additional information about the chunk,
                  such as page number, confidence score, length, etc.
                  Initialized as an empty dictionary.
    """
    text: str
    doc_id: str
    start_idx: int
    end_idx: int
    metadata: Dict[str, Any] = field(default_factory=dict)

# --- Main Indexer Class ---

class MarkdownDocumentIndexer:
    """
    Handles the processing, chunking, embedding, and indexing of Markdown documents,
    optionally linking chunks to their corresponding pages in associated PDF files.
    Includes functionality to generate and save analysis plots and control index saving.
    """

    def __init__(self,
                 pdf_directory: Optional[Union[str, Path]] = None,
                 model_name: str = "intfloat/multilingual-e5-large-instruct",
                 chunk_size: int = 1024, # Default from llama-index, can be adjusted
                 chunk_overlap: int = 20, # Default from llama-index, can be adjusted
                 embedding_dim: int = 1024, # Dimension for multilingual-e5-large
                 generate_plots: bool = False,
                 plot_output_dir: str = "document_indexing_plots",
                 save_index: bool = True, # New parameter to control saving
                 output_dir: str = "index_output"): # Default output dir if saving
        """
        Initializes the MarkdownDocumentIndexer.

        Args:
            pdf_directory: Optional path to the directory containing corresponding PDF files.
                           If provided, page numbers will be estimated for chunks.
            model_name: Name of the Sentence Transformer model to use for embeddings.
            chunk_size: The target size for text chunks (used by the parser).
            chunk_overlap: The overlap between consecutive chunks (used by the parser).
            embedding_dim: The dimensionality of the embeddings produced by the model.
            generate_plots: If True, generate and save analysis plots instead of showing them.
            plot_output_dir: Directory where plots will be saved if generate_plots is True.
            save_index: If True, the FAISS index and chunk metadata will be saved to disk.
            output_dir: The directory where index files will be saved if save_index is True.
                        If relative, it will be created relative to the script's directory.
                        If absolute, the absolute path will be used.
        """
        self.save_index = save_index
        # Store the original passed value or default for logic checks
        _initial_output_dir_param = output_dir

        if self.save_index:
            try:
                # Determine the directory where the script is located
                script_dir = Path(__file__).parent.resolve()
                provided_output_path = Path(_initial_output_dir_param)

                if provided_output_path.is_absolute():
                    # User provided an absolute path, use it directly
                    self.output_dir = provided_output_path
                    print(f"Index saving enabled. Using user-specified absolute path: {self.output_dir}")
                else:
                    # User provided a relative path (or the default was used)
                    # Create this path relative to the script directory
                    self.output_dir = script_dir / provided_output_path
                    print(f"Index saving enabled. Output directory resolved relative to script: {self.output_dir}")

                # Ensure the final directory exists
                self.output_dir.mkdir(parents=True, exist_ok=True)

            except NameError: # __file__ is not defined (e.g., interactive session)
                # Fallback if script path cannot be determined
                self.output_dir = Path(_initial_output_dir_param) # Use the provided or default name directly
                self.output_dir.mkdir(parents=True, exist_ok=True)
                print("Warning: Cannot determine script directory (__file__ not defined).")
                print(f"Index saving enabled (fallback). Index files will be saved to: {self.output_dir.resolve()}")
        else:
            # Save index is false, output_dir doesn't matter for saving.
            # Assign the path object based on input, though it won't be used for saving.
            self.output_dir = Path(_initial_output_dir_param)
            print("Index saving is disabled.")

        # --- Continue with other initializations ---
        self.pdf_directory = Path(pdf_directory) if pdf_directory else None
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.embedding_dim = embedding_dim
        self.generate_plots = generate_plots
        self.plot_output_dir = Path(plot_output_dir) if generate_plots else None
        self.current_doc_id: Optional[str] = None # Track the document being processed
        self.all_plot_data: Dict[str, Dict[str, Any]] = {} # Stores data for the final summary plot

        # --- Internal State ---
        self._chunks: List[Chunk] = []
        self._index: Optional[faiss.Index] = None

        # --- Plotting Setup ---
        if self.generate_plots and self.plot_output_dir:
            # Make plot output dir relative to script dir if it's relative
            if not self.plot_output_dir.is_absolute():
                try:
                     script_dir = Path(__file__).parent.resolve()
                     self.plot_output_dir = script_dir / self.plot_output_dir
                except NameError:
                     print(f"Warning: Cannot determine script directory for relative plot path '{plot_output_dir}'. Using current working directory.")
                     # Fallback to CWD if script dir unavailable
                     self.plot_output_dir = Path.cwd() / self.plot_output_dir

            self.plot_output_dir.mkdir(parents=True, exist_ok=True)
            print(f"Plots will be saved to: {self.plot_output_dir.resolve()}")

        # --- Model Loading ---
        self._load_model(model_name)

        # --- PDF File Listing (if applicable) ---
        self.pdf_file_paths: Dict[str, Path] = {}
        if self.pdf_directory:
            try:
                pdf_dir_path = Path(self.pdf_directory)
                if not pdf_dir_path.is_absolute():
                     # Attempt to make PDF directory relative to script if not absolute
                     try:
                          script_dir = Path(__file__).parent.resolve()
                          pdf_dir_path = script_dir / pdf_dir_path
                          print(f"Resolved relative PDF directory to: {pdf_dir_path}")
                     except NameError:
                          print(f"Warning: Cannot determine script directory for relative PDF path '{self.pdf_directory}'. Using current working directory.")
                          pdf_dir_path = Path.cwd() / pdf_dir_path

                self.pdf_directory = pdf_dir_path # Update self.pdf_directory to the resolved path
                if not self.pdf_directory.exists():
                     raise FileNotFoundError(f"PDF directory not found at resolved path: {self.pdf_directory}")

                self.pdf_file_paths = self._get_pdf_path_mapping(self.pdf_directory)
                print(f"Found {len(self.pdf_file_paths)} PDF files in {self.pdf_directory}")
            except FileNotFoundError as e:
                print(f"Warning: {e}. Page number estimation will be skipped.")
                self.pdf_directory = None # Disable PDF processing
            except Exception as e_pdf:
                 print(f"Error processing PDF directory '{pdf_directory}': {e_pdf}")
                 self.pdf_directory = None


    def _load_model(self, model_name: str):
        """Loads the Sentence Transformer model, attempting GPU usage."""
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            print("CUDA is available. Cleared GPU memory.")
            # os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'expandable_segments:True' # Maybe remove if causing issues
            device = 'cuda'
        else:
            print("CUDA not available, using CPU.")
            device = 'cpu'

        print(f"Loading Sentence Transformer model: {model_name} onto {device}")
        try:
            self.model = SentenceTransformer(model_name, trust_remote_code=True, device=device)
            print(f"Model loaded successfully onto {device}.")
        except Exception as e:
            print(f"Error loading model {model_name}: {e}")
            if device == 'cuda':
                 print("Falling back to CPU.")
                 try:
                     self.model = SentenceTransformer(model_name, trust_remote_code=True, device='cpu')
                     print("Model loaded successfully onto CPU.")
                 except Exception as e_cpu:
                     print(f"Fatal Error: Could not load model on CPU either: {e_cpu}")
                     raise
            else:
                raise

    def _get_pdf_path_mapping(self, pdf_dir: Path) -> Dict[str, Path]:
        """Creates a mapping from document stem (filename without extension) to PDF Path."""
        if not pdf_dir.is_dir(): # Add check if it's actually a directory
             raise FileNotFoundError(f"Provided PDF path is not a directory: '{pdf_dir}'")
        pdf_files = list(pdf_dir.glob("*.pdf"))
        if not pdf_files:
            # Relaxed this to a warning instead of error, as PDF dir might be optional
            print(f"Warning: No PDF files found in '{pdf_dir}'. Page number estimation will be skipped for documents needing PDFs from here.")
            return {} # Return empty dict
        return {pdf_path.stem: pdf_path for pdf_path in pdf_files}

    def _format_chunk_for_e5(self, chunk_text: str) -> str:
        """Formats chunk text with an instruction for E5-instruct models."""
        # Adjusted instruction based on common E5 usage for retrieval tasks
        # task = "Given a document, represent its content for retrieval"
        task = "Represent the document passage for retrieval:" # More concise instruction often used
        return f"Instruct: {task}\nQuery: {chunk_text}"

    def _create_markdown_chunks(self, text: str, doc_id: str) -> List[Chunk]:
        """Chunks the input Markdown text using LlamaIndex's MarkdownNodeParser."""
        try:
            # Using MarkdownNodeParser to leverage Markdown structure awareness.
            # Chunk size/overlap are parser defaults unless explicitly set.
            # Note: MarkdownNodeParser might not strictly adhere to size/overlap like text splitters.
            parser = MarkdownNodeParser() # Consider passing chunk_size/overlap if parser supports it directly? (Check LlamaIndex docs if needed)
            nodes = parser.get_nodes_from_documents([Document(text=text, doc_id=doc_id)])

            chunks = []
            min_chunk_length = 20 # Minimum characters to consider a chunk valid

            for i, node in enumerate(nodes):
                # Get text content; metadata_mode="all" might include useful section headers
                chunk_text = node.get_content(metadata_mode="all").strip() # Changed to "all"

                if not chunk_text or len(chunk_text) < min_chunk_length:
                    # print(f"Skipping short or empty node {i} for {doc_id} (length {len(chunk_text)})")
                    continue

                # Estimate start/end index based on raw text finding (can be imprecise)
                # Use the node's internal start/end char index if available and reliable
                node_start = node.start_char_idx if node.start_char_idx is not None else -1
                node_end = node.end_char_idx if node.end_char_idx is not None else -1

                # Fallback if node indices are missing
                if node_start == -1:
                     start_idx = text.find(node.get_content(metadata_mode="none").strip()) # Search for the core text
                     if start_idx == -1: start_idx = 0 # Fallback
                else:
                     start_idx = node_start

                if node_end == -1:
                     # Use length of the *actual* chunk text we are storing
                     end_idx = start_idx + len(chunk_text)
                else:
                     end_idx = node_end

                metadata = {
                    'char_length': len(chunk_text),
                    'original_node_index': i,
                    'total_nodes': len(nodes),
                    'start_char_idx': start_idx,
                    'end_char_idx': end_idx,
                    'page_number': None, # Placeholder
                    'page_confidence': 0.0 # Placeholder
                }
                # Add LlamaIndex node metadata (like headers if metadata_mode="all")
                # Filter out potentially large/unserializable metadata if necessary
                if node.metadata:
                    for k, v in node.metadata.items():
                        if isinstance(v, (str, int, float, bool, list, dict, type(None))):
                             metadata[k] = v
                        # else: print(f"Skipping non-serializable metadata key '{k}' type {type(v)}")


                chunk = Chunk(
                    text=chunk_text,
                    doc_id=doc_id,
                    start_idx=start_idx,
                    end_idx=end_idx,
                    metadata=metadata
                )
                chunks.append(chunk)

            if not chunks:
                 print(f"Warning: No valid chunks generated for document {doc_id} after filtering.")
            # else: print(f"Generated {len(chunks)} chunks for {doc_id} using MarkdownNodeParser.")
            return chunks

        except Exception as e:
            print(f"Error creating chunks for {doc_id}: {e}")
            traceback.print_exc()
            return []

    def _find_chunk_page_worker(self, args: Tuple[Chunk, int, List[str], int, float]) -> Tuple[int, Tuple[Optional[int], float]]:
        """Worker function to find the page number for a single chunk."""
        chunk, chunk_index, page_texts, n_gram_size, min_confidence = args

        # Use the core text for matching, excluding potential metadata like headers
        match_text = chunk.metadata.get('text', chunk.text) # Prefer 'text' if available from node metadata, else use full chunk text
        words = match_text.split()
        if not words: return chunk_index, (None, 0.0)

        # Ensure n_gram_size is valid
        n_gram_size_actual = min(n_gram_size, len(words))
        if n_gram_size_actual <= 0: return chunk_index, (None, 0.0) # Need at least one word

        # Extract N-gram from the middle of the chunk text for better representativeness
        start_idx = max(0, (len(words) - n_gram_size_actual) // 2)
        n_gram = ' '.join(words[start_idx : start_idx + n_gram_size_actual])
        if not n_gram: return chunk_index, (None, 0.0) # Handle empty n-gram case

        best_match = (None, 0.0) # (page_num, confidence)
        # Optimization: Prefer pages around the previously found page for the last chunk
        # This needs state sharing or passing previous result, complex for parallel; skipping for now.

        for page_num, page_text in enumerate(page_texts):
            page_text_clean = page_text.strip()
            if not page_text_clean: continue # Skip empty pages

            # Use partial_ratio for robustness against OCR errors / formatting differences
            # Normalize score to 0-1 range
            try:
                confidence = fuzz.partial_ratio(n_gram, page_text_clean) / 100.0
            except Exception as fuzz_err: # Catch potential errors in fuzz matching
                print(f"Warning: Rapidfuzz error on chunk {chunk_index}, n-gram '{n_gram[:50]}...': {fuzz_err}")
                confidence = 0.0

            # Update best match if current confidence is higher
            if confidence > best_match[1]:
                best_match = (page_num + 1, confidence) # Store 1-based page number

            # Early exit if confidence is very high (e.g., > 0.98)
            if confidence >= 0.98:
                break

        # Return result only if confidence meets the minimum threshold
        if best_match[1] >= min_confidence:
            return chunk_index, best_match
        else:
            # Return None for page number if below threshold, but keep the confidence score for analysis
            return chunk_index, (None, best_match[1])


    def find_chunk_pages(self,
                         chunks: List[Chunk],
                         pdf_path: Path,
                         n_gram_size: int = 15,
                         min_confidence: float = 0.75,
                         workers: int = 4
                         ) -> List[Tuple[int, Tuple[Optional[int], float]]]:
        """Finds the most likely page number for each chunk using parallel fuzzy search."""
        if not pdf_path or not pdf_path.exists():
            print(f"Warning: PDF path '{pdf_path}' invalid or not found. Skipping page finding.")
            return [(idx, (None, 0.0)) for idx in range(len(chunks))]
        if not chunks: return []

        # Initialize results list correctly
        results: List[Optional[Tuple[int, Tuple[Optional[int], float]]]] = [None] * len(chunks)
        try:
            print(f"Opening PDF: {pdf_path.name}")
            doc = fitz.open(pdf_path)
            # Improve text extraction: use 'blocks' for better structure preservation, sort by position
            page_texts = []
            for page in doc:
                 # Extract text blocks with coordinates, sort them vertically then horizontally
                 blocks = page.get_text("blocks", sort=True)
                 # blocks.sort(key=lambda b: (b[1], b[0])) # Sort by y0, then x0
                 page_text = "\n".join([b[4] for b in blocks]) # Join text from blocks
                 page_texts.append(page_text)
            # page_texts = [page.get_text("text", sort=True) for page in doc] # Simpler alternative
            doc.close()
            print(f"Extracted text from {len(page_texts)} pages.")

            # Prepare tasks for parallel execution
            tasks = [(chunk, idx, page_texts, n_gram_size, min_confidence) for idx, chunk in enumerate(chunks)]

            if not tasks: return [(idx, (None, 0.0)) for idx in range(len(chunks))] # Handle empty chunks case

            with ThreadPoolExecutor(max_workers=workers) as executor:
                future_to_index = {executor.submit(self._find_chunk_page_worker, task): task[1] for task in tasks}
                # Use tqdm for progress visualization
                progress = tqdm(as_completed(future_to_index), total=len(chunks), desc=f"Finding pages in {pdf_path.name}", unit="chunk", ncols=100)
                for future in progress:
                    chunk_index = future_to_index[future]
                    try:
                        # result is (original_chunk_index, (page_num | None, confidence))
                        result_index, page_confidence_tuple = future.result()
                        # Ensure the result index matches the expected chunk index
                        if result_index == chunk_index:
                             results[chunk_index] = (result_index, page_confidence_tuple)
                        else:
                             print(f"Warning: Mismatched index from worker! Expected {chunk_index}, got {result_index}. Storing at {chunk_index}.")
                             # Still store it at the expected index to avoid gaps/errors
                             results[chunk_index] = (chunk_index, page_confidence_tuple)

                    except Exception as exc:
                        print(f"\nError: Chunk {chunk_index} generated an exception during page finding: {exc}")
                        traceback.print_exc() # Print traceback for debugging
                        # Store a default failure result for this chunk index
                        results[chunk_index] = (chunk_index, (None, 0.0))

            # Verify all results have been collected
            final_results = []
            for i in range(len(chunks)):
                 if results[i] is None:
                      print(f"Warning: Result for chunk index {i} was not populated. Assigning default.")
                      final_results.append((i, (None, 0.0)))
                 else:
                      final_results.append(results[i]) # type: ignore

            self._analyze_page_finding_results(final_results, pdf_path.stem) # Analyze using doc_id (stem)
            return final_results # type: ignore

        except Exception as e:
            print(f"Unexpected error during page finding for {pdf_path.name}: {e}")
            traceback.print_exc()
            return [(idx, (None, 0.0)) for idx in range(len(chunks))]


    def _analyze_page_finding_results(self, results: List[Tuple[int, Tuple[Optional[int], float]]], doc_id: str):
        """Analyzes and logs statistics about the page finding process."""
        if not results: return

        num_mapped = sum(1 for _, (page_num, _) in results if page_num is not None)
        num_unmapped = len(results) - num_mapped
        # Get confidences for *all* chunks, even unmapped ones, to see distribution
        all_confidences = [conf for _, (_, conf) in results if conf is not None]
        mapped_confidences = [conf for _, (page_num, conf) in results if page_num is not None and conf is not None]

        print(f"\n--- Page Finding Statistics ({doc_id}) ---")
        print(f"Total chunks processed: {len(results)}")
        print(f"Chunks mapped to a page (>= threshold): {num_mapped} ({num_mapped / len(results):.1%})")
        print(f"Chunks unmapped (below threshold): {num_unmapped}")

        if mapped_confidences:
            print(f"Confidence scores (for mapped chunks):")
            print(f"  Average: {np.mean(mapped_confidences):.3f}, Median: {np.median(mapped_confidences):.3f}")
            print(f"  Min:     {min(mapped_confidences):.3f}, Max:     {max(mapped_confidences):.3f}")
        else: print("No chunks were mapped with sufficient confidence.")

        if all_confidences:
            print(f"Confidence scores (all chunks):")
            print(f"  Average: {np.mean(all_confidences):.3f}, Median: {np.median(all_confidences):.3f}")
            print(f"  Min:     {min(all_confidences):.3f}, Max:     {max(all_confidences):.3f}")

        # --- Log statistics to CSV ---
        stats_dict = {
            'document_name': doc_id, 'timestamp': pd.Timestamp.now(tz='UTC').isoformat(), # Use ISO format with TZ
            'total_chunks': len(results), 'mapped_chunks': num_mapped,
            'unmapped_chunks': num_unmapped,
            'mapping_success_rate': (num_mapped / len(results)) * 100 if results else 0,
            'avg_confidence_mapped': np.mean(mapped_confidences) if mapped_confidences else 0,
            'median_confidence_mapped': np.median(mapped_confidences) if mapped_confidences else 0,
            'min_confidence_mapped': min(mapped_confidences) if mapped_confidences else 0,
            'max_confidence_mapped': max(mapped_confidences) if mapped_confidences else 0,
            'avg_confidence_all': np.mean(all_confidences) if all_confidences else 0,
            'median_confidence_all': np.median(all_confidences) if all_confidences else 0,
        }
        stats_df = pd.DataFrame([stats_dict])

        try:
            # Ensure log dir exists (relative to script if possible)
            log_dir_name = "logs"
            try:
                 script_dir = Path(__file__).parent.resolve()
                 log_dir = script_dir / log_dir_name
            except NameError:
                 print("Warning: Cannot determine script dir for logs. Using CWD.")
                 log_dir = Path.cwd() / log_dir_name
            log_dir.mkdir(exist_ok=True)

            date_str = datetime.now().strftime("%Y-%m-%d")
            output_path = log_dir / f"page_finding_stats_{date_str}.csv"
            file_exists = output_path.exists()

            stats_df.to_csv(output_path, mode='a', header=not file_exists, index=False, encoding='utf-8')
        except Exception as e:
            print(f"Warning: Could not log page finding stats to {output_path}: {e}")


    def _save_or_show_plot(self, fig, filename_base: str):
        """Helper function to either save the plot or show it."""
        if self.generate_plots:
            if not self.plot_output_dir or not self.current_doc_id:
                 print("Warning: Cannot save plot. Plot directory or current document ID not set.")
                 plt.close(fig); return

            # self.plot_output_dir should be absolute path resolved in __init__
            self.plot_output_dir.mkdir(parents=True, exist_ok=True)
            filename = f"{filename_base}_{self.current_doc_id}.png"
            filepath = self.plot_output_dir / filename
            try:
                fig.savefig(filepath, bbox_inches='tight', dpi=150) # Added dpi
                # print(f"Plot saved: {filepath}") # Keep this less verbose maybe
            except Exception as e: print(f"Error saving plot {filepath}: {e}")
            finally: plt.close(fig) # Ensure plot is closed
        else:
            try:
                 # Check if running in non-interactive environment
                 if 'ipykernel' not in str(get_ipython.__class__) and os.environ.get('DISPLAY') is None: # type: ignore
                      print("Non-interactive environment detected, cannot show plot.")
                 else:
                      plt.show()
            except NameError: # get_ipython not defined
                 if os.environ.get('DISPLAY') is None:
                      print("Non-interactive environment detected, cannot show plot.")
                 else:
                      plt.show() # Assume interactive if DISPLAY is set
            except Exception as e:
                 print(f"Error showing plot: {e}")
            finally:
                 plt.close(fig) # Ensure plot is closed even if showing fails


    # --- Plotting Methods (Simplified calls using _save_or_show_plot) ---

    def plot_chunk_length_distribution(self, chunks: List[Chunk], doc_id: str):
        """Analyzes and visualizes chunk length distribution."""
        if not chunks: print(f"No chunks to plot for {doc_id}."); return
        lengths = [len(chunk.text) for chunk in chunks]
        if not lengths: print(f"Chunks have zero length for {doc_id}."); return

        fig, axes = plt.subplots(1, 2, figsize=(15, 6))
        fig.suptitle(f'Chunk Length Analysis for: {doc_id}', fontsize=14)

        # Histogram and KDE
        ax = axes[0]
        ax.hist(lengths, bins=30, density=True, alpha=0.7, label='Histogram', color='skyblue', edgecolor='black') # Adjusted bins
        try: # KDE calculation
            # Check if data is suitable for KDE (requires variation)
            if len(set(lengths)) > 1 and np.std(lengths) > 1e-6: # Check for non-zero std dev
                # Using scipy's gaussian_kde which is generally more robust
                from scipy.stats import gaussian_kde
                kde = gaussian_kde(lengths)
                x_range = np.linspace(min(lengths), max(lengths), 500)
                ax.plot(x_range, kde(x_range), 'r-', label='KDE', lw=1.5)
            elif len(set(lengths)) == 1: # Handle constant value case
                ax.axvline(lengths[0], color='r', linestyle='--', label=f'Constant: {lengths[0]}')
            else: # Not enough distinct points or zero std dev
                 print(f"Note: KDE plot skipped for {doc_id} due to insufficient data variation.")
        except ImportError: print(f"Note: SciPy not installed. KDE plot skipped for {doc_id}.")
        except Exception as e: print(f"Note: KDE plot failed for {doc_id}. {e}")
        ax.set(xlabel='Chunk Length (chars)', ylabel='Density', title='Distribution')
        ax.grid(True, linestyle='--', alpha=0.6); ax.legend()

        # Box Plot
        ax = axes[1]
        ax.boxplot(lengths, vert=True, patch_artist=True, showmeans=True,
                    boxprops=dict(facecolor='lightblue'), medianprops=dict(color='red', lw=1.5))
        ax.set(ylabel='Chunk Length (chars)', title='Box Plot', xticks=[])
        ax.grid(True, linestyle='--', alpha=0.6)

        plt.tight_layout(rect=[0, 0.03, 1, 0.95]) # Adjust layout
        self._save_or_show_plot(fig, "chunk_length_distribution")

        print(f"\n--- Chunk Length Statistics ({doc_id}) ---")
        mean_len = np.mean(lengths) if lengths else 0
        median_len = np.median(lengths) if lengths else 0
        std_len = np.std(lengths) if lengths else 0
        min_len = min(lengths) if lengths else 0
        max_len = max(lengths) if lengths else 0
        print(f"Total Chunks: {len(chunks)}, Mean: {mean_len:.1f}, Median: {median_len:.1f}")
        print(f"StdDev: {std_len:.1f}, Min: {min_len}, Max: {max_len}")

        # Store data for summary plot
        self.all_plot_data[doc_id] = {'avg_length': mean_len, 'total_chunks': len(chunks)}


    def plot_chunk_page_mapping(self, chunk_pages: List[Tuple[int, Tuple[Optional[int], float]]], doc_id: str):
        """Visualizes chunk index vs. estimated page number."""
        if not chunk_pages: return
        # Extract pairs where page number is not None
        valid_pairs = [(idx, pc[0]) for idx, pc in chunk_pages if pc and pc[0] is not None]
        if not valid_pairs: print(f"No valid chunk-page pairs for {doc_id}. Skipping mapping plot."); return

        chunk_indices, page_numbers = map(np.array, zip(*valid_pairs))
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.scatter(chunk_indices, page_numbers, alpha=0.6, s=15, label='Chunk Mapping') # Increased size slightly
        ax.set(xlabel='Chunk Index', ylabel='Estimated Page Number', title=f'Chunk Index vs. Page ({doc_id})')
        ax.grid(True, linestyle='--', alpha=0.6)

        # Add a trend line if there's enough data and variation
        if len(set(page_numbers)) > 1 and len(chunk_indices) > 5: # Need variation and > 5 points
            try: # Trend line (linear fit)
                z = np.polyfit(chunk_indices, page_numbers, 1)
                p = np.poly1d(z)
                ax.plot(chunk_indices, p(chunk_indices), "r--", alpha=0.8, label=f'Trend (Linear Fit)', lw=1.5)
                ax.legend()
            except Exception as e: print(f"Trend line calculation failed for {doc_id}: {e}")
        elif len(valid_pairs) > 0:
             ax.legend() # Show legend even without trend line

        plt.tight_layout()
        self._save_or_show_plot(fig, "chunk_page_mapping")
        print(f"\n--- Chunk-Page Mapping Plot ({doc_id}) ---")
        print(f"Total chunks analyzed for mapping: {len(chunk_pages)}, Plotted (mapped): {len(valid_pairs)}")


    def plot_page_confidence_analysis(self, chunk_pages: List[Tuple[int, Tuple[Optional[int], float]]], doc_id: str):
        """Plots page distribution and confidence scores."""
        if not chunk_pages: return
        # Data for mapped chunks (page number is not None)
        mapped_data = [(pc[0], pc[1]) for _, pc in chunk_pages if pc and pc[0] is not None and pc[1] is not None]
        # Data for all chunks (including unmapped, where page is None but confidence exists)
        all_confidences = [pc[1] for _, pc in chunk_pages if pc and pc[1] is not None]

        if not mapped_data and not all_confidences:
             print(f"No page/confidence data to plot for {doc_id}.")
             return

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        fig.suptitle(f'Page Mapping Analysis for: {doc_id}', fontsize=14)

        # Plot 1: Chunks per Page (only for mapped chunks)
        if mapped_data:
            page_numbers, _ = map(np.array, zip(*mapped_data))
            if len(page_numbers) > 0:
                # Determine bins more dynamically based on page range
                page_min, page_max = int(min(page_numbers)), int(max(page_numbers))
                num_bins = min(30, page_max - page_min + 1) # Max 30 bins, or one per page if fewer
                if num_bins <= 0: num_bins = 1 # Handle case of single page
                ax1.hist(page_numbers, bins=num_bins, alpha=0.75, color='skyblue', edgecolor='black')
                ax1.set(xlabel='Estimated Page Number', ylabel='Number of Chunks', title='Chunks per Mapped Page')
                ax1.grid(True, axis='y', linestyle='--', alpha=0.6) # Grid on y-axis only
            else: ax1.text(0.5, 0.5, 'No pages mapped', ha='center', va='center', transform=ax1.transAxes); ax1.set_title('Chunks per Mapped Page')
        else: ax1.text(0.5, 0.5, 'No pages mapped', ha='center', va='center', transform=ax1.transAxes); ax1.set_title('Chunks per Mapped Page')

        # Plot 2: Confidence Score Distribution (for ALL chunks with confidence)
        if all_confidences:
            confidences = np.array(all_confidences)
            ax2.hist(confidences, bins=np.linspace(0, 1, 21), alpha=0.75, color='lightcoral', edgecolor='black')
            mean_conf = np.mean(confidences)
            ax2.axvline(mean_conf, color='red', linestyle='dashed', lw=1.5, label=f'Mean Conf: {mean_conf:.3f}')
            # Optionally add median line
            median_conf = np.median(confidences)
            ax2.axvline(median_conf, color='purple', linestyle='dotted', lw=1.5, label=f'Median Conf: {median_conf:.3f}')

            ax2.set(xlabel='Confidence Score', ylabel='Number of Chunks', title='Confidence Score Distribution (All Chunks)', xlim=(0, 1))
            ax2.grid(True, axis='y', linestyle='--', alpha=0.6)
            ax2.legend()
        else: ax2.text(0.5, 0.5, 'No confidence scores available', ha='center', va='center', transform=ax2.transAxes); ax2.set_title('Confidence Scores')

        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        self._save_or_show_plot(fig, "page_confidence_analysis")


    def _verify_chunks(self, chunks: List[Chunk], doc_id: str) -> bool:
        """Verifies basic validity of generated chunks."""
        if not chunks: print(f"Warning: No chunks generated for {doc_id}, verification skipped."); return False # Changed to return False if no chunks
        valid = True
        for i, chunk in enumerate(chunks):
            issues = []
            if not isinstance(chunk, Chunk): issues.append(f"Invalid type: {type(chunk)}"); valid = False; break # Stop on wrong type
            if not chunk.text or not chunk.text.strip(): issues.append("Empty text") # Warn but don't fail? Depends on goal. Let's just warn for now.
            if not isinstance(chunk.doc_id, str) or chunk.doc_id != doc_id: issues.append(f"Bad doc_id: '{chunk.doc_id}'")
            if not isinstance(chunk.metadata, dict): issues.append(f"Bad metadata type: {type(chunk.metadata)}")
            if chunk.start_idx < 0 or chunk.end_idx < 0 or chunk.end_idx < chunk.start_idx: issues.append(f"Invalid indices: start={chunk.start_idx}, end={chunk.end_idx}")

            if issues:
                 print(f"Warning ({doc_id}): Issues found at chunk {i}: {'; '.join(issues)}")
                 # Decide if any issue should make valid = False
                 if "Bad doc_id" in '; '.join(issues) or "Bad metadata type" in '; '.join(issues) or "Invalid indices" in '; '.join(issues):
                     valid = False # Consider these fatal

        if not valid: print(f"Error: Chunk verification failed for {doc_id}.")
        return valid

    def index_document(self, markdown_content: str, doc_id: str, pdf_path: Optional[Path]):
        """Processes, chunks, optionally finds pages, embeds, and indexes a single document."""
        print(f"\n--- Processing Document: {doc_id} ---")
        self.current_doc_id = doc_id # Set current doc ID for plotting context

        # 1. Chunking
        print("Creating chunks...")
        doc_chunks = self._create_markdown_chunks(markdown_content, doc_id)
        if not self._verify_chunks(doc_chunks, doc_id):
            print(f"Skipping further processing for {doc_id} due to chunk verification failure.")
            return # Stop processing this document

        print(f"Generated {len(doc_chunks)} valid chunks.")

        # 2. Page Finding (if PDF available and chunks exist)
        chunk_pages: List[Tuple[int, Tuple[Optional[int], float]]] = []
        if self.pdf_directory and pdf_path and pdf_path.exists() and doc_chunks:
            print(f"Attempting page finding with PDF: {pdf_path.name}")
            # Pass parameters from __init__ or defaults if needed
            chunk_pages = self.find_chunk_pages(doc_chunks, pdf_path, workers=os.cpu_count() or 4) # Use more workers

            # Update chunk metadata with page info
            num_updated = 0
            for chunk_index, (page_number, confidence) in chunk_pages:
                 # Check index validity from find_chunk_pages which returns original index
                 if 0 <= chunk_index < len(doc_chunks):
                    doc_chunks[chunk_index].metadata['page_number'] = page_number
                    doc_chunks[chunk_index].metadata['page_confidence'] = confidence
                    num_updated += 1
                 else: print(f"Warning ({doc_id}): Invalid chunk index {chunk_index} received from page finding. Max index: {len(doc_chunks)-1}")
            if num_updated != len(chunk_pages): print(f"Warning ({doc_id}): Mismatch in updated page metadata count ({num_updated} vs {len(chunk_pages)} results)")

        elif self.pdf_directory and pdf_path and not pdf_path.exists():
             print(f"Note ({doc_id}): Provided PDF path does not exist '{pdf_path}'. Skipping page estimation.")
        elif self.pdf_directory and not pdf_path:
             print(f"Note ({doc_id}): No matching PDF found for this document stem in the PDF directory. Skipping page estimation.")
        elif not doc_chunks:
             print(f"Note ({doc_id}): No chunks generated, skipping page estimation.")
        # No message needed if self.pdf_directory is None (already handled in __init__)

        # 3. Plotting (if enabled and data available)
        if self.generate_plots:
            print(f"Generating plots for {doc_id}...")
            if doc_chunks:
                self.plot_chunk_length_distribution(doc_chunks, doc_id)
            if chunk_pages: # Only plot page-related things if page finding ran
                self.plot_chunk_page_mapping(chunk_pages, doc_id)
                self.plot_page_confidence_analysis(chunk_pages, doc_id)
            else: print(f"Skipping page plots for {doc_id} (no page data).")

        # 4. Embedding (if chunks exist)
        if not doc_chunks:
             print(f"Skipping embedding and indexing for {doc_id} as there are no chunks.")
             return

        try:
            # Format chunks specifically for the E5 model
            chunk_texts_formatted = [self._format_chunk_for_e5(chunk.text) for chunk in doc_chunks]
            if not chunk_texts_formatted:
                 print(f"Warning ({doc_id}): No text content found in chunks to embed after formatting."); return

            print(f"Generating embeddings for {len(chunk_texts_formatted)} chunks ...")
            # Ensure model is accessible
            if not hasattr(self, 'model'):
                 print(f"Error ({doc_id}): Embedding model not loaded. Cannot embed."); return

            # Choose appropriate batch size based on available memory (adjust if needed)
            batch_size = 64 if torch.cuda.is_available() else 32
            print(f"Using batch size: {batch_size}")

            chunk_embeddings = self.model.encode(
                chunk_texts_formatted, batch_size=batch_size, normalize_embeddings=True, # Normalize for IP index
                show_progress_bar=True, convert_to_numpy=True
            )
            print("Embeddings generated.")

            # Ensure embeddings are float32 for FAISS
            if chunk_embeddings.dtype != np.float32:
                 print(f"Converting embeddings from {chunk_embeddings.dtype} to float32.")
                 chunk_embeddings = chunk_embeddings.astype(np.float32)

            # Check embedding dimension consistency
            if chunk_embeddings.shape[1] != self.embedding_dim:
                print(f"FATAL ERROR ({doc_id}): Embedding dimension mismatch! Expected {self.embedding_dim}, got {chunk_embeddings.shape[1]}. Aborting indexing for this doc.")
                return

            # 5. Indexing
            if self._index is None:
                print(f"Initializing FAISS index (IndexFlatIP) with dimension={self.embedding_dim}")
                # Using IndexFlatIP because we normalized embeddings (cosine similarity = dot product on normalized vectors)
                self._index = faiss.IndexFlatIP(self.embedding_dim)
                # Sanity check index type
                if not self._index: raise RuntimeError("Failed to initialize FAISS index.")

            # Add embeddings to index if they exist
            if isinstance(chunk_embeddings, np.ndarray) and chunk_embeddings.shape[0] > 0:
                 if self._index is not None: # Double check index exists
                    self._index.add(chunk_embeddings)
                    self._chunks.extend(doc_chunks) # Add corresponding chunks to the list
                    print(f"Added {len(doc_chunks)} chunks ({chunk_embeddings.shape[0]} vectors) to index for {doc_id}.")
                    print(f"Total items in index now: {self._index.ntotal}, Total chunks stored: {len(self._chunks)}")
                 else: print(f"Error ({doc_id}): Index is None, cannot add embeddings.")
            elif chunk_embeddings.shape[0] == 0:
                 print(f"Warning ({doc_id}): No embeddings were generated (possibly empty formatted text). Index not updated.")
            else:
                 # This case should ideally not happen if checks above pass
                 raise ValueError(f"({doc_id}) Embeddings type or shape unexpected: {type(chunk_embeddings)}, shape {chunk_embeddings.shape if isinstance(chunk_embeddings, np.ndarray) else 'N/A'}")

        except torch.cuda.OutOfMemoryError as oom_err:
            print(f"\n--- CUDA Out of Memory Error ({doc_id}) ---")
            print("Reduce batch size or model size if possible.")
            print(f"Error details: {oom_err}")
            torch.cuda.empty_cache()
            print("Attempted to clear CUDA cache. You might need to restart the script.")
            # Potentially try again with CPU or smaller batch? For now, just fail the doc.
            print(f"Failed to index document {doc_id} due to OOM.")
        except Exception as e:
            print(f"\n--- Error during embedding or indexing for {doc_id} ---")
            print(f"Error type: {type(e).__name__}")
            print(f"Error details: {e}")
            traceback.print_exc()
            print(f"Failed to index document {doc_id}.")


    def index_markdown_source(self, source_path: Union[str, Path], save_index_per_doc: bool = False) -> Dict[str, List[str]]:
        """
        Indexes Markdown files from a source path (file or directory).

        Args:
            source_path: Path to a single .md file or a directory containing .md files.
                         If relative, resolved relative to the script's directory.
            save_index_per_doc: If True, save index+chunks after each document.
                                If False, accumulates all docs into one index potentially
                                saved at the end (depends on self.save_index).

        Returns:
            A dictionary containing lists of 'success' and 'error' file paths processed.
        """
        try:
            # Resolve source path relative to script dir if it's relative
            path = Path(source_path)
            if not path.is_absolute():
                try:
                     script_dir = Path(__file__).parent.resolve()
                     path = script_dir / path
                     print(f"Resolved relative source path to: {path}")
                except NameError:
                     print(f"Warning: Cannot determine script directory for relative source path '{source_path}'. Using current working directory.")
                     path = Path.cwd() / path # Fallback to CWD

            if not path.exists():
                 print(f"Error: Source path does not exist: {path}")
                 return {"success": [], "error": [str(source_path)]} # Return original path in error

        except Exception as path_e:
             print(f"Error resolving source path '{source_path}': {path_e}")
             return {"success": [], "error": [str(source_path)]}


        results = {"success": [], "error": []}
        markdown_files_to_process: List[Tuple[Path, str]] = [] # List of (Path, doc_id)

        # --- Reset state if combining indices ---
        if not save_index_per_doc:
            # Only reset if we intend to build a single combined index
            if self._index is not None or self._chunks:
                print("Clearing previous index state for combined processing...")
                self._chunks = []
                self._index = None # FAISS index will be re-initialized on first add
                self.all_plot_data = {}
            else:
                 print("Index state already clear. Starting combined processing.")

        # --- Identify files ---
        if path.is_file():
            if path.suffix.lower() == '.md':
                markdown_files_to_process.append((path, path.stem)) # Use filename stem as doc_id
            else:
                results["error"].append(str(path))
                print(f"Error: Provided file is not a Markdown file (.md): {path}")
                return results
        elif path.is_dir():
            found_files = sorted(list(path.glob("*.md"))) # Sort for consistent processing order
            if not found_files:
                print(f"No *.md files found in directory: {path}")
                return results
            print(f"Found {len(found_files)} Markdown files in {path}.")
            markdown_files_to_process = [(md_file, md_file.stem) for md_file in found_files]
        else:
            results["error"].append(str(path))
            print(f"Error: Invalid source path (not a file or directory): {path}")
            return results

        # --- Process files ---
        total_files = len(markdown_files_to_process)
        for i, (md_path, doc_id) in enumerate(markdown_files_to_process):
            print(f"\n[{i+1}/{total_files}] Starting processing: {md_path.name} (ID: {doc_id})")

            if save_index_per_doc: # Reset state before each doc if saving per-doc
                 self._chunks = []
                 self._index = None # Re-init index for each doc
                 # Optionally reset plot data too if plots should be strictly per-doc
                 # self.all_plot_data = {} # Keep commented if summary plot should include all processed

            # Find corresponding PDF using the doc_id (stem)
            pdf_path: Optional[Path] = None
            if self.pdf_directory and self.pdf_file_paths: # Check if PDF dir and mapping exist
                 pdf_path = self.pdf_file_paths.get(doc_id)
                 if pdf_path: print(f"Found corresponding PDF: {pdf_path.name}")
                 # else: print(f"No matching PDF found for stem '{doc_id}'") # Can be verbose
            # else: print("PDF directory not configured or no PDFs found, skipping PDF lookup.") # Also potentially verbose

            try:
                # Read Markdown content with error handling
                with open(md_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                if not content.strip():
                     print(f"Warning: Markdown file is empty or contains only whitespace: {md_path.name}. Skipping.")
                     results["error"].append(str(md_path)) # Count as error or skip? Let's count as error.
                     continue

                # Core processing function call
                self.index_document(content, doc_id, pdf_path)

                # Check if indexing actually added anything for this doc before claiming success
                # This depends on whether index_document added to self._chunks or self._index
                # If saving per doc, check if self._index exists now
                processed_successfully = False
                if save_index_per_doc:
                    processed_successfully = self._index is not None and self._index.ntotal > 0
                else:
                    # If combining, success means *something* was processed, check overall counts later
                    # For now, assume success if index_document didn't raise fatal error
                    processed_successfully = True # Revisit this logic? Maybe check chunk count diff?

                if processed_successfully:
                     results["success"].append(str(md_path))
                else:
                    # If index_document ran but resulted in no indexed data (e.g., only short chunks)
                    print(f"Note: Processing completed for {md_path.name}, but no data was added to the index.")
                    # Decide whether to count this as success or error - let's lean towards error if nothing indexed.
                    if str(md_path) not in results["error"]: # Avoid double listing if index_document failed earlier
                         results["error"].append(str(md_path))


                # --- Save per-document index if requested ---
                if self.save_index and save_index_per_doc:
                    if self._index is not None and self._chunks:
                         # Use doc_id for prefix to distinguish files
                         self._save_index_data(prefix=f"{doc_id}")
                    else:
                         print(f"Warning: No index/chunks generated for {doc_id} in this iteration. Nothing saved.")

            except FileNotFoundError:
                 results["error"].append(str(md_path))
                 print(f"--- ERROR processing {md_path.name}: File not found (unexpected). ---")
            except IOError as e:
                 results["error"].append(str(md_path))
                 print(f"--- ERROR processing {md_path.name}: IO Error reading file: {e} ---")
            except Exception as e:
                # Catch any other unexpected errors during the processing of a single file
                results["error"].append(str(md_path))
                print(f"--- UNEXPECTED ERROR processing {md_path.name}: {type(e).__name__} - {e} ---")
                traceback.print_exc() # Print detailed traceback for debugging

        # --- Final Actions after processing all files ---
        if self.generate_plots and self.all_plot_data:
            print("\nGenerating summary plot...")
            self._generate_summary_plot()

        # --- Save combined index if requested and not saving per doc ---
        if self.save_index and not save_index_per_doc:
            if self._index is not None and self._chunks:
                print("\nSaving combined index for all successfully processed documents...")
                self._save_index_data(prefix="combined_index") # Use a generic prefix
            elif results["success"]:
                 # This case means docs were processed, but maybe none resulted in indexable chunks
                 print("\nWarning: Processing finished, but no combined index was generated (no data added).")
            else:
                 print("\nNo documents were successfully processed or added to index. No combined index to save.")
        elif not self.save_index:
             print("\nIndex saving was disabled by configuration. No index files were written.")

        # --- Print Summary ---
        print("\n--- Indexing Run Summary ---")
        print(f"Total Markdown files found: {total_files}")
        print(f"Successfully processed files: {len(results['success'])}")
        print(f"Files with errors or no data indexed: {len(results['error'])}")
        if results["error"]:
            print("  Files with issues:")
            for error_file in results["error"]: print(f"    - {Path(error_file).name}")
        print("--- --- ---")
        return results


    def _generate_summary_plot(self):
        """Generates a plot comparing avg chunk length and total chunks across documents."""
        if not self.generate_plots or not self.all_plot_data: return
        if not self.plot_output_dir: print("Warning: Cannot save summary plot. Plot dir not set."); return

        doc_ids = list(self.all_plot_data.keys())
        if not doc_ids: print("No data collected for summary plot."); return

        avg_lengths = [d.get('avg_length', 0) for d in self.all_plot_data.values()]
        total_chunks = [d.get('total_chunks', 0) for d in self.all_plot_data.values()]

        # Filter out docs with no chunks if necessary, or plot them as 0
        valid_data = [(doc_id, length, count) for doc_id, length, count in zip(doc_ids, avg_lengths, total_chunks) if count > 0]
        if not valid_data: print("No documents with valid chunk data for summary plot."); return

        plot_doc_ids, plot_avg_lengths, plot_total_chunks = zip(*valid_data)

        num_docs = len(plot_doc_ids)
        fig, axes = plt.subplots(2, 1, figsize=(max(12, num_docs * 0.6), 10), sharex=True) # Share X axis
        fig.suptitle('Document Indexing Summary Comparison', fontsize=16)

        # Plot 1: Average Chunk Length
        axes[0].bar(plot_doc_ids, plot_avg_lengths, color='teal', alpha=0.8)
        axes[0].set(ylabel='Avg Chunk Length (chars)', title='Average Chunk Length per Document')
        axes[0].grid(True, axis='y', linestyle='--', alpha=0.6)
        axes[0].tick_params(axis='y', labelsize=9)

        # Plot 2: Total Chunks
        axes[1].bar(plot_doc_ids, plot_total_chunks, color='coral', alpha=0.8)
        axes[1].set(ylabel='Total Chunks', title='Total Chunks per Document')
        axes[1].grid(True, axis='y', linestyle='--', alpha=0.6)
        axes[1].tick_params(axis='y', labelsize=9)

        # Shared X axis labels
        plt.xticks(rotation=45, ha='right', fontsize=9) # Rotate labels for better readability

        plt.tight_layout(rect=[0, 0.03, 1, 0.95]) # Adjust layout to prevent overlap

        # Ensure plot output dir exists (it should from __init__)
        self.plot_output_dir.mkdir(parents=True, exist_ok=True)
        filepath = self.plot_output_dir / "summary_comparison_plot.png"
        try:
             fig.savefig(filepath, bbox_inches='tight', dpi=150)
             print(f"Summary plot saved: {filepath}")
        except Exception as e: print(f"Error saving summary plot {filepath}: {e}")
        finally: plt.close(fig) # Close plot


    def _save_index_data(self, prefix: str = "index"):
        """Internal helper to save the current FAISS index and chunk data."""
        # This method assumes self.save_index was already checked by the caller
        # and self.output_dir is set correctly (and exists)
        if self._index is None or not self._chunks:
            print(f"Warning: Index or chunks empty for prefix '{prefix}'. Nothing saved.")
            return
        if not self.output_dir: # Should not happen if save_index is true, but check anyway
             print("Error: Output directory is not set. Cannot save index data.")
             return

        index_path = self.output_dir / f"{prefix}_faiss_index.bin"
        chunks_path = self.output_dir / f"{prefix}_chunks.pkl"

        try:
            # Ensure index vectors match chunk count - critical!
            if self._index.ntotal != len(self._chunks):
                print(f"CRITICAL ERROR saving index for prefix '{prefix}':")
                print(f"  FAISS index vectors ({self._index.ntotal}) != Number of chunks ({len(self._chunks)})")
                print("  Index and chunks mismatch. Aborting save to prevent corruption.")
                # Consider adding more diagnostics here if possible
                # For example, which doc processing caused the mismatch?
                return # Do not save inconsistent data

            print(f"Saving FAISS index ({self._index.ntotal} vectors) to: {index_path}")
            faiss.write_index(self._index, str(index_path))

            print(f"Saving {len(self._chunks)} chunks metadata to: {chunks_path}")
            with open(chunks_path, "wb") as f:
                pickle.dump(self._chunks, f, protocol=pickle.HIGHEST_PROTOCOL) # Use highest protocol

            print(f"Index and chunks for '{prefix}' saved successfully to {self.output_dir}.")

        except Exception as e:
            print(f"\n--- Error saving index/chunks for prefix '{prefix}' ---")
            print(f"Attempted save path: {self.output_dir}")
            print(f"Error type: {type(e).__name__}")
            print(f"Error details: {e}")
            traceback.print_exc()
            # Cleanup potentially partially written files?
            if index_path.exists():
                 try: index_path.unlink(); print(f"Removed potentially corrupt file: {index_path}")
                 except OSError: pass
            if chunks_path.exists():
                 try: chunks_path.unlink(); print(f"Removed potentially corrupt file: {chunks_path}")
                 except OSError: pass


    # Public save method (optional, if manual saving outside index_markdown_source is needed)
    def save_index_to_disk(self, prefix: str = "manual_save"):
         """Manually triggers saving the current index state if saving is enabled."""
         if self.save_index:
             print(f"\nManual save requested with prefix '{prefix}'...")
             self._save_index_data(prefix=prefix)
         else:
              print("\nManual save requested, but index saving is disabled in the configuration.")


    def get_statistics(self) -> Dict[str, Any]:
        """Returns statistics about the currently loaded index and chunks."""
        total_chunks = len(self._chunks)
        if self._index is None:
            index_vectors = 0
            is_trained = False
            index_dim = self.embedding_dim # Assumed dim even if index not created
        else:
            index_vectors = self._index.ntotal
            is_trained = self._index.is_trained # Relevant for some index types
            index_dim = self._index.d

        unique_doc_ids = set(chunk.doc_id for chunk in self._chunks)

        stats = {
            "total_chunks_stored": total_chunks,
            "unique_documents_in_chunks": len(unique_doc_ids),
            "faiss_index_vectors": index_vectors,
            "faiss_index_dimensionality": index_dim,
            "faiss_index_is_trained": is_trained,
        }
        # Add a check for consistency
        if self._index is not None and total_chunks != index_vectors:
             stats["consistency_warning"] = f"Mismatch: {total_chunks} chunks vs {index_vectors} vectors!"

        return stats


    def get_unique_documents(self) -> List[str]:
        """Returns a sorted list of unique document IDs present in the loaded chunks."""
        if not self._chunks: return []
        return sorted(list(set(chunk.doc_id for chunk in self._chunks)))


# --- Main Execution Block ---

if __name__ == "__main__":
    print("--- Starting Document Indexing Process ---")
    # Get the directory where the script is located
    try:
        SCRIPT_DIR = Path(__file__).parent.resolve()
    except NameError:
        print("Warning: Cannot determine script directory automatically (__file__ not defined). Using current working directory.")
        SCRIPT_DIR = Path.cwd()

    print(f"Script directory: {SCRIPT_DIR}")

    # --- Configuration ---
    # Define paths RELATIVE TO THE SCRIPT DIRECTORY for portability
    PDF_DIR_REL = r"data/pdf_documents"
    MARKDOWN_SOURCE_REL = r"data/markdown_no_instruct" # Directory or single file relative path
    OUTPUT_INDEX_DIR_REL = "index"              # Relative path for index output
    PLOT_OUTPUT_DIR_REL = "document_indexing_plots"    # Relative path for plot output

    # Resolve paths based on script directory
    PDF_DIR = SCRIPT_DIR / PDF_DIR_REL
    MARKDOWN_SOURCE = SCRIPT_DIR / MARKDOWN_SOURCE_REL
    # Output directories will be handled inside the class constructor relative to script dir

    MODEL = "intfloat/multilingual-e5-large-instruct"
    EMBEDDING_DIMENSION = 1024

    # --- Control Flags ---
    GENERATE_PLOTS_FLAG = True       # Generate plots?
    SAVE_INDEX_FLAG = True           # Save the index to disk?
    SAVE_INDEX_PER_DOC_FLAG = True  # Save one index per doc, or one combined?

    # --- Initialization ---
    print("\n--- Initializing Indexer ---")
    try:
        indexer = MarkdownDocumentIndexer(
            # Provide absolute or relative paths (relative will be resolved inside constructor)
            pdf_directory=PDF_DIR, # Pass resolved absolute path
            model_name=MODEL,
            embedding_dim=EMBEDDING_DIMENSION,
            generate_plots=GENERATE_PLOTS_FLAG,
            plot_output_dir=PLOT_OUTPUT_DIR_REL,    # Pass relative path, resolved inside
            save_index=SAVE_INDEX_FLAG,             # Pass the flag here
            output_dir=OUTPUT_INDEX_DIR_REL         # Pass relative path, resolved inside
        )
    except Exception as main_init_error:
         print(f"\n--- CRITICAL ERROR DURING INITIALIZATION ---")
         print(f"{type(main_init_error).__name__}: {main_init_error}")
         traceback.print_exc()
         print("Exiting program.")
         exit(1)

    # --- Indexing ---
    print(f"\n--- Starting Indexing ---")
    print(f"Source: {MARKDOWN_SOURCE}")
    # The indexer's __init__ already printed where files will be saved if save_index=True
    print(f"Save index per document: {SAVE_INDEX_PER_DOC_FLAG}")

    # Call the indexing function
    results = indexer.index_markdown_source(
        source_path=MARKDOWN_SOURCE, # Pass resolved absolute path
        save_index_per_doc=SAVE_INDEX_PER_DOC_FLAG, # Pass per-doc flag here
    )

    # --- Final Statistics (Optional) ---
    print("\n--- Final Index State Statistics ---")
    stats = indexer.get_statistics()
    for key, value in stats.items():
        # Improved formatting for clarity
        key_formatted = key.replace('_', ' ').title()
        print(f"{key_formatted:<30}: {value}")

    if stats.get("total_chunks_stored", 0) > 0:
        unique_docs = indexer.get_unique_documents()
        print(f"\n{'Documents in Final Index':<30}: {len(unique_docs)}")
        # Display first few document IDs
        display_limit = 15
        if unique_docs:
             docs_str = ', '.join(unique_docs[:display_limit])
             if len(unique_docs) > display_limit: docs_str += '...'
             print(f"  Examples: {docs_str}")

    # Example of manually saving if needed (and if saving is enabled)
    # print("\nAttempting manual save (if enabled)...")
    # indexer.save_index_to_disk(prefix="final_manual_save")

    print("\n--- Indexing Process Complete ---")