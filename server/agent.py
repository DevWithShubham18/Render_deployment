import os
from typing import TypedDict
from dotenv import load_dotenv
from pydantic import BaseModel, Field

from langchain_groq import ChatGroq
from langchain_pinecone import PineconeVectorStore
from langchain_voyageai import VoyageAIEmbeddings
from langgraph.graph import StateGraph, END

load_dotenv()


class ReportInsights(BaseModel):
    summary: str = Field(description="A concise 2-sentence summary answering the user's question.")
    metrics: list[str] = Field(description="A list of specific numbers, percentages, or KPIs extracted from the text.")


class AgentState(TypedDict):
    question: str
    context: str
    final_json: dict


def retrieve_node(state: AgentState):
    embeddings = VoyageAIEmbeddings(model="voyage-2")
    vectorstore = PineconeVectorStore(
        index_name="report-analyzer",
        embedding=embeddings
    )

    docs = vectorstore.similarity_search(state["question"], k=3)
    context = "\n\n".join([doc.page_content for doc in docs])

    return {"context": context}


def generate_node(state: AgentState):
    llm = ChatGroq(
        model_name="llama3-8b-8192",
        temperature=0
    )

    structured_llm = llm.with_structured_output(ReportInsights)

    prompt = f"""
    You are a financial analyst.
    Use the context to answer the question clearly and concisely.

    Context:
    {state["context"]}

    Question:
    {state["question"]}
    """

    result = structured_llm.invoke(prompt)

    return {"final_json": result.dict()}


workflow = StateGraph(AgentState)
workflow.add_node("retrieve", retrieve_node)
workflow.add_node("generate", generate_node)

workflow.set_entry_point("retrieve")
workflow.add_edge("retrieve", "generate")
workflow.add_edge("generate", END)

app_graph = workflow.compile()


def query_agent(question: str) -> dict:
    state = {"question": question}
    result = app_graph.invoke(state)
    return result["final_json"]