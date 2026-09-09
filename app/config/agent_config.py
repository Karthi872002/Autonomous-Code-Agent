from pydantic import BaseModel


class AgentConfig(BaseModel):
    MODEL: str
    LLM_API_KEY: str
    LLM_PROVIDER: str  = "nvidia"



AGENT_CONFIG: AgentConfig = None
