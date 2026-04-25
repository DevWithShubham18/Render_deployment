from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from schemas.report_schema import ChartConfig

ORCHESTRATOR_PROMPT = """
You are Chartify, a central intelligence and orchestration agent, which routes to tools whenever necessary. You have a list of tools available and user's context. Utilize it to prevent a useful response to the user query.

For some queries you may not require the tools use, you can use your general intelligence available to answer the user's query

**Follow Strictly**
In the final answer, only return the textual information **DO NOT INCLUDE** JSON parts of the react-chartjs-2 or ```json like these.
"""


def chart_template():
    parser = PydanticOutputParser(pydantic_object=ChartConfig)

    prompt = PromptTemplate(
        template="""
You are a **STRICT** chart config agent.

Your job is **ONLY** to generate a structured ChartConfig for the chart rendering on the frontend.

User Query:
{query}

Rules:
- Do NOT hallucinate tools and follow the tools description, it is their **ROLE**

{format_instructions}
    """,
        input_variables=["query"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    return prompt, parser
