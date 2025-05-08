# API Documentation

This document provides details about the JARVIS 2.0 API endpoints and their usage.

## Base URL

When running locally, the base URL is: `http://localhost:8000`

## Authentication

The current demo implementation does not include authentication. In a production environment, you would want to add proper authentication mechanisms.

## Endpoints

### Document Ingestion

#### Upload Document

- **URL**: `/api/ingest/upload`
- **Method**: `POST`
- **Content-Type**: `multipart/form-data`
- **Parameters**:
  - `file`: The document file to upload (PDF or TXT)
- **Response**:
  - `200 OK`: Document successfully processed
  - `400 Bad Request`: Invalid file format or content
  - `500 Internal Server Error`: Processing error

Example response:
```json
{
  "message": "Document processed successfully",
  "chunks_count": 5,
  "document_ids": ["uuid1", "uuid2", "uuid3", "uuid4", "uuid5"]
}
```

### Querying

#### Ask Question

- **URL**: `/api/query/ask`
- **Method**: `POST`
- **Content-Type**: `application/json`
- **Request Body**:
  ```json
  {
    "question": "What is the capital of France?"
  }
  ```
- **Response**:
  - `200 OK`: Question answered successfully
  - `500 Internal Server Error`: Processing error

Example response:
```json
{
  "answer": "The capital of France is Paris.",
  "sources": [
    {
      "id": "uuid1",
      "content": "Paris is the capital and most populous city of France.",
      "doc_metadata": {
        "source": "geography.txt",
        "chunk_index": 3
      }
    }
  ]
}
```

## Error Handling

All endpoints return appropriate HTTP status codes:

- `400 Bad Request`: Invalid input or parameters
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server-side error

Error responses include a detail message:

```json
{
  "detail": "Error message describing what went wrong"
}
```

## Rate Limiting

The current implementation does not include rate limiting. In a production environment, you would want to add rate limiting to prevent abuse.

## Data Models

### Document

```json
{
  "id": "uuid",
  "content": "Text content of the document chunk",
  "doc_metadata": {
    "source": "filename.txt",
    "chunk_index": 0
  }
}
```

### Query

```json
{
  "question": "What is the capital of France?"
}
```

### Response

```json
{
  "answer": "The capital of France is Paris.",
  "sources": [
    {
      "id": "uuid",
      "content": "Text content of the source document",
      "doc_metadata": {
        "source": "filename.txt",
        "chunk_index": 0
      }
    }
  ]
}
```
