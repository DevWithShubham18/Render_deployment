import json
from datetime import datetime

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq
from langgraph.graph import END, START, StateGraph
from schemas import AgentState
from schemas.prompts.query import query_template
from schemas.report_schema import LLMResponse
from services.mem.manager import MemoryManager
from services.tools.chart_tool import render_chart
from utils.config import settings

# LLM with binded tools
llm = ChatGroq(
    api_key=settings.GROQ_API_KEY,
    model="llama-3.1-8b-instant",
    temperature=0,
).bind_tools([render_chart])


# Memory Manager client
memory_manager = MemoryManager(
    llm_client=ChatGroq(
        api_key=settings.GROQ_API_KEY,
        model="llama-3.3-70b-versatile",
    )
)


async def memory_retrieve(state: AgentState) -> AgentState:

    query_text = state["question"]

    memories = memory_manager.search(
        query=str(query_text),
        user_id=state["user_id"],
        k=5,
    )

    state["memory_context"] = "\n".join(
        [f"{m['content']} (context:{m['context']})" for m in memories]
    )

    return state


def generate_node(state: AgentState):
    llm = ChatGroq(
        api_key=settings.GROQ_API_KEY,
        model="llama-3.1-8b-instant",
        temperature=0,
    )

    prompt = query_template()

    messages = [
        SystemMessage(content=prompt.format(context=state.get("memory_context", ""))),
        HumanMessage(content=state["question"]),
    ]

    try:
        output = llm.invoke(messages)
        parsed = json.loads(output.content)  # type:ignore

        validated = LLMResponse.model_validate(parsed)

        state["response"] = validated.model_dump()

    except Exception as e:
        state["response"] = {"type": "text", "text": f"Error: {str(e)}"}

    return state


async def memory_store(state: AgentState) -> AgentState:

    user_msg = state["question"]
    assistant_msg = state["response"]

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

# Nodes
workflow.add_node("memory_retrieve", memory_retrieve)
workflow.add_node("generate", generate_node)
workflow.add_node("memory_store", memory_store)

# Flow
workflow.set_entry_point("memory_retrieve")
workflow.add_edge("memory_retrieve", "generate")
workflow.add_edge("generate", "memory_store")
workflow.add_edge("memory_store", END)

graph = workflow.compile()
