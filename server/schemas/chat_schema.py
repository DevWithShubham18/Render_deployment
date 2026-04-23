from pydantic import BaseModel, Field


class QuerySchema(BaseModel):
    query: str = Field(..., description="user query to be executed")
