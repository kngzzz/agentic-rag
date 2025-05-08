# JARVIS - Agentic RAG

An AI-powered personal assistant leveraging Retrieval Augmented Generation (RAG) and agentic capabilities for advanced knowledge management, semantic search, and task automation.

## Key Features

-   **Advanced RAG Pipeline**: Sophisticated retrieval and generation for accurate, context-aware responses.
-   **Multi-Document Support**: Ingests and processes various file types including PDF, DOCX, and PPTX.
-   **Semantic Search**: Leverages vector search (e.g., Weaviate) and potentially external APIs (e.g., Exa AI) for deep understanding of queries.
-   **Agentic Framework**: Capable of performing complex, multi-step tasks by composing tools and reasoning about actions.
-   **Vector Store Integration**: Utilizes Weaviate for efficient storage and retrieval of embeddings.
-   **Interactive Frontend**: User interface (potentially Streamlit or React-based) for file uploads, querying, and interacting with the assistant.
-   **Automated Ingestion**: Local folder watcher (using `watchdog`) to automatically process new or modified files.
-   **Multi-Layered Memory Architecture**: Designed with working, short-term, episodic, semantic, and procedural memory layers (conceptual).
-   **Observability**: Integrated with LangSmith for tracing and monitoring application performance and behavior.


## Tech Stack

-   **Backend**: Python (likely FastAPI or Flask)
-   **Frontend**: TypeScript, React (implied by `.tsx` files)
-   **Vector Database**: Weaviate
-   **Core AI/ML Libraries**: LangChain / LangGraph, sentence-transformers
-   **File Processing**: `python-docx`, `python-pptx`
-   **Connectors/Automation**: `watchdog`
-   **Observability**: LangSmith
-   **Development Environment**: Node.js, npm/yarn

## Getting Started

### Prerequisites

-   Python (version 3.9+ recommended)
-   Node.js and npm/yarn
-   Git
-   Access to a Weaviate instance (local or cloud)
-   API keys for any integrated services (e.g., Exa AI, LangSmith, LLM provider)

### Setup Instructions

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/kngzzz/agentic-rag.git
    cd agentic-rag
    ```

2.  **Set up Backend**:
    ```bash
    cd backend
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    pip install -r requirements.txt
    ```

3.  **Set up Frontend**:
    ```bash
    cd ../frontend
    npm install  # or yarn install
    ```

4.  **Configure Environment Variables**:
    -   Copy `.env.example` to `.env` in both the `backend` and `frontend` directories (if applicable).
    -   Fill in the required environment variables such as:
        -   `WEAVIATE_URL`
        -   `WEAVIATE_API_KEY` (if applicable)
        -   `OPENAI_API_KEY` (or other LLM provider keys)
        -   `EXA_API_KEY` (if using Exa AI)
        -   `LANGSMITH_API_KEY`
        -   Other service-specific keys.

5.  **Run the Application**:
    -   **Backend Server** (from the `backend` directory):
        ```bash
        # Example: uvicorn main:app --reload (if using FastAPI)
        python app.py # or your main backend script
        ```
    -   **Frontend Development Server** (from the `frontend` directory):
        ```bash
        npm start # or yarn start
        ```

## Project Structure (High-Level)

```
agentic-rag/
├── backend/            # Python backend (FastAPI/Flask, RAG logic, agent core)
│   ├── app/            # Core application logic
│   ├── services/       # Business logic (ingestion, query, etc.)
│   ├── models/         # Data models, Pydantic schemas
│   ├── core/           # Core components (LLM wrappers, vector store manager)
│   ├── apis/           # API endpoints
│   ├── connectors/     # Connectors to data sources (e.g., local folder watcher)
│   ├── schemas/        # Database/API schemas (like document.py)
│   └── requirements.txt
├── frontend/           # React/TypeScript frontend
│   ├── src/
│   │   ├── components/ # Reusable UI components (ChatInterface, FileUpload)
│   │   ├── App.tsx     # Main application component
│   │   └── ...
│   ├── public/
│   └── package.json
├── .gitignore
├── README.md
└── ... (config files, Dockerfile, etc.)
```

## Roadmap (Based on M1 MVP)

-   **[M1.1, M1.2]** Expand file type support (DOCX, PPTX) and improve metadata extraction.
-   **[M1.3]** Upgrade/Configure Vector Store (Weaviate).
-   **[M1.4]** Implement Local Folder Watcher Connector.
-   **[M1.5]** Develop Basic UI for Upload & Q&A.
-   **[M1.6]** Integrate Initial Observability with LangSmith.

## Contributing

Contributions are welcome! Please feel free to open an issue or submit a pull request.

(Consider adding guidelines for development, testing, and commit messages if this becomes a collaborative project).
