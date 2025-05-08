import logging
import io
import uuid
from typing import List, Dict, Any, Optional
import json # Added for JSON processing
import weaviate # Added for Weaviate client type hint

# Setup basic logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

from fastapi import UploadFile
# from core.database import WeaviateDBService # Removed
from backend.core.weaviate_manager import get_weaviate_client, ensure_schema_exists # Added
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from pypdf import PdfReader

# from models.document import Document # Removed
from backend.core.config import settings # Ensure backend. is used for consistency

# Initialize embeddings model
# Ensure OPENAI_API_KEY is set in the environment or .env file
embeddings = OpenAIEmbeddings(api_key=settings.OPENAI_API_KEY, model=settings.EMBEDDING_MODEL)

async def _generate_embeddings(texts: List[str], batch_size: int = 100) -> List[List[float]]:
    """Generates embeddings for a list of texts in batches."""
    all_embeddings = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        logger.info(f"Generating embeddings for batch {i // batch_size + 1}...")
        batch_embeddings = await embeddings.aembed_documents(batch)
        all_embeddings.extend(batch_embeddings)
        logger.info(f"Batch {i // batch_size + 1} embeddings generated.")
    return all_embeddings

def _extract_text_from_pdf(file_content: bytes) -> str:
    """Extracts text from a PDF file."""
    try:
        reader = PdfReader(io.BytesIO(file_content))
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n" 
        return text
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {e}")
        return ""

def _extract_text_from_txt(file_content: bytes) -> str:
    """Extracts text from a TXT file."""
    try:
        return file_content.decode("utf-8")
    except UnicodeDecodeError:
        try:
            return file_content.decode("latin-1") # Common fallback encoding
        except Exception as e:
            logger.error(f"Error decoding text file with fallback: {e}")
            return ""
    except Exception as e:
        logger.error(f"Error reading text file: {e}")
        return ""

async def process_file(file: UploadFile) -> List[uuid.UUID]:
    """
    Processes an uploaded file, extracts text units based on content type,
    chunks them, generates embeddings, and stores them in Weaviate.
    Returns a list of UUIDs for the stored document chunks.
    """
    content_bytes = await file.read()
    filename = file.filename or "unknown_file"
    content_type = file.content_type or "application/octet-stream" # Default if not provided
    logger.info(f"Processing file: {filename}, type: {content_type}")

    client: Optional[weaviate.WeaviateClient] = None
    try:
        client = get_weaviate_client()
        ensure_schema_exists(client)
    except Exception as e:
        logger.error(f"Failed to initialize Weaviate client or ensure schema for {filename}: {e}")
        # Depending on desired behavior, you might re-raise or return empty list
        raise ConnectionError(f"Could not connect to Weaviate or ensure schema: {e}") from e


    original_document_id = uuid.uuid4() # UUID for the entire source document/file
    extracted_text_units: List[Dict[str, Any]] = []

    if content_type == "application/json" or filename.endswith(".json"):
        try:
            json_data = json.loads(content_bytes.decode("utf-8"))
            # More robust JSON handling (e.g. ChatGPT exports might be a list of conversations)
            if isinstance(json_data, list): # Common for chat exports
                logger.info(f"JSON file {filename} contains a list. Processing each item as a text unit.")
                for idx, item in enumerate(json_data):
                    # Attempt to find a 'text' or 'content' field, or stringify the whole item
                    item_text_content = ""
                    if isinstance(item, dict):
                        item_text_content = item.get("text", item.get("content", item.get("message", json.dumps(item, ensure_ascii=False))))
                    elif isinstance(item, str):
                        item_text_content = item
                    else:
                        item_text_content = json.dumps(item, ensure_ascii=False)
                    extracted_text_units.append({"text": item_text_content, "source_type": "json_list_item", "original_index": idx})
                if not extracted_text_units:
                    logger.warning(f"JSON file {filename} was an empty list or items had no processable text. No text units extracted.")
            elif isinstance(json_data, dict): # A single JSON object
                logger.info(f"JSON file {filename} is a dictionary. Processing as a single text unit.")
                extracted_text_units.append({"text": json.dumps(json_data, indent=2, ensure_ascii=False), "source_type": "json_dict", "original_index": 0})
            else: # Scalar value
                logger.info(f"JSON file {filename} contains a scalar value. Processing as a single text unit.")
                extracted_text_units.append({"text": str(json_data), "source_type": "json_scalar", "original_index": 0})
        except Exception as e:
            logger.warning(f"Error parsing or processing JSON in {filename}: {e}. Falling back to plain text extraction.")
            extracted_text_units.append({"text": _extract_text_from_txt(content_bytes), "source_type": "text_fallback_json_error", "original_index": 0})
    elif content_type == "application/pdf":
        extracted_text_units.append({"text": _extract_text_from_pdf(content_bytes), "source_type": "pdf", "original_index": 0})
    elif content_type == "text/plain" or content_type == "text/markdown" or filename.endswith(".md") or filename.endswith(".txt"):
        extracted_text_units.append({"text": _extract_text_from_txt(content_bytes), "source_type": "text_or_markdown", "original_index": 0})
    else:
        logger.warning(f"Unsupported file type: {content_type} for {filename}. Attempting plain text extraction as fallback.")
        txt_fallback = _extract_text_from_txt(content_bytes)
        if not txt_fallback or txt_fallback.isspace():
             logger.error(f"Fallback text extraction failed for unsupported file type: {content_type} on {filename}")
             if client: client.close() # Ensure client is closed
             raise ValueError(f"Unsupported file type: {content_type} which could not be processed as text either.")
        extracted_text_units.append({"text": txt_fallback, "source_type": "text_fallback_unsupported", "original_index": 0})

    weaviate_objects_to_insert = [] # Store dicts for Weaviate
    all_processed_chunk_ids = [] # Store UUIDs of successfully processed chunks
    
    global_chunk_index_counter = 0 # Counter for chunk_index across the entire file

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        # add_start_index=True, # Weaviate doesn't need this directly, we manage chunk_index
    )

    for unit_index, unit_data in enumerate(extracted_text_units):
        unit_text = unit_data["text"]
        unit_source_type = unit_data["source_type"] # e.g. "pdf", "json_list_item"
        # unit_original_index = unit_data["original_index"] # Index within the original file if it was a list

        if not unit_text or unit_text.isspace():
            logger.warning(f"Text unit {unit_index} from {filename} (type: {unit_source_type}) is empty or whitespace. Skipping.")
            continue

        current_unit_chunk_texts = text_splitter.split_text(unit_text)

        if not current_unit_chunk_texts:
            logger.warning(f"Text unit {unit_index} from {filename} (type: {unit_source_type}) extracted but no chunks created. Skipping.")
            continue
        
        logger.info(f"Created {len(current_unit_chunk_texts)} chunks for text unit {unit_index} from {filename} (type: {unit_source_type}).")
        
        try:
            current_unit_chunk_embeddings = await _generate_embeddings(current_unit_chunk_texts)
            logger.info(f"Generated {len(current_unit_chunk_embeddings)} embeddings for text unit {unit_index}.")

            for i, chunk_text in enumerate(current_unit_chunk_texts):
                chunk_id = uuid.uuid4() # Generate UUID for this chunk
                
                # Prepare properties for Weaviate object
                # Ensure these match the schema in weaviate_manager.py
                properties = {
                    "content": chunk_text,
                    "source_filename": filename,
                    "chunk_index": global_chunk_index_counter,
                    "doc_id": str(original_document_id), # Store the original document's ID
                    # Optional fields, can be None if not available
                    # "author": None, 
                    # "creation_date": None,
                    # "modification_date": None,
                    # Additional metadata we might want to store, ensure schema supports them or add later
                    # "text_unit_source_type": unit_source_type,
                    # "file_content_type": content_type
                }
                
                weaviate_object = {
                    "properties": properties,
                    "vector": current_unit_chunk_embeddings[i],
                    "id": str(chunk_id) # Provide our own UUID
                }
                weaviate_objects_to_insert.append(weaviate_object)
                all_processed_chunk_ids.append(chunk_id)
                global_chunk_index_counter += 1

        except Exception as e:
            logger.error(f"Error generating embeddings or creating Weaviate objects for text unit {unit_index} from {filename}: {e}. Skipping this unit's chunks.")
            continue

    if weaviate_objects_to_insert:
        try:
            collection = client.collections.get(settings.WEAVIATE_INDEX_NAME)
            with collection.batch.dynamic() as batch: # Using dynamic batching
                for obj in weaviate_objects_to_insert:
                    batch.add_object(
                        properties=obj["properties"],
                        vector=obj["vector"],
                        uuid=obj["id"]
                    )
            
            # Check for batch errors if the client version supports detailed results
            # For now, we assume success if no exception is raised by the context manager
            # or if batch.add_object doesn't raise immediately.
            # More robust error handling can be added based on Weaviate client's batch reporting.
            logger.info(f"Successfully added {len(weaviate_objects_to_insert)} document chunks from {filename} to Weaviate.")

        except Exception as e:
            logger.error(f"Error adding document chunks from {filename} to Weaviate: {e}")
            # If batch insertion fails, we might have partial success.
            # For now, returning all IDs that were prepared.
            # Robust error handling would involve checking Weaviate's batch error reports.
            if client: client.close()
            return all_processed_chunk_ids # Or an empty list if total failure
    else:
        logger.warning(f"No document chunks were prepared for insertion from file: {filename}")
        if client: client.close()
        return []

    logger.info(f"Total {len(all_processed_chunk_ids)} chunks successfully processed and stored from file: {filename}")
    if client: client.close()
    return all_processed_chunk_ids
