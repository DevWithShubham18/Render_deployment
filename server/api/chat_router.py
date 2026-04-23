from agent import query_agent
from fastapi import APIRouter
from schemas import QuerySchema

chat_router = APIRouter(prefix="/conversation")


@chat_router.post("/query")
async def ask_question(req: QuerySchema):
    try:
        answer_data = query_agent(req.query)
        return {"success": True, "data": answer_data}
    except Exception as e:
        return {"success": False, "error": str(e)}
