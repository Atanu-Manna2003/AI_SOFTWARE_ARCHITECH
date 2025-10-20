import os
from dotenv import load_dotenv
import time

load_dotenv()

class Config:
    # Free Gemini API
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    MODEL_NAME = "gemini/gemini-2.5-flash" 
    MODEL_TEMPERATURE = 0.1

    # Project settings
    OUTPUT_DIR = "output"
    
    # **FIX: Better rate limiting for free tier**
    MAX_REQUESTS_PER_RUN = 10  # Increased for full workflow
    REQUEST_DELAY = 60  # Reduced to 1 minute between major steps
    
    # **NEW: Agent-specific delays to avoid rate limits**
    AGENT_DELAYS = {
        "coordinator": 30,  # 30 seconds after spec generation
        "backend": 45,      # 45 seconds after backend generation  
        "frontend": 45,     # 45 seconds after frontend generation
        "integration": 30   # 30 seconds after integration review
    }
    
    # Agent configurations
    COORDINATOR_CONFIG = {
        "role": "AI Project Coordinator & Technical Architect",
        "goal": "Break down high-level project briefs into concrete technical tasks and coordinate specialized agents",
        "backstory": """You are an experienced Technical Project Manager and Software Architect with 10+ years of experience.
        You excel at analyzing vague project requirements and transforming them into specific, actionable technical tasks.
        You understand both frontend and backend development patterns and can create clear task assignments."""
    }
    
    BACKEND_AGENT_CONFIG = {
        "role": "Backend API & Database Specialist",
        "goal": "Create REST/GraphQL APIs, business logic workflows, and optimized database schemas",
        "backstory": """You are a backend expert specializing in API design, database architecture, authentication systems, 
        data validation, and business logic implementation. You create scalable, maintainable backend systems."""
    }
    
    FRONTEND_AGENT_CONFIG = {
        "role": "React UI/UX Specialist", 
        "goal": "Create responsive React components and user interfaces based on project requirements",
        "backstory": """You are a frontend expert focused on building modern, responsive React applications. 
        You specialize in creating intuitive user interfaces, component architecture, state management, 
        and ensuring excellent user experience across all devices."""
    }
    
    @classmethod
    def get_llm(cls):
        """Get configured free Gemini LLM with better error handling"""
        from crewai import LLM
        if not cls.GEMINI_API_KEY:
            raise Exception("GEMINI_API_KEY not found. Get free key from: https://aistudio.google.com/app/apikey")
        
        return LLM(
            model=cls.MODEL_NAME,
            temperature=cls.MODEL_TEMPERATURE,
            api_key=cls.GEMINI_API_KEY
        )
    
    @classmethod
    def apply_delay(cls, agent_type: str):
        """Apply appropriate delay to avoid rate limits"""
        delay_seconds = cls.AGENT_DELAYS.get(agent_type, 30)
        print(f"⏳ Applying {delay_seconds}s delay for {agent_type} to avoid rate limits...")
        time.sleep(delay_seconds)