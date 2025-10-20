from crewai import Task

class FrontendTask:
    def __init__(self, frontend_agent, specification: str, api_structure: str):
        self.frontend_agent = frontend_agent
        self.specification = specification
        self.api_structure = api_structure
    
    def create_task(self) -> Task:
        return Task(
            description=f"""
            Based on the following specifications, generate a complete, modern React frontend application.
            
            FRONTEND SPECIFICATION:
            {self.specification}
            
            BACKEND API STRUCTURE (for integration reference):
            {self.api_structure}
            
            **TECHNOLOGY REQUIREMENTS:**
            - Use React with TypeScript
            - Use Tailwind CSS for styling
            - Implement proper state management (React Context or hooks)
            - Create API service layer for backend communication
            - Implement routing if needed (React Router)
            - Ensure responsive design
            
            **FILE GENERATION GUIDELINES:**
            
            1. Analyze the specification to determine the optimal file structure
            2. Create modular components based on the project's domain
            3. Generate API services that match the backend API structure
            4. Implement state management appropriate for the application
            5. Create a proper package.json with required dependencies
            
            **MANDATORY ACTIONS:**
            - Use the File Writer tool for EVERY file you create
            - Place all files in the 'frontend/' subfolder
            - Include at minimum: package.json, main App component, and core feature components
            - Ensure API services perfectly match the backend endpoints
            
            Return a summary of the created file structure and how it addresses the project requirements.
            """,
            agent=self.frontend_agent,
            expected_output="Summary of the generated React frontend structure including: file organization, key components created, state management approach, and API integration strategy."
        )