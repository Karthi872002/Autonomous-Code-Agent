from pydantic import BaseModel

class CodeReview(BaseModel):
    summary: str
    issues: list[str]
    severity: str
    suggested_changes: list[str]



class AgentQuery(BaseModel):
    query: str