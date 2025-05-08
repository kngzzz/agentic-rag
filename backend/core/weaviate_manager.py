import weaviate
import weaviate.classes as wvc # Updated import for v4
from weaviate.auth import AuthApiKey
from weaviate.exceptions import WeaviateQueryException, UnexpectedStatusCodeException
from typing import Optional
import logging # Added for logging

from backend.core.config import settings

# Configure basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_weaviate_client() -> weaviate.WeaviateClient:
    """Initializes and returns a Weaviate client."""
    try:
        client = weaviate.connect_to_weaviate_cloud( # Updated method name
            cluster_url=settings.WEAVIATE_URL,
            auth_credentials=AuthApiKey(settings.WEAVIATE_API_KEY),
            # grpc_port=50051 if settings.WEAVIATE_GRPC_ENABLED else None, # Enable gRPC if configured
            # skip_init_checks=False # Set to True if you want to skip startup checks
        )
        logger.info(f"Successfully connected to Weaviate at {settings.WEAVIATE_URL}")
        return client
    except Exception as e:
        logger.error(f"Failed to connect to Weaviate: {e}")
        raise

def ensure_schema_exists(client: weaviate.WeaviateClient):
    """Ensures the 'DocumentChunk' schema (collection) exists in Weaviate."""
    collection_name = settings.WEAVIATE_INDEX_NAME
    try:
        if not client.collections.exists(collection_name):
            logger.info(f"Collection '{collection_name}' does not exist. Creating it...")
            client.collections.create(
                name=collection_name,
                description="Stores document chunks and their embeddings for semantic search.",
                vectorizer_config=wvc.config.Configure.Vectorizer.none(), # Using pre-computed vectors
                vector_index_config=wvc.config.Configure.VectorIndex.hnsw(
                    distance_metric=wvc.config.VectorDistances.COSINE # Or DOT, EUCLIDEAN as per your embedding model's best practice
                ),
                properties=[
                    wvc.config.Property(
                        name="content",
                        data_type=wvc.config.DataType.TEXT,
                        description="Text content of the document chunk"
                        # tokenization removed, typically not needed for primary vector search field
                        # If specific keyword search on content is needed, consider "word" or "whitespace"
                    ),
                    wvc.config.Property(
                        name="source_filename",
                        data_type=wvc.config.DataType.TEXT,
                        description="Original filename of the document source",
                        tokenization=wvc.config.Tokenization.FIELD # Use enum member
                    ),
                    wvc.config.Property(
                        name="chunk_index",
                        data_type=wvc.config.DataType.INT,
                        description="Index of the chunk within the original document"
                    ),
                    wvc.config.Property(
                        name="doc_id",
                        data_type=wvc.config.DataType.TEXT,
                        description="Unique identifier for the original document",
                        tokenization=wvc.config.Tokenization.FIELD # Use enum member
                    ),
                    wvc.config.Property(
                        name="author",
                        data_type=wvc.config.DataType.TEXT,
                        description="Author of the document (optional)",
                        skip_indexing=True # If not directly searching/filtering on it often
                    ),
                    wvc.config.Property(
                        name="creation_date",
                        data_type=wvc.config.DataType.DATE,
                        description="Creation date of the document (optional)",
                        skip_indexing=True
                    ),
                    wvc.config.Property(
                        name="modification_date",
                        data_type=wvc.config.DataType.DATE,
                        description="Last modification date of the document (optional)",
                        skip_indexing=True
                    ),
                ]
            )
            logger.info(f"Collection '{collection_name}' created successfully.")
        else:
            logger.info(f"Collection '{collection_name}' already exists.")
            # Optionally, you could add logic here to verify/update existing schema if needed.
    except UnexpectedStatusCodeException as e:
        logger.error(f"Error creating or checking collection '{collection_name}': {e.message} (Status code: {e.status_code})")
        raise
    except WeaviateQueryException as e:
        logger.error(f"Query error during schema check/creation for '{collection_name}': {e.message}")
        raise
    except Exception as e:
        logger.error(f"An unexpected error occurred with Weaviate schema for '{collection_name}': {e}")
        raise

# Example usage (optional, for testing this module directly):
if __name__ == "__main__":
    logger.info("Attempting to connect to Weaviate and ensure schema exists...")
    try:
        # This requires your .env file to be in the same directory or PYTHONPATH to be set correctly
        # when running this script directly for 'from backend.core.config import settings' to work.
        # Alternatively, load .env explicitly here for standalone testing.
        # from dotenv import load_dotenv
        # import os
        # load_dotenv(dotenv_path='../../.env') # Adjust path as needed
        # settings.WEAVIATE_URL = os.getenv("WEAVIATE_URL")
        # settings.WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")
        
        if not settings.WEAVIATE_URL or not settings.WEAVIATE_API_KEY:
            logger.error("WEAVIATE_URL and WEAVIATE_API_KEY must be set in .env or environment.")
        else:
            weaviate_client = get_weaviate_client()
            if weaviate_client.is_connected():
                ensure_schema_exists(weaviate_client)
                logger.info("Schema check/creation process completed.")
                weaviate_client.close()
                logger.info("Weaviate client connection closed.")
            else:
                logger.error("Failed to connect to Weaviate. Schema check not performed.")
    except Exception as e:
        logger.error(f"Error in Weaviate manager direct execution: {e}")
