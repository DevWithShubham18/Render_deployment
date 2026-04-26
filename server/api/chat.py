from fastapi import APIRouter
from schemas import QuerySchema
from services.workflow import graph
from structlog import get_logger

chat_router = APIRouter(prefix="/conversation", tags=["conversation"])
chat_logger = get_logger(__name__)

@chat_router.post("/query")
async def ask_question(req: QuerySchema):
    try:
        print(req.userId)
        state = {
            "question": req.query,
            "memory_context": "",
            "user_id": req.userId,
        }

        chat_logger.info("Invoking Workflow")

        result = await graph.ainvoke(state)  # type:ignore

        payload = result.get("response", {})

        chat_logger.info("Workflow completed")
        text = payload.get("text")
        chart = payload.get("chart")

        if text and chart:
            data = {
                "type": "both",
                "text": text,
                "charts": chart,
            }
        elif chart:
            data = {
                "type": "chart",
                "charts": chart,
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
