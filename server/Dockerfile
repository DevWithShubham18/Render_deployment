FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

COPY . .

# RUN pip install --no-cache-dir \
#     fastapi \
#     uvicorn \
#     python-multipart \
#     pymupdf \
#     langchain-text-splitters \
#     langchain-voyageai \
#     langchain-pinecone \
#     pinecone-client \
#     python-dotenv \
#     langchain-groq \
#     langgraph \
#     pydantic

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]