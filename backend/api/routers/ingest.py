from fastapi import APIRouter, UploadFile, File, HTTPException # Removed Depends
from typing import List # Removed Dict, Any, uuid, AsyncSession

# from core.database import get_db # Removed
from backend.services import ingestion_service # Ensure backend. prefix
# from schemas.document import DocumentResponse # Removed, not used

router = APIRouter()

@router.post("/upload", status_code=201)
async def upload_document(
    file: UploadFile = File(...)
    # db: AsyncSession = Depends(get_db) # Removed
):
    """
    Endpoint to upload a document (PDF, TXT, MD, JSON) for ingestion using Weaviate.
    """
    # Extended content types to include markdown and JSON
    supported_content_types = [
        "application/pdf", 
        "text/plain", 
        "text/markdown", 
        "application/json",
        "text/json"
    ]
    
    # Check if the content type is supported or can be processed as text
    if not file.content_type in supported_content_types:
        # Allow fallback for text-like content types
        if file.content_type is None or not (
            file.content_type.startswith("text") or 
            file.filename and (
                file.filename.endswith(".md") or 
                file.filename.endswith(".json") or
                file.filename.endswith(".txt")
            )
        ):
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type: {file.content_type}. Supported types: PDF, TXT, MD, JSON."
            )
    
    try:
        print(f"Received file for upload: {file.filename}")
        doc_ids = await ingestion_service.process_file(file) # Removed db argument
        if not doc_ids:
            # This could happen if the file was empty or text extraction failed
            raise HTTPException(
                status_code=400,
                detail=f"Could not extract text or process file: {file.filename}"
            )
        print(f"File processed successfully: {file.filename}, {len(doc_ids)} chunks stored.")
        # Return the number of chunks created or their IDs
        return {"filename": file.filename, "message": f"{len(doc_ids)} chunks ingested successfully.", "doc_ids": doc_ids}
    except ValueError as ve:
        # Catch specific errors like unsupported file type from the service
        raise HTTPException(status_code=400, detail=str(ve))
    except ConnectionError as ce: # Added to catch Weaviate connection issues
        print(f"Connection error during file upload processing: {ce}")
        raise HTTPException(status_code=503, detail=f"Service unavailable: Could not connect to Weaviate. {ce}")
    except Exception as e:
        print(f"Error during file upload processing: {e}")
        # Log the full error details here in a real application
        raise HTTPException(status_code=500, detail=f"Internal server error processing file: {e}")

@router.post("/upload-batch", status_code=201)
async def upload_multiple_documents(
    files: List[UploadFile] = File(...)
    # db: AsyncSession = Depends(get_db) # Removed
):
    """
    Endpoint to upload multiple documents (PDF, TXT, MD, JSON) for batch ingestion using Weaviate.
    """
    if not files or len(files) == 0:
        raise HTTPException(
            status_code=400,
            detail="No files provided for upload"
        )
    
    results = []
    errors = []
    total_chunks = 0
    
    # Process each file in the batch
    for file in files:
        print(f"Attempting to process in batch: {file.filename}, content_type: {file.content_type}")
        try:
            # Extended content types to include markdown and JSON
            supported_content_types = [
                "application/pdf", 
                "text/plain", 
                "text/markdown", 
                "application/json",
                "text/json"
            ]
            
            # Check content type or file extension
            is_supported = (
                file.content_type in supported_content_types or
                file.content_type and file.content_type.startswith("text") or
                file.filename and (
                    file.filename.endswith(".pdf") or
                    file.filename.endswith(".txt") or
                    file.filename.endswith(".md") or
                    file.filename.endswith(".json")
                )
            )
            
            if not is_supported:
                errors.append({
                    "filename": file.filename,
                    "error": f"Unsupported file type: {file.content_type}"
                })
                continue
                
            # Process file
            doc_ids = await ingestion_service.process_file(file) # Removed db argument
            
            if not doc_ids:
                errors.append({
                    "filename": file.filename,
                    "error": "Could not extract text or process file"
                })
            else:
                results.append({
                    "filename": file.filename,
                    "chunks": len(doc_ids),
                    "doc_ids": doc_ids
                })
                total_chunks += len(doc_ids)
                print(f"File processed successfully: {file.filename}, {len(doc_ids)} chunks stored.")
        
        except Exception as e:
            print(f"Error processing file {file.filename}: {e}")
            errors.append({
                "filename": file.filename,
                "error": str(e)
            })
    
    # Return results summary
    return {
        "message": f"Batch processing complete. {len(results)} files processed successfully, {len(errors)} failed. {total_chunks} total chunks ingested.",
        "successful_files": results,
        "failed_files": errors
    }
