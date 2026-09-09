from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.agents.agent import Agent
from app.routes.AnalyseRoutes import router as analyse_router
from app.config.config_loader import ConfigLoader, AGENT_CONFIG

@asynccontextmanager
async def lifespan(app: FastAPI):
    config = ConfigLoader.initialize_config()

    agent = Agent(config)

    await agent.initialize()

    app.state.agent_config = config
    app.state.agent = agent

    yield

app = FastAPI(lifespan=lifespan, title="Autonomous Code Agent")

app.include_router(analyse_router, prefix="/analyse", tags=["Analyse"])




