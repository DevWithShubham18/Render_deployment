from fastapi import APIRouter
from schemas import QuerySchema
from services.workflow import graph

chat_router = APIRouter(prefix="/conversation")


@chat_router.post("/query")
async def ask_question(req: QuerySchema):
    try:
        state = {"question": req.query}
        response = graph.invoke(state)  # type: ignore
        return (
            {
                "success": True,
                "data": response.get("final_json", {}),
            },
        )
    except Exception as e:
        return {"success": False, "error": str(e)}
