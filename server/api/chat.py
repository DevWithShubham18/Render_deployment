from fastapi import APIRouter
from schemas import QuerySchema
from schemas.report_schema import LLMResponse
from services.workflow import graph

chat_router = APIRouter(prefix="/conversation", tags=["conversation"])


@chat_router.post("/query")
async def ask_question(req: QuerySchema):
    try:
        state = {
            "question": req.query,
            "memory_context": "",
            "user_id": "demo-user-001",
        }

        result = await graph.ainvoke(state)  # type:ignore

        payload = result.get("response", {})

        text = payload.get("text")
        chart = payload.get("chart")

        if text and chart:
            data = {
                "type": "both",
                "text": text,
                "chart": chart,
            }
        elif chart:
            data = {
                "type": "chart",
                "chart": chart,
            }
        else:
            data = {
                "type": "text",
                "text": text or "No response",
            }

        return {
            "success": True,
            "data": data,
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }
