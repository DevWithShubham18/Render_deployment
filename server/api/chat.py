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

        response = result.get("response")

        validated = LLMResponse.model_validate(response)

        return {
            "success": True,
            "data": validated.model_dump(),
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }
