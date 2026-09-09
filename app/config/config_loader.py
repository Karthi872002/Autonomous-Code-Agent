from .agent_config import AgentConfig,AGENT_CONFIG
from dotenv import load_dotenv
import os

load_dotenv()

class ConfigLoader:
    @staticmethod
    def load_from_env() -> AgentConfig:
        # Load the agent configuration from a file or environment variables
        # For simplicity, we will return a hardcoded configuration here
        return AgentConfig(
            MODEL=os.getenv("MODEL", "meta/llama2-70b"),
            LLM_API_KEY=os.getenv("LLM_API_KEY"), 
            LLM_PROVIDER=os.getenv("LLM_PROVIDER")
        )

    @staticmethod
    def initialize_config() -> None:
        """Initialize the global service configuration."""
        global AGENT_CONFIG
        if AGENT_CONFIG is None:
            switch_env = os.getenv("SWITCH_ENV", "false").lower() == "true"
            if switch_env:
                # Load configuration from environment variables
                AGENT_CONFIG = ConfigLoader.load_from_env()

        return AGENT_CONFIG

 