from dataclasses import dataclass

@dataclass
class RuntimeContext:
    repository: str
    workspace: str
    github_token: str | None = None