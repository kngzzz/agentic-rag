from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from backend.api.routers import ingest, query
# from backend.core.database import init_db # Removed
from backend.core.config import settings # Import settings to ensure env vars are loaded
from backend.core.weaviate_manager import get_weaviate_client, ensure_schema_exists # Added for startup schema check

app = FastAPI(title="JARVIS Demo API")

# CORS Middleware (adjust origins as needed for your frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows all origins for demo purposes
    allow_credentials=True,
    allow_methods=["*"], # Allows all methods
    allow_headers=["*"], # Allows all headers
)

@app.on_event("startup")
async def on_startup():
    print("Application startup...")
    print(f"Using OpenAI API Key: {'********' + settings.OPENAI_API_KEY[-4:] if settings.OPENAI_API_KEY else 'Not Set'}")
    print(f"Weaviate URL: {settings.WEAVIATE_URL}")
    print(f"Weaviate Index Name: {settings.WEAVIATE_INDEX_NAME}")
    
    try:
        client = None # Initialize client to None
        print("Ensuring Weaviate schema exists...")
        client = get_weaviate_client()
        ensure_schema_exists(client)
        print("Weaviate schema check complete.")
    except Exception as e:
        print(f"Error during Weaviate schema initialization: {e}")
        # Depending on severity, you might want to raise an error or prevent app startup
    finally:
        if client:
            client.close() # Close client if it was opened

# Include routers
app.include_router(ingest.router, prefix="/api/ingest", tags=["Ingestion"])
app.include_router(query.router, prefix="/api/query", tags=["Query"])

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the JARVIS Demo API"}

# Optional: Add entry point for running with uvicorn directly
# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
