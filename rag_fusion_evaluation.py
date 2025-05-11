# rag_fusion_evaluation.py
from typing import Dict, List, Any, Optional, Union
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import time

from rag_evaluation import RAGEvaluator
from rag_fusion import FusionRetriever
from metrics import Metric

class FusionRAGEvaluator(RAGEvaluator):
    """Evaluates FusionRAG system performance using various metrics."""

    def __init__(
            self,
            index_dir: str,
            document_name: str,
            model_name: str = "microsoft/phi-4",
            cross_encoder_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2",
            max_context_tokens: int = 100000,
            device: str = None,
            rerank: bool = True,
            metrics: Optional[List[Metric]] = None,
            num_chunks: int = 5,
            use_openai: bool = False,
            enable_multimodal: bool = True,
            num_generated_queries: int = 5,
            rrf_k: float = 60.0
    ):
        """Initialize with FusionRetriever instead of EnhancedRetriever."""
        # Setup OpenAI API key if needed
        if use_openai:
            from dotenv import load_dotenv
            load_dotenv()

        # Initialize the FusionRAG system
        self.retriever = FusionRetriever(
            index_dir=index_dir,
            document_name=document_name,
            model_name=model_name,
            cross_encoder_name=cross_encoder_name,
            max_context_tokens=max_context_tokens,
            device=device,
            rerank=rerank,
            num_generated_queries=num_generated_queries,
            rrf_k=rrf_k
        )

        # Initialize metrics if not provided (copied from RAGEvaluator)
        if metrics is None:
            from metrics import (
                AlphaSimilarity, QuestionAnswerRelevanceMetric,
                HallucinationMetric, FaithfulnessMetric,
                MultimodalAnswerRelevancyMetric, MultimodalFaithfulnessMetric
            )
            metrics = [
                AlphaSimilarity(),
                QuestionAnswerRelevanceMetric(),
                HallucinationMetric(),
                FaithfulnessMetric(),
                MultimodalFaithfulnessMetric(),
                MultimodalAnswerRelevancyMetric()
            ]

        self.metrics = metrics

        # Save configuration
        self.document_name = document_name
        self.index_dir = index_dir
        self.num_chunks = num_chunks
        self.num_generated_queries = num_generated_queries
        self.rrf_k = rrf_k

        # Initialize results storage
        self.results = []

    def evaluate_question(self, question: Dict, output_path: Optional[Union[str, Path]] = None) -> Dict:
        """Evaluate a single question with fusion-specific metrics."""
        # Get result from parent method
        result = super().evaluate_question(question, output_path)
        
        # Rename 'rag_answer' to 'answer'
        result['answer'] = result.pop('rag_answer', None)
        
        # Add sample answer from the question
        result['reference_answer'] = question.get('answer')
        
        # Add retriever times if available
        if hasattr(self.retriever, 'retrieval_time'):
            result['retrieval_time'] = self.retriever.retrieval_time
            # self.retriever.retrieval_time = 0
        
        if hasattr(self.retriever, 'generation_time'):
            result['generation_time'] = self.retriever.generation_time
        
        # Add fusion-specific metrics
        if hasattr(self.retriever, 'generate_queries_time'):
            result['generate_queries_time'] = self.retriever.generate_queries_time
        
        if hasattr(self.retriever, 'fusion_time'):
            result['fusion_time'] = self.retriever.fusion_time
        
        # Add metric reasoning
        for metric in self.metrics:
            if hasattr(metric, 'last_reason'):
                result[f'{metric.name}_reasoning'] = metric.last_reason
        
        return result

    def visualize_results(self, results: Optional[pd.DataFrame] = None, output_dir: Optional[Union[str, Path]] = None):
        """
        Visualize evaluation results with additional fusion metrics.
        """
        # First call the parent method to visualize standard metrics
        super().visualize_results(results, output_dir)
        
        # Then visualize fusion-specific metrics
        if results is None:
            results = pd.DataFrame(self.results)
            
        if len(results) == 0:
            print("No results to visualize.")
            return
        
        # Filter to only include answerable questions
        answerable_results = results[results["answerable"] == True]
        
        if len(answerable_results) == 0:
            print("No answerable questions to visualize fusion metrics for.")
            return
        
        # Check if we have fusion metrics
        fusion_metrics = ['generate_queries_time', 'fusion_time']
        has_fusion_metrics = any(metric in answerable_results.columns for metric in fusion_metrics)
        
        if not has_fusion_metrics:
            print("No fusion-specific metrics found in results.")
            return
        
        # Print fusion-specific statistics
        print("\nFusion-Specific Metrics:")
        print(f"Number of generated queries: {self.num_generated_queries}")
        print(f"RRF smoothing parameter (k): {self.rrf_k}")
        
        # Convert output_dir to Path if it's a string
        if output_dir is not None:
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
        
        if 'generate_queries_time' in answerable_results.columns:
            valid_results = answerable_results[answerable_results['generate_queries_time'].notna()]
            if len(valid_results) > 0:
                mean_gen_time = valid_results['generate_queries_time'].mean()
                median_gen_time = valid_results['generate_queries_time'].median()
                min_gen_time = valid_results['generate_queries_time'].min()
                max_gen_time = valid_results['generate_queries_time'].max()
                
                print(f"\nQuery Generation Time Summary Statistics:")
                print(f"Average: {mean_gen_time:.4f} seconds")
                print(f"Median: {median_gen_time:.4f} seconds")
                print(f"Min: {min_gen_time:.4f} seconds")
                print(f"Max: {max_gen_time:.4f} seconds")
                
                # Visualize query generation time
                plt.figure(figsize=(10, 6))
                plt.hist(valid_results['generate_queries_time'], bins=10, alpha=0.7)
                plt.title("Distribution of Query Generation Time")
                plt.xlabel("Time (seconds)")
                plt.ylabel("Count")
                plt.grid(True, alpha=0.3)
                if output_dir:
                    plt.savefig(output_dir / "generate_queries_time_histogram.png")
                    plt.close()
                else:
                    plt.show()
        
        if 'fusion_time' in answerable_results.columns:
            valid_results = answerable_results[answerable_results['fusion_time'].notna()]
            if len(valid_results) > 0:
                mean_fusion_time = valid_results['fusion_time'].mean()
                median_fusion_time = valid_results['fusion_time'].median()
                min_fusion_time = valid_results['fusion_time'].min()
                max_fusion_time = valid_results['fusion_time'].max()
                
                print(f"\nFusion Time Summary Statistics:")
                print(f"Average: {mean_fusion_time:.4f} seconds")
                print(f"Median: {median_fusion_time:.4f} seconds")
                print(f"Min: {min_fusion_time:.4f} seconds")
                print(f"Max: {max_fusion_time:.4f} seconds")
                
                # Visualize fusion time
                plt.figure(figsize=(10, 6))
                plt.hist(valid_results['fusion_time'], bins=10, alpha=0.7)
                plt.title("Distribution of Fusion Time")
                plt.xlabel("Time (seconds)")
                plt.ylabel("Count")
                plt.grid(True, alpha=0.3)
                if output_dir:
                    plt.savefig(output_dir / "fusion_time_histogram.png")
                    plt.close()
                else:
                    plt.show()