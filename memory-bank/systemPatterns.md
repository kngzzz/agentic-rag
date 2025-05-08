# System Patterns: JARVIS 2.0

## 1. System Architecture Overview

JARVIS 2.0 employs a client-server architecture:

*   **Backend:** A FastAPI application responsible for:
    *   API endpoints for document ingestion and querying.
    *   Core services for ingestion, retrieval, and agent-based question answering.
    *   Interaction with the Weaviate vector database.
    *   Orchestration of LLM interactions via LangChain.
*   **Vector Database:** Weaviate serves as the primary data store for document chunks, their vector embeddings, and associated metadata. It's crucial for semantic search and retrieval.
*   **Frontend:** (Details less emphasized in the current context, but implied) A user interface (likely web-based, given `frontend/` directory) for uploading documents and interacting with the Q&A system.
*   **AI/LLM Services:** Utilizes OpenAI for generating embeddings and (presumably) for the LLM powering the ReAct agent.

```mermaid
graph TD
    UserInterface[Frontend UI] -->|HTTP API Calls| BackendAPI[FastAPI Backend]

    subgraph BackendAPI
        APIRouters[API Routers (ingest.py, query.py)]
        Services[Core Services (ingestion_service, retrieval_service, agent_service)]
        WeaviateManager[Weaviate Manager (weaviate_manager.py)]
        LangChainIntegration[LangChain (ReAct Agent, Prompts)]
        OpenAIClient[OpenAI Client (Embeddings, LLM)]

        APIRouters --> Services
        Services --> WeaviateManager
        Services --> LangChainIntegration
        LangChainIntegration --> OpenAIClient
        WeaviateManager --> WeaviateDB[(Weaviate Database)]
    end

    style BackendAPI fill:#f9f,stroke:#333,stroke-width:2px
    style WeaviateDB fill:#ccf,stroke:#333,stroke-width:2px
```

## 2. Key Technical Decisions & Patterns

*   **Weaviate as Primary Datastore:**
    *   **Decision:** Shifted from potential FAISS/PostgreSQL to exclusively use Weaviate for both vector storage and metadata.
    *   **Rationale:** Simplifies the database stack, leverages Weaviate's native vector search capabilities and metadata filtering.
*   **Centralized Weaviate Client Management:**
    *   **Pattern:** The `backend/core/weaviate_manager.py` module is responsible for initializing the Weaviate client and ensuring the schema exists.
    *   **Rationale:** Promotes consistency, avoids redundant client initializations, and makes it easier to manage Weaviate configurations and schema updates. Services obtain the client via `weaviate_manager.get_weaviate_client()`.
*   **Service-Oriented Backend:**
    *   **Pattern:** Backend logic is organized into distinct services:
        *   `ingestion_service.py`: Handles file processing, chunking, embedding generation, and storage in Weaviate.
        *   `retrieval_service.py`: Finds relevant document chunks from Weaviate based on query embeddings.
        *   `agent_service.py`: Orchestrates the ReAct agent, using retrieved chunks to generate answers.
    *   **Rationale:** Improves modularity, separation of concerns, and testability.
*   **FastAPI for Asynchronous Operations:**
    *   **Pattern:** FastAPI is used for its asynchronous capabilities, suitable for I/O-bound operations like interacting with Weaviate and external LLM APIs.
    *   **Rationale:** Enhances performance and responsiveness.
*   **LangChain for AI Orchestration:**
    *   **Pattern:** LangChain is used to implement the ReAct agent, manage prompts, and interact with LLMs and tools (like the retrieval service).
    *   **Rationale:** Provides a robust framework for building LLM-powered applications, simplifying complex agent logic.
*   **Direct Weaviate Client Usage in Services:**
    *   **Decision:** Refactored away from a `WeaviateDBService` abstraction. Services now directly use the Weaviate client (e.g., `client.collections.get(INDEX_NAME).batch.dynamic()` for ingestion, `client.collections.get(INDEX_NAME).query.near_vector()` for retrieval).
    *   **Rationale:** Reduces an unnecessary layer of abstraction, giving services more direct control and potentially better performance by using Weaviate's native Python client features.
*   **Data Model for Weaviate:**
    *   **Pattern:** Data is prepared as dictionaries for insertion into Weaviate. The `backend/models/document.py` `Document` class is likely no longer central to the Weaviate storage flow, as Weaviate's Python client works directly with dictionaries.
    *   **Rationale:** Aligns with Weaviate's data input requirements.

## 3. Component Relationships & Critical Paths

*   **Ingestion Path:**
    1.  File uploaded via `ingest.py` API endpoint.
    2.  `ingestion_service.process_file` is called.
    3.  File is read, chunked, and embeddings are generated (likely via OpenAI).
    4.  `weaviate_manager.get_weaviate_client()` provides the client.
    5.  Data (chunks, embeddings, metadata) is batch-inserted into Weaviate as dictionaries.
*   **Querying Path:**
    1.  Question submitted via `query.py` API endpoint.
    2.  `agent_service.answer_question` is called.
    3.  `retrieval_service.find_relevant_chunks` is called:
        *   Query is embedded (likely via OpenAI).
        *   `weaviate_manager.get_weaviate_client()` provides the client.
        *   `near_vector` search is performed in Weaviate.
        *   Relevant chunks (as dictionaries) are returned.
    4.  `agent_service` uses the retrieved chunks and LangChain (ReAct agent, LLM) to formulate an answer.
    5.  Answer, sources, and thought process are returned.

## 4. Deprecated Patterns

*   **`WeaviateDBService` Abstraction:** The class in `backend/core/database.py` and the associated `get_db` dependency injection for FastAPI routes have been removed.
*   **FAISS/PostgreSQL Usage:** Any previous considerations or implementations related to FAISS or PostgreSQL for vector storage have been superseded by Weaviate.

This document provides a snapshot of the system's internal workings and design choices, crucial for understanding how components interact and how to approach future development.
