from dataclasses import dataclass
from typing import Dict, List, Tuple

@dataclass
class Chunk:
    """Data class for storing document chunks."""
    text: str
    doc_id: str
    start_idx: int
    end_idx: int
    metadata: Dict = None


@dataclass
class ImageMetadata:
    """Data class for storing image metadata."""
    doc_id: str
    page: str
    image_id: str
    description: str


@dataclass
class RAGResponse:
    """Data class for storing RAG results"""
    answer: str
    source_chunks: List[Tuple[Chunk, float]]
    prompt_tokens: int
    completion_tokens: int
    # Optional list of images that were included in the prompt context (page_number, figure_number, image_path, relevance_score)
    included_images: List[Dict] = None