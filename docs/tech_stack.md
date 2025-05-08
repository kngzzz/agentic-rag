# JARVIS 2.0 - Technology Stack Architecture

documentId: "TECH-JARVIS-2.0-20250508" # Updated Date
projectName: "JARVIS 2.0 - Advanced Agentic RAG Personal Assistant"
version: "1.1.0" # Incremented version due to significant architecture change
date: "2025-05-08" # Updated Date
status: "Active" # Changed from Draft
relatedDocs: ["PRD-JARVIS-2.0-20250505", "FSD-JARVIS-2.0-20250505", "DESIGN.MD"]

---

# 1. Technology Stack Overview

## 1.1 Core Technologies

### Programming Languages
- **Python 3.11+**: Primary backend language
  - Strong typing with type hints
  - Asyncio for concurrent operations
- **TypeScript 5.0+**: Frontend and tooling
  - Static typing for improved maintainability
  - Modern ECMAScript features

### Core Frameworks & Libraries

#### Backend
- **FastAPI 0.111+**: API framework
  - High performance, async-native
  - Automatic OpenAPI documentation
  - Type validation and coercion

- **LangChain 0.2+**: AI orchestration
  - Modular components for RAG pipelines
  - Agent frameworks
  - Tool integration

- **Weaviate Client (`weaviate-client`)**: Python client for Weaviate
  - Used for all interactions with the Weaviate vector database.
  - Replaces SQLAlchemy for core RAG data operations.

#### Frontend
- **React 19+**: UI library (Assumption, based on project structure)
  - Server and client components
  - Suspense and concurrent features

- **TanStack Query 5+ / Axios / Fetch**: Data fetching (Assumption, based on project structure)
  - Caching and synchronization
  - Optimistic updates
  - Prefetching

- **Tailwind CSS 4+ / Standard CSS**: Styling (Assumption, based on project structure)
  - Utility-first approach or standard CSS files.

### Databases & Storage

- **Weaviate**: Primary vector database and data store for RAG.
  - Stores document chunks, vector embeddings, and metadata.
  - Leveraged for efficient `near_vector` search.
  - Schema managed by `backend/core/weaviate_manager.py`.

- **Redis 7+ (Optional)**: Caching and job queue
  - In-memory performance
  - Pub/sub capabilities
  - Advanced data structures

- **Neo4j 5+ (Optional)**: Knowledge graph storage
  - Native graph database
  - Cypher query language
  - Traversal optimizations

### AI & ML Components

#### Embedding Models
- **OpenAI `text-embedding-ada-002`**: Default model for text embeddings.
  - 1536-dimensional embeddings.
- **Image (Future)**: CLIP ViT-L/14 (or similar)
  - Multi-modal capabilities

#### LLM Support
- **Cloud APIs (Primary for Demo)**:
  - OpenAI (e.g., `gpt-4o`, `gpt-3.5-turbo`) - Current default.
  - Anthropic (Claude 3 Opus)
  - Google AI (Gemini Pro)
- **Local Models (Future Consideration)**:
  - Llama 3 70B
  - Mistral Large
  - Supports GGUF format (via tools like Ollama)

#### LangChain Components

| Component Type | Implementation | Purpose |
|----------------|---------------|--------|
| **Chains** | | |
| | RetrievalQA | Basic RAG for simple queries (Implicitly used or can be built upon) |
| | Custom ReAct | Current agent implementation (`agent_service.py`) for reasoning with tools. |
| **Agents** | | |
| | AgentExecutor | Orchestrates agent thinking process (`agent_service.py`). |
| | `create_react_agent` | Used to construct the ReAct agent. |
| **Tools** | | |
| | `create_retriever_tool` | Wraps the Weaviate retriever for agent use. |
| | `TavilySearchResults` | Optional web search tool. |
| **Memory** | | |
| | `ConversationBufferWindowMemory` | Short-term context for chat history. |
| **Callbacks** | | |
| | (Implied) Default LangChain logging/verbose output. | Detailed chain/agent logging. |

### Development Tools

- **Docker**: Containerization
  - Compose for development (if Weaviate is run locally via Docker)
  - Multi-stage builds (for production)

- **Dependency Management**: `requirements.txt` for pip.
  - (Poetry files `pyproject.toml`, `poetry.lock` also present, indicating potential for Poetry use).

- **ESLint/Prettier (Frontend)**: Code quality
  - Consistent style
  - Static analysis

- **GitHub Actions (Assumed/Planned)**: CI/CD
  - Automated testing
  - Deployment pipelines

- **PyTest (Assumed/Planned)**: Testing framework
  - Fixture-based testing
  - Parameterized tests

- **Playwright (Assumed/Planned Frontend)**: E2E testing
  - Cross-browser testing
  - Visual regression tests

---

# 2. Component Architecture (Simplified for RAG focus)

## 2.1 Core System

### Configuration Service
- **Implementation**: `backend/core/config.py` using Pydantic's `BaseSettings`.
- **Purpose**: Manages application settings, loads from `.env` file.
- **Key Features**: Environment-specific overrides, type validation.

## 2.2 Ingestion System

### Content Processing
- **Implementation**: `backend/services/ingestion_service.py`
- **Purpose**: Handles file uploads (PDF, TXT, JSON), parses content, chunks text, generates embeddings (via OpenAI), and stores data in Weaviate.
- **Key Features**: Batch processing for Weaviate, dynamic type handling.

## 2.3 Storage System

### Vector Database (Weaviate)
- **Implementation**: Weaviate instance (Cloud or self-hosted). Managed via `backend/core/weaviate_manager.py` and `weaviate-client`.
- **Purpose**: Stores document chunks, pre-computed vector embeddings, and metadata. Primary data source for RAG.
- **Key Features**:
  - Schema definition for "Documents" collection.
  - Vector indexing (HNSW with Cosine distance).
  - Efficient batch operations.
  - Metadata filtering capabilities (though not heavily used yet).

## 2.4 Retrieval System

### Query Processing & Hybrid Search
- **Implementation**: `backend/services/retrieval_service.py`
- **Purpose**: Generates query embeddings, performs `near_vector` search against Weaviate.
- **Key Features**:
  - Semantic similarity search.
  - Returns top_k relevant chunks with metadata and distance.

## 2.5 Agent System

### Reasoning Engine & Tool Usage
- **Implementation**: `backend/services/agent_service.py` using LangChain.
- **Purpose**: Implements a ReAct agent that uses the retrieval tool (and optionally Tavily web search) to answer questions.
- **Key Features**:
  - Thought-Action-Observation cycles.
  - Dynamic tool use based on agent's reasoning.
  - Manages conversation history.

## 2.6 Interface Systems

### API Gateway
- **Implementation**: FastAPI application in `backend/main.py`.
- **Purpose**: Exposes REST API endpoints for ingestion (`/api/ingest/upload`) and querying (`/api/query/ask`).
- **Key Features**:
  - CORS middleware.
  - Startup event for Weaviate schema check.

### Web Application (Frontend)
- **Implementation**: React/TypeScript application in `frontend/` directory.
- **Purpose**: Provides UI for file upload and chat-based Q&A.
- **Key Features**: Interacts with backend API via `apiClient.ts`.

---

# 3. Infrastructure Architecture (Conceptual)

## 3.1 Development Environment
- **Local Development**:
  - Backend (FastAPI) run via Uvicorn from project root.
  - Frontend (Vite dev server).
  - Connection to Weaviate instance (Cloud or local Docker).
  - `.env` file for managing API keys and configurations.

## 3.2 Deployment Options (Conceptual)
- **Backend**: Dockerized FastAPI application.
- **Frontend**: Static build deployed to a web server or CDN.
- **Database**: Weaviate Cloud instance or a managed/self-hosted Weaviate cluster.

---

# 4. Integration Architecture

## 4.1 External Systems Integration
- **LLM Provider Integration (OpenAI)**: Direct API calls via OpenAI Python client, integrated within LangChain components and embedding generation.
- **Weaviate Integration**: Via `weaviate-client` library for all database operations.

---

# 5. Development Guidelines

## 5.1 Coding Standards
- **Python**: PEP 8, type hints, docstrings.
- **TypeScript**: ESLint/Prettier.

## 5.2 Testing Strategy (Planned)
- **Unit Testing**: For individual functions and classes.
- **Integration Testing**: For service interactions, API endpoint validation.
- **End-to-End Testing**: For full RAG pipeline.

## 5.3 Documentation Requirements
- **Code Documentation**: Docstrings, comments.
- **API Documentation**: Auto-generated by FastAPI (Swagger/ReDoc).
- **Project Documentation**: Markdown files in `/docs` directory, including this tech stack, design, and installation guide. Memory Bank for Cline.

---

# 6. Technology Selection Rationale (Updated)

| Technology | Alternatives Considered | Selection Rationale |
|------------|-------------------------|---------------------|
| **Weaviate** | PostgreSQL+pgvector, FAISS, Pinecone, ChromaDB | Native vector database with good Python client, metadata storage, filtering capabilities, and scalability options (cloud/self-hosted). Chosen for its focus on vector search and ease of integration for RAG. |
| **FastAPI** | Flask, Django | High performance, native async support, automatic OpenAPI docs, Pydantic integration. |
| **React** | Vue, Svelte | Widespread adoption, rich ecosystem, strong typing with TypeScript. |
| **LangChain** | LlamaIndex, Custom | Comprehensive RAG and agent capabilities, active community, extensible architecture. |

---
