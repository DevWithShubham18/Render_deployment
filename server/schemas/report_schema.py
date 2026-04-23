from pydantic import BaseModel, Field


class ReportInsights(BaseModel):
    summary: str = Field(
        description="A concise 2-sentence summary answering the user's question."
    )
    metrics: list[str] = Field(
        description="A list of specific numbers, percentages, or KPIs extracted from the text."
    )
