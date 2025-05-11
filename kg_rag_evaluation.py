# kg_rag_evaluation.py
from typing import Dict, List, Any, Optional, Union
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import time

from rag_evaluation import RAGEvaluator
from knowledge_graph_llm_response import KGEnhancedRetriever
from metrics import Metric

class KGEnhancedRAGEvaluator(RAGEvaluator):
    """Evaluates Knowledge Graph Enhanced RAG system performance using various metrics."""

    def __init__(
        self,
        index_dir: str,
        document_name: str,
        kg_file_path: str,
        image_descriptions_path: Optional[str] = None,
        model_name: str = "unsloth/Qwen2.5-VL-32B-Instruct-bnb-4bit",
        device: str = None,
        metrics: Optional[List[Metric]] = None,
        num_chunks: int = 5,
        use_openai: bool = False,
        enable_multimodal: bool = True,
        cache_dir: Optional[str] = None
        ):
        """Initialize with KGEnhancedRetriever instead of EnhancedRetriever."""
        # Setup OpenAI API key if needed
        if use_openai:
            from dotenv import load_dotenv
            load_dotenv()

        # Initialize the KGEnhancedRAG system
        self.retriever = KGEnhancedRetriever(
            kg_file_path=kg_file_path,
            index_dir=index_dir,
            document_name=document_name,
            image_descriptions_path=image_descriptions_path,
            model_name=model_name,
            device=device,
            cache_dir=cache_dir
        )

        # Set up the figures directory for image resolution
        figures_base_dir = f"extracted_figures/{document_name}"
        
        # Initialize metrics if not provided
        if metrics is None:
            from metrics import (
                AlphaSimilarity, QuestionAnswerRelevanceMetric,
                HallucinationMetric, FaithfulnessMetric,
                MultimodalAnswerRelevancyMetric, MultimodalFaithfulnessMetric
            )
            
            # Create regular metrics
            regular_metrics = [
                AlphaSimilarity(),
                QuestionAnswerRelevanceMetric(),
                HallucinationMetric(),
                FaithfulnessMetric()
            ]
            
            # Create multimodal metrics with figures directory if enabled
            if enable_multimodal:
                multimodal_metrics = [
                    MultimodalFaithfulnessMetric(model="gpt-4o-mini", figures_base_dir=figures_base_dir),
                    MultimodalAnswerRelevancyMetric(model="gpt-4o-mini", figures_base_dir=figures_base_dir)
                ]
                metrics = regular_metrics + multimodal_metrics
            else:
                metrics = regular_metrics
        else:
            # Update existing metrics with figures_base_dir if they're multimodal
            for metric in metrics:
                if hasattr(metric, 'name') and metric.name in ["multimodal_answer_relevancy", "multimodal_faithfulness"]:
                    if hasattr(metric, 'figures_base_dir'):
                        metric.figures_base_dir = figures_base_dir
                        print(f"Updated {metric.name} with figures_base_dir: {figures_base_dir}")

        self.metrics = metrics

        # Save configuration
        self.document_name = document_name
        self.index_dir = index_dir
        self.num_chunks = num_chunks
        self.kg_file_path = kg_file_path
        self.cache_dir = cache_dir

        # Initialize results storage
        self.results = []

    def evaluate_question(self, question: Dict, output_path: Optional[Union[str, Path]] = None) -> Dict:
        """Evaluate a single question with KG-specific metrics."""
        # First, we need to extract the image paths and document name before calling the parent method
        question_text = question["question"]
        reference_answer = question.get("answer")
        image_paths = []

        # Call the parent method to get base results
        result = super().evaluate_question(question, output_path)
        
        # Rename 'rag_answer' to 'answer'
        result['answer'] = result.pop('rag_answer', None)

        # Add retriever times if available
        if hasattr(self.retriever, 'retrieval_time'):
            result['retrieval_time'] = self.retriever.retrieval_time
        
        if hasattr(self.retriever, 'generation_time'):
            result['generation_time'] = self.retriever.generation_time
        
        # Add KG-specific times
        if hasattr(self.retriever, 'extract_entities_time'):
            result['extract_entities_time'] = self.retriever.extract_entities_time
        
        if hasattr(self.retriever, 'relevant_kg_nodes_time'):
            result['relevant_kg_nodes_time'] = self.retriever.relevant_kg_nodes_time
        
        if hasattr(self.retriever, 'format_kg_time'):
            result['format_kg_time'] = self.retriever.format_kg_time
        
        # Add metric reasoning
        for metric in self.metrics:
            if hasattr(metric, 'last_reason'):
                result[f'{metric.name}_reasoning'] = metric.last_reason
        
        return result

    def visualize_results(self, results: Optional[pd.DataFrame] = None, output_dir: Optional[Union[str, Path]] = None):
        """
        Visualize evaluation results with additional KG metrics.
        """
        # First call the parent method to visualize standard metrics
        super().visualize_results(results, output_dir)
        
        # Then visualize KG-specific metrics
        if results is None:
            results = pd.DataFrame(self.results)
            
        if len(results) == 0:
            print("No results to visualize.")
            return
        
        # Filter to only include answerable questions
        answerable_results = results[results["answerable"] == True]
        
        if len(answerable_results) == 0:
            print("No answerable questions to visualize KG metrics for.")
            return
        
        # Check if we have KG metrics
        kg_metrics = ['extract_entities_time', 'relevant_kg_nodes_time', 'format_kg_time']
        has_kg_metrics = any(metric in answerable_results.columns for metric in kg_metrics)
        
        if not has_kg_metrics:
            print("No KG-specific metrics found in results.")
            return
        
        # Print KG-specific statistics
        print("\nKnowledge Graph Metrics:")
        print(f"Knowledge Graph file: {self.kg_file_path}")
        
        # Convert output_dir to Path if it's a string
        if output_dir is not None:
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate visualizations for KG-specific metrics
        for kg_metric in kg_metrics:
            if kg_metric in answerable_results.columns:
                valid_results = answerable_results[answerable_results[kg_metric].notna()]
                if len(valid_results) > 0:
                    mean_time = valid_results[kg_metric].mean()
                    median_time = valid_results[kg_metric].median()
                    min_time = valid_results[kg_metric].min()
                    max_time = valid_results[kg_metric].max()
                    
                    print(f"\n{kg_metric.replace('_', ' ').title()} Summary Statistics:")
                    print(f"Average: {mean_time:.4f} seconds")
                    print(f"Median: {median_time:.4f} seconds")
                    print(f"Min: {min_time:.4f} seconds")
                    print(f"Max: {max_time:.4f} seconds")
                    
                    # Visualize metric
                    plt.figure(figsize=(10, 6))
                    plt.hist(valid_results[kg_metric], bins=10, alpha=0.7)
                    plt.title(f"Distribution of {kg_metric.replace('_', ' ').title()}")
                    plt.xlabel("Time (seconds)")
                    plt.ylabel("Count")
                    plt.grid(True, alpha=0.3)
                    if output_dir:
                        plt.savefig(output_dir / f"{kg_metric}_histogram.png")
                        plt.close()
                    else:
                        plt.show()