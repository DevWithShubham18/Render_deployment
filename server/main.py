from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from parser import process_pdf, embed_and_store
from agent import query_agent

app = FastAPI(title="Report Analyzer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_bytes = await file.read()
    try:
        chunks = process_pdf(file_bytes)
        embed_and_store(chunks)
        return {
            "filename": file.filename, 
            "message": f"Success! PDF shredded into {len(chunks)} chunks and saved."
        }
    except Exception as e:
        return {"error": str(e)}


@app.post("/query")
async def ask_question(question: str = Form(...)):
    try:
        answer_data = query_agent(question)
        return {"success": True, "data": answer_data}
    except Exception as e:
        return {"success": False, "error": str(e)}