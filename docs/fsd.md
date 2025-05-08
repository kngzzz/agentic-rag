# JARVIS 2.0 u2013 Functional Specification Document

documentId: "FSD-JARVIS-2.0-20250505"
projectName: "JARVIS 2.0 u2013 Advanced Agentic RAG Personal Assistant"
version: "1.0.0"
date: "2025-05-05"
status: "Draft"
relatedDocs: "PRD-JARVIS-2.0-20250505"

---

# 1. System Overview

## 1.1 Purpose and Scope

This Functional Specification Document (FSD) provides a detailed technical description of the JARVIS 2.0 system, an advanced personal knowledge management platform built on Retrieval-Augmented Generation (RAG) with agentic capabilities. This document serves as the bridge between the Product Requirements Document (PRD) and the technical implementation, providing engineers with sufficient detail to build the system.

## 1.2 System Architecture Overview

```
+----------------------------------+
|           User Interfaces        |
|   +------------+  +----------+   |
|   |    CLI     |  |   Web    |   |
|   +------------+  +----------+   |
+----------------------------------+
              |
              v
+----------------------------------+
|           API Gateway            |
+----------------------------------+
              |
              v
+------------------+------------------+------------------+
|                  |                  |                  |
 v                  v                  v                  v
+------------+    +------------+    +------------+    +------------+
| Ingestion  |    | Retrieval  |    |   Agent    |    |  Memory    |
|  System    |<-->|  System    |<-->|  System    |<-->|  System    |
+------------+    +------------+    +------------+    +------------+
      |                 |                 |                 |
      v                 v                 v                 v
+----------------------------------+    +------------------+
|        Storage System           |    |  Plugin System   |
| +------------+ +-------------+  |    +------------------+
| |   Vector   | | Knowledge   |  |
| |   Store    | |   Graph     |  |
| +------------+ +-------------+  |
+----------------------------------+
```

## 1.3 Key User Journeys

1. **Content Ingestion Journey**: User uploads export files from various platforms and monitors processing
2. **Knowledge Retrieval Journey**: User searches for information across their knowledge base
3. **Complex Query Journey**: User asks questions requiring multi-step reasoning
4. **Knowledge Management Journey**: User reviews and refines automatically extracted memories
5. **Collaboration Journey**: User shares specific knowledge with team members

## 1.4 Core Workflow Sequences

### 1.4.1 Ingestion → Storage → Memory Extraction Workflow

```
User                  Ingestion System             Storage System             Memory System
 |                          |                            |                           |
 |  Upload content          |                            |                           |
 |------------------------->|                            |                           |
 |                          |                            |                           |
 |                          | Parse content              |                            |
 |                          |------------------------    |                           |
 |                          |                       |   |                           |
 |                          |<-----------------------    |                           |
 |                          |                            |                           |
 |                          | Extract metadata          |                           |
 |                          |------------------------    |                           |
 |                          |                       |   |                           |
 |                          |<-----------------------    |                           |
 |                          |                            |                           |
 |                          | Generate chunks           |                           |
 |                          |------------------------    |                           |
 |                          |                       |   |                           |
 |                          |<-----------------------    |                           |
 |                          |                            |                           |
 |                          | Create embeddings         |                           |
 |                          |------------------------    |                           |
 |                          |                       |   |                           |
 |                          |<-----------------------    |                           |
 |                          |                            |                           |
 |                          | Store chunks/embeddings   |                           |
 |                          |--------------------------->|                           |
 |                          |                            |                           |
 |                          |                            | Store in vector DB       |
 |                          |                            |------------------------   |
 |                          |                            |                       |   |
 |                          |                            |<-----------------------   |
 |                          |                            |                           |
 |                          |                            | Trigger memory extraction |
 |                          |                            |-------------------------->|
 |                          |                            |                           |
 |                          |                            |                           | Extract entities
 |                          |                            |                           |----------------|
 |                          |                            |                           |              |
 |                          |                            |                           |<--------------|
 |                          |                            |                           |
 |                          |                            |                           | Extract relations
 |                          |                            |                           |----------------|
 |                          |                            |                           |              |
 |                          |                            |                           |<--------------|
 |                          |                            |                           |
 |                          |                            |                           | Check for contradictions
 |                          |                            |                           |-------------------|
 |                          |                            |                           |                  |
 |                          |                            |                           |<-----------------|
 |                          |                            |                           |
 |                          |                            |                           | Store in knowledge graph
 |                          |                            |                           |-------------------|
 |                          |                            |                           |                  |
 |                          |                            |                           |<-----------------|
 |                          |                            |                           |
 | Notification complete    |                            |                           |
 |<------------------------------------------------------------------------------------|

```

### 1.4.2 Agent ReAct Loop with Retrieval

```
User               Agent System              Retrieval System            Storage System
 |                      |                           |                           |
 | Complex Query        |                           |                           |
 |--------------------->|                           |                           |
 |                      |                           |                           |
 |                      | Parse query and plan      |                           |
 |                      |------------------        |                           |
 |                      |                   |      |                           |
 |                      |<-----------------       |                           |
 |                      |                           |                           |
 |                      | Generate subqueries       |                           |
 |                      |------------------        |                           |
 |                      |                   |      |                           |
 |                      |<-----------------       |                           |
 |                      |                           |                           |
 |                      | Execute retrieval tool    |                           |
 |                      |-------------------------->|                           |
 |                      |                           |                           |
 |                      |                           | Generate embedding        |
 |                      |                           |------------------        |
 |                      |                           |                   |      |
 |                      |                           |<-----------------       |
 |                      |                           |                           |
 |                      |                           | Query vector store       |
 |                      |                           |------------------------->|
 |                      |                           |                           |
 |                      |                           |                           | Execute search
 |                      |                           |                           |--------------|
 |                      |                           |                           |             |
 |                      |                           |                           |<-------------|
 |                      |                           |                           |
 |                      |                           | Apply MMR                |
 |                      |                           |------------------        |
 |                      |                           |                   |      |
 |                      |                           |<-----------------       |
 |                      |                           |                           |
 |                      |                           | Return relevant chunks   |
 |                      |<--------------------------|                           |
 |                      |                           |                           |
 |                      | Analyze and synthesize    |                           |
 |                      |------------------        |                           |
 |                      |                   |      |                           |
 |                      |<-----------------       |                           |
 |                      |                           |                           |
 |                      | Generate final answer     |                           |
 |                      |------------------        |                           |
 |                      |                   |      |                           |
 |                      |<-----------------       |                           |
 |                      |                           |                           |
 | Return answer        |                           |                           |
 |<---------------------|                           |                           |
 |                      |                           |                           |
```

# 2. Detailed Functional Requirements

## 2.1 Ingestion System

### 2.1.1 Multi-Format Parser Framework

The ingestion system must support multiple content types through a pluggable parser architecture:

- **ChatGPT Export Parser**
  - Support for both ZIP archives and JSON files
  - Preserve all metadata (timestamps, conversation titles, etc.)
  - Maintain thread structure and user/assistant roles

- **Claude Export Parser**
  - Support for Claude's export format
  - Proper handling of tool use and citations

- **Bard/Gemini Parser**
  - Support for Google's AI platform exports

- **PDF Parser**
  - Extract text with layout preservation
  - OCR for scanned documents
  - Handle tables and structured content
  - Extract images for separate processing

- **Image Parser**
  - Extract text via OCR
  - Generate image descriptions
  - Extract metadata (EXIF, etc.)

- **Web Content Parser**
  - Extract main content from saved web pages
  - Preserve link structure
  - Handle embedded media

### 2.1.2 Chunking Strategy Manager

- **Adaptive Chunking**
  - Content-aware chunk boundaries (paragraphs, sections)
  - Variable chunk size based on content semantic density
  - Configurable overlap between chunks

- **Hierarchical Chunking**
  - Generate both document-level, section-level, and paragraph-level chunks
  - Maintain parent-child relationships between chunks

- **Special Content Handling**
  - Code block preservation
  - Table integrity maintenance
  - List structure preservation

### 2.1.3 Metadata Extraction System

- **Source Attribution**
  - Original platform/document
  - Creation and modification dates
  - Author information when available

- **Content Classification**
  - Automatic topic detection
  - Language identification
  - Content type classification

- **Entity Recognition**
  - People, organizations, locations
  - Technical terms and concepts
  - Dates and numerical data

### 2.1.4 Processing Pipeline Manager

- **Job Scheduling**
  - Priority-based processing queue
  - Resource throttling to prevent system overload
  - Background processing for large imports

- **Progress Tracking**
  - Real-time progress updates
  - Detailed logging of processing steps
  - Error handling with recovery options

- **Batch Processing**
  - Support for bulk imports
  - Deduplication across import sessions
  - Incremental updates for existing content

## 2.2 Storage System

### 2.2.1 Database Schema

- **Core Entities**
  - Sources (original documents/conversations)
  - Chunks (text segments with embeddings)
  - Entities (extracted concepts, people, etc.)
  - Facts (extracted knowledge statements)
  - Relations (connections between entities)
  - Tags (user and auto-generated)

- **Relationships**
  - Source-to-chunks (one-to-many)
  - Chunk-to-entities (many-to-many)
  - Entity-to-facts (many-to-many)
  - Entity-to-entity via relations (many-to-many)

- **Metadata Fields**
  - Creation, modification timestamps
  - Confidence scores
  - User feedback metrics
  - Privacy settings

### 2.2.2 Vector Store Implementation

- **Multiple Index Support**
  - HNSW for speed optimization
  - IVFFlat for storage optimization
  - Configurable based on deployment needs

- **Hybrid Search Capabilities**
  - Combined vector and keyword indices
  - Metadata filtering integration
  - Score normalization and combination

- **Performance Optimizations**
  - Chunked vector loading
  - Batch query processing
  - Query result caching

### 2.2.3 Knowledge Graph Store

- **Triple Store Design**
  - Subject-Predicate-Object structure
  - Support for advanced queries
  - Temporal versioning of facts

- **Inference Rules**
  - Basic transitive reasoning
  - Contradiction detection
  - Confidence propagation

- **Graph Traversal**
  - Path-finding algorithms
  - Centrality calculations
  - Sub-graph extraction

#### Knowledge Graph Data Model

```
+----------------+       +----------------+       +----------------+
|     Entity     |       |    Relation    |       |     Entity     |
+----------------+       +----------------+       +----------------+
| id: UUID       |       | id: UUID       |       | id: UUID       |
| type: String   |<----->| type: String   |<----->| type: String   |
| name: String   |       | confidence: Float|      | name: String   |
| aliases: [String]|      | provenance: UUID|     | aliases: [String]|
| created: Datetime|      | created: Datetime|     | created: Datetime|
| updated: Datetime|      | updated: Datetime|     | updated: Datetime|
| metadata: JSON |       | metadata: JSON |       | metadata: JSON |
+----------------+       +----------------+       +----------------+
         ^                       ^                       ^
         |                       |                       |
         v                       v                       v
+----------------+       +----------------+       +----------------+
|   Attribute   |       |   Evidence     |       |    Context    |
+----------------+       +----------------+       +----------------+
| entity_id: UUID|      | relation_id: UUID|     | entity_id: UUID|
| key: String    |       | chunk_id: UUID |       | topic: String  |
| value: Any     |       | source_id: UUID|       | domain: String |
| confidence: Float|      | text: String    |       | time_period: Any|
| created: Datetime|      | created: Datetime|     | importance: Float|
+----------------+       +----------------+       +----------------+
```

**Entity Types**:
- Person (people mentioned in conversations)
- Organization (companies, institutions)
- Concept (abstract ideas, technologies, methods)
- Topic (subject areas, domains of knowledge)
- Event (meetings, conferences, occurrences)
- Resource (files, documents, links)

**Relation Types**:
- is_related_to (generic relationship)
- works_at (Person → Organization)
- knows (Person → Person)
- created_by (Any → Person/Organization)
- part_of (Any → Any)
- instance_of (Any → Concept)
- happened_at (Event → Datetime)
- references (Any → Resource)
- contradicts (Any → Any)
- derived_from (Any → Any)

### 2.2.4 Security and Privacy Controls

- **Data Encryption**
  - Configurable encryption for sensitive data
  - Key management system
  - Field-level encryption options

- **Access Control**
  - Object-level permissions
  - Role-based access
  - Audit logging

- **Data Lifecycle Management**
  - Retention policies
  - Secure deletion
  - Archival processes

## 2.3 Retrieval System

### 2.3.1 Query Processing

- **Query Understanding**
  - Intent classification
  - Entity extraction
  - Parameter identification

- **Query Expansion**
  - Synonym expansion
  - Context-aware term addition
  - User history incorporation

- **Multi-Modal Queries**
  - Text query processing
  - Image-based queries
  - Combined text+image queries

### 2.3.2 Search Algorithm

- **Vector Search**
  - Embedding generation with same model as ingestion
  - ANN (Approximate Nearest Neighbor) search
  - Distance metric configuration

- **Keyword Search**
  - Inverted index implementation
  - BM25 ranking
  - Fuzzy matching

- **Hybrid Combination**
  - Score normalization
  - Weighted combination
  - Re-ranking strategies

### 2.3.3 Result Processing

- **Diversification**
  - Maximal Marginal Relevance (MMR)
  - Clustering-based diversity
  - Source diversity measures

- **Enrichment**
  - Context expansion
  - Related entity inclusion
  - Citation generation

- **Personalization**
  - User preference application
  - History-based adaptation
  - Explicit feedback incorporation

## 2.4 Agent System

### 2.4.1 Reasoning Framework

- **Enhanced ReAct Pattern**
  - Thought-Action-Observation cycles
  - Self-criticism and revision
  - Confidence tracking

- **Planning Module**
  - Task decomposition
  - Sub-goal identification
  - Progress monitoring

- **Verification System**
  - Fact checking against knowledge base
  - Logical consistency validation
  - Uncertainty acknowledgment

### 2.4.2 Tool Integration

- **Internal Tools**
  - Vector search tool
  - Knowledge graph query tool
  - Memory management tool
  - Calculation and data analysis tools

- **Tool Registry**
  - Capability description format
  - Parameter specification
  - Error handling protocols

- **Tool Execution**
  - Secure sandbox environment
  - Resource limitation
  - Timeout management

### 2.4.3 Response Generation

- **Answer Synthesis**
  - Information integration from multiple sources
  - Contradictory information handling
  - Uncertainty representation

- **Citation System**
  - Source attribution
  - Quote context preservation
  - Citation formatting

- **Output Formatting**
  - Template-based generation
  - Markdown/rich text support
  - Multi-modal outputs (text, tables, simple visualizations)

## 2.5 Memory System

### 2.5.1 Fact Extraction Pipeline

- **Entity Recognition**
  - Named entity recognition (NER)
  - Custom entity types
  - Coreference resolution

- **Relation Extraction**
  - Predicate identification
  - Semantic role labeling
  - Temporal relation extraction

- **Fact Formulation**
  - Triple generation
  - Confidence scoring
  - Source attribution

### 2.5.2 Memory Consistency Management

- **Contradiction Detection**
  - Logical inconsistency identification
  - Temporal inconsistency detection
  - Confidence-based arbitration

- **Fact Merging**
  - Duplicate identification
  - Complementary fact combination
  - Provenance tracking

- **Validation Mechanics**
  - User confirmation requests
  - Automated cross-referencing
  - Confidence threshold policies

#### Contradiction Detection Algorithm

```pseudo
Function DetectContradiction(fact1, fact2):
    // Check if facts are about the same subject predicate
    If fact1.subject == fact2.subject AND fact1.predicate == fact2.predicate:
        // If objects directly contradict (e.g., A != B)
        If AreContradictoryValues(fact1.object, fact2.object):
            Return DIRECT_CONTRADICTION, CalculateConflictSeverity(fact1, fact2)
        
        // If temporal contradiction (e.g., A was true, then B became true)
        If HasTemporalContext(fact1) AND HasTemporalContext(fact2):
            If AreOverlappingTimeRanges(fact1.timeContext, fact2.timeContext):
                // Only a contradiction if they overlap in time
                If AreContradictoryValues(fact1.object, fact2.object):
                    Return TEMPORAL_CONTRADICTION, CalculateConflictSeverity(fact1, fact2)
        
        // If logical transitive contradiction (e.g., A > B, B > C, but A < C)
        If IsTransitiveRelation(fact1.predicate):
            // Check knowledge graph for transitive chains
            transitiveChain = FindTransitiveChain(fact1, fact2)
            If transitiveChain AND IsContradictoryChain(transitiveChain):
                Return LOGICAL_CONTRADICTION, CalculateConflictSeverity(fact1, fact2)
    
    // Check for entailment contradictions using LLM
    If entailmentModel.CheckContradiction(fact1, fact2) > CONTRADICTION_THRESHOLD:
        Return ENTAILMENT_CONTRADICTION, entailmentModel.ConfidenceScore
    
    Return NO_CONTRADICTION, 0.0

Function ResolveContradiction(fact1, fact2, contradictionType, severity):
    // Prioritize facts with higher source credibility
    If fact1.sourceCredibility > fact2.sourceCredibility + CREDIBILITY_THRESHOLD:
        return fact1
    If fact2.sourceCredibility > fact1.sourceCredibility + CREDIBILITY_THRESHOLD:
        return fact2
    
    // Prioritize more recent facts for temporal data
    If contradictionType == TEMPORAL_CONTRADICTION:
        If fact1.created > fact2.created + RECENCY_THRESHOLD:
            return fact1
        If fact2.created > fact1.created + RECENCY_THRESHOLD:
            return fact2
    
    // Prioritize facts with more evidence
    If fact1.evidenceCount > fact2.evidenceCount * EVIDENCE_FACTOR:
        return fact1
    If fact2.evidenceCount > fact1.evidenceCount * EVIDENCE_FACTOR:
        return fact2
    
    // If we can't automatically resolve, flag for user review
    return RequestUserVerification(fact1, fact2, contradictionType, severity)
```

```python
# Example implementation of AreContradictoryValues
def are_contradictory_values(value1, value2, tolerance=0.05):
    # Direct negation
    if isinstance(value1, bool) and isinstance(value2, bool):
        return value1 != value2
        
    # Numerical contradiction (outside tolerance range)
    if is_numeric(value1) and is_numeric(value2):
        # If the relative difference exceeds tolerance
        if abs(value1 - value2) / max(abs(value1), abs(value2)) > tolerance:
            return True
            
    # String contradiction - using NLI model
    if isinstance(value1, str) and isinstance(value2, str):
        # Use Natural Language Inference model to detect contradictions
        result = nli_model.predict(premise=value1, hypothesis=value2)
        if result["contradiction"] > 0.7:  # Threshold for contradiction
            return True
            
    # Categorical contradiction
    if is_categorical(value1) and is_categorical(value2):
        if are_mutually_exclusive_categories(value1, value2):
            return True
            
    return False
```

### 2.5.3 Knowledge Organization

- **Hierarchical Categorization**
  - Topic clustering
  - Concept hierarchy maintenance
  - Relationship type taxonomy

- **Temporal Management**
  - Fact versioning
  - Belief state tracking over time
  - Change history

- **Importance Ranking**
  - Centrality in knowledge graph
  - Usage frequency
  - User-defined importance

## 2.6 Interface Systems

### 2.6.1 CLI Framework

- **Command Structure**
  - Root commands: `ingest`, `search`, `ask`, `memory`, `config`
  - Sub-commands with consistent patterns
  - Parameter handling

- **Interactive Features**
  - Auto-completion
  - History navigation
  - Context-aware help

- **Output Formatting**
  - Structured data display (tables, trees)
  - Color coding
  - Progress indicators

### 2.6.2 Web API

- **Core Endpoints**
  - `/api/ingest`: Content ingestion
  - `/api/search`: Vector and hybrid search
  - `/api/ask`: Agent-based question answering
  - `/api/memory`: Memory management
  - `/api/admin`: System administration

- **Security Controls**
  - Authentication middleware
  - Rate limiting
  - Input validation

- **Performance Optimization**
  - Response compression
  - Caching headers
  - Asynchronous processing

### 2.6.3 Web UI

- **Main Components**
  - Navigation system
  - Search interface
  - Chat/query interface
  - Memory browser
  - Settings panel

- **Interaction Patterns**
  - Progressive disclosure
  - Contextual actions
  - Keyboard shortcuts

- **Responsive Design**
  - Mobile-first approach
  - Adaptive layouts
  - Touch optimization

# 3. Edge Cases and Error Handling

## 3.1 Connection Failures

- **Database Connectivity**
  - Retry with exponential backoff
  - Read-only mode when write operations fail
  - Cache utilization during outages

- **LLM API Disconnection**
  - Fallback to local models
  - Graceful degradation of capabilities
  - Clear error messaging

## 3.2 Content Processing Errors

- **Malformed Input Files**
  - Robust parsing with partial extraction
  - Detailed error reporting
  - Manual intervention options

- **Embedding Generation Failures**
  - Queue for retry
  - Alternative model fallback
  - Placeholder embeddings for searchability

## 3.3 Security Incidents

- **Authentication Breach**
  - Session termination
  - Activity logging
  - Notification protocols

- **Data Exposure**
  - Access revocation
  - Audit trail generation
  - Exposed data inventory

## 3.4 Resource Constraints

- **Memory Pressure**
  - Graceful degradation
  - Prioritized resource allocation
  - Background task deferral

- **Storage Limitations**
  - Warning thresholds
  - Automatic archiving policies
  - Compression strategies

# 4. Performance Requirements

## 4.1 Response Time

- **Vector Search Operations**
  - P50: <100ms
  - P95: <500ms
  - P99: <1000ms

- **Agent Reasoning**
  - Simple queries: <1s
  - Complex reasoning: <5s
  - Extended analysis: <30s with progress updates

- **Web UI Interactions**
  - Initial page load: <2s
  - Interface actions: <200ms

## 4.2 Throughput

- **Ingestion Processing**
  - Minimum: 100 documents/hour on standard hardware
  - Target: 1000 documents/hour

- **Concurrent Users**
  - Single-user mode: unlimited operations
  - Multi-user mode: 50 concurrent users per server instance

## 4.3 Scalability

- **Data Volume**
  - Up to 10M chunks per instance
  - Up to 1M entities in knowledge graph
  - Up to 10M facts in memory system

- **Distribution Strategy**
  - Horizontal scaling for web tier
  - Vertical scaling for database tier
  - Sharding strategy for very large deployments

# 5. Integration Requirements

## 5.1 External Services

- **LLM Providers**
  - OpenAI API
  - Anthropic API
  - Google AI API
  - Local model API (Ollama, etc.)

- **Embedding Services**
  - Support for hosted embedding generation
  - Local embedding model integration

## 5.2 Authentication Systems

- **Local Authentication**
  - Username/password
  - API key management

- **SSO Integration**
  - OAuth 2.0 support
  - SAML for enterprise
  - OpenID Connect compatibility

## 5.3 Storage Systems

- **Local Storage**
  - File system integration
  - Local database support

- **Cloud Storage**
  - S3-compatible object storage
  - Managed database services

# 6. Deployment Requirements

## 6.1 Installation Options

- **Local Installation**
  - Single-user desktop mode
  - Multi-user server mode

- **Containerized Deployment**
  - Docker Compose for simple deployments
  - Kubernetes for enterprise scale

## 6.2 Configuration Management

- **Environment Variables**
  - Core system configuration
  - Security parameters
  - Feature flags

- **Configuration Files**
  - Detailed component configuration
  - Override hierarchies
  - Environment-specific settings

## 6.3 Monitoring and Maintenance

- **Logging**
  - Structured log format
  - Configurable verbosity
  - Log rotation policies

- **Health Checks**
  - Component status endpoints
  - Self-diagnostic tools
  - Automatic recovery procedures

# 7. Security and Privacy

## 7.1 Authentication and Authorization

- **User Authentication**
  - Multi-factor options
  - Session management
  - Password policies

- **Permission Model**
  - Role-based access control
  - Object-level permissions
  - Permission inheritance

## 7.2 Data Protection

- **At-Rest Encryption**
  - AES-256 for sensitive data
  - Key rotation capabilities
  - Encrypted backups

- **In-Transit Encryption**
  - TLS 1.3 for all communications
  - Certificate management
  - HSTS implementation

## 7.3 Privacy Controls

- **Data Minimization**
  - Configurable retention policies
  - Selective processing options
  - Purpose limitation enforcement

- **User Controls**
  - Data export functionality
  - Deletion requests
  - Processing limitation options

# 8. Accessibility Requirements

- **Screen Reader Compatibility**
  - ARIA attributes
  - Semantic HTML
  - Keyboard focus management

- **Visual Accommodations**
  - High contrast mode
  - Text scaling
  - Color blind friendly palettes

- **Interaction Alternatives**
  - Keyboard navigation for all functions
  - Voice input support where possible
  - Reduced motion options

---

# 9. Configuration and Environment Settings

## 9.1 Configuration by Environment

The following table outlines which features and configurations are enabled in different deployment environments.

| Feature/Configuration | Development | Staging | Production |
|----------------------|-------------|---------|------------|
| **Ingestion System** ||||
| ChatGPT Export Support | Enabled | Enabled | Enabled |
| Claude Export Support | Enabled | Enabled | Enabled |
| PDF Parsing | Enabled | Enabled | Enabled |
| Image Processing | Disabled | Enabled | Enabled |
| Web Content Parsing | Disabled | Enabled | Enabled |
| **Vector Store** ||||
| Vector Index Type | HNSW | HNSW | HNSW/IVFFlat (configurable) |
| Max Vectors | 1M | 10M | 100M+ |
| MMR Reranking | Enabled | Enabled | Enabled |
| **Memory System** ||||
| Fact Extraction | Enabled | Enabled | Enabled |
| Contradiction Detection | Basic | Advanced | Advanced |
| User Verification Threshold | Low | Medium | High |
| **Agent System** ||||
| Multi-Step Planning | Enabled | Enabled | Enabled |
| Tool Usage | Limited | Full | Full |
| Max Iterations | 5 | 10 | 15 |
| **LLM Integration** ||||
| Local LLM Support | Enabled | Enabled | Enabled |
| OpenAI Integration | Enabled | Enabled | Enabled |
| Anthropic Integration | Enabled | Enabled | Enabled |
| **Security** ||||
| API Key Encryption | Enabled | Enabled | Enabled |
| Field-Level Encryption | Optional | Required | Required |
| Session Timeout (minutes) | 120 | 60 | 30 |
| Rate Limiting | Disabled | Enabled | Enabled |
| **Monitoring** ||||
| Debug Logging | Verbose | Limited | Errors Only |
| Performance Metrics | Enabled | Enabled | Enabled |
| User Analytics | Opt-In | Opt-In | Opt-In |
| Error Reporting | Detailed | Limited | Limited |

## 9.2 Test Case Inventory

The following is a skeleton inventory of test cases that should be developed for JARVIS 2.0:

| Test Category | Test Area | Test Cases |
|--------------|-----------|------------|
| **Unit Tests** | Ingestion | - Parse ChatGPT export format
 | | | - Parse Claude export format
 | | | - Chunking algorithm tests
 | | | - Metadata extraction tests |
| | Vector Store | - Vector search accuracy
 | | | - MMR implementation tests
 | | | - Hybrid search functionality |
| | Agent | - ReAct loop progression
 | | | - Tool usage tests
 | | | - Error handling tests |
| | Memory | - Entity extraction tests
 | | | - Relation extraction tests
 | | | - Contradiction detection tests |
| **Integration Tests** | End-to-End | - Ingestion → Storage → Retrieval flow
 | | | - Query → Agent → Response flow
 | | | - Memory extraction pipeline |
| | Cross-Component | - LLM integration tests
 | | | - Database interaction tests
 | | | - API endpoint tests |
| **Performance Tests** | Load Testing | - Concurrent query handling
 | | | - Large-scale ingestion
 | | | - Vector search scaling |
| | Benchmark | - Retrieval latency tests
 | | | - Memory extraction speed
 | | | - Web UI responsiveness |
| **Security Tests** | Authentication | - Login flow tests
 | | | - API key validation
 | | | - Session management |
| | Authorization | - Role-based access control
 | | | - Object-level permissions
 | | | - API endpoint protections |
| | Vulnerability | - SQL injection tests
 | | | - XSS prevention tests
 | | | - Prompt injection tests |
