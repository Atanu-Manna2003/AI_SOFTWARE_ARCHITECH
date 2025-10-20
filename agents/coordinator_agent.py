from crewai import Agent
from config import Config

class CoordinatorAgent:
    def __init__(self, tools: list = None):
        self.tools = tools or []
        self.agent = self._create_agent()
        
    def _create_agent(self) -> Agent:
        return Agent(
            role=Config.COORDINATOR_CONFIG["role"],
            goal=Config.COORDINATOR_CONFIG["goal"],
            backstory=Config.COORDINATOR_CONFIG["backstory"],
            tools=self.tools,
            verbose=True,
            allow_delegation=True,
            llm=Config.get_llm()  # Use the configured Gemini LLM
        )

    def get_agent(self) -> Agent:
        return self.agent