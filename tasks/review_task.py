from crewai import Task
import os
import json
from pathlib import Path

class ReviewTask:
    def __init__(self, review_agent, project_brief: str, specifications: dict):
        self.review_agent = review_agent
        self.project_brief = project_brief
        self.specifications = specifications
    
    def _scan_project_structure(self) -> dict:
        """Analyze project structure without hardcoded expectations"""
        project_structure = {
            "backend": {"files": {}, "categories": {}},
            "frontend": {"files": {}, "categories": {}},
            "analysis": {
                "completeness_score": 0,
                "missing_patterns": [],
                "architecture_issues": []
            }
        }
        
        output_dir = "output"
        
        if os.path.exists(output_dir):
            for root, dirs, files in os.walk(output_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, output_dir)
                    
                    file_info = self._get_file_info(file_path)
                    
                    # Categorize intelligently based on path patterns
                    if relative_path.startswith('backend/'):
                        category = self._categorize_backend_file(relative_path)
                        project_structure["backend"]["files"][relative_path] = file_info
                        project_structure["backend"]["categories"].setdefault(category, []).append(relative_path)
                    elif relative_path.startswith('frontend/'):
                        category = self._categorize_frontend_file(relative_path)
                        project_structure["frontend"]["files"][relative_path] = file_info
                        project_structure["frontend"]["categories"].setdefault(category, []).append(relative_path)
        
        # Analyze completeness based on actual project structure
        self._analyze_completeness(project_structure)
        
        return project_structure
    
    def _categorize_backend_file(self, file_path: str) -> str:
        """Intelligently categorize backend files without hardcoding"""
        if 'router' in file_path or 'route' in file_path:
            return 'routers'
        elif 'model' in file_path:
            return 'models'
        elif 'schema' in file_path:
            return 'schemas'
        elif 'crud' in file_path or 'service' in file_path:
            return 'services'
        elif 'auth' in file_path or 'security' in file_path:
            return 'authentication'
        elif 'config' in file_path or 'setting' in file_path:
            return 'configuration'
        elif 'database' in file_path or 'db' in file_path:
            return 'database'
        elif 'main' in file_path or 'app' in file_path:
            return 'application'
        else:
            return 'other'
    
    def _categorize_frontend_file(self, file_path: str) -> str:
        """Intelligently categorize frontend files without hardcoding"""
        if 'component' in file_path:
            return 'components'
        elif 'page' in file_path or 'view' in file_path:
            return 'pages'
        elif 'service' in file_path or 'api' in file_path:
            return 'services'
        elif 'context' in file_path or 'store' in file_path:
            return 'state_management'
        elif 'hook' in file_path:
            return 'hooks'
        elif 'type' in file_path or 'interface' in file_path:
            return 'types'
        elif 'util' in file_path or 'helper' in file_path:
            return 'utilities'
        elif 'config' in file_path:
            return 'configuration'
        else:
            return 'other'
    
    def _analyze_completeness(self, project_structure: dict):
        """Analyze project completeness based on architecture patterns"""
        backend_cats = project_structure["backend"]["categories"]
        frontend_cats = project_structure["frontend"]["categories"]
        
        missing_patterns = []
        
        # Check for common architectural patterns (not specific files)
        if not backend_cats.get('routers') and not backend_cats.get('application'):
            missing_patterns.append("Backend lacks API routing layer")
        
        if not backend_cats.get('services') and not backend_cats.get('crud'):
            missing_patterns.append("Backend lacks business logic layer")
        
        if not frontend_cats.get('components'):
            missing_patterns.append("Frontend lacks UI components")
        
        if not frontend_cats.get('pages') and len(frontend_cats.get('components', [])) < 3:
            missing_patterns.append("Frontend lacks sufficient component structure")
        
        if not frontend_cats.get('services'):
            missing_patterns.append("Frontend lacks API service layer")
        
        # Calculate completeness score
        backend_score = min(len(backend_cats) * 10, 40)  # Max 40 points for backend
        frontend_score = min(len(frontend_cats) * 10, 40)  # Max 40 points for frontend
        implementation_score = self._calculate_implementation_score(project_structure)
        
        total_score = backend_score + frontend_score + implementation_score
        project_structure["analysis"]["completeness_score"] = total_score
        project_structure["analysis"]["missing_patterns"] = missing_patterns
    
    def _calculate_implementation_score(self, project_structure: dict) -> int:
        """Score based on actual implementation quality"""
        score = 0
        
        # Check if files have real content vs placeholders
        all_files = {**project_structure["backend"]["files"], **project_structure["frontend"]["files"]}
        
        implemented_files = 0
        for file_path, info in all_files.items():
            if info.get('has_content') and not info.get('is_placeholder'):
                implemented_files += 1
        
        if implemented_files > 10:
            score += 20
        elif implemented_files > 5:
            score += 10
        
        return score
    
    def _get_file_info(self, file_path: str) -> dict:
        """Get detailed file information"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            lines = content.split('\n')
            non_empty_lines = [line for line in lines if line.strip() and not line.strip().startswith('#') and not line.strip().startswith('//')]
            
            return {
                "size": len(content),
                "lines": len(lines),
                "non_empty_lines": len(non_empty_lines),
                "has_content": len(non_empty_lines) > 0,
                "is_placeholder": self._is_placeholder_content(content),
                "implementation_level": self._assess_implementation_level(content)
            }
        except:
            return {"size": 0, "lines": 0, "non_empty_lines": 0, "has_content": False, "is_placeholder": True, "implementation_level": "none"}
    
    def _is_placeholder_content(self, content: str) -> bool:
        """Check if content is just placeholder/boilerplate"""
        placeholder_indicators = [
            "# Add your code here",
            "# TODO: Implement",
            "// TODO: Implement", 
            "pass",
            "...",
            "# Write your code here",
            "// Write your code here",
            "return {}",
            "return null",
            "return undefined"
        ]
        content_lower = content.lower()
        return any(indicator.lower() in content_lower for indicator in placeholder_indicators)
    
    def _assess_implementation_level(self, content: str) -> str:
        """Assess how well the file is implemented"""
        if not content.strip():
            return "empty"
        
        lines = content.split('\n')
        code_lines = [line for line in lines if line.strip() and not line.strip().startswith(('#', '//'))]
        
        if len(code_lines) <= 2:
            return "skeleton"
        elif self._is_placeholder_content(content):
            return "placeholder"
        elif len(code_lines) > 10:
            return "implemented"
        else:
            return "partial"
    
    def create_task(self) -> Task:
        project_structure = self._scan_project_structure()
        
        return Task(
            description=f"""
            Perform INTELLIGENT PROJECT COMPLETION review for: {self.project_brief}
            
            CURRENT PROJECT ANALYSIS:
            - Completeness Score: {project_structure['analysis']['completeness_score']}/100
            - Missing Architectural Patterns: {project_structure['analysis']['missing_patterns']}
            - Backend Structure: {json.dumps(project_structure['backend']['categories'], indent=2)}
            - Frontend Structure: {json.dumps(project_structure['frontend']['categories'], indent=2)}
            
            PROJECT BRIEF: {self.project_brief}
            
            ORIGINAL SPECIFICATIONS:
            Backend: {self.specifications.get('backend_spec', 'N/A')}
            Frontend: {self.specifications.get('frontend_spec', 'N/A')}
            
            **INTELLIGENT COMPLETION STRATEGY:**
            
            ANALYZE the current structure and:
            1. Identify missing architectural layers based on the project domain
            2. Complete partial implementations
            3. Replace placeholder code with functional implementations
            4. Ensure all generated code actually works for the intended purpose
            
            **COMPLETION GUIDELINES:**
            
            For Backend Completion:
            - If routers exist but are empty, implement proper endpoint handlers
            - If models exist but no services, create business logic layer
            - If schemas exist but no validation, add proper Pydantic validation
            - Ensure database operations are properly implemented
            - Add authentication if the project requires user management
            
            For Frontend Completion:
            - If components exist but are empty, implement actual UI logic
            - If services exist but are incomplete, add proper API integration
            - If state management exists but unused, connect it to components
            - Create missing pages/views based on the application flow
            - Ensure proper TypeScript types and error handling
            
            **ACTION PRINCIPLES:**
            - Analyze WHAT exists before deciding WHAT to create
            - Complete existing implementations before creating new files
            - Focus on making the current structure functional
            - Ensure the final result actually runs and delivers value
            
            Use your expertise to determine what completion means for THIS specific project structure.
            """,
            agent=self.review_agent,
            expected_output="""
            INTELLIGENT COMPLETION REPORT:
            
            1. STRUCTURE ANALYSIS: What the current project contained
            2. COMPLETION STRATEGY: How you approached finishing the project
            3. IMPLEMENTATIONS ADDED: Specific functionality completed
            4. ARCHITECTURE ENHANCED: Missing patterns you addressed
            5. FUNCTIONALITY ACHIEVED: What the project can now do
            6. READINESS ASSESSMENT: How complete the project is now
            
            Focus on the INTELLIGENT decisions you made based on the existing structure.
            """
        )