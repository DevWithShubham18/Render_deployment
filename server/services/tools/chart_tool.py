from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from schemas.prompts.orch_and_chart import chart_template
from utils.config import settings


@tool(
    description="Generates a config for react-chart-js2 library for frontend rendering whenever the user query asks for infographic or chart generation. Can use this tool when the file context is available and the user is asking for generating possible infographics from it.",
    # return_direct=True,
)
def render_chart(query: str, file_content: str):
    prompt, parser = chart_template()
    chart_llm = ChatGroq(
        api_key=settings.GROQ_API_KEY,
        model="openai/gpt-oss-20b",
    )

    messages = [HumanMessage(prompt.format(query=query, file_content=file_content))]
    response = chart_llm.invoke(messages)

    generated_plan = parser.parse(response.content)  # type:ignore
    return generated_plan.model_dump()
