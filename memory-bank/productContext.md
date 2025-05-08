# Product Context: JARVIS 2.0

## 1. Purpose & Vision

JARVIS 2.0 aims to be an intelligent assistant capable of understanding and responding to queries by leveraging a knowledge base built from various ingested documents. The vision is to provide users with accurate, context-aware answers, supported by verifiable sources from the ingested data. It's designed to be a flexible RAG (Retrieval Augmented Generation) system that can adapt to different types of information and user needs.

## 2. Problem Solved

Many individuals and organizations possess large volumes of information in documents (text files, PDFs, potentially emails, chat logs, etc.). Accessing specific information within this corpus can be time-consuming and inefficient. JARVIS 2.0 addresses this by:

*   **Centralizing Knowledge:** Providing a single point of access to a diverse set of documents.
*   **Semantic Search:** Enabling users to find relevant information not just by keywords, but by the meaning and context of their queries.
*   **Synthesized Answers:** Offering direct answers to questions, rather than just a list of potentially relevant documents, by using an LLM to process retrieved information.
*   **Reducing Information Overload:** Helping users quickly get to the core information they need without manually sifting through numerous files.

## 3. How It Should Work (User Experience Goals)

*   **Simple Ingestion:** Users should be able to easily upload documents through a straightforward interface or API. The system should handle the backend processing (chunking, embedding, storing) transparently.
*   **Intuitive Querying:** Users should be able to ask questions in natural language.
*   **Clear & Actionable Results:** The system should provide:
    *   A direct answer to the question.
    *   Clear references to the source documents (and specific chunks) used to generate the answer, allowing users to verify information and explore further.
    *   (Future) Indication of the agent's thought process or confidence in the answer.
*   **Responsive Performance:** Both ingestion and querying should be performed within a reasonable timeframe.
*   **Reliability:** The system should consistently provide relevant and accurate information based on its knowledge base.
*   **Extensibility:** The system is envisioned to grow in terms of supported file types, integration with other AI models/tools, and advanced features like API authentication and local LLM support.

## 4. Target Users (Implicit)

While not explicitly defined, the system appears targeted towards users who need to:
*   Quickly find information within a collection of documents.
*   Understand complex topics by asking questions against a curated knowledge base.
*   Researchers, analysts, students, or any knowledge worker dealing with significant amounts of textual data.

This document, in conjunction with `projectbrief.md`, helps define the "what" and "why" of JARVIS 2.0.
