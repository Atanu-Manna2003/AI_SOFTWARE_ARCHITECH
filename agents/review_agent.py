from crewai import Agent
from config import Config

class ReviewAgent:
    def __init__(self, tools: list = None):
        self.tools = tools or []
        self.agent = self._create_agent()
        
    def _create_agent(self) -> Agent:
        backstory = """
        You are a Senior Software Architect and Code Completion Expert. You don't assume 
        specific file structures - instead you INTELLIGENTLY ANALYZE existing codebases 
        and COMPLETE them based on their current architecture and the project requirements.
        
        **KEY ABILITIES:**
        - Analyze existing code structure and identify what's missing
        - Complete partial implementations without rewriting everything
        - Add missing architectural layers based on the project domain
        - Ensure the final result is functional and coherent
        - Make intelligent decisions about what completion means for each unique project
        
        **APPROACH:**
        You look at what EXISTS first, then determine what's needed to make it WORK.
        You don't impose rigid templates - you enhance the existing structure.
        """
        
        return Agent(
            role="Intelligent Code Completion Architect",
            goal="Analyze existing project structures and intelligently complete them to working state",
            backstory=backstory,
            tools=self.tools,
            verbose=True,
            allow_delegation=False,
            llm=Config.get_llm()
        )
    
    def get_agent(self) -> Agent:
        return self.agent