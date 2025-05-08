# Installation Guide

This document provides detailed instructions for setting up and running the JARVIS 2.0 demo application.

## Prerequisites

- Python 3.11+
- Node.js 18+ and npm (for frontend)
- Access to a Weaviate instance (Cloud or self-hosted)
- OpenAI API key
- Tavily API key (Optional, for web search tool)

## Backend Setup

1.  **Set up Weaviate Instance:**
    *   **Option A: Weaviate Cloud Service (WCS)**
        *   Create a free sandbox or a paid cluster on [Weaviate Cloud](https://console.weaviate.cloud/).
        *   Note your Weaviate Cluster URL and an Admin API Key for the instance.
    *   **Option B: Self-Hosted Weaviate (e.g., using Docker)**
        *   Follow the official Weaviate documentation to set up a local instance, for example, using Docker Compose:
          ```bash
          curl -o docker-compose.yml "https://configuration.weaviate.io/v2/docker-compose/docker-compose.yml?modules=standalone&runtime=docker-compose&weaviate_version=v1.24.1" # Or latest
          docker-compose up -d
          ```
        *   The default local URL is typically `http://localhost:8080`. No API key is needed by default for local unauthenticated instances.

2.  **Clone the Repository (if not already done):**
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

3.  **Set up Python Virtual Environment:**
    Navigate to the `backend` directory:
    ```bash
    cd backend
    ```
    Create and activate a virtual environment:
    ```bash
    python -m venv env
    # On Windows
    .\env\Scripts\activate
    # On macOS/Linux
    source env/bin/activate
    ```

4.  **Install Backend Dependencies:**
    While still in the `backend` directory with the virtual environment activated:
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: `pyproject.toml` and `poetry.lock` exist, suggesting Poetry was used previously. If you prefer Poetry, you can use `poetry install` after ensuring Poetry is installed.)*

5.  **Configure Environment Variables:**
    Create a `.env` file in the `backend` directory (`c:/projects/jarvis/backend/.env`) with the following content. **Adjust values based on your setup, especially for Weaviate.**

    ```env
    OPENAI_API_KEY="your_openai_api_key_here"
    
    # --- Weaviate Settings ---
    # For Weaviate Cloud Service (WCS):
    WEAVIATE_URL="your_wcs_cluster_url_e.g_https_yourcluster.c0.region.gcp.weaviate.cloud"
    WEAVIATE_API_KEY="your_wcs_instance_admin_api_key" 
    # For local Docker Weaviate (default, unauthenticated):
    # WEAVIATE_URL="http://localhost:8080"
    # WEAVIATE_API_KEY="" # Leave blank or omit if no auth for local
    
    WEAVIATE_INDEX_NAME="Documents" # Default collection name
    WEAVIATE_GRPC_ENABLED="True" # Or "False"

    # --- LLM and Embedding Models ---
    EMBEDDING_MODEL="text-embedding-ada-002"
    LLM_MODEL="gpt-4o" # Or another model like gpt-3.5-turbo
    EMBEDDING_DIM="1536"

    # --- Optional: Tavily Search API Key (for web search tool) ---
    TAVILY_API_KEY="your_tavily_api_key_here" # If you want to use the Tavily search tool

    # --- Deprecated/Unused Variables (can be removed or left commented) ---
    # DATABASE_URL="postgresql+asyncpg://user:pass@host:port/db" # No longer used for core RAG
    ```
    **Important:**
    *   Replace placeholder values with your actual keys and URLs.
    *   If using a local Weaviate instance without authentication, `WEAVIATE_API_KEY` can be empty or the line omitted (the application code should handle `Optional[str]`).
    *   The `DATABASE_URL` for PostgreSQL is no longer used by the core RAG system but might be present from previous setups.

6.  **Run the Backend Server:**
    Navigate to the project root directory (`c:/projects/jarvis/`):
    ```bash
    cd .. 
    ```
    Then run the Uvicorn server (ensure your backend virtual environment is active):
    ```bash
    # If your venv is c:/projects/jarvis/backend/env/
    .\backend\env\Scripts\python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
    # Or, if python command correctly points to venv's python:
    # python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
    ```
    The server should start on `http://127.0.0.1:8000`.

## Frontend Setup

1.  **Navigate to Frontend Directory:**
    ```bash
    cd frontend
    ```

2.  **Install Frontend Dependencies:**
    ```bash
    npm install
    ```

3.  **Configure API Endpoint (if necessary):**
    The frontend is likely configured to connect to `http://localhost:8000` or `http://127.0.0.1:8000`. If your backend is running on a different host or port (e.g., in a Docker container with port mapping), update the API endpoint in `frontend/src/apiClient.ts` or relevant configuration files.

4.  **Run Development Server:**
    ```bash
    npm run dev
    ```
    This will typically start the frontend on `http://localhost:5173` (Vite's default).

5.  **Build for Production:**
    ```bash
    npm run build
    ```
    This creates a `dist` folder with static assets for deployment.

## Troubleshooting

-   **Weaviate Connection Issues**:
    *   Verify your Weaviate instance is running and accessible.
    *   Double-check `WEAVIATE_URL` and `WEAVIATE_API_KEY` in `backend/.env`.
    *   Ensure network connectivity (firewalls, Docker networking if applicable).
-   **OpenAI/Tavily API Errors**: Ensure your API keys are valid, correctly set in `backend/.env`, and have sufficient quota.
-   **Python Import Errors**: Ensure you are running the backend server from the project root directory (`c:/projects/jarvis/`) and that your virtual environment is activated.
-   **Large File Uploads**: The system processes embeddings in batches. However, very large files might still encounter server timeouts or memory issues depending on the deployment environment.

## Production Deployment Considerations

For production deployment:

1.  Set up a robust Weaviate instance (Cloud or a well-maintained self-hosted cluster).
2.  Deploy the backend (FastAPI application) to a suitable server environment (e.g., Docker container on a cloud platform like Google Cloud Run, AWS ECS, Azure App Service).
3.  Build the frontend (`npm run build`) and deploy the static assets from the `dist` folder to a static hosting service (e.g., Vercel, Netlify, AWS S3+CloudFront, Google Cloud Storage).
4.  Configure CORS settings in the backend (`backend/main.py`) to allow requests from your frontend's production domain.
5.  Ensure all environment variables (API keys, Weaviate URL) are securely managed in the production backend environment.
