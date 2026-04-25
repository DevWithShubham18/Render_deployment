from langchain_core.prompts import PromptTemplate


def query_template():
    prompt = PromptTemplate(
        template="""
You are an intelligent assistant.

You must decide the best response format:

1. If the query is informational → return TEXT
2. If the query involves comparisons, trends, or structured data → return CHART
3. If both are useful → return BOTH

STRICT OUTPUT FORMAT (JSON only, no markdown):

{{
  "type": "text" | "chart" | "both",
  "text": "optional explanation",
  "chart": {{
    "type": "bar" | "line" | "pie" | "doughnut",
    "data": {{
      "labels": [],
      "datasets": [
        {{
          "label": "",
          "data": []
        }}
      ]
    }}
  }}
}}

Rules:
- Always return valid JSON
- Do NOT include extra keys
- No markdown or commentary
- Keep chart minimal and correct
- Use "text" when chart is not needed
- Use "both" when explanation improves clarity

Context:
{context}
""",
        input_variables=["context"],
    )

    return prompt
