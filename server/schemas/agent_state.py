from typing import Annotated, List, Optional, TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    question: Annotated[List[BaseMessage], add_messages]
    user_id: str
    user_id: str
    memory_context: Optional[str]
    response: Optional[dict]
