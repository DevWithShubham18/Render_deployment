from parser import embed_and_store, process_pdf

from fastapi import APIRouter, File, UploadFile

file_router = APIRouter(
    prefix="/file",
    tags=[
        "file related routes",
    ],
)


@file_router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_bytes = await file.read()
    try:
        chunks = process_pdf(file_bytes)
        embed_and_store(chunks)
        return {
            "filename": file.filename,
            "message": f"Success! PDF shredded into {len(chunks)} chunks and saved.",
        }
    except Exception as e:
        return {
            "error": f"Error occurred due to {e}",
        }
