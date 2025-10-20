from crewai import Task

class SpecificationTask:
    def __init__(self, coordinator_agent):
        self.coordinator_agent = coordinator_agent
    
    def create_task(self, project_brief: str) -> Task:
        return Task(
            description=f"""
            Analyze the following project brief and create detailed, technology-agnostic technical specifications.
            
            PROJECT BRIEF: {project_brief}
            
            **ANALYSIS APPROACH:**
            1. Identify core domain entities and their relationships
            2. Determine required user roles and permissions
            3. Define data models and business logic requirements
            4. Specify API endpoints needed for frontend-backend communication
            5. Identify frontend components and user interface requirements
            
            **SPECIFICATION GUIDELINES:**
            - Keep specifications technology-agnostic where possible
            - Focus on functionality rather than implementation details
            - Ensure frontend and backend specifications are perfectly aligned
            - Consider scalability and maintainability
            
            **OUTPUT FORMAT:**
            
            ---
            
            ## Technical Specifications for: "{project_brief}"
            
            ### PROJECT ANALYSIS
            [Brief overview of the project domain and key requirements]
            
            ### BACKEND_SPEC
            [Technology-agnostic backend specification covering:
             - Data models and relationships
             - API endpoint requirements
             - Authentication/authorization needs
             - Business logic workflows]
            
            ### FRONTEND_SPEC  
            [Technology-agnostic frontend specification covering:
             - User interface components
             - User interaction flows
             - State management requirements
             - API integration points]
            
            ---
            """,
            agent=self.coordinator_agent,
            expected_output="Comprehensive technical specifications with clearly separated BACKEND_SPEC and FRONTEND_SPEC sections, following the requested markdown structure."
        )