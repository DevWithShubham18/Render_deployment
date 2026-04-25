from typing import Optional, TypedDict


class AgentState(TypedDict):
    question: str
    user_id: str
    user_id: str
    memory_context: Optional[str]
    response: Optional[dict]
