from crewai import Agent
from config import Config

class BackendAgent:
    def __init__(self, tools: list = None):
        self.tools = tools or []
        self.agent = self._create_agent()
        
    def _create_agent(self) -> Agent:
        return Agent(
            role=Config.BACKEND_AGENT_CONFIG["role"],
            goal=Config.BACKEND_AGENT_CONFIG["goal"],
            backstory=Config.BACKEND_AGENT_CONFIG["backstory"],
            tools=self.tools,
            verbose=True,
            allow_delegation=False,
            llm=Config.get_llm()  # Use the configured Gemini LLM
        )
    
    def get_agent(self) -> Agent:
        return self.agent