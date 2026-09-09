import os

from langchain_mcp_adapters.client import MultiServerMCPClient

import base64
import json
from langchain.tools import tool
from langchain_core.tools import BaseTool


class GitHubMCP:

    def __init__(self):
        github_token = os.environ["GITHUB_PERSONAL_ACCESS_TOKEN"]

        self.client = MultiServerMCPClient(
            {
                "github": {
                    "transport": "http",
                    "url": "https://api.githubcopilot.com/mcp/",
                    "headers": {
                        "Authorization": f"Bearer {github_token}",
                    },
                }
            }
        )

    async def get_tools(self):
        return await self.client.get_tools()

def wrap_github_tools(tools: list[BaseTool]) -> list[BaseTool]:
    wrapped = []
    for t in tools:
        if t.name == "get_file_contents":
            original_arun = t._arun

            async def decoded_run(*args, _original_arun=original_arun, config=None, **kwargs):
                result = await _original_arun(*args, config=config, **kwargs)
                try:
                    parsed = json.loads(result)
                    if isinstance(parsed, dict) and parsed.get("encoding") == "base64":
                        content = base64.b64decode(parsed["content"]).decode("utf-8")
                        parsed["content"] = content
                        parsed["encoding"] = "utf-8"
                        return json.dumps(parsed)
                except Exception:
                    pass
                return result

            t._arun = decoded_run

        wrapped.append(t)
    return wrapped