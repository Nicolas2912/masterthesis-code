# metrics.py
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
import torch
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from pathlib import Path
import sys
import os
from dotenv import load_dotenv
from pathlib import Path
from typing import Optional, Dict, Any, List
import matplotlib.pyplot as plt
import time
import os
import base64
import traceback
import threading

import concurrent.futures
import time
import os
import base64
import traceback
import gc
import signal
from contextlib import contextmanager
import logging
from typing import Optional, Dict, Any, List

# Add necessary imports for Gemini/Vertex AI
from langchain_google_vertexai import (
    ChatVertexAI,
    HarmBlockThreshold,
    HarmCategory
)
from deepeval.models.base_model import DeepEvalBaseLLM

# Suppress excessive logging from google.api_core
logging.getLogger('google.api_core').setLevel(logging.WARNING)
logging.getLogger('google.auth').setLevel(logging.WARNING)
logging.getLogger('google.cloud').setLevel(logging.WARNING)

class TimeoutException(Exception):
    pass

# Add necessary imports
sys.path.append('.')  # Add current directory to path to ensure imports work

# Import data models in case they're needed for deserialization
from data_models import Chunk, RAGResponse, ImageMetadata

@contextmanager
def timeout_context(seconds):
    """Context manager for enforcing timeouts using SIGALRM."""
    def handle_timeout(signum, frame):
        raise TimeoutException("Operation timed out")
    
    # Only set alarm on platforms that support it (not Windows)
    if hasattr(signal, 'SIGALRM'):
        signal.signal(signal.SIGALRM, handle_timeout)
        signal.alarm(seconds)
    try:
        yield
    finally:
        if hasattr(signal, 'SIGALRM'):
            signal.alarm(0)  # Reset the alarm


def process_image(path):
    """Process image file to base64 string for MLLMImage."""
    try:
        print(f"Processing image at: {path}")
        
        # Open and read the raw image file
        with open(path, "rb") as f:
            img_data = f.read()
            
        # Directly encode the raw bytes
        encoded_string = base64.b64encode(img_data).decode('utf-8')
        
        # Create MLLMImage with base64 data
        mime_type = "image/png"  # Assuming PNG format
        img_obj = MLLMImage(
            data=f"data:{mime_type};base64,{encoded_string}",
            mime_type=mime_type
        )
        
        print(f"Successfully processed image ({len(encoded_string)} bytes)")
        return img_obj
    
    except Exception as e:
        print(f"Error processing image: {str(e)}")
        print(f"File exists check: {os.path.exists(path)}")
        print(f"File size: {os.path.getsize(path) if os.path.exists(path) else 'N/A'} bytes")
        # Add traceback for debugging
        import traceback
        traceback.print_exc()
        return None

class Metric(ABC):
    """Base class for evaluation metrics."""

    @abstractmethod
    def calculate(self, prediction: str, reference: str, **kwargs) -> float:
        """Calculate the metric between prediction and reference.

        Additional keyword arguments may be required by specific metrics.
        """
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the metric."""
        pass

    def visualize(self, results: pd.DataFrame, output_dir: Optional[str] = None) -> None:
        """Visualize results for this metric."""
        pass

    def summarize(self, results: pd.DataFrame) -> Dict[str, Any]:
        """Generate summary statistics for this metric."""
        pass


class AlphaSimilarity(Metric):
    """
    Alpha similarity metric using embedding cosine similarity.

    This metric calculates the cosine similarity between embeddings of
    prediction and reference texts as a measure of semantic similarity.
    """

    def __init__(self, embedding_model: str = "sentence-transformers/all-mpnet-base-v2"):
        self.model_name = embedding_model
        self._model = None
        self.last_reason = None  # Add this to store reasoning


    @property
    def embedding_model(self):
        """Lazy load the embedding model."""
        if self._model is None:
            self._model = SentenceTransformer(self.model_name)
            # Move to GPU if available
            if torch.cuda.is_available():
                self._model = self._model.to("cuda")
        return self._model

    def cleanup(self):
        """Release resources and clear memory."""
        if self._model is not None:
            print(f"Unloading {self.name} embedding model...")
            # Delete the model reference
            self._model = None
            # Force garbage collection
            import gc
            gc.collect()
            # Clear CUDA cache if available
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
                print(f"{self.name} model unloaded and GPU memory cleared")

    def calculate(self, prediction: str, reference: str, **kwargs) -> float:
        """Calculate alpha similarity between prediction and reference."""
        # Existing implementation - ignores kwargs
        if not prediction or not reference:
            self.last_reason = "Empty prediction or reference"
            return 0.0

        start = time.time()

        try:
            # Generate embeddings
            embedding1 = self.embedding_model.encode([prediction])[0]
            embedding2 = self.embedding_model.encode([reference])[0]

            # Calculate cosine similarity
            similarity = cosine_similarity([embedding1], [embedding2])[0][0]

            print(f"Alpha Similarity calculation time: {round(time.time() - start, 3)}s")

            if similarity > 0.9:
                self.last_reason = f"The prediction and reference have extremely high semantic similarity ({similarity:.4f}), indicating nearly identical meaning."
            elif similarity > 0.8:
                self.last_reason = f"The prediction and reference have very high semantic similarity ({similarity:.4f}), capturing most of the same information."
            elif similarity > 0.7:
                self.last_reason = f"The prediction and reference have good semantic similarity ({similarity:.4f}), sharing significant meaning."
            elif similarity > 0.5:
                self.last_reason = f"The prediction and reference have moderate semantic similarity ({similarity:.4f}), with some shared concepts."
            else:
                self.last_reason = f"The prediction and reference have low semantic similarity ({similarity:.4f}), with significant differences in meaning."

            return float(similarity)
        except Exception as e:
            print(f"Error calculating alpha similarity: {str(e)}")
            return 0.0

    @property
    def name(self) -> str:
        return "alpha_similarity"

    def visualize(self, results: pd.DataFrame, output_dir: Optional[str] = None) -> None:
        """Visualize alpha similarity results."""
        # Filter out entries without alpha similarity
        valid_results = results[results[self.name].notna()]

        if len(valid_results) == 0:
            print(f"No valid results to visualize for {self.name}.")
            return

        # Create output directory if needed
        if output_dir:
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)

        # Create histogram
        plt.figure(figsize=(10, 6))
        plt.hist(valid_results[self.name], bins=10, alpha=0.7)
        plt.title(f"Distribution of {self.name.replace('_', ' ').title()} Scores")
        plt.xlabel(self.name.replace('_', ' ').title())
        plt.ylabel("Count")
        plt.grid(True, alpha=0.3)
        if output_dir:
            plt.savefig(output_dir / f"{self.name}_histogram.png")
            plt.close()
        else:
            plt.show()

        # Create box plots by category
        if "category" in valid_results.columns:
            plt.figure(figsize=(12, 6))
            valid_results.boxplot(column=[self.name], by="category")
            plt.title(f"{self.name.replace('_', ' ').title()} by Question Category")
            plt.suptitle("")  # Remove default title
            plt.ylabel(self.name.replace('_', ' ').title())
            plt.grid(True, alpha=0.3)
            plt.xticks(rotation=45)
            if output_dir:
                plt.savefig(output_dir / f"{self.name}_by_category.png")
                plt.close()
            else:
                plt.show()

    def summarize(self, results: pd.DataFrame) -> Dict[str, Any]:
        """Generate summary statistics for alpha similarity."""
        try:
            valid_results = results[results[self.name].notna()]

            if len(valid_results) == 0:
                return {
                    "mean": None,
                    "median": None,
                    "min": None,
                    "max": None,
                    "by_category": {}
                }

            summary = {
                "mean": float(valid_results[self.name].mean()),
                "median": float(valid_results[self.name].median()),
                "min": float(valid_results[self.name].min()),
                "max": float(valid_results[self.name].max()),
                "by_category": {}
            }

            if "category" in valid_results.columns:
                category_means = valid_results.groupby("category")[self.name].mean()
                for category, mean in category_means.items():
                    summary["by_category"][category] = float(mean)

            reasoning_column = f"{self.name}_reasoning"
            if reasoning_column in results.columns:
                valid_reasoning = results[results[reasoning_column].notna()]
                if len(valid_reasoning) > 0:
                    # Include up to 3 sample reasoning entries
                    sample_size = min(3, len(valid_reasoning))
                    samples = valid_reasoning.sample(sample_size)
                    
                    summary["sample_reasoning"] = []
                    for _, row in samples.iterrows():
                        summary["sample_reasoning"].append({
                            "question_id": row.get("id", "unknown"),
                            "score": row.get(self.name, 0.0),
                            "reasoning": row.get(reasoning_column, "No reasoning provided")
                        })

            return summary
        except Exception as e:
            print(f"Error summarizing results: {str(e)}")
            return {
                "mean": None,
                "median": None,
                "min": None,
                "max": None,
                "by_category": {},
                "error": str(e)
            }


class GoogleVertexAI(DeepEvalBaseLLM):
    """Class to implement Vertex AI for DeepEval"""
    def __init__(self, model):
        self.model = model

    def load_model(self):
        return self.model

    def generate(self, prompt: str) -> str:
        chat_model = self.load_model()
        try:
            if not callable(getattr(chat_model, 'invoke', None)):
                 raise TypeError("Loaded model does not have an 'invoke' method.")
            # print(f"Generating response for prompt: '{prompt[:50]}...'") # Optional: uncomment for debug
            response = chat_model.invoke(prompt).content
            # print(f"Received response: '{response[:50]}...'") # Optional: uncomment for debug
            return response
        except Exception as e:
            print(f"Error during Vertex AI generation: {e}")
            traceback.print_exc()
            return f"[Vertex AI Error: {e}]"

    async def a_generate(self, prompt: str) -> str:
        chat_model = self.load_model()
        try:
            if not callable(getattr(chat_model, 'ainvoke', None)):
                 raise TypeError("Loaded model does not have an 'ainvoke' method.")
            # print(f"Async generating response for prompt: '{prompt[:50]}...'") # Optional: uncomment for debug
            res = await chat_model.ainvoke(prompt)
            # print(f"Received async response: '{res.content[:50]}...'") # Optional: uncomment for debug
            return res.content
        except Exception as e:
            print(f"Error during async Vertex AI generation: {e}")
            traceback.print_exc()
            return f"[Vertex AI Error: {e}]"

    def get_model_name(self):
        try:
            # Try to get the specific model name from the wrapped Langchain model
            if hasattr(self.model, 'model_name'):
                return f"Vertex AI ({self.model.model_name})"
        except Exception:
            pass # Fallback if attribute doesn't exist or causes error
        return "Vertex AI Model" # Generic fallback


class QuestionAnswerRelevanceMetric(Metric):
    """Measures relevance of an answer to a question using deepeval."""

    # Simplified __init__ accepting a pre-configured model object or name string
    def __init__(self, threshold=0.7, include_reason=True, model=None, async_mode=True, **kwargs):
        from deepeval.metrics import AnswerRelevancyMetric
        
        # Store model info for summarization
        if isinstance(model, str): # OpenAI model name
             self.model_description = f"OpenAI ({model})"
             self._setup_openai() # Still need to ensure API key is loaded if using OpenAI
        elif hasattr(model, 'get_model_name'): # Wrapped models like GoogleVertexAI
             self.model_description = model.get_model_name()
        else:
             self.model_description = "Unknown/Not Provided"

        if model is None:
            print(f"Warning: No model provided for {type(self).__name__}. Metric cannot be calculated.")
            self.deepeval_metric = None
            return

        # Initialize DeepEval metric
        try:
            # Pass the model object/string directly
            self.deepeval_metric = AnswerRelevancyMetric(
                threshold=threshold,
                model=model,
                include_reason=include_reason,
                async_mode=async_mode, # Pass async_mode
                **kwargs # Pass any other relevant kwargs
            )
            self.last_reason = None
        except Exception as e:
            print(f"Error initializing DeepEval {type(self).__name__} with model '{self.model_description}': {e}")
            traceback.print_exc()
            self.deepeval_metric = None # Mark as unusable

    def calculate(self, prediction: str, reference: str, **kwargs) -> float:
        """Calculate answer relevancy score."""
        if self.deepeval_metric is None:
            print(f"Skipping {self.name} calculation as DeepEval metric initialization failed.")
            return np.nan # Use NaN for skipped/failed calculations

        from deepeval.test_case import LLMTestCase
        question = kwargs.get('question', '')
        test_case = LLMTestCase(input=question, actual_output=prediction)

        try:
            self.deepeval_metric.measure(test_case)
            self.last_reason = self.deepeval_metric.reason
            # Ensure score is float or handle None
            score = self.deepeval_metric.score
            return float(score) if score is not None else np.nan
        except Exception as e:
             print(f"Error during {self.name} measurement with model '{self.model_description}': {e}")
             # traceback.print_exc() # Optional: reduce noise
             self.last_reason = f"Error: {e}"
             return np.nan # Use NaN for errors


    @property
    def name(self) -> str:
        return "question_answer_relevance"

    def _setup_openai(self):
        """Setup OpenAI API key from .env file"""
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("Warning: OPENAI_API_KEY not found in .env file")

    def visualize(self, results: pd.DataFrame, output_dir: Optional[str] = None) -> None:
        # ... (Keep existing implementation, should work with self.name) ...
        pass # Placeholder

    def summarize(self, results: pd.DataFrame) -> Dict[str, Any]:
        # Adjusted summary logic
        summary_dict = {"mean": None, "median": None, "min": None, "max": None, "by_category": {}}
        try:
            # Use self.name which comes from the property
            metric_col = self.name
            valid_results = results[results[metric_col].notna()]

            if not valid_results.empty:
                 summary_dict["mean"] = float(valid_results[metric_col].mean())
                 summary_dict["median"] = float(valid_results[metric_col].median())
                 summary_dict["min"] = float(valid_results[metric_col].min())
                 summary_dict["max"] = float(valid_results[metric_col].max())
                 if "category" in valid_results.columns:
                     category_means = valid_results.groupby("category")[metric_col].mean()
                     summary_dict["by_category"] = {cat: float(mean) for cat, mean in category_means.items()}

            # Add LLM provider info stored during __init__
            summary_dict["model_used"] = self.model_description

            reasoning_column = f"{metric_col}_reasoning"
            if reasoning_column in results.columns:
                 # ... (Keep existing reasoning sampling logic) ...
                 valid_reasoning = results[results[reasoning_column].notna()]
                 if len(valid_reasoning) > 0:
                     sample_size = min(3, len(valid_reasoning))
                     samples = valid_reasoning.sample(sample_size)
                     summary_dict["sample_reasoning"] = []
                     for _, row in samples.iterrows():
                          summary_dict["sample_reasoning"].append({
                              "question_id": row.get("id", "unknown"),
                              "score": row.get(metric_col, np.nan),
                              "reasoning": row.get(reasoning_column, "No reasoning provided")
                          })
            return summary_dict
        except Exception as e:
             print(f"Error summarizing {metric_col} results: {e}")
             summary_dict["error"] = str(e)
             return summary_dict


class HallucinationMetric(Metric):
    """Measures hallucination in generated answers using deepeval."""

    # Simplified __init__
    def __init__(self, threshold=0.5, include_reason=True, model=None, async_mode=True, **kwargs):
        from deepeval.metrics import HallucinationMetric as DeepEvalHallucinationMetric

        if isinstance(model, str): self.model_description = f"OpenAI ({model})"; self._setup_openai()
        elif hasattr(model, 'get_model_name'): self.model_description = model.get_model_name()
        else: self.model_description = "Unknown/Not Provided"

        if model is None:
            print(f"Warning: No model provided for {type(self).__name__}. Metric cannot be calculated.")
            self.deepeval_metric = None; return

        try:
            self.deepeval_metric = DeepEvalHallucinationMetric(
                threshold=threshold, model=model, include_reason=include_reason, async_mode=async_mode, **kwargs
            )
            self.last_reason = None
        except Exception as e:
             print(f"Error initializing DeepEval {type(self).__name__} with model '{self.model_description}': {e}")
             traceback.print_exc(); self.deepeval_metric = None

    def calculate(self, prediction: str, reference: str, **kwargs) -> float:
        """Calculate hallucination score."""
        if self.deepeval_metric is None: print(f"Skipping {self.name} calculation."); return np.nan
        from deepeval.test_case import LLMTestCase
        context = kwargs.get('context', [])
        test_case = LLMTestCase(input="", actual_output=prediction, context=context)
        try:
            self.deepeval_metric.measure(test_case)
            self.last_reason = self.deepeval_metric.reason
            score = self.deepeval_metric.score
            return float(score) if score is not None else np.nan
        except Exception as e:
             print(f"Error during {self.name} measurement with model '{self.model_description}': {e}")
             # traceback.print_exc()
             self.last_reason = f"Error: {e}"; return np.nan

    @property
    def name(self) -> str:
        return "hallucination"

    def _setup_openai(self):
        """Setup OpenAI API key from .env file"""
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("Warning: OPENAI_API_KEY not found in .env file")

    def visualize(self, results: pd.DataFrame, output_dir: Optional[str] = None) -> None:
        # ... (Keep existing implementation) ...
        pass # Placeholder

    # Use the same summarize logic as QuestionAnswerRelevanceMetric by inheriting or copying
    summarize = QuestionAnswerRelevanceMetric.summarize


class FaithfulnessMetric(Metric):
    """Measures faithfulness of generated answers to the retrieved context."""

    # Simplified __init__
    def __init__(self, threshold=0.7, include_reason=True, model=None, async_mode=True, **kwargs):
        from deepeval.metrics import FaithfulnessMetric as DeepEvalFaithfulnessMetric

        if isinstance(model, str): self.model_description = f"OpenAI ({model})"; self._setup_openai()
        elif hasattr(model, 'get_model_name'): self.model_description = model.get_model_name()
        else: self.model_description = "Unknown/Not Provided"

        if model is None:
            print(f"Warning: No model provided for {type(self).__name__}. Metric cannot be calculated.")
            self.deepeval_metric = None; return

        try:
            self.deepeval_metric = DeepEvalFaithfulnessMetric(
                threshold=threshold, model=model, include_reason=include_reason, async_mode=async_mode, **kwargs
            )
            self.last_reason = None
        except Exception as e:
             print(f"Error initializing DeepEval {type(self).__name__} with model '{self.model_description}': {e}")
             traceback.print_exc(); self.deepeval_metric = None

    def calculate(self, prediction: str, reference: str, **kwargs) -> float:
        """Calculate faithfulness score."""
        if self.deepeval_metric is None: print(f"Skipping {self.name} calculation."); return np.nan
        from deepeval.test_case import LLMTestCase
        retrieval_context = kwargs.get('retrieval_context', [])
        test_case = LLMTestCase(input="", actual_output=prediction, retrieval_context=retrieval_context)
        try:
            self.deepeval_metric.measure(test_case)
            self.last_reason = self.deepeval_metric.reason
            score = self.deepeval_metric.score
            return float(score) if score is not None else np.nan
        except Exception as e:
             print(f"Error during {self.name} measurement with model '{self.model_description}': {e}")
             # traceback.print_exc()
             self.last_reason = f"Error: {e}"; return np.nan

    @property
    def name(self) -> str:
        return "faithfulness"

    def _setup_openai(self):
        """Setup OpenAI API key from .env file"""
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("Warning: OPENAI_API_KEY not found in .env file")

    def visualize(self, results: pd.DataFrame, output_dir: Optional[str] = None) -> None:
        # ... (Keep existing implementation) ...
        pass # Placeholder

    # Use the same summarize logic
    summarize = QuestionAnswerRelevanceMetric.summarize

class MultimodalAnswerRelevancyMetric(Metric):
    """Measures relevancy of generated answers in multimodal contexts."""

    def __init__(self, threshold=0.7, model="gpt-4o-mini", include_reason=True, figures_base_dir=None):
        from deepeval.metrics import MultimodalAnswerRelevancyMetric as DeepEvalMultimodalAnswerRelevancyMetric
        # Load API key
        self._setup_openai()
        self.deepeval_metric = DeepEvalMultimodalAnswerRelevancyMetric(
            threshold=threshold,
            model=model,
            include_reason=include_reason,
            async_mode=False,
            verbose_mode=False
        )
        self.last_reason = None
        # Store base directory for extracted figures
        self.figures_base_dir = figures_base_dir

    def _preprocess_image(self, img_path, max_size=(800, 800)):
        """Reduces image size to avoid memory and API issues."""
        from PIL import Image
        import io
        
        try:
            with Image.open(img_path) as img:
                # Resize if larger than max dimensions
                if img.width > max_size[0] or img.height > max_size[1]:
                    img.thumbnail(max_size)
                    
                # Save to buffer
                buffer = io.BytesIO()
                img.save(buffer, format="PNG", optimize=True)
                buffer.seek(0)
                return buffer.read()
        except Exception as e:
            print(f"Error preprocessing image: {str(e)}")
            return None

    def calculate(self, prediction: str, reference: str, **kwargs) -> float:
        """Calculate multimodal answer relevancy score."""
        from deepeval.test_case import MLLMTestCase, MLLMImage
        import base64
        import os
        
        # Get required parameters from kwargs
        input_text = kwargs.get('input_text', '')
        input_images = kwargs.get('input_images', [])
        retrieval_context = kwargs.get('retrieval_context', [])
        document_name = kwargs.get('document_name', '')
        figures_dir = kwargs.get('figures_dir', self.figures_base_dir)
        
        print(f"\n==== {self.name} ====")
        print(f"Processing {len(input_images)} images for document: {document_name}")
        print(f"Figures directory: {figures_dir}")
        
        # Process input images
        processed_images = []
        for img_path in input_images:
            full_path = None
            # Try different possible paths
            possible_paths = [
                os.path.join(figures_dir, img_path) if figures_dir else None,
                os.path.join(f"extracted_figures/{document_name}", img_path),
                img_path
            ]
            possible_paths = [p for p in possible_paths if p]
            
            for path in possible_paths:
                if os.path.exists(path) and os.path.isfile(path):
                    full_path = path
                    break
            
            if full_path:
                try:
                    print(f"Processing image at: {full_path}")
                    # Read the image file
                    with open(full_path, "rb") as f:
                        img_data = f.read()
                    # img_data = self._preprocess_image(full_path)
                        
                    encoded_string = base64.b64encode(img_data).decode('utf-8')
                    img_obj = MLLMImage(f"data:image/png;base64,{encoded_string}")
                    processed_images.append(img_obj)
                    print("Successfully processed image")
                except Exception as e:
                    print(f"Error processing image: {str(e)}")
                    import traceback
                    traceback.print_exc()
            else:
                print(f"Could not find image: {img_path}")
                print(f"Tried paths: {possible_paths}")
        
        # If we have no images, return a default score
        if not processed_images:
            print(f"No images were processed, skipping {self.name}")
            return 0.0
            
        # Create the test case correctly
        try:
            # Input should be just the question text
            input_list = [input_text]
            
            # Output should include the text response and any images that should be 
            # considered part of the response (if applicable)
            output_list = [prediction]
            # If your response includes generated images (usually not the case in RAG):
            # output_list.extend(processed_images)
            
            # Retrieval context is the context used for generating the answer
            context_list = retrieval_context.copy()
            # Images should be included if they were part of the retrieved context
            context_list.extend(processed_images)
            
            # Create the test case with proper structure
            test_case = MLLMTestCase(
                input=input_list,  # Just the question text
                actual_output=output_list,  # Just the answer text
                retrieval_context=context_list  # All context including images
            )
            
            # Add timeout in case it hangs
            with timeout_context(60):  # 60-second timeout
                self.deepeval_metric.measure(test_case)
            
            # Store reason for later use and return score
            self.last_reason = self.deepeval_metric.reason
            return self.deepeval_metric.score
        except Exception as e:
            print(f"Error in {self.name}: {str(e)}")
            traceback.print_exc()
            return 0.0

    @property
    def name(self) -> str:
        return "multimodal_answer_relevancy"

    def _setup_openai(self):
        """Setup OpenAI API key from .env file"""
        from dotenv import load_dotenv
        import os
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("Warning: OPENAI_API_KEY not found in .env file")

    # Implement visualize and summarize methods
    def visualize(self, results: pd.DataFrame, output_dir: Optional[str] = None) -> None:
        """Visualize alpha similarity results."""
        # Filter out entries without alpha similarity
        valid_results = results[results[self.name].notna()]

        if len(valid_results) == 0:
            print(f"No valid results to visualize for {self.name}.")
            return

        # Create output directory if needed
        if output_dir:
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)

        # Create histogram
        plt.figure(figsize=(10, 6))
        plt.hist(valid_results[self.name], bins=10, alpha=0.7)
        plt.title(f"Distribution of {self.name.replace('_', ' ').title()} Scores")
        plt.xlabel(self.name.replace('_', ' ').title())
        plt.ylabel("Count")
        plt.grid(True, alpha=0.3)
        if output_dir:
            plt.savefig(output_dir / f"{self.name}_histogram.png")
            plt.close()
        else:
            plt.show()

        # Create box plots by category
        if "category" in valid_results.columns:
            plt.figure(figsize=(12, 6))
            valid_results.boxplot(column=[self.name], by="category")
            plt.title(f"{self.name.replace('_', ' ').title()} by Question Category")
            plt.suptitle("")  # Remove default title
            plt.ylabel(self.name.replace('_', ' ').title())
            plt.grid(True, alpha=0.3)
            plt.xticks(rotation=45)
            if output_dir:
                plt.savefig(output_dir / f"{self.name}_by_category.png")
                plt.close()
            else:
                plt.show()

    def summarize(self, results: pd.DataFrame) -> Dict[str, Any]:
        """Generate summary statistics."""
        try:
            valid_results = results[results[self.name].notna()]

            if len(valid_results) == 0:
                return {
                    "mean": None,
                    "median": None,
                    "min": None,
                    "max": None,
                    "by_category": {}
                }

            summary = {
                "mean": float(valid_results[self.name].mean()),
                "median": float(valid_results[self.name].median()),
                "min": float(valid_results[self.name].min()),
                "max": float(valid_results[self.name].max()),
                "by_category": {}
            }

            if "category" in valid_results.columns:
                category_means = valid_results.groupby("category")[self.name].mean()
                for category, mean in category_means.items():
                    summary["by_category"][category] = float(mean)

            reasoning_column = f"{self.name}_reasoning"
            if reasoning_column in results.columns:
                valid_reasoning = results[results[reasoning_column].notna()]
                if len(valid_reasoning) > 0:
                    # Include up to 3 sample reasoning entries
                    sample_size = min(3, len(valid_reasoning))
                    samples = valid_reasoning.sample(sample_size)
                    
                    summary["sample_reasoning"] = []
                    for _, row in samples.iterrows():
                        summary["sample_reasoning"].append({
                            "question_id": row.get("id", "unknown"),
                            "score": row.get(self.name, 0.0),
                            "reasoning": row.get(reasoning_column, "No reasoning provided")
                        })

            return summary
        except Exception as e:
            print(f"Error summarizing results: {str(e)}")
            return {
                "mean": None,
                "median": None,
                "min": None,
                "max": None,
                "by_category": {},
                "error": str(e)
            }

class MultimodalFaithfulnessMetric(Metric):
    """Measures faithfulness of generated answers in multimodal contexts."""

    def __init__(self, threshold=0.7, model="gpt-4o-mini", include_reason=True, figures_base_dir=None):
        from deepeval.metrics import MultimodalFaithfulnessMetric as DeepEvalMultimodalFaithfulnessMetric
        # Load API key
        self._setup_openai()
        self.deepeval_metric = DeepEvalMultimodalFaithfulnessMetric(
            threshold=threshold,
            model=model,
            include_reason=include_reason,
            async_mode=False,
            verbose_mode=False

        )
        self.last_reason = None
        # Store base directory for extracted figures
        self.figures_base_dir = figures_base_dir

    def calculate(self, prediction: str, reference: str, **kwargs) -> float:
        """Calculate multimodal faithfulness/answer relevancy score."""
        from deepeval.test_case import MLLMTestCase, MLLMImage
        import base64
        import os
        
        # Get required parameters from kwargs
        input_text = kwargs.get('input_text', '')
        input_images = kwargs.get('input_images', [])
        retrieval_context = kwargs.get('retrieval_context', [])
        document_name = kwargs.get('document_name', '')
        figures_dir = kwargs.get('figures_dir', self.figures_base_dir)
        
        print(f"\n==== {self.name} ====")
        print(f"Processing {len(input_images)} images for document: {document_name}")
        print(f"Figures directory: {figures_dir}")
        
        # Process input images
        processed_images = []
        for img_path in input_images:
            full_path = None
            # Try different possible paths
            possible_paths = [
                os.path.join(figures_dir, img_path) if figures_dir else None,
                os.path.join(f"extracted_figures/{document_name}", img_path),
                img_path
            ]
            possible_paths = [p for p in possible_paths if p]
            
            for path in possible_paths:
                if os.path.exists(path) and os.path.isfile(path):
                    full_path = path
                    break
            
            if full_path:
                try:
                    print(f"Processing image at: {full_path}")
                    # Read the image file
                    with open(full_path, "rb") as f:
                        img_data = f.read()
                        
                    # Create MLLMImage correctly - it expects the base64 data as a single argument
                    encoded_string = base64.b64encode(img_data).decode('utf-8')
                    img_obj = MLLMImage(f"data:image/png;base64,{encoded_string}")
                    processed_images.append(img_obj)
                    print(f"Successfully processed image")
                except Exception as e:
                    print(f"Error processing image: {str(e)}")
                    import traceback
                    traceback.print_exc()
            else:
                print(f"Could not find image: {img_path}")
                print(f"Tried paths: {possible_paths}")
        
        # If we have no images, return a default score
        if not processed_images:
            print(f"No images were processed, skipping {self.name}")
            return 0.0
            
        # Create the test case correctly
        try:
            # Input should be just the question text
            input_list = [input_text]
        
            # (Images would only go here if they were *generated* by the model, not for RAG)
            output_list = [prediction]
            
            # that were used as context for the answer
            context_list = []
            # Add text context first
            if isinstance(retrieval_context, list):
                context_list.extend(retrieval_context)
            # Add images to context
            context_list.extend(processed_images)
            
            # Create the test case
            test_case = MLLMTestCase(
                input=input_list,
                actual_output=output_list,
                retrieval_context=context_list
            )
            
            # Add timeout in case it hangs
            with timeout_context(60):  # 60-second timeout
                self.deepeval_metric.measure(test_case)
            
            # Store reason for later use and return score
            self.last_reason = self.deepeval_metric.reason
            return self.deepeval_metric.score
        except Exception as e:
            print(f"Error in {self.name}: {str(e)}")
            traceback.print_exc()
            return 0.0

    @property
    def name(self) -> str:
        return "multimodal_faithfulness"

    def _setup_openai(self):
        """Setup OpenAI API key from .env file"""
        from dotenv import load_dotenv
        import os
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("Warning: OPENAI_API_KEY not found in .env file")

    # Implement visualize and summarize methods
    def visualize(self, results: pd.DataFrame, output_dir: Optional[str] = None) -> None:
        """Visualize faithfulness results."""
        # Filter out entries without the metric
        valid_results = results[results[self.name].notna()]

        if len(valid_results) == 0:
            print(f"No valid results to visualize for {self.name}.")
            return

        # Create output directory if needed
        if output_dir:
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)

        # Create histogram
        plt.figure(figsize=(10, 6))
        plt.hist(valid_results[self.name], bins=10, alpha=0.7)
        plt.title(f"Distribution of {self.name.replace('_', ' ').title()} Scores")
        plt.xlabel(self.name.replace('_', ' ').title())
        plt.ylabel("Count")
        plt.grid(True, alpha=0.3)
        if output_dir:
            plt.savefig(output_dir / f"{self.name}_histogram.png")
            plt.close()
        else:
            plt.show()

        # Create box plots by category
        if "category" in valid_results.columns:
            plt.figure(figsize=(12, 6))
            valid_results.boxplot(column=[self.name], by="category")
            plt.title(f"{self.name.replace('_', ' ').title()} by Question Category")
            plt.suptitle("")  # Remove default title
            plt.ylabel(self.name.replace('_', ' ').title())
            plt.grid(True, alpha=0.3)
            plt.xticks(rotation=45)
            if output_dir:
                plt.savefig(output_dir / f"{self.name}_by_category.png")
                plt.close()
            else:
                plt.show()

    def summarize(self, results: pd.DataFrame) -> Dict[str, Any]:
        """Generate summary statistics."""
        try:
            valid_results = results[results[self.name].notna()]

            if len(valid_results) == 0:
                return {
                    "mean": None,
                    "median": None,
                    "min": None,
                    "max": None,
                    "by_category": {}
                }

            summary = {
                "mean": float(valid_results[self.name].mean()),
                "median": float(valid_results[self.name].median()),
                "min": float(valid_results[self.name].min()),
                "max": float(valid_results[self.name].max()),
                "by_category": {}
            }

            if "category" in valid_results.columns:
                category_means = valid_results.groupby("category")[self.name].mean()
                for category, mean in category_means.items():
                    summary["by_category"][category] = float(mean)

            reasoning_column = f"{self.name}_reasoning"
            if reasoning_column in results.columns:
                valid_reasoning = results[results[reasoning_column].notna()]
                if len(valid_reasoning) > 0:
                    # Include up to 3 sample reasoning entries
                    sample_size = min(3, len(valid_reasoning))
                    samples = valid_reasoning.sample(sample_size)
                    
                    summary["sample_reasoning"] = []
                    for _, row in samples.iterrows():
                        summary["sample_reasoning"].append({
                            "question_id": row.get("id", "unknown"),
                            "score": row.get(self.name, 0.0),
                            "reasoning": row.get(reasoning_column, "No reasoning provided")
                        })

            return summary
        except Exception as e:
            print(f"Error summarizing results: {str(e)}")
            return {
                "mean": None,
                "median": None,
                "min": None,
                "max": None,
                "by_category": {},
                "error": str(e)
            }