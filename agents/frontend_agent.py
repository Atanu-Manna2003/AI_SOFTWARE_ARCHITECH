from crewai import Agent
from config import Config

class FrontendAgent:
    def __init__(self, tools: list = None):
        self.tools = tools or []
        self.agent = self._create_agent()
        
    def _create_agent(self) -> Agent:
        generic_backstory = """
        You are a frontend expert focused on building modern, responsive React applications. 
        You specialize in creating intuitive user interfaces, component architecture, state management, 
        and ensuring excellent user experience across all devices.
        
        **KEY RESPONSIBILITIES:**
        - Analyze project requirements to determine optimal component structure
        - Create modular, reusable React components with TypeScript
        - Implement proper state management based on project needs
        - Ensure responsive design and accessibility
        - Generate ALL code files using the File Writer tool
        - Structure files logically based on project complexity
        """
        
        return Agent(
            role=Config.FRONTEND_AGENT_CONFIG["role"],
            goal=Config.FRONTEND_AGENT_CONFIG["goal"],
            backstory=generic_backstory,
            tools=self.tools,
            verbose=True,
            allow_delegation=False,
            llm=Config.get_llm()
        )
    
    def get_agent(self) -> Agent:
        return self.agent