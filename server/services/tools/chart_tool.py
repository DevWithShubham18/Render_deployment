from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from schemas.prompts.orch_and_chart import chart_template
from utils.config import settings


@tool(
    description="Generates a config for react-chart-js2 library for frontend rendering whenever the user query asks for infographic or chart generation",
    # return_direct=True,
)
def render_chart(query: str):
    prompt, parser = chart_template()
    chart_llm = ChatGroq(
        api_key=settings.GROQ_API_KEY,
        model="llama-3.3-70b-versatile",
    )

    messages = [HumanMessage(prompt.format(query=query))]
    response = chart_llm.invoke(messages)

    generated_plan = parser.parse(response.content)  # type:ignore
    return generated_plan.model_dump()
