import json
import torch
import re
import hashlib
import os
from dotenv import load_dotenv
import pickle
from pathlib import Path
from typing import List, Dict, Any, Optional, Union, Tuple, Set
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import numpy as np
from tqdm import tqdm
import logging
import time
import gc

from sentence_transformers import CrossEncoder
# Import specific classes for Qwen-VL
from transformers import (
    Qwen2_5_VLForConditionalGeneration, # Changed from AutoModelForCausalLM
    AutoProcessor,                     # Changed from AutoTokenizer
    BitsAndBytesConfig
)
# Import Qwen VL utils
from qwen_vl_utils import process_vision_info

# Import existing classes from your implementation
from document_retrieval import DocumentRetriever
from data_models import Chunk, RAGResponse

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class KGEnhancedRetriever:
    """
    Enhances RAG retrieval with knowledge graph information and image descriptions.

    This class works with the existing DocumentRetriever to enhance query results
    with knowledge graph information and image descriptions.
    """

    def __init__(
            self,
            kg_file_path: str,
            index_dir: str,
            document_name: str = None,
            image_descriptions_path: Optional[str] = None,
            model_name: str = "unsloth/Qwen2.5-VL-32B-Instruct-bnb-4bit",
            device: Optional[str] = None,
            cache_dir: Optional[str] = None,
            max_context_tokens: int = 8000
    ):
        """
        Initialize the KG-enhanced retriever.

        Args:
            kg_file_path: Path to the knowledge graph file
            index_dir: Directory containing the saved index files
            document_name: Name of the document to retrieve
            image_descriptions_path: Path to image descriptions pickle file
            llm_model_name: Name of the small language model for KG transformation
            device: Device to use for models ('cpu', 'cuda', etc.)
            cache_dir: Directory to store cached transformations
            max_context_tokens: Maximum number of tokens allowed in the context
        """
        load_dotenv()
        self.index_dir = index_dir
        self.document_name = document_name

        logger.info(f"Initializing KGEnhancedRetriever with KG file: {kg_file_path}")
        self.max_image_references = 12
        self.max_text_tokens = 8000

        # Set the device
        self.device = device or ('cuda' if torch.cuda.is_available() else 'cpu')
        logger.info(f"Using device: {self.device}")

        # Initialize base retriever
        self.base_retriever = DocumentRetriever(index_dir, document_name=document_name)
        logger.info(f"Initialized base retriever with index from {index_dir}")

        # Load the knowledge graph
        self.kg = self._load_kg(kg_file_path)
        logger.info(f"Loaded {len(self.kg)} triplets from knowledge graph")

        # Load image descriptions if provided        
        self.image_descriptions = self._load_image_descriptions()

        self.VLM = True

        if not self.VLM:
            # Initialize LLM for KG transformation
            self.llm_model_name = model_name
            self.llm_model, self.llm_tokenizer = self._initialize_llm()

            # Initialize pipeline
            self.pipe = pipeline(
                "text-generation",
                model=self.llm_model,
                tokenizer=self.llm_tokenizer,
                device_map="auto",
                framework="pt"
            )
        else:
            quantization_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4", # or "fp4" based on unsloth documentation/recommendation
                bnb_4bit_compute_dtype=torch.bfloat16, # Recommended compute dtype
                bnb_4bit_use_double_quant=True,
            )
            try:
                max_pixels = 512*28*28
                self.model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
                    model_name,
                    quantization_config=quantization_config,
                    device_map="auto", # Handles placing layers on devices
                    trust_remote_code=True
                ).eval() # Set to evaluation mode

                # Load the corresponding processor
                print(f"Loading processor for {model_name}...")
                self.processor = AutoProcessor.from_pretrained(model_name, trust_remote_code=True, max_pixels=max_pixels)

                print("VL Model and Processor loaded successfully.")
                # Log device placement if possible
                try:
                    print(f"Model is mapped to devices: {self.model.hf_device_map}")
                except AttributeError:
                    print(f"Model device map info not readily available, likely using 'auto'.")
            except Exception as e:
                print(f"Error loading Qwen-VL model or processor: {str(e)}")
                raise # Re-raise the exception as it's critical

        # Cache for LLM transformations to avoid redundant processing
        self.cache_dir = cache_dir
        if cache_dir:
            os.makedirs(cache_dir, exist_ok=True)
        self.transformation_cache = self._load_cache()

        # Extract and index unique entities from the KG for faster lookup
        self.entity_index = self._build_entity_index()

        # Extract common terms from KG for enhanced entity recognition
        self.common_kg_terms = self._extract_common_kg_terms()

        # Extract patterns from the KG
        self.kg_patterns = self._extract_kg_patterns()

        # Initialize timers
        self.retrieval_time = 0
        self.generation_time = 0
        self.extract_entities_time = 0
        self.relevant_kg_nodes_time = 0
        self.format_kg_time = 0
        self.image_desc_time = 0

        # Add max_context_tokens attribute
        self.max_context_tokens = max_context_tokens

    def _load_kg(self, kg_file_path: str) -> List[Dict[str, str]]:
        """
        Load the knowledge graph from the file.

        Args:
            kg_file_path: Path to the knowledge graph file

        Returns:
            List of triplet dictionaries with 'head', 'type', and 'tail' keys
        """
        try:
            # Try reading the file with different encodings
            with open(kg_file_path, 'r', encoding='utf-8') as f:
                kg_text = f.read()
        except UnicodeDecodeError:
            try:
                # Try Windows-1252 encoding (common for Windows-generated files)
                with open(kg_file_path, 'r', encoding='windows-1252') as f:
                    kg_text = f.read()
            except UnicodeDecodeError:
                try:
                    # Try Latin-1 encoding as a fallback
                    with open(kg_file_path, 'r', encoding='latin-1') as f:
                        kg_text = f.read()
                except Exception as e:
                    logging.error(f"Error loading knowledge graph: {e}")
                    kg_text = ""

        kg_data = eval(kg_text)  # Parse as Python literal
        return kg_data

    def _load_image_descriptions(self) -> Dict[int, List[Dict]]:
        """Load image descriptions from pickle file."""
        try:
            # Use Path object for joining
            # make index dir to Path object
            self.index_dir = Path(self.index_dir)
            descriptions_path = self.index_dir / f"{self.document_name}_image_description.pkl"
            print(f"PATH: {descriptions_path}")

            if not descriptions_path.exists():
                print(f"Warning: No image descriptions found at {descriptions_path}")
                return {}

            with open(descriptions_path, 'rb') as f:
                data = pickle.load(f)
                print(f"Loaded image descriptions for {len(data)} pages from {descriptions_path}")
                return data # Should be Dict[int, List[Dict]]
        except Exception as e:
            print(f"Error loading image descriptions: {str(e)}")
            return {}

    def _initialize_llm(self) -> Tuple[Optional[Any], Optional[Any]]:
        """
        Initialize the small language model for KG transformation.

        Returns:
            Tuple of (model, tokenizer)
        """
        try:
            logger.info(f"Loading LLM model: {self.llm_model_name}")

            # Half-precision for efficiency
            model = AutoModelForCausalLM.from_pretrained(
                self.llm_model_name,
                device_map="auto",       # Distribute model across available devices
                torch_dtype=torch.float16,  # Use half precision
                trust_remote_code=True
            )

            tokenizer = AutoTokenizer.from_pretrained(
                self.llm_model_name,
                trust_remote_code=True
            )

            logger.info(f"Successfully loaded LLM model: {self.llm_model_name}")
            return model, tokenizer

        except Exception as e:
            logger.error(f"Error loading LLM model: {str(e)}")
            logger.warning("Will use fallback rule-based transformation")
            return None, None

    def _load_cache(self) -> Dict[str, str]:
        """
        Load cached KG transformations if available.

        Returns:
            Dictionary mapping cache keys to transformed text
        """
        if not self.cache_dir:
            return {}

        cache_path = Path(self.cache_dir) / "kg_transformations.pkl"

        if cache_path.exists():
            try:
                with open(cache_path, 'rb') as f:
                    cache = pickle.load(f)
                    logger.info(f"Loaded {len(cache)} cached transformations")
                    return cache
            except Exception as e:
                logger.error(f"Error loading cache: {str(e)}")

        return {}

    def _save_cache(self):
        """Save the transformation cache."""
        if not self.cache_dir:
            return

        cache_path = Path(self.cache_dir) / "kg_transformations.pkl"

        try:
            with open(cache_path, 'wb') as f:
                pickle.dump(self.transformation_cache, f)
        except Exception as e:
            logger.error(f"Error saving cache: {str(e)}")

    def _build_entity_index(self) -> Dict[str, Set[int]]:
        """
        Build an index of entities to triplet indices for efficient lookup.

        Returns:
            Dictionary mapping normalized entity names to sets of triplet indices
        """
        entity_index = {}

        for idx, triplet in enumerate(self.kg):
            # Process head entity
            head = triplet['head'].lower()
            if head not in entity_index:
                entity_index[head] = set()
            entity_index[head].add(idx)

            # Process tail entity
            tail = triplet['tail'].lower()
            if tail not in entity_index:
                entity_index[tail] = set()
            entity_index[tail].add(idx)

            # Add variants (e.g., without hyphens, without spaces)
            for entity in [head, tail]:
                # Without hyphens
                no_hyphens = entity.replace('-', ' ')
                if no_hyphens != entity:
                    if no_hyphens not in entity_index:
                        entity_index[no_hyphens] = set()
                    entity_index[no_hyphens].add(idx)

                # Without spaces (for codes like G-codes, M-codes)
                no_spaces = entity.replace(' ', '')
                if no_spaces != entity:
                    if no_spaces not in entity_index:
                        entity_index[no_spaces] = set()
                    entity_index[no_spaces].add(idx)

        logger.info(f"Built entity index with {len(entity_index)} unique entities")
        return entity_index

    def _extract_kg_patterns(self) -> List[str]:
        """
        Analyze the knowledge graph to identify important entity patterns.

        This method uses statistical analysis rather than hardcoded assumptions
        to discover potentially important patterns in entity structure.

        Returns:
            List of important entity patterns from the KG
        """
        # Instead of looking for predefined patterns, we'll analyze
        # the structure of entities in the KG to discover patterns

        # Step 1: Collect all entities and analyze their structure
        all_entities = []
        for triplet in self.kg:
            all_entities.append(triplet['head'])
            all_entities.append(triplet['tail'])

        # Focus only on unique entities
        unique_entities = list(set(all_entities))
        logger.info(f"Analyzing {len(unique_entities)} unique entities in knowledge graph")

        # Step 2: Extract character class frequencies
        # This helps us understand what kinds of patterns exist
        char_class_counts = {
            'uppercase': 0,  # 'ABC'
            'lowercase': 0,  # 'abc'
            'digits': 0,  # '123'
            'mixed_case': 0,  # 'AbcDef'
            'alpha_num': 0,  # 'A1B2C3'
            'has_symbols': 0,  # 'x-axis'
            'has_spaces': 0,  # 'two words'
        }

        # Also gather length statistics
        entity_lengths = []

        for entity in unique_entities:
            entity_lengths.append(len(entity))

            # Skip empty entities
            if not entity:
                continue

            # Check character classes
            if re.match(r'^[A-Z]+$', entity):
                char_class_counts['uppercase'] += 1
            elif re.match(r'^[a-z]+$', entity):
                char_class_counts['lowercase'] += 1
            elif re.match(r'^[0-9]+$', entity):
                char_class_counts['digits'] += 1
            elif re.match(r'^[A-Za-z]+$', entity) and not re.match(r'^[A-Z]+$', entity) and not re.match(r'^[a-z]+$',
                                                                                                         entity):
                char_class_counts['mixed_case'] += 1
            elif re.match(r'^[A-Za-z0-9]+$', entity) and re.search(r'[0-9]', entity) and re.search(r'[A-Za-z]', entity):
                char_class_counts['alpha_num'] += 1

            # Check for spaces and symbols
            if ' ' in entity:
                char_class_counts['has_spaces'] += 1
            if re.search(r'[^A-Za-z0-9\s]', entity):
                char_class_counts['has_symbols'] += 1

        # Calculate basic statistics for length
        if entity_lengths:
            avg_length = sum(entity_lengths) / len(entity_lengths)
            logger.info(f"Average entity length: {avg_length:.1f} characters")

        # Log character class statistics
        total = len(unique_entities)
        for cls, count in char_class_counts.items():
            if count > 0:
                logger.info(f"Character class '{cls}': {count} entities ({count / total:.1%})")

        # Step 3: Generate adaptive patterns based on the KG structure
        patterns = []

        # Add patterns for significant character classes only
        threshold = 0.05  # At least 5% of entities should match a pattern to include it

        if char_class_counts['uppercase'] / total > threshold:
            patterns.append(r'\b[A-Z]{2,}\b')  # All uppercase words (acronyms)

        if char_class_counts['mixed_case'] / total > threshold:
            patterns.append(r'\b[A-Z][a-z]+(?:[A-Z][a-z]*)*\b')  # CamelCase terms

        if char_class_counts['alpha_num'] / total > threshold:
            # Patterns for alphanumeric terms - different variations
            patterns.append(r'\b[A-Za-z]\d+\b')  # Letter(s) followed by number(s)
            patterns.append(r'\b\d+[A-Za-z]+\b')  # Number(s) followed by letter(s)

        if char_class_counts['has_symbols'] / total > threshold:
            # Common symbol patterns in technical documents
            patterns.append(r'\b[A-Za-z0-9]+-[A-Za-z0-9]+\b')  # Hyphenated terms
            patterns.append(r'\b[A-Za-z0-9]+\.[A-Za-z0-9]+\b')  # Dot-separated terms

        # Add general patterns for multi-word terms if spaces are common
        if char_class_counts['has_spaces'] / total > threshold:
            patterns.append(r'\b[A-Z][a-z]+\s+[A-Z]?[a-z]+\b')  # Capitalized phrases
            patterns.append(r'\b[A-Z][a-z]+\s+\d+\b')  # Words followed by numbers

        # Step 4: Extract actual prefix-number patterns from the data
        # This discovers patterns like G01, M30, T01 without hardcoding the prefixes
        prefix_counts = {}

        for entity in unique_entities:
            # Look for patterns where a letter/letters is followed by numbers
            matches = re.finditer(r'\b([A-Za-z]+)(\d+)\b', entity)
            for match in matches:
                prefix = match.group(1)
                if prefix not in prefix_counts:
                    prefix_counts[prefix] = 0
                prefix_counts[prefix] += 1

        # Add patterns for common prefixes
        prefix_threshold = 3  # Need at least 3 occurrences to be considered a pattern
        for prefix, count in prefix_counts.items():
            if count >= prefix_threshold:
                patterns.append(rf'\b{re.escape(prefix)}\d+(?:\.\d+)?\b')
                # logger.info(f"Found numerical pattern with prefix '{prefix}' ({count} occurrences)")

        # If we still don't have many patterns, add some reasonable fallbacks
        # that often work well in technical documents
        if len(patterns) < 3:
            fallback_patterns = [
                r'\b\d+(?:\.\d+)?\b',  # Numbers with optional decimal part
                r'\b[A-Za-z]+\s+\d+\b'  # Words followed by numbers
            ]
            for pattern in fallback_patterns:
                if pattern not in patterns:
                    patterns.append(pattern)

        logger.info(f"Generated {len(patterns)} adaptive patterns based on KG structure")
        return patterns

    def _extract_entities(self, query: str) -> List[str]:
        """
        Extract entities from the user query using adaptive analysis.

        Args:
            query: The user's question

        Returns:
            List of extracted entities
        """
        entities = []

        # Apply patterns derived from KG analysis
        for pattern in self.kg_patterns:
            try:
                matches = re.findall(pattern, query)
                if matches:
                    entities.extend(matches)
            except Exception as e:
                logger.warning(f"Error applying pattern '{pattern}': {str(e)}")

        # Always look for exact matches with terms from the KG
        query_lower = query.lower()
        for term in self.common_kg_terms:
            term_lower = term.lower()
            if term_lower in query_lower:
                # Find word boundaries to avoid partial matches
                if re.search(rf'\b{re.escape(term_lower)}\b', query_lower):
                    entities.append(term)

        # Split query into words and n-grams to catch additional matches
        words = re.findall(r'\b\w+\b', query)

        # Add multi-word combinations for n-gram matching
        if len(words) >= 2:
            for i in range(len(words) - 1):
                entities.append(f"{words[i]} {words[i + 1]}")

            if len(words) >= 3:
                for i in range(len(words) - 2):
                    entities.append(f"{words[i]} {words[i + 1]} {words[i + 2]}")

        # Add individual words (filtered to avoid common stopwords)
        stopwords = {'a', 'an', 'the', 'and', 'or', 'but', 'is', 'are', 'was', 'were',
                     'to', 'of', 'in', 'on', 'at', 'by', 'for', 'with', 'about',
                     'like', 'through', 'over', 'before', 'after', 'between', 'after'}

        for word in words:
            if word.lower() not in stopwords and len(word) > 2:
                entities.append(word)

        # Remove duplicates
        return list(set(entities))

    def _find_kg_matches(self, entities: List[str]) -> List[Dict[str, str]]:
        """
        Find KG triplets related to extracted entities.

        Args:
            entities: List of extracted entities

        Returns:
            List of matching KG triplets
        """
        matching_indices = set()

        # Find direct matches in the entity index
        for entity in entities:
            entity_lower = entity.lower()

            # Check exact match
            if entity_lower in self.entity_index:
                matching_indices.update(self.entity_index[entity_lower])

            # Check partial matches - entity contained in longer entity
            for indexed_entity, triplet_indices in self.entity_index.items():
                if entity_lower in indexed_entity and entity_lower != indexed_entity:
                    matching_indices.update(triplet_indices)

        # Convert matching indices to KG triplets
        return [self.kg[idx] for idx in matching_indices]

    def _get_relevant_image_descriptions(self, chunks: List[Tuple[Chunk, float]]) -> Dict[int, List[Dict]]:
        """
        Get image descriptions for pages containing the top 5 chunks AND pages
        within a +/- 2 range of those top chunks' pages, grouped by page.
        (Adapted from llm_response.py)
        """
        relevant_descriptions_by_page: Dict[int, List[Dict]] = {}
        target_pages = set() # Use a set to store all pages to check (original + range)

        # 0. Sort chunks by score (descending) and select top N (e.g., top 3 or 5)
        # Let's use top 3 like in the provided llm_response.py snippet
        sorted_chunks = sorted(chunks, key=lambda item: item[1], reverse=True)
        top_chunks = sorted_chunks[:3] # Consider top 3 chunks for image context range
        logger.info(f"  - Considering top {len(top_chunks)} chunks for image context range determination.")

        # 1. Identify initial pages from the top chunks
        initial_pages = set()
        for chunk, score in top_chunks:
            page = chunk.metadata.get('page_number')
            if page is not None:
                initial_pages.add(page)

        if not initial_pages:
            logger.info("  - No page numbers found in top retrieved chunks for image context.")
            return {} # Return empty if no pages found in top chunks

        # 2. Expand the range for each initial page from top chunks
        logger.info(f"  - Initial pages found in top chunks: {sorted(list(initial_pages))}")
        page_range = 2 # Define the range (e.g., 2 pages before and after)
        for page in initial_pages:
            for i in range(-page_range, page_range + 1):
                page_to_check = page + i
                # Add page to target set if it's a valid page number (e.g., > 0)
                if page_to_check > 0:
                    target_pages.add(page_to_check)

        logger.info(f"  - Checking for images on pages (based on top chunks, including +/- {page_range} range): {sorted(list(target_pages))}")

        # 3. Fetch descriptions for all target pages
        found_images = False
        for page in sorted(list(target_pages)): # Process pages in order
            # Check if descriptions exist for this page in the loaded data
            if page in self.image_descriptions:
                logger.info(f"    - Found images on page {page}")
                page_descriptions = self.image_descriptions[page]

                # Store descriptions, ensuring figure number order if available
                # Make a copy to avoid modifying the original list if sorting is needed elsewhere
                sorted_descriptions = sorted(page_descriptions, key=lambda x: x.get('figure_number', 0))

                relevant_descriptions_by_page[page] = sorted_descriptions
                found_images = True
            # else: # Optional: uncomment to log pages checked but without images
            #     logger.debug(f"    - No images found on page {page}")

        if not found_images:
             logger.info("  - No images found within the target page range.")

        # 4. Return the dictionary sorted by page number (already sorted due to iteration order)
        return relevant_descriptions_by_page

    def _format_image_descriptions(self, descriptions_by_page: Dict[int, List[Dict]]) -> str:
        """
        Format image descriptions grouped by page for inclusion in context.
        (Copied from llm_response.py)
        """
        if not descriptions_by_page:
            return ""

        formatted_text = "\n\n--- Relevant Visual Context ---\n"

        for page, descriptions in descriptions_by_page.items():
            if not descriptions: # Should not happen with current logic, but safe check
                continue

            # Add page header
            formatted_text += f"\n**Page {page} Images:**\n"

            for desc in descriptions:
                image_path = desc.get('image_path', 'unknown_path') # Use .get for safety
                # Extract filename robustly
                try:
                    image_name = Path(image_path).name
                except Exception:
                    image_name = image_path.split("/")[-1] # Fallback

                description_text = desc.get('description', 'No description available') # Use .get

                # Format each image entry clearly
                formatted_text += f"*   Image: [{image_name}] - {description_text}\n"

        formatted_text += "\n------------------------------\n" # Footer for the visual context block
        return formatted_text

    def _transform_kg_with_openai(self, kg_triplets: List[Dict[str, str]],
                                  api_key: Optional[str] = None,
                                  model: str = "gpt-4o-mini") -> str:
        """
        Transform KG triplets to natural language using OpenAI's models.

        Args:
            kg_triplets: List of KG triplets
            api_key: OpenAI API key (if None, tries to get from environment)
            model: OpenAI model to use

        Returns:
            Natural language description
        """
        if not kg_triplets:
            return ""

        try:
            # Create a cache key to avoid redundant processing
            kg_str = str(sorted(str(t) for t in kg_triplets))
            cache_key = f"openai_{hashlib.md5(kg_str.encode()).hexdigest()}"

            # Check cache
            if cache_key in self.transformation_cache:
                return self.transformation_cache[cache_key]

            # Get the API key
            api_key = os.getenv("OPENAI_API_KEY")

            # Initialize the OpenAI client
            from openai import Client
            client = Client(api_key=api_key)

            # Group triplets by head for better organization
            triplet_groups = {}
            for triplet in kg_triplets:
                head = triplet['head']
                if head not in triplet_groups:
                    triplet_groups[head] = []
                triplet_groups[head].append(triplet)

            # Format input for OpenAI
            structured_input = ""
            for head, triplets in triplet_groups.items():
                structured_input += f"About {head}:\n"
                for triplet in triplets:
                    relation = triplet['type'].replace('_', ' ')
                    tail = triplet['tail']
                    structured_input += f"- {relation} {tail}\n"
                structured_input += "\n"

            # Create the prompt
            prompt = f"""
            Transform these knowledge graph triplets into clear, concise natural language descriptions.
            For each entity, explain its relationships with other entities as complete sentences.

            Example input:
            About Machine Tool:
            - has part Spindle
            - has part Table
            - instance of CNC Machine

            Example output:
            The Machine Tool is a type of CNC Machine. It consists of several components including a Spindle and a Table.

            Now transform these triplets:

            {kg_triplets}
            """

            # Call OpenAI API
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system",
                     "content": "You are a technical documentation expert that transforms knowledge graph data into readable natural language."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=1024
            )

            # Extract the response
            if response.choices and len(response.choices) > 0:
                result = response.choices[0].message.content.strip()

                # Cache the result
                self.transformation_cache[cache_key] = result
                self._save_cache()

                return result
            else:
                logger.warning("OpenAI API returned empty response")

        except Exception as e:
            logger.error(f"Error using OpenAI for transformation: {str(e)}")


    def _get_relevant_image_paths(
        self,
        # Function needs all retrieved chunks with scores
        all_retrieved_chunks: List[Tuple[Chunk, float]],
        max_images: int,
        page_range: int = 1 # Add page_range parameter, default to 1
        ) -> List[Dict[str, Union[str, int, float]]]: # Return type includes score
        """
        Gets image paths, prioritizing based on the relevance score of chunks
        on the same page. Also considers images from adjacent pages (+/- page_range).
        Limits the total number of images based on score priority.

        Returns:
            List of dicts, each containing 'page_number', 'figure_number',
            'image_path', and 'relevance_score'.
            The list returned is initially sorted by relevance score (desc).
            The CALLER (_prepare_context_and_messages) will re-sort by page/figure
            for the final prompt text generation.
        """
        print(f"Selecting relevant images based on chunk relevance and +/- {page_range} page range...")

        if not all_retrieved_chunks:
            print("  - No chunks provided for image relevance calculation.")
            return []

        # 1. Map page numbers with DIRECT hits to their highest score
        page_max_scores: Dict[int, float] = {}
        direct_hit_pages = set()
        for chunk, score in all_retrieved_chunks:
            page = chunk.metadata.get('page_number')
            print(f"  - Chunk on page {page} with score {score}")
            if page is not None:
                direct_hit_pages.add(page)
                try:
                    current_score = float(score)
                    page_max_scores[page] = max(page_max_scores.get(page, -float('inf')), current_score)
                except (ValueError, TypeError):
                    print(f"Warning: Could not convert score '{score}' to float for chunk on page {page}. Skipping score.")
                    if page not in page_max_scores: page_max_scores[page] = -float('inf') # Assign default if page is new

        if not page_max_scores:
            print("  - No valid page numbers found in retrieved chunks.")
            return []
        print(f"  - Direct hit pages with max scores: { {p: f'{s:.4f}' for p, s in sorted(page_max_scores.items())} }")

        # 2. Determine the full set of target pages (direct hits + range)
        target_pages = set(direct_hit_pages) # Start with direct hits
        print(f"  - Expanding range by +/- {page_range} page(s)...")
        for page in direct_hit_pages:
            for i in range(-page_range, page_range + 1):
                if i == 0: continue # Skip the page itself (already added)
                page_to_check = page + i
                if page_to_check > 0: # Ensure valid page number
                    target_pages.add(page_to_check)
        print(f"  - Final target pages to check for images: {sorted(list(target_pages))}")


        # 3. Gather all candidate images from ALL target pages.
        #    Assign actual score if page had a direct hit, else assign very low score.
        candidate_images_with_scores = []
        VERY_LOW_SCORE = -float('inf') # Score for images from adjacent-only pages
        print(f"  DEBUG: Available page keys in self.image_descriptions: {sorted(list(self.image_descriptions.keys()))[:50]}...")
        for page_num in sorted(list(target_pages)): # Iterate through all target pages
            # Assign score: actual max score if direct hit, otherwise VERY_LOW_SCORE
            page_score = page_max_scores.get(page_num, VERY_LOW_SCORE)
            print(f"\n  DEBUG: Checking target page {page_num}...")


            # Check if descriptions exist for this page
            if self.image_descriptions and page_num in self.image_descriptions:
                page_image_list = self.image_descriptions[page_num]
                if not page_image_list:
                    print(f"    DEBUG: Image list for page {page_num} is empty.")
                    continue # Skip to next page
                print(f"    DEBUG: Found {len(page_image_list)} stored image entries for page {page_num}.")

                for stored_img_data in page_image_list:
                    # Ensure required keys exist and figure number is usable
                    print(f"        DEBUG: VALID entry found. Appending.")
                    if ('image_path' in stored_img_data and
                        'figure_number' in stored_img_data and
                        isinstance(stored_img_data['figure_number'], (int, float))):

                        candidate_images_with_scores.append({
                            'page_number': page_num,
                            'figure_number': int(stored_img_data['figure_number']),
                            'image_path': str(stored_img_data['image_path']),
                            'relevance_score': page_score # Use actual score or VERY_LOW_SCORE
                        })
                    else:
                        print(f"Warning: Skipping image data due to missing keys or invalid figure_number on page {page_num}: {stored_img_data}")
            else:
                print(f"    DEBUG: Page {page_num} not found as a key in self.image_descriptions.")

        if not candidate_images_with_scores:
            print("  - No valid images found on any target pages.")
            return []
        print(f"  - Found {len(candidate_images_with_scores)} candidate images across target pages.")


        # 4. Sort primarily by relevance score (desc), then page/figure (asc) for stable limiting
        #    Images from adjacent-only pages (with VERY_LOW_SCORE) will naturally end up last.
        candidate_images_with_scores.sort(
            key=lambda x: (x['relevance_score'], -x['page_number'], -x['figure_number']), # Score desc, page/fig asc
            reverse=True
        )


        # 5. Limit the number of images based on this score priority
        selected_images_info_relevance_sorted = candidate_images_with_scores[:max_images]
        print(f"  - Selected top {len(selected_images_info_relevance_sorted)} images based on relevance score (incl. adjacent pages).")

        # --- Optional: Log which pages might have been excluded ---
        # (Keep the previous logging logic here if desired)
        if len(candidate_images_with_scores) > max_images:
            included_pages = {img['page_number'] for img in selected_images_info_relevance_sorted}
            potential_candidate_pages = {img['page_number'] for img in candidate_images_with_scores}
            excluded_pages = potential_candidate_pages - included_pages
            partially_included_pages = set()
            if excluded_pages or len(selected_images_info_relevance_sorted) < len(candidate_images_with_scores):
                scores_of_excluded = {img['relevance_score'] for img in candidate_images_with_scores[max_images:]}
                min_score_excluded = min(scores_of_excluded) if scores_of_excluded else -float('inf')
                last_included_score = selected_images_info_relevance_sorted[-1]['relevance_score'] if selected_images_info_relevance_sorted else -float('inf')

                for img in selected_images_info_relevance_sorted:
                    # Check if this included image's score is low enough that some images on the same page *might* have been cut
                    # Or if its score is the same as the lowest score that got excluded (meaning page was cut mid-way)
                    if img['relevance_score'] <= last_included_score :
                        partially_included_pages.add(img['page_number'])

            print(f"    - Pages with direct hits fully included: {included_pages.intersection(direct_hit_pages) - partially_included_pages}")
            print(f"    - Adjacent-only pages fully included: {included_pages - direct_hit_pages - partially_included_pages}")
            if partially_included_pages.intersection(direct_hit_pages): print(f"    - Pages with direct hits potentially partially included: {partially_included_pages.intersection(direct_hit_pages)}")
            if partially_included_pages - direct_hit_pages: print(f"    - Adjacent-only pages potentially partially included: {partially_included_pages - direct_hit_pages}")
            if excluded_pages: print(f"    - Pages fully excluded (due to lower relevance or limit): {excluded_pages}")
        # --- End optional logging ---


        # 6. Ensure image paths exist and prepare the final list (including scores)
        #    NO final sort by page/figure here - return sorted by relevance
        final_relevant_images = []
        for img_info in selected_images_info_relevance_sorted: # Use the relevance sorted list
            img_path = img_info['image_path']
            if Path(img_path).exists():
                # Include score in the returned dictionary
                final_relevant_images.append({
                    'page_number': img_info['page_number'],
                    'figure_number': img_info['figure_number'],
                    'image_path': img_path,
                    'relevance_score': img_info['relevance_score'] # Keep the score
                })
            else:
                print(f"Warning: Selected image path does not exist, skipping final inclusion: {img_path}")

        print(f"  - Returning {len(final_relevant_images)} existing images, sorted by relevance score (desc).")
        # RETURN THE LIST SORTED BY RELEVANCE SCORE
        return final_relevant_images

    def _format_kg_triplets(self, kg_triplets: List[Dict[str, str]]) -> str:
        """
        Format KG triplets for display, removing duplicates.

        Args:
            kg_triplets: List of KG triplets

        Returns:
            Formatted text
        """
        # Create a dictionary to store unique relation-tail pairs for each head
        triplet_groups = {}
        unique_relations = {}  # To track unique relation-tail pairs for each head
        
        for triplet in kg_triplets:
            head = triplet['head']
            relation = triplet['type'].replace('_', ' ')
            tail = triplet['tail']
            
            # Initialize if this head hasn't been seen before
            if head not in triplet_groups:
                triplet_groups[head] = []
                unique_relations[head] = set()
            
            # Create a unique key for this relation-tail pair
            relation_tail_key = f"{relation}|{tail}"
            
            # Only add if we haven't seen this relation-tail pair for this head
            if relation_tail_key not in unique_relations[head]:
                unique_relations[head].add(relation_tail_key)
                triplet_groups[head].append((relation, tail))
        
        # Format input for display
        structured_input = ""
        for head, relation_tails in triplet_groups.items():
            structured_input += f"About {head}:\n"
            for relation, tail in relation_tails:
                structured_input += f"- {relation} {tail}\n"
            structured_input += "\n"

        logger.info(f"Formatted {sum(len(relation_tails) for relation_tails in triplet_groups.values())} unique KG triplets after deduplication")
        return structured_input

    def _format_enhanced_context(self,
                                 chunks: List[Tuple[Chunk, float]],
                                 kg_triplets: List[Dict[str, str]] # Pass raw triplets
                                 ) -> str:
        """
        Formats context with text chunks, KG info, and a grouped image description block.
        Aligns formatting with llm_response.py.

        Args:
            chunks: Retrieved document chunks with relevance scores.
            kg_triplets: Raw list of relevant knowledge graph triplets.

        Returns:
            Formatted enhanced context string.
        """
        # 1. Format text chunks, tracking tokens and included chunks
        formatted_chunks_text = []
        current_tokens = 0
        included_chunks_for_images = [] # Track which chunks actually fit

        # logger.info("Formatting text context...")
        for chunk, score in chunks:
            # Format chunk content without page number in text
            formatted_chunk = (
                f"\n{chunk.text}\n"
                f"{'=' * 40}"
            )

            chunk_tokens = self._count_tokens(formatted_chunk)
            # Check if adding this chunk exceeds the text portion of the limit
            # We leave some room for KG and image context to be added later
            # Let's allocate roughly 80% for text initially, adjustable
            text_token_limit = int(self.max_context_tokens * 0.8)
            if current_tokens + chunk_tokens > text_token_limit:
                logger.warning(f"Text content reached token limit ({text_token_limit}). Stopping text chunk inclusion.")
                break

            formatted_chunks_text.append(formatted_chunk)
            included_chunks_for_images.append((chunk, score)) # Add to list for image fetching
            current_tokens += chunk_tokens

        logger.info(f"Formatted {len(formatted_chunks_text)} text chunks. Text tokens: {current_tokens}")

        # Combine text context first
        combined_context = "\n".join(formatted_chunks_text)

        # 2. Get and format image descriptions based on *included* chunks
        logger.info("Fetching and formatting image context...")
        image_start = time.time()
        image_descriptions_by_page = self._get_relevant_image_descriptions(included_chunks_for_images)
        image_context = ""
        image_tokens = 0
        if image_descriptions_by_page:
            image_context = self._format_image_descriptions(image_descriptions_by_page)
            image_tokens = self._count_tokens(image_context)
            self.image_desc_time = time.time() - image_start
            logger.info(f"Image context generation took {self.image_desc_time:.2f}s")
            logger.info(f"  - Image context tokens: {image_tokens}")
        else:
            logger.info("\nNo relevant image context found or generated.")

        # 3. Format Knowledge Graph context
        logger.info("Formatting KG context...")
        kg_start_format = time.time()
        kg_context = ""
        kg_tokens = 0
        if kg_triplets:
            # Use the existing method to format triplets textually
            formatted_kg_text = self._format_kg_triplets(kg_triplets) # Use the raw triplets passed in
            kg_context = f"\n\n--- Knowledge Graph Information ---\n{formatted_kg_text}\n------------------------------\n"
            kg_tokens = self._count_tokens(kg_context)
            self.format_kg_time = time.time() - kg_start_format # Overwrite timer with formatting time
            logger.info(f"KG context generation took {self.format_kg_time:.2f}s")
            logger.info(f"  - KG context tokens: {kg_tokens}")
        else:
             logger.info("No relevant KG context found or generated.")

        # 4. Combine contexts respecting the total token limit
        logger.info(f"Combining contexts. Current text tokens: {current_tokens}")
        logger.info(f"Image tokens: {image_tokens}. KG tokens: {kg_tokens}")
        logger.info(f"Max total tokens: {self.max_context_tokens}")

        # Add KG context if it fits
        if kg_context and (current_tokens + kg_tokens <= self.max_text_tokens):
            combined_context += kg_context
            current_tokens += kg_tokens
            logger.info("  - Added KG context.")
        elif kg_context:
            logger.warning("Could not add KG context as it would exceed token limit.")

        # Add Image context if it fits
        if image_context and (current_tokens + image_tokens <= self.max_text_tokens):
            combined_context += image_context
            current_tokens += image_tokens
            logger.info("  - Added Image context.")
        elif image_context:
            logger.warning("Could not add Image context as it would exceed token limit.")

        logger.info(f"Final combined context size: {current_tokens} tokens.")

        # Final truncation (should be rare if initial limits are good)
        # combined_context = self._truncate_context(combined_context, self.max_context_tokens)
        return combined_context

    def _count_tokens(self, text: str) -> int:
        """Count tokens using the processor's tokenizer"""
        # The processor object usually wraps the tokenizer
        if hasattr(self.processor, 'tokenizer'):
             return len(self.processor.tokenizer.encode(text))
        else:
             # Fallback if tokenizer is accessed differently or unavailable
             print("Warning: Could not access processor.tokenizer directly for token counting.")
             # Approximate by splitting, less accurate
             return len(text.split())

    def _create_system_message(self) -> str:
        """Create a system message for the LLM (Aligned with llm_response.py)."""
        # Content copied exactly from llm_response.py's _create_system_message
        return """
                **Instructions for Answer Generation:**

                **Guiding Principle:** Your primary goal is to provide accurate, context-based answers derived *strictly* from the provided text context and the visual information in the referenced images. Enhance answers by referencing specific images using their filenames when they directly illustrate key points.

                1.  **Image References Provided:**
                    *   You have been given text context and potentially relevant images.
                    *   These images are introduced in the text with lines like: `Image N: reference: <filename>: [description]`.
                    *   The string immediately following `reference:` (e.g., `page_10_figure_1.png`) is the **exact filename** you must use for referencing.

                2.  **Image Referencing Requirement:**
                    *   When an image visually clarifies or demonstrates something mentioned in your text answer, **you MUST reference it using the specific filename identified above.**
                    *   **Correct Reference Format:** `[Image: <image_filename.png>]`
                    *   **Example:** If the text introduces `Image 3: reference: page_45_diagram_2.png: A flowchart...`, and you refer to it, you MUST write `[Image: page_45_diagram_2.png]`.
                    *   **Incorrect:** Do NOT use sequential labels like `Image 3` or `Image reference 3` in your final answer's references. Use the FILENAME.

                3.  **Image Placement:**
                    *   Integrate image references (using the filename format) naturally *within the sentence* it supports.
                    *   Avoid placing references at the end of paragraphs or as standalone items.

                4.  **Relevance & Grounding:**
                    *   Base your entire answer **only** on the provided text context and the visual information in the images whose references were provided.
                    *   Reference an image **only** if its visual content directly supports the specific point you are making. Use the information from the image description line and the image itself.

                5.  **Content Structure & Style:**
                    *   Respond in clear and precise **markdown format**.
                    *   Structure answers logically (headings, lists). Keep explanations concise.

                6.  **Handling Insufficient Information:**
                    *   If the text and images *together* are insufficient to answer accurately, respond *only* with:
                        > *"Based on the provided context and images, I am unable to provide a correct answer."*

                7.  **Truthfulness & Strict Grounding:**
                    *   **Do NOT** invent or hallucinate information, procedures, or visual details not present in the provided text or images/descriptions.
                    *   Verify every statement against the provided materials. **Strict adherence to the provided context (text, image references, and visual content) is mandatory.**
                """

    def _create_user_message(self, query: str, context: str) -> str:
        """Create a user message with query and context (Aligned with llm_response.py)."""
        # Content structure copied exactly from llm_response.py's _create_user_message
        return f"""**Context:**
                {context}

                ---

                **Question:**
                {query}"""


    def _prepare_context_and_messages(
        self,
        query: str,
        chunks: List[Tuple[Chunk, float]],
        kg_triplets: List[Dict[str, str]],
        ) -> Tuple[List[Dict], List[Dict[str, Union[str, int]]]]:
        """
        Formats text context, identifies relevant images, looks up their descriptions,
        introduces them explicitly in the text prompt using the specified format,
        and constructs the 'messages' list for Qwen-VL.

        Returns:
            Tuple: (messages_list, included_image_info_list)
        """
        # 1. Format Text Chunks (respecting max_context_tokens)
        formatted_text_chunks = []
        current_text_tokens = 0
        final_chunks_in_context = []

        print("Formatting text context...")
        for chunk, score in chunks:
            # Ensure chunk text is string and handle potential None
            chunk_text = chunk.text if chunk.text is not None else ""
            formatted_chunk = f"\n{chunk_text}\n{'=' * 40}"
            chunk_tokens = self._count_tokens(formatted_chunk) # Count tokens for this chunk

            if current_text_tokens + chunk_tokens <= self.max_context_tokens:
                formatted_text_chunks.append(formatted_chunk)
                current_text_tokens += chunk_tokens
                final_chunks_in_context.append((chunk, score)) # Add chunk to the list of used ones
            else:
                print(f"Text context reached token limit ({self.max_context_tokens}). Stopping text inclusion.")
                break # Stop adding text chunks

        print(f"Formatted {len(formatted_text_chunks)} text chunks. Total text tokens: {current_text_tokens}")
        combined_text_context = "\n".join(formatted_text_chunks)

        # 2. Combine KG triplets into context
        formatted_kg_context = self._format_kg_triplets(kg_triplets)
        kg_context = f"\n\n--- Knowledge Graph Information ---\n{formatted_kg_context}\n-------------------------\n"
        combined_context = combined_text_context + kg_context

        # 3. Get Relevant Image Paths based on included chunks
        print("Fetching relevant image paths...")
        relevant_images_info = self._get_relevant_image_paths(
            final_chunks_in_context,
            max_images=self.max_image_references
        ) # List[Dict{'page_number', 'figure_number', 'image_path'}]


        # 3. Construct the Textual Introduction for Images (with Descriptions)
        image_introduction_text = ""
        image_paths_for_message = [] # Store paths in order for message construction
        if relevant_images_info:
            print(f"Constructing image introduction block for {len(relevant_images_info)} images with descriptions.")
            # Optional Header - adjust or remove if needed
            image_introduction_text += "**Image References:**\n"

            for i, img_info in enumerate(relevant_images_info):
                target_image_path = img_info['image_path']
                page_num = img_info['page_number']
                filename = Path(target_image_path).name

                # --- Find the description ---
                description = "Description not available." # Default fallback
                if self.image_descriptions and page_num in self.image_descriptions:
                    # Get the list of image dicts for the correct page
                    page_image_list = self.image_descriptions[page_num]
                    # Find the specific image dict by matching the path
                    found_desc = False
                    for stored_img_data in page_image_list:
                        # Ensure paths match (or use filename if paths might differ slightly)
                        if stored_img_data.get('image_path') == target_image_path:
                            description = stored_img_data.get('description', "Description not available.")
                            found_desc = True
                            break # Found the matching image on this page
                    if not found_desc:
                         print(f"Warning: Image path '{target_image_path}' not found in stored descriptions for page {page_num}.")

                else:
                     print(f"Warning: No stored image descriptions found for page {page_num}.")
                # -----------------------------

                # Construct the line in the desired format
                image_introduction_line = f"Image reference {i+1}: {filename}: {description}\n"
                image_introduction_text += image_introduction_line

                image_paths_for_message.append(target_image_path) # Add path for message construction

            image_introduction_text += "---\n" # Separator after image intros
        else:
            print("No relevant images identified to include in the prompt.")


        # 4. Construct the Final Text Prompt for the User Message
        # Combine image introductions, context, and query
        final_text_prompt = f"""{image_introduction_text}
                        **Relevant Document Context:**
                        {combined_context}

                        ---
                        **Question:**
                        {query}
                        """
        # print("Context")
        # print(combined_context)
        # 5. Construct the 'messages' list for Qwen-VL
        messages = []

        # -- System Message --
        messages.append({"role": "system", "content": self._create_system_message()})

        # -- User Message --
        user_content = []

        # Add image entries first (in the order they were introduced in the text)
        if image_paths_for_message:
            for img_path in image_paths_for_message:
                # Ensure path exists before adding
                if Path(img_path).exists():
                    user_content.append({"type": "image", "image": img_path})
                else:
                     print(f"Error: Image path does not exist, cannot add to message: {img_path}")


        # Add the single text entry containing the structured prompt
        user_content.append({"type": "text", "text": final_text_prompt})

        messages.append({"role": "user", "content": user_content})

        print(f"Constructed messages list. User role has {len(user_content)} items ({len(image_paths_for_message)} actual image paths included, 1 text block).")
        # print(f"DEBUG: Final Text Prompt Part:\n{final_text_prompt[:1000]}...") # Optional: Print start of text prompt

        # Return messages and the structured image info list
        return messages, relevant_images_info


    def query(self, user_query: str, num_chunks: int = 5) -> RAGResponse:
        """
        Main method that combines all steps to enhance the prompt with KG info.

        Args:
            user_query: The user's question
            num_chunks: Number of chunks to retrieve

        Returns:
            RAGResponse with enhanced context
        """
        try:
            start_time = time.time()
            logger.info(f"Processing query: {user_query}")

            # 1. Get relevant chunks using the base retriever
            start_retrieval = time.time()
            chunks = self.base_retriever.search(user_query, k=num_chunks)
            self.retrieval_time = time.time() - start_retrieval
            logger.info(f"Retrieved {len(chunks)} chunks in {self.retrieval_time:.2f}s")
            # Optional: Unload embedding model early if memory is tight
            # self.base_retriever.unload_embedding_model()

            # 2. Extract entities from query
            entities_start = time.time()
            entities = self._extract_entities(user_query)
            self.extract_entities_time = time.time() - entities_start
            logger.info(f"Extracted {len(entities)} entities: {entities[:5]}... "
                        f"in {self.extract_entities_time:.2f}s")

            # 3. Find relevant KG nodes (get raw triplets)
            kg_start = time.time()
            kg_triplets = self._find_kg_matches(entities) # Get the raw list of dicts
            self.relevant_kg_nodes_time = time.time() - kg_start
            logger.info(f"Found {len(kg_triplets)} relevant KG triplets "
                        f"in {self.relevant_kg_nodes_time:.2f}s")

            # 4. Combine everything into a unified context using the NEW method
            #    This method now handles text chunk formatting, image fetching/formatting,
            #    and KG formatting internally.
            # enhanced_context = self._format_enhanced_context(chunks, kg_triplets)
            # Note: _format_enhanced_context now also logs token counts and timings internally

            # 5. Create messages for chat template (using the new methods)
            # messages = [
            #     {"role": "system", "content": self._create_system_message()},
            #     {"role": "user", "content": self._create_user_message(user_query, enhanced_context)}
            # ]

            # Apply chat template if tokenizer supports it
            if not self.VLM:
                if hasattr(self.llm_tokenizer, 'apply_chat_template'):
                    prompt = self.llm_tokenizer.apply_chat_template(
                        messages,
                        tokenize=False,
                        add_generation_prompt=True
                    )
                else:
                    # Fallback for tokenizers without chat template
                    logger.warning("Tokenizer does not support chat template, using fallback")
                    # Ensure fallback aligns with how llm_response might handle it if needed
                    prompt = f"{messages[0]['content']}\n\n{messages[1]['content']}\n\n**Answer:**" # Example fallback

            # Count tokens for metrics
            # prompt_tokens = self._count_tokens(prompt)
            # logger.info(f"Final prompt tokens: {prompt_tokens}")

            # Generate the response
            response_start = time.time()
            if not self.VLM:
                if self.llm_model is None:
                    raise RuntimeError("LLM model not initialized (expected inheritance).")
                with torch.inference_mode():
                    # Debugging: Check device placement
                    # device_info = f"Device: {self.llm_model.device}" # Already logged in _initialize_llm
                    # logger.info(device_info)

                    response_output = self.pipe(
                        prompt,
                        max_new_tokens=1024, # Consider making this configurable
                        do_sample=True,
                        temperature=0.1, # Consider making this configurable
                        return_full_text=False,
                        pad_token_id=self.llm_tokenizer.eos_token_id,
                        use_cache=True,
                    )
                    self.generation_time = time.time() - response_start

                    # Log raw output for debugging
                    # logger.info(f"Raw output: {response_output}")

                    if not response_output or len(response_output) == 0:
                        logger.error("Empty response from model")
                        response = "Error: The model returned an empty response."
                    else:
                        response = response_output[0]["generated_text"].strip()

                    # Fallback for empty responses
                    if not response:
                        logger.warning("Empty response after processing, using fallback")
                        response = "I couldn't generate a proper response based on the available information. Please try rephrasing your question."

                logger.info(f"Generation time: {self.generation_time:.2f}s")
                logger.info(f"Total processing time: {time.time() - start_time:.2f}s")

                completion_tokens = self._count_tokens(response)

                # Return as RAGResponse
                return RAGResponse(
                    answer=response,
                    source_chunks=chunks, # Return original chunks for potential inspection
                    prompt_tokens=prompt_tokens,
                    completion_tokens=completion_tokens
                )
            else:
                print("Preparing context and messages for VL model...")
                start_context = time.time()
                # Pass only the final desired number of chunks after potential reranking
                messages, included_images = self._prepare_context_and_messages(user_query, chunks, kg_triplets)
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
                    source_chunks=chunks, # Or pass original Chunk objects if serializable
                    prompt_tokens=prompt_tokens,
                    completion_tokens=completion_tokens,
                    included_images=included_images # Add the list of image dicts used
                )

        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            import traceback
            traceback.print_exc() # Print traceback for debugging
            # Return a basic response with the error
            return RAGResponse(
                answer=f"An error occurred while processing your request. Please check the logs.",
                source_chunks=[],
                prompt_tokens=0,
                completion_tokens=0,
                included_images=[]
            )

    def _extract_common_kg_terms(self, min_freq: int = 2, min_length: int = 3) -> List[str]:
        """
        Extract common terms from the knowledge graph for better entity recognition.

        Args:
            min_freq: Minimum frequency for a term to be considered common
            min_length: Minimum length for a term in characters

        Returns:
            List of common terms from the knowledge graph
        """
        # Count term frequencies
        term_counts = {}

        for triplet in self.kg:
            for field in ['head', 'tail']:
                term = triplet[field]

                # Skip very short terms
                if len(term) < min_length:
                    continue

                if term not in term_counts:
                    term_counts[term] = 0
                term_counts[term] += 1

        # Filter by frequency
        common_terms = [term for term, count in term_counts.items()
                        if count >= min_freq]

        logger.info(f"Extracted {len(common_terms)} common terms from knowledge graph")
        return common_terms

    def unload_models(self):
        """
        Unload models to free GPU memory.
        """
        try:
            # Unload LLM model
            if hasattr(self, 'llm_model') and self.llm_model is not None:
                self.llm_model.cpu()
                del self.llm_model
                self.llm_model = None

            # Clean up GPU memory
            if torch.cuda.is_available():
                torch.cuda.empty_cache()

            logger.info("Successfully unloaded models")

        except Exception as e:
            logger.error(f"Error unloading models: {str(e)}")


# Example usage
if __name__ == "__main__":
    # Configuration
    IMAGE_DESCRIPTIONS_PATH = r"C:\Users\Anwender\Desktop\Nicolas\Dokumente\FH Bielefeld\Optimierung und Simulation\4. Semester\masterthesis\programming\server_backup\image_descriptions\english---mill-ngc---operator's-manual---2017_image_description.pkl"
    INDEX_DIR = "index"
    DOCUMENT_NAME = "english---mill-ngc---operator's-manual---2017"
    KG_FILE_PATH = r"C:\Users\Anwender\Desktop\Nicolas\Dokumente\FH Bielefeld\Optimierung und Simulation\4. Semester\masterthesis\programming\knowledge_graphs\english---mill-ngc---operator's-manual---2017_kg.txt"
    CACHE_DIR = "kg_cache"

    try:
        # Initialize the KG-enhanced retriever
        retriever = KGEnhancedRetriever(
            kg_file_path=KG_FILE_PATH,
            index_dir=INDEX_DIR,
            document_name=DOCUMENT_NAME,
            image_descriptions_path=IMAGE_DESCRIPTIONS_PATH,
            llm_model_name="unsloth/Qwen2.5-VL-32B-Instruct-bnb-4bit",
            cache_dir=CACHE_DIR
        )

        # Example query
        query = "How do I use G41 for cutter compensation?"

        # Get enhanced response
        response = retriever.query(query)
        print(response.answer)

        # Print results
        # print("\nQuery:", query)
        # print("\nSource Documents:")
        # for i, (chunk, score) in enumerate(response.source_chunks[:3]):
        #     page_info = ""
        #     if hasattr(chunk, 'metadata') and chunk.metadata and 'page_number' in chunk.metadata:
        #         page_info = f" (Page {chunk.metadata['page_number']})"

        #     print(f"\nChunk {i + 1}{page_info} (Relevance: {score:.2f}):")
        #     print(chunk.text[:150] + "...")

        print(f"\nUsed {response.prompt_tokens} prompt tokens")

        # Clean up
        retriever.unload_models()

    except Exception as e:
        logger.error(f"Error in example: {str(e)}")
        import traceback

        traceback.print_exc()
