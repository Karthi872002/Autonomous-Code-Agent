from fastapi import APIRouter,Request

from app.agents.agent import Agent
from app.context.runtime import RuntimeContext
from app.models.api_schema import AnalyzeRequest
from app.models.review import AgentQuery

router = APIRouter()





@router.post("/analyze")
async def analyze(
    http_request: Request,
    request: AnalyzeRequest,
):
    agent = http_request.app.state.agent

    print(request.repository)
    print(request)

    context = RuntimeContext(
        repository=request.repository,
        workspace=request.workspace,
    )

    response = await agent.analyze_code(
        runtime_context=context,
        user_request=request.question,
    )

    return response

@router.post("/test-agent")
async def test_agent(
    request: Request,
    agent_query: AgentQuery,
):
    agent = request.app.state.agent

    return await agent.analyze_code(runtime_context=None, user_request=agent_query.query)