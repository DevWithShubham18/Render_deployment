import fitz
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pinecone import Pinecone
from utils.config import settings
from voyageai.client import Client

voyage_client = Client(api_key=settings.VOYAGE_API_KEY)
pc = Pinecone(api_key=settings.PINECONE_API_KEY)
index = pc.Index("report-analyzer")


def embed_texts(texts: list[str]):
    res = voyage_client.embed(texts, model="voyage-2")
    return res.embeddings


def store_chunks(chunks: list[str], user_id: str, file_hash: str):
    vectors = embed_texts(chunks)

    to_upsert = []
    for i, (text, vec) in enumerate(zip(chunks, vectors)):
        to_upsert.append(
            {
                "id": f"{user_id}_{file_hash}_{i}",
                "values": vec,
                "metadata": {
                    "text": text,
                    "user_id": user_id,
                    "file_hash": file_hash,
                },
            }
        )

    index.upsert(vectors=to_upsert)


def process_pdf(file_bytes: bytes) -> list[str]:
    
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    text = ""

    for p in doc:
        text += p.get_text() + "\n"

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200, length_function=len
    )
    chunks = splitter.split_text(text)
    return chunks


def file_exists(index, user_id: str, file_hash: str) -> bool:
    results = index.query(
        vector=[0.0] * 1024,  # dummy vector
        top_k=1,
        include_metadata=True,
        filter={
            "user_id": {"$eq": user_id},
            "file_hash": {"$eq": file_hash},
        },
    )
    return len(results.get("matches", [])) > 0
