import os
import shutil
import uuid
from typing import Optional

from fastapi import APIRouter, File, Form, UploadFile
from services.ingestion import file_exists, index, process_pdf, store_chunks
from services.workflow import graph
from structlog import get_logger
from utils.file_hash import get_file_hash

chat_router = APIRouter(prefix="/conversation", tags=["conversation"])
chat_logger = get_logger(__name__)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@chat_router.post("/query")
async def ask_question(
    query: str = Form(...),
    userId: str = Form(...),
    file: Optional[UploadFile] = File(None),
):
    file_path = None

    try:
        file_hash = None

        if file:
            file_id = str(uuid.uuid4())
            file_path = os.path.join(UPLOAD_DIR, f"{file_id}_{file.filename}")

            # Save file
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            # Read bytes
            file.file.seek(0)
            file_bytes = await file.read()

            file_hash = get_file_hash(file_bytes)

            # Avoid re-embedding
            if not file_exists(index, userId, file_hash):
                chat_logger.info("New file → processing & embedding")

                chunks = process_pdf(file_bytes)
                store_chunks(chunks, userId, file_hash)

            else:
                chat_logger.info("File already processed → skipping")

        state = {
            "question": query,
            "memory_context": "",
            "user_id": userId,
            "file_context": file_hash,
        }

        chat_logger.info("Invoking Workflow")

        result = await graph.ainvoke(state)  # type:ignore

        payload = result.get("response", {})

        text = payload.get("text")
        chart = payload.get("chart")

        if text and chart:
            data = {"type": "both", "text": text, "charts": chart}
        elif chart:
            data = {"type": "chart", "charts": chart}
        else:
            data = {"type": "text", "text": text or "No response"}

        return {"success": True, "data": data}

    except Exception as e:
        return {"success": False, "error": str(e)}

    finally:
        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
                chat_logger.info(f"Deleted temp file: {file_path}")
            except Exception as cleanup_err:
                chat_logger.error(f"Failed to delete file: {cleanup_err}")
