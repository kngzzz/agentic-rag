# Project Brief: JARVIS 2.0

## 1. Overview

JARVIS 2.0 is a Retrieval Augmented Generation (RAG) application designed to answer questions based on a corpus of ingested documents. The backend is built with FastAPI, and the primary data store and vector database is Weaviate. LangChain is utilized for AI orchestration, particularly for the ReAct agent responsible for question answering.

## 2. Core Requirements

*   **Data Ingestion:** The system must be able to ingest various file formats (initially text-based, with plans to expand to JSON and other types), process them into manageable chunks, generate embeddings (using OpenAI), and store them in Weaviate.
*   **Data Retrieval:** The system must efficiently retrieve relevant document chunks from Weaviate based on semantic similarity to a user's query.
*   **Question Answering:** The system must use a ReAct agent (LangChain) to synthesize answers from retrieved chunks and provide them to the user, along with source information.
*   **Scalability & Maintainability:** The architecture should be modular and allow for future expansion and easy maintenance. The recent refactoring to centralize Weaviate client management via `backend/core/weaviate_manager.py` supports this.

## 3. Current State (as of May 2025)

*   The backend has been refactored to consistently use Weaviate as the sole vector database and primary data store, removing previous abstractions and remnants of other database considerations (FAISS, PostgreSQL).
*   Services (`ingestion_service.py`, `retrieval_service.py`, `agent_service.py`) and API routers (`ingest.py`, `query.py`) now directly utilize a Weaviate client obtained from `backend/core/weaviate_manager.py`.
*   The `WeaviateDBService` abstraction layer in `backend/core/database.py` has been deprecated.

## 4. High-Level Goals & Next Steps

The immediate focus after the Weaviate refactoring includes:

1.  **Testing:** Thoroughly test the end-to-end ingestion and querying functionality to ensure the Weaviate integration is working correctly.
2.  **Documentation Update:** Update all relevant project documentation (`DESIGN.MD`, `INSTALLATION.MD`, `tech_stack.md`, and internal Memory Bank files) to reflect the Weaviate-centric architecture.
3.  **New Feature Development:**
    *   Implement robust ingestion for `.json` files, particularly those exported from AI platforms (e.g., ChatGPT, Claude).
    *   Expand support for other content ingestion types.
    *   Implement API authentication.
    *   Add support for local LLM configurations.
    *   Enhance agent capabilities (e.g., explainability, confidence scores).
    *   Improve UI/UX.

This document serves as the foundational understanding for all subsequent Memory Bank files and development efforts.
