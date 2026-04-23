from typing import TypedDict


class AgentState(TypedDict):
    question: str
    context: str
    final_json: dict
