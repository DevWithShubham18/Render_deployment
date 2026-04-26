import json
from datetime import datetime

from langchain.agents import create_agent
from langchain_core.messages import AIMessage, SystemMessage, ToolMessage
from langchain_groq import ChatGroq
from langgraph.graph import END, START, StateGraph
from pinecone import Pinecone
from schemas import AgentState
from schemas.prompts.orch_and_chart import ORCHESTRATOR_PROMPT
from services.mem.manager import MemoryManager
from services.tools.chart_tool import render_chart
from structlog import get_logger
from utils.config import settings
from voyageai.client import Client

workflow_logger = get_logger(__name__)

# Memory Manager client
memory_manager = MemoryManager(
    llm_client=ChatGroq(
        api_key=settings.GROQ_API_KEY,
        model="llama-3.3-70b-versatile",
    )
)

voyage_client = Client(api_key=settings.VOYAGE_API_KEY)
pc = Pinecone(api_key=settings.PINECONE_API_KEY)
index = pc.Index("report-analyzer")


def embed_query(text: str):
    res = voyage_client.embed([text], model="voyage-2")
    return res.embeddings[0]


async def file_retrieve(state: AgentState) -> AgentState:

    if not state.get("file_context"):
        return state

    query = state["question"]
    if isinstance(query, list):
        query = str(query[-1])

    query_vector = embed_query(query)

    results = index.query(
        vector=query_vector,  # type:ignore
        top_k=5,
        include_metadata=True,
        filter={"user_id": state["user_id"]},
    )

    texts = [
        match["metadata"]["text"]
        for match in results.get("matches", [])
        if match.get("metadata")
    ]

    state["file_content"] = "\n\n".join(texts) if texts else None
    return state


async def memory_retrieve(state: AgentState) -> AgentState:

    workflow_logger.info(f"Retrieving Memories")
    query_text = state["question"]

    memories = memory_manager.search(
        query=str(query_text),
        user_id=state["user_id"],
        k=5,
    )
    workflow_logger.debug(f"Memories:{memories[:1]}")

    state["memory_context"] = "\n".join(
        [f"{m['content']} (context:{m['context']})" for m in memories]
    )

    workflow_logger.info(f"Memories retrieved")
    return state


def generate_node(state: AgentState):

    workflow_logger.info(f"Initializing Agent")

    agent = create_agent(
        model=ChatGroq(
            api_key=settings.GROQ_API_KEY,
            model="openai/gpt-oss-20b",
        ),
        system_prompt=SystemMessage(content=ORCHESTRATOR_PROMPT),
        tools=[render_chart],
    )

    available_tools = [render_chart]
    agent_input = {
        "messages": state["question"]
        + [
            SystemMessage(
                content=f"Use the user memories: {state['memory_context']}",
            ),
            SystemMessage(
                content=f"""
                FILE CONTENT (HIGH PRIORITY DATA SOURCE):
                {state.get("file_content")}

                INSTRUCTION:
                - This data MUST be used if the query relates to charts or data.
                - If chart/graph is requested → YOU MUST CALL render_chart TOOL.
                """
            ),
            SystemMessage(
                content=f"Available tools for this request: {available_tools if available_tools else 'None'}"
            ),
        ]
    }

    text_response = None
    chart_response = None

    workflow_logger.info(f"Invoking Agent")
    result = agent.invoke(agent_input)  # type:ignore
    messages = result.get("messages", [])
    for msg in reversed(messages):
        if isinstance(msg, AIMessage) and msg.content:
            text_response = msg.content
            break

    for msg in reversed(messages):
        if isinstance(msg, ToolMessage):
            try:
                parsed = json.loads(msg.content)  # type:ignore

                if isinstance(parsed, dict) and "charts" in parsed:
                    chart_response = parsed["charts"]
                else:
                    chart_response = [parsed]

                break
            except Exception:
                pass

    state["response"] = {
        "text": text_response,
        "chart": chart_response,
    }
    workflow_logger.info(f"Agent Invocation completed")
    return state


async def memory_store(state: AgentState) -> AgentState:

    workflow_logger.info("Storing Memory")

    user_msg = state["question"]
    assistant_msg = state["response"].get("text") if state["response"] else None

    content = f"""
User: {user_msg}
Assistant: {assistant_msg}
"""

    await memory_manager.add_note(
        content=content,
        time=str(datetime.utcnow()),
        user_id=state["user_id"],
    )

    return state


workflow = StateGraph(AgentState)

workflow.add_node("memory_retrieve", memory_retrieve)
workflow.add_node("file_retrieve", file_retrieve)
workflow.add_node("generate", generate_node)
workflow.add_node("memory_store", memory_store)

# Flow
workflow.set_entry_point("memory_retrieve")
workflow.add_edge("memory_retrieve", "file_retrieve")
workflow.add_edge("file_retrieve", "generate")
workflow.add_edge("generate", "memory_store")
workflow.add_edge("memory_store", END)

graph = workflow.compile()
