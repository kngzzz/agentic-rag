from typing import List, Tuple
import uuid

from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools.retriever import create_retriever_tool
from langchain_core.prompts import PromptTemplate, MessagesPlaceholder
from langchain_openai import OpenAIEmbeddings
# from core.database import WeaviateDBService # Removed
from backend.services import retrieval_service # Added for direct use
from langchain.memory import ConversationBufferWindowMemory
from langchain_community.tools.tavily_search import TavilySearchResults
# from langchain_core.runnables import RunnablePassthrough # Not directly used in this refactor

from backend.core.config import settings # Ensure backend. prefix
# from models.document import Document as ModelDocument # Removed, using dicts
from backend.schemas.document import DocumentResponse # Ensure backend. prefix

from langchain_core.documents import Document as LangchainDocument

# Initialize embeddings model (ensure consistency)
embeddings_model = OpenAIEmbeddings(api_key=settings.OPENAI_API_KEY, model=settings.EMBEDDING_MODEL) # Renamed for clarity

# --- LLM and Agent Setup --- #
llm = ChatOpenAI(model_name=settings.LLM_MODEL, temperature=0, api_key=settings.OPENAI_API_KEY)

# Define the ReAct prompt template with memory placeholder
# This is a simplified version that strictly follows the ReAct format
react_prompt_template = """
You are an intelligent assistant with access to a knowledge base and web search tools.
You can help users find information by using the available tools.

TOOLS:
{tools}

FORMAT INSTRUCTIONS - YOU MUST FOLLOW THIS EXACT FORMAT:
Question: the input question
Thought: think step-by-step about how to solve this
Action: the tool name to use (one of [{tool_names}])
Action Input: the input to the tool, formatted as required
Observation: the result from the tool
... (repeat Thought/Action/Action Input/Observation as needed)
Thought: I now have enough information to answer the question
Final Answer: the final answer to the question

REMEMBER: Always use the format Thought, then Action, then Action Input, then Observation.
Always begin with a Thought and always end with a Final Answer.

Previous conversation history:
{chat_history}

New question: {input}
{agent_scratchpad}
"""

# Prompt template will be fully defined inside answer_question to correctly capture tools
# --- Service Function --- #

async def answer_question(question: str) -> Tuple[str, List[DocumentResponse], str]: # Removed db argument
    """
    Uses a LangChain ReAct agent with a retrieval tool to answer a question
    based on the documents stored in Weaviate.
    """

    # --- Create Retriever Tool Dynamically --- #
    class AsyncRetrieverWrapper:
        def __init__(self):
            # self.db = db_service # Removed
            self.embeddings = embeddings_model # Use the globally initialized one
            self.hyde_prompt = PromptTemplate.from_template("Generate a short, hypothetical answer to the question: {question}")
            self.hyde_chain = self.hyde_prompt | llm

        async def get_relevant_documents(self, query: str, top_k: int = 3) -> List[LangchainDocument]:
            # Directly call the updated retrieval_service function
            retrieved_chunks = await retrieval_service.find_relevant_chunks(query=query, top_k=top_k)
            
            langchain_documents = []
            for chunk_dict in retrieved_chunks:
                # chunk_dict now contains 'id', 'content', 'source_filename', 'chunk_index', 'doc_id', 'distance'
                metadata = {
                    "id": chunk_dict.get("id"), # This is the chunk's own UUID from Weaviate
                    "source_filename": chunk_dict.get("source_filename"),
                    "chunk_index": chunk_dict.get("chunk_index"),
                    "doc_id": chunk_dict.get("doc_id"), # Original document ID
                    "distance": chunk_dict.get("distance")
                }
                # Filter out None values from metadata if necessary
                metadata = {k: v for k, v in metadata.items() if v is not None}
                
                doc = LangchainDocument(
                    page_content=chunk_dict.get('content', ''),
                    metadata=metadata
                )
                langchain_documents.append(doc)
            return langchain_documents
            
        async def get_relevant_documents_with_hyde(self, query: str, top_k: int = 3) -> List[LangchainDocument]:
            hypothetical_answer_result = await self.hyde_chain.ainvoke({"question": query})
            hypothetical_answer = hypothetical_answer_result.content if hasattr(hypothetical_answer_result, 'content') else str(hypothetical_answer_result)
            
            # Using the hypothetical answer to retrieve documents
            # This part assumes find_relevant_chunks can be called with the hypothetical answer string
            retrieved_chunks = await retrieval_service.find_relevant_chunks(query=hypothetical_answer, top_k=top_k)
            
            langchain_documents = []
            for chunk_dict in retrieved_chunks:
                metadata = {
                    "id": chunk_dict.get("id"),
                    "source_filename": chunk_dict.get("source_filename"),
                    "chunk_index": chunk_dict.get("chunk_index"),
                    "doc_id": chunk_dict.get("doc_id"),
                    "distance": chunk_dict.get("distance")
                }
                metadata = {k: v for k, v in metadata.items() if v is not None}
                doc = LangchainDocument(
                    page_content=chunk_dict.get('content', ''),
                    metadata=metadata
                )
                langchain_documents.append(doc)
            return langchain_documents

        async def ainvoke(self, input_str: str, **kwargs) -> List[LangchainDocument]: # Renamed input to input_str
            # Decide whether to use HyDE or direct retrieval, or make it configurable
            # For now, let's stick to HyDE as it was in the original code
            return await self.get_relevant_documents_with_hyde(input_str, top_k=kwargs.get('top_k', 3))

    retriever_instance = AsyncRetrieverWrapper() # Removed db_session argument

    retriever_tool = create_retriever_tool(
        retriever_instance, # type: ignore # Langchain might expect a BaseRetriever, this wrapper is a workaround
        "search_knowledge_base",
        "Searches and returns relevant document chunks from the knowledge base based on the query. Use this first to find answers in the internal knowledge base."
    )
    
    # Ensure Tavily API key is present before creating the tool
    tools_list = [retriever_tool]
    if settings.TAVILY_API_KEY:
        tavily_tool = TavilySearchResults(tavily_api_key=settings.TAVILY_API_KEY, max_results=3)
        tools_list.append(tavily_tool)
    else:
        print("TAVILY_API_KEY not found. Tavily search tool will not be available.")

    # Update prompt partials to use the dynamic tools_list
    current_tools = tools_list
    
    # Define the prompt within the function scope to correctly capture current_tools
    agent_prompt = PromptTemplate.from_template(react_prompt_template).partial(
        tools=lambda: "\n".join([f"{tool.name}: {tool.description}" for tool in current_tools]),
        tool_names=lambda: ", ".join([tool.name for tool in current_tools]),
    )

    memory = ConversationBufferWindowMemory(
        k=3,
        memory_key="chat_history",
        input_key="input",
        output_key="output",
        return_messages=True
    )

    agent = create_react_agent(llm, current_tools, agent_prompt) # Use current_tools and agent_prompt

    agent_executor = AgentExecutor(
        agent=agent,
        tools=current_tools, # Use current_tools
        memory=memory,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=10,
        return_intermediate_steps=True
    )

    try:
        question_lower_stripped = question.lower().strip()
        simple_greetings = ["hello", "hi", "hey", "test", "hello there", "hi there", "hey there", "greetings", "howdy"]
        meta_database_queries = [
            "what is in your database", 
            "what's in your database", 
            "what do you have in your database",
            "what information do you have",
            "what do you know",
            "what is in your knowledge base",
            "what's in your knowledge base",
            "what is in our knowledgebase", 
            "what is in your knowledgebase", 
            "what's in your knowledgebase"   
        ]

        if question_lower_stripped in simple_greetings or len(question_lower_stripped) < 3:
            return f"Hello! I'm JARVIS, your AI assistant. How can I help you today?", [], "Direct response: simple query."
        
        if question_lower_stripped in meta_database_queries:
            meta_answer = (
                "My knowledge base contains information from the documents you've uploaded. "
                "This can include text files, PDFs, JSON files, and other supported formats. "
                "I can search this information to answer your questions. "
                "Do you have a specific topic you'd like to ask about from your documents?"
            )
            return meta_answer, [], "Direct response: meta-query about database content."
        
        result = await agent_executor.ainvoke({"input": question})
        final_answer = result.get("output", "Sorry, I could not find an answer.")

        thought_process = ""
        intermediate_steps = result.get("intermediate_steps", [])
        for step in intermediate_steps:
            action, observation = step
            thought_process += f"Thought: {action.log}\n"
            thought_process += f"Action: {action.tool}\n"
            thought_process += f"Action Input: {action.tool_input}\n"
            observation_str = str(observation)
            if len(observation_str) > 500:
                thought_process += f"Observation: {observation_str[:500]}...\n"
            else:
                thought_process += f"Observation: {observation_str}\n"
            thought_process += "\n"

        sources = []
        for step in intermediate_steps:
            action, observation = step
            if action.tool == retriever_tool.name and isinstance(observation, list) and all(isinstance(doc, LangchainDocument) for doc in observation):
                sources.extend([
                    DocumentResponse(
                        # 'id' in metadata is the chunk's Weaviate UUID
                        id=uuid.UUID(doc.metadata.get('id')) if doc.metadata.get('id') and isinstance(doc.metadata.get('id'), str) else uuid.uuid4(),
                        content=doc.page_content,
                        doc_metadata=doc.metadata or {} # metadata is already a dict
                    ) for doc in observation
                ])

        unique_sources = []
        seen_content = set()
        for src in sources:
            if src.content not in seen_content:
                unique_sources.append(src)
                seen_content.add(src.content)

        return final_answer, unique_sources, thought_process

    except Exception as e:
        print(f"Error running agent: {e}")
        return f"An error occurred: {e}", [], f"Error occurred during execution: {e}"
