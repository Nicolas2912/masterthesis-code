import pickle
import torch
from pathlib import Path
from typing import List, Tuple, Dict, Union, Any
from dataclasses import dataclass

import faiss
from sentence_transformers import SentenceTransformer

from data_models import Chunk, ImageMetadata


@dataclass
class Chunk:
    """
    Data class for storing document chunks.

    Attributes:
        text (str): The text content of the chunk.
        doc_id (str): The document ID associated with the chunk.
        start_idx (int): The starting index of the chunk in the document.
        end_idx (int): The ending index of the chunk in the document.
        metadata (Dict[str, Any], optional): Additional metadata for the chunk. Defaults to None.
    """
    text: str
    doc_id: str
    start_idx: int
    end_idx: int
    metadata: Dict[str, Any] = None


@dataclass
class ImageMetadata:
    """Data class for storing image metadata."""
    doc_id: str
    page: str
    image_id: str
    description: str


class DocumentRetriever:
    """
    Class for loading and querying saved document indexes.

    Attributes:
        index_dir (Union[str, Path]): Directory containing the saved index files.
        model_name (str): Name of the sentence transformer model to use.
        document_name (str): Name of the document index file.
        model (SentenceTransformer): The loaded sentence transformer model.
        index (faiss.Index): The loaded index.
        chunks (List[Chunk]): List of chunks in the index.

    Methods:
        load_index(): Load the saved index and associated data from disk.
        list_available_indices(): List all available indices in the directory.
        wrap_text(): Wrap text to specified width while preserving markdown headers and structure.
        search(): Search for relevant chunks with formatted output.
        unload_embedding_model(): Unload the embedding model to free GPU memory.
        get_statistics(): Get statistics about the loaded index.
        get_unique_documents(): Get list of unique document IDs in the index.
    """
    def __init__(self, index_dir: Union[str, Path],
                 document_name: str = "faiss_index.bin",
                 model_name: str = "intfloat/multilingual-e5-large-instruct"):
        """
        Initialize the document retriever.

        Args:
            index_dir: Directory containing the saved index files
            model_name: Name of the sentence transformer model to use
        """
        self.index_dir = Path(index_dir)
        self.model_name = model_name
        print(f"Loading model: {model_name}")
        self.model = SentenceTransformer(model_name, trust_remote_code=True, device="cuda")

        self.document_name = document_name  # Default if not specified

        # Initialize empty state
        self.index = None
        self.chunks: List[Chunk] = []

        # Load the index
        self.load_index()

    def load_index(self) -> None:
        """
        Load the saved FAISS index and associated chunks from disk.

        Raises:
            FileNotFoundError: If the index directory, FAISS index, or chunks file is not found.
            Exception: For other errors that occur during loading.
        """
        try:
            # Ensure the index directory exists
            if not self.index_dir.exists():
                raise FileNotFoundError(f"Index directory not found: {self.index_dir}")

            # Construct paths for the FAISS index and chunks
            index_path = self.index_dir / f"{self.document_name}_faiss_index.bin"
            chunks_path = self.index_dir / f"{self.document_name}_chunks.pkl"

            # Load the FAISS index
            if not index_path.exists():
                raise FileNotFoundError(f"FAISS index not found at {index_path}")
            self.index = faiss.read_index(str(index_path))

            # Load the document chunks
            if not chunks_path.exists():
                raise FileNotFoundError(f"Chunks file not found at {chunks_path}")
            with open(chunks_path, "rb") as f:
                self.chunks = pickle.load(f)

        except Exception as e:
            raise Exception(f"Error loading index: {str(e)}")

    def _format_query_for_e5(self, query: str) -> str:
        """
        Format the query for the E5 model with appropriate instruction.

        Args:
            query: The search query

        Returns:
            Formatted query with instruction
        """
        # For technical manuals and corrective maintenance
        task = "Given a document, represent its content for retrieval"
        return f"Instruct: {task}\nQuery: {query}"

    @classmethod
    def list_available_indices(cls, index_dir: Union[str, Path]) -> List[str]:
        """
        List all available indices in the directory.

        Args:
            index_dir: Directory containing index files

        Returns:
            List of available index names (without file extensions)
        """
        index_dir = Path(index_dir)
        if not index_dir.exists():
            raise FileNotFoundError(f"Index directory not found: {index_dir}")

        # Look for FAISS index files
        index_files = list(index_dir.glob("*_faiss_index.bin"))

        # Extract index names (remove '_faiss_index.bin' suffix)
        index_names = [f.stem.replace('_faiss_index', '') for f in index_files]

        return sorted(index_names)

    def wrap_text(self, text: str, width: int = 100) -> str:
        """
        Wrap text to specified width while preserving markdown headers and structure.
        """
        lines = []
        # Split text into lines first to preserve markdown formatting
        for line in text.split('\n'):
            # Preserve header formatting
            if line.startswith('#'):
                lines.append(line)
                continue

            # Wrap normal text
            while len(line) > width:
                # Find the last space within the width limit
                split_point = line[:width].rfind(' ')
                if split_point == -1:  # No space found, force split
                    split_point = width

                lines.append(line[:split_point])
                line = line[split_point:].lstrip()

            if line:  # Add remaining text
                lines.append(line)

        return '\n'.join(lines)

    def search(self, query: str, k: int = 5) -> List[Tuple[Chunk, float]]:
        """Search for relevant chunks with formatted output."""
        if not self.chunks or self.index is None:
            print("No documents have been indexed yet.")
            return []

        # Reinitialize model if it's None
        if not hasattr(self, 'model') or self.model is None:
            print("Reinitializing the embedding model...")
            self.model = SentenceTransformer(self.model_name, trust_remote_code=True, device="cuda")

        # Format query for E5 model
        formatted_query = self._format_query_for_e5(query)

        # Create query embedding
        query_embedding = self.model.encode(
            [formatted_query],
            normalize_embeddings=True,
            convert_to_numpy=True
        )
        # Move model back to CPU immediately after use
        self.model.cpu()
        torch.cuda.empty_cache()

        # Adjust k if needed
        k = min(k, len(self.chunks))

        # Search the index
        distances, indices = self.index.search(query_embedding, k)

        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx != -1:  # Valid index
                chunk = self.chunks[idx]
                # Format the text with wrapping
                results.append((
                    Chunk(
                        text=chunk.text,
                        doc_id=chunk.doc_id,
                        start_idx=chunk.start_idx,
                        end_idx=chunk.end_idx,
                        metadata=chunk.metadata
                    ),
                    float(dist)
                ))

        # Print formatted results
        print(f"\nQuery: {self.wrap_text(query)}\n")
        print("=" * 80)  # Separator line

        verbose = False
        if verbose:
            for chunk, score in results:
                print(f"\nScore: {score:.4f}")
                print(f"Document: {chunk.doc_id}")
                print("-" * 80)  # Separator line
                print(f"Text:\n{chunk.text}")
                print("=" * 80)  # Separator line

        # unload model from gpu memory

        return results

    def unload_embedding_model(self):
        """Unload the embedding model to free GPU memory"""
        if hasattr(self, 'model'):
            self.model.cpu()  # Move to CPU
            self.model = None
            torch.cuda.empty_cache()
            import gc
            gc.collect()

    def get_statistics(self) -> Dict[str, int]:
        """Get statistics about the loaded index."""
        return {
            "total_chunks": len(self.chunks),
            "unique_documents": len(set(chunk.doc_id for chunk in self.chunks)),
            "index_size": self.index.ntotal if self.index else 0
        }

    def get_unique_documents(self) -> List[str]:
        """Get list of unique document IDs in the index."""
        return list(set(chunk.doc_id for chunk in self.chunks))


# Example usage
if __name__ == "__main__":
    try:
        # Initialize retriever
        document = "Service_Software_BAL_0420_EN"
        retriever = DocumentRetriever("index", document_name=document)

        # Get some statistics
        stats = retriever.get_statistics()
        print("\nIndex Statistics:")
        for key, value in stats.items():
            print(f"{key}: {value}")

        # List available documents
        docs = retriever.get_unique_documents()
        print("\nAvailable Documents:")
        for doc in docs:
            print(f"- {doc}")

        # Perform a search
        query = "What is the Signal Type of the Start Trigger?"

        results = retriever.search(
            query=query,
            k=8)

        # Print results
        for chunk, score in results:
            print(f"\nScore: {score:.4f}")
            print(f"Document: {chunk.doc_id}")  # Access doc_id directly from Chunk object
            print(f"Text: {chunk.text}")  # Access text directly from Chunk object
            if chunk.metadata:
                page = chunk.metadata["page_number"]
                confidence = chunk.metadata["confidence"]
                section_path = chunk.metadata["section_path"]
                print(f"Page: {page}; Confidence: {confidence}")

        # Get image metadata for a specific document
        # if docs:
        #     print(f"\nImage Metadata for {docs[0]}:")
        #         print(f"\nImage: {meta.image_id}")
        #         print(f"Page: {meta.page}")
        #         print(f"Description: {meta.description}")

    except Exception as e:
        print(f"Error: {str(e)}")
