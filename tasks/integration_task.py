from crewai import Task

class IntegrationTask:
    def __init__(self, coordinator_agent, backend_code: str, frontend_code: str):
        self.coordinator_agent = coordinator_agent
        self.backend_code = backend_code
        self.frontend_code = frontend_code
    
    def create_task(self) -> Task:
        return Task(
            description=f"""
            Perform comprehensive integration review between the generated backend and frontend code.
            
            BACKEND CODE SUMMARY:
            {self.backend_code}
            
            FRONTEND CODE SUMMARY:  
            {self.frontend_code}
            
            **INTEGRATION REVIEW CRITERIA:**
            
            1. **API COMPATIBILITY**: Do frontend API calls match backend endpoint expectations?
            2. **DATA CONSISTENCY**: Are request/response structures aligned?
            3. **AUTHENTICATION FLOW**: Does auth implementation work end-to-end?
            4. **ERROR HANDLING**: Is error handling consistent across the stack?
            5. **BUSINESS LOGIC**: Do frontend workflows match backend capabilities?
            6. **DATA FLOW**: Can data move seamlessly between frontend and backend?
            
            **REVIEW APPROACH:**
            - Identify specific mismatches with line-by-line analysis if possible
            - Provide concrete correction suggestions
            - Consider both technical and functional alignment
            - Assess overall system coherence
            
            Provide actionable feedback for both backend and frontend adjustments.
            """,
            agent=self.coordinator_agent,
            expected_output="""Comprehensive integration review containing:
            - Overall integration readiness assessment
            - Specific technical mismatches identified
            - Backend adjustments needed
            - Frontend adjustments needed  
            - Priority of fixes (critical/high/medium)
            """
        )