import uuid
from typing import Dict, List, Optional, Any

from core.config import settings

# Base class for SQLAlchemy (when needed)
class Base:
    pass

# Document model for the RAG system
class Document:
    def __init__(
        self,
        content: str,
        embedding: Optional[List[float]] = None,
        id: Optional[uuid.UUID] = None,
        doc_metadata: Optional[Dict[str, Any]] = None
    ):
        self.id = id or uuid.uuid4()
        self.content = content
        self.embedding = embedding  # Vector embedding for the document
        self.doc_metadata = doc_metadata or {}  # Metadata (source, timestamps, etc.)

