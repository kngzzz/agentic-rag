from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
import uuid

class DocumentBase(BaseModel):
    content: str
    doc_metadata: Optional[Dict[str, Any]] = None

class DocumentCreate(DocumentBase):
    pass

class DocumentResponse(DocumentBase):
    id: uuid.UUID

    class Config:
        from_attributes = True # Replaces orm_mode = True in Pydantic v2

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str
    sources: Optional[list[DocumentResponse]] = None
    thought_process: Optional[str] = None # Added field
