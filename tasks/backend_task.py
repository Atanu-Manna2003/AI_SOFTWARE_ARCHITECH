from crewai import Task

class BackendTask:
    def __init__(self, backend_agent, specification: str):
        self.backend_agent = backend_agent
        self.specification = specification
    
    def create_task(self) -> Task:
        return Task(
            description=f"""
            Based on the following backend specification, generate complete, production-ready backend code.
            
            BACKEND SPECIFICATION:
            {self.specification}
            
            **TECHNOLOGY RECOMMENDATIONS (Adjust based on specification):**
            - FastAPI for REST APIs
            - SQLAlchemy for database ORM  
            - Pydantic for data validation
            - JWT for authentication when needed
            
            **IMPLEMENTATION REQUIREMENTS:**
            
            1. Analyze the specification to determine the optimal architecture
            2. Design database models based on the domain entities
            3. Create API endpoints with proper request/response validation
            4. Implement business logic and data access layers
            5. Add authentication/authorization if required by the specification
            6. Include proper error handling and validation
            7. Generate requirements.txt with necessary dependencies
            
            **FILE GENERATION:**
            - Use the File Writer tool for ALL files
            - Place all files in the 'backend/' subfolder  
            - Structure files logically (models, routes, services, etc.)
            - Ensure the architecture matches the project complexity
            
            Return a summary of the backend architecture including: database models, API endpoints, authentication strategy, and file structure.
            """,
            agent=self.backend_agent,
            expected_output="Summary of the generated backend architecture including key models, endpoints, authentication approach, and file organization."
        )