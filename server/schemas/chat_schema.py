from pydantic import BaseModel, Field


class QuerySchema(BaseModel):
    query: str = Field(..., description="user query to be executed")
    userId: str = Field(..., description="unique user id of the current logged in user")
