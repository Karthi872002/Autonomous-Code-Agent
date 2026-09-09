from pydantic import BaseModel

class AnalyzeRequest(BaseModel):
    repository: str
    workspace: str
    question: str