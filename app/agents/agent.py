from langchain.agents import create_agent
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_groq import ChatGroq
from langchain_core.language_models import BaseChatModel
from sqlalchemy import event
import json

from app.agents.prompts import SYSTEM_PROMPT
from app.config.config_loader import AGENT_CONFIG
from app.context.runtime import RuntimeContext
from app.config.agent_config import AgentConfig
from app.tools.github_mcp import GitHubMCP, wrap_github_tools
from app.agents.model_factory import create_model
from app.models.review import CodeReview


class Agent:
    def __init__(self, config):
        self.model:BaseChatModel = create_model(
            provider=config.LLM_PROVIDER,
            model=config.MODEL,
            api_key=config.LLM_API_KEY
        )

        self.agent = None

    async def initialize(self):
        github_mcp = GitHubMCP()

        github_tools = await github_mcp.get_tools()
        github_tools = wrap_github_tools(github_tools)  # ← add this

        print("GitHub MCP tools:")
        for tool in github_tools:
            print(f"  - {tool.name}: {tool.description}")
            print(f"    Args schema: {tool.args_schema if tool.args_schema else 'None'}")

        self.agent = create_agent(
        model=self.model,
        tools=github_tools,
        system_prompt=SYSTEM_PROMPT,
        context_schema=RuntimeContext,
        response_format=CodeReview,
        )



    async def analyze_code(
    self,
    runtime_context: RuntimeContext,
    user_request: str,
):
        owner, repo = runtime_context.repository.split("/")

        message = f"""
    Repository (runtime context):
    - Full: {runtime_context.repository}
    - Owner: {owner}
    - Repo: {repo}

    Task:
    {user_request}
    """

        final_response = None

        async for event in self.agent.astream_events(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": message,
                    }
                ]
            },
            context=runtime_context,
            version="v2",
        ):
            event_type = event["event"]

            if event_type == "on_tool_start":
                print("\n🔧 TOOL CALL")
                print("Tool:", event["name"])
                print("Input:", event["data"].get("input"))

            elif event_type == "on_tool_end":
                print("\n📤 TOOL RESULT")
                print("Tool:", event["name"])
                print(
                    "Output:",
                    str(event["data"].get("output"))[:500],
                )

            elif event_type == "on_chain_end":
                output = event["data"].get("output")

                if isinstance(output, dict):
                    if "structured_response" in output:
                        final_response = output["structured_response"]

        return final_response