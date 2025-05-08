# Technical Context: JARVIS 2.0

## 1. Core Technologies

*   **Backend Framework:** FastAPI
    *   Chosen for its high performance, asynchronous support, and Python type hints for data validation.
*   **Vector Database:** Weaviate
    *   Serves as the primary data store for document chunks, embeddings, and metadata.
    *   Utilized for its efficient vector search (`near_vector`) and metadata filtering capabilities.
    *   Interacted with via the `weaviate-client` Python library.
*   **AI Orchestration:** LangChain
    *   Used for building and managing the ReAct (Reason+Act) agent.
    *   Handles prompt templating, LLM interactions, and tool integration for the agent.
*   **Embedding Model:** OpenAI Embeddings
    *   Used to generate vector representations of text chunks for semantic search.
    *   Accessed via an OpenAI API client.
*   **Language Model (LLM):** OpenAI (assumed, for ReAct agent)
    *   The LLM that powers the ReAct agent's reasoning and answer generation capabilities.
    *   Accessed via an OpenAI API client.
*   **Programming Language:** Python
    *   Primary language for the backend development.

## 2. Development Setup & Environment

*   **Configuration:**
    *   `backend/core/config.py`: Manages application settings, including Weaviate connection details (URL, API key, index name) and OpenAI API key.
    *   `.env` file: Likely used to store sensitive credentials like API keys, loaded by `config.py`.
*   **Weaviate Client Initialization:**
    *   Managed by `backend/core/weaviate_manager.py`. This module handles:
        *   Creating the Weaviate client instance.
        *   Ensuring the required Weaviate schema (collection) exists.
*   **Dependencies:**
    *   Managed via `backend/requirements.txt` (and potentially `poetry.lock` / `pyproject.toml` if Poetry is fully adopted).
    *   Key Python libraries:
        *   `fastapi`
        *   `uvicorn` (for running FastAPI)
        *   `weaviate-client`
        *   `langchain`
        *   `openai`
        *   `python-dotenv` (for loading `.env` files)
        *   `tiktoken` (often used with LangChain/OpenAI for token counting)
*   **Frontend Stack (Inferred from file structure):**
    *   TypeScript
    *   React (based on `react.svg`, `App.tsx`)
    *   Vite (build tool, based on `vite.config.ts`)
    *   `apiClient.ts` suggests a dedicated module for frontend-backend communication.

## 3. Technical Constraints & Considerations

*   **Async Operations:** The backend heavily relies on Python's `async` and `await` for non-blocking I/O, especially when dealing with Weaviate and OpenAI API calls.
*   **Weaviate Schema:** The structure of the data stored in Weaviate (properties, vectorizer configuration) is defined and managed, likely within `weaviate_manager.py` or through initial setup scripts. The current schema supports storing text chunks, their embeddings, and associated metadata (e.g., source document ID, chunk ID).
*   **Data Flow for Weaviate:**
    *   **Ingestion:** Python dictionaries are used to represent objects for batch insertion into Weaviate.
    *   **Retrieval:** Query results from Weaviate are also typically returned as lists of dictionaries or Weaviate-specific object types that can be easily converted to dictionaries.
*   **Modularity:** The recent refactoring aimed to improve modularity by ensuring services directly use the Weaviate client from the `weaviate_manager`, rather than relying on a shared database session or an intermediate service class.
*   **Error Handling:** Robust error handling will be important, especially for external API calls (OpenAI, Weaviate if run as a separate service) and file processing.
*   **Security:** API authentication is a planned feature, indicating current endpoints might be unauthenticated. Storing API keys and sensitive data securely (e.g., via `.env` and proper configuration management) is crucial.

## 4. Tool Usage Patterns

*   **Weaviate Client:**
    *   `weaviate.Client()`: For initialization.
    *   `client.collections.get(COLLECTION_NAME)`: To get a reference to a collection.
    *   `collection.batch.dynamic()`: For efficient batch data insertion.
    *   `collection.query.near_vector()`: For performing semantic vector searches.
    *   `collection.schema.exists()` / `client.collections.create()`: For schema management.
*   **LangChain:**
    *   `PromptTemplate`: For creating and managing prompts for the ReAct agent.
    *   `create_react_agent`: To construct the agent.
    *   `AgentExecutor`: To run the agent with queries and tools.
    *   Tools: Custom tools (like the retrieval service) are integrated into the agent.
*   **OpenAI Client:**
    *   Used for generating embeddings and interacting with the LLM.

This document provides the technical underpinnings necessary to understand the tools, libraries, and environment of JARVIS 2.0.
