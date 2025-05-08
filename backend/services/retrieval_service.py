from typing import List, Dict, Any, Optional
import logging
import weaviate # Added
import uuid # Added for type hinting

# from sqlalchemy.ext.asyncio import AsyncSession # Removed
from langchain_openai import OpenAIEmbeddings
# from langchain_community.vectorstores import FAISS # Removed

# from models.document import Document # Removed
from backend.core.config import settings # Ensure backend. prefix
from backend.core.weaviate_manager import get_weaviate_client # Added

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Initialize embeddings model (ensure consistency with ingestion)
embeddings_model = OpenAIEmbeddings(api_key=settings.OPENAI_API_KEY, model=settings.EMBEDDING_MODEL)

async def find_relevant_chunks(query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """
    Finds the most relevant document chunks for a given query using Weaviate vector similarity search.
    Returns a list of dictionaries, each containing chunk content and metadata.
    """
    client: Optional[weaviate.WeaviateClient] = None
    try:
        client = get_weaviate_client()
        # Schema check is typically done at startup or by ingestion, not usually per query.
        # If client.is_connected() or similar check is available, it might be good.
        # For now, assume client is connected if get_weaviate_client() doesn't raise.

        query_embedding = await embeddings_model.aembed_query(query)
        logger.info(f"Generated query embedding (dim: {len(query_embedding)}) for query: '{query[:50]}...'")

        collection = client.collections.get(settings.WEAVIATE_INDEX_NAME)
        
        response = collection.query.near_vector(
            near_vector=query_embedding,
            limit=top_k,
            return_metadata=weaviate.classes.query.MetadataQuery(distance=True), # Include distance
            return_properties=["content", "source_filename", "chunk_index", "doc_id"] # Specify properties to return
        )

        relevant_chunks = []
        if response.objects:
            for obj in response.objects:
                chunk_data = {
                    "id": str(obj.uuid), # The UUID of the Weaviate object (chunk)
                    "content": obj.properties.get("content"),
                    "source_filename": obj.properties.get("source_filename"),
                    "chunk_index": obj.properties.get("chunk_index"),
                    "doc_id": obj.properties.get("doc_id"), # Original document ID
                    "distance": obj.metadata.distance if obj.metadata else None,
                    # Add other metadata from obj.properties as needed
                }
                relevant_chunks.append(chunk_data)
        
        logger.info(f"Retrieved {len(relevant_chunks)} relevant chunks from Weaviate for query: '{query[:50]}...'")
        return relevant_chunks

    except ConnectionError as ce:
        logger.error(f"Connection error during Weaviate retrieval: {ce}")
        return []
    except Exception as e:
        logger.error(f"Error during Weaviate retrieval: {e}")
        return [] # Return empty list on error
    finally:
        if client:
            client.close()
            logger.info("Weaviate client connection closed after retrieval.")
