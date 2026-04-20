import fitz
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_pinecone import PineconeVectorStore
from langchain_voyageai import VoyageAIEmbeddings

def process_pdf(file_bytes: bytes) -> list[str]:
    print("opening pdf")
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    text = ""
    for p in doc:
        text += p.get_text() + "\n"
    
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, length_function=len)
    chunks = splitter.split_text(text)
    return chunks

def embed_and_store(chunks: list[str]):
    print("Storing in Pinecone...")
    embeddings = VoyageAIEmbeddings(model="voyage-2")
    PineconeVectorStore.from_texts(chunks, embeddings, index_name="report-analyzer")