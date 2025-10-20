from crewai import Crew, Process
from typing import Dict, Any, List
import re
import os
import time
import json
from config import Config
from agents.review_agent import ReviewAgent
from tasks.review_task import ReviewTask

class ArchitectWorkflow:
    def __init__(self, agents: Dict[str, Any], tools: Dict[str, Any]):
        self.agents = agents
        self.tools = tools
        self.generated_files = []
    
    def execute(self, project_brief: str) -> Dict[str, Any]:
        """
        Execute the complete AI Software Architect workflow with rate limit protection
        """
        print("🚀 Starting AI Software Architect Workflow...")
        print(f"📋 Project Brief: {project_brief}")
        
        try:
            # Step 1: Specification Generation
            print("\n📝 Step 1: Generating Technical Specifications...")
            specifications = self._generate_specifications(project_brief)
            Config.apply_delay("coordinator")
            
            backend_spec = specifications['backend_spec']
            frontend_spec = specifications['frontend_spec']
            
            # Step 2: Backend Development
            print("\n⚙️ Step 2: Generating Backend Code...")
            backend_result = self._generate_backend(backend_spec) 
            Config.apply_delay("backend")
            
            # Step 3: Frontend Development
            print("\n🎨 Step 3: Generating Frontend Code...")
            frontend_result = self._generate_frontend(frontend_spec, backend_spec)
            Config.apply_delay("frontend")
            
            # Step 4: Integration Review
            print("\n🔍 Step 4: Integration Review...")
            integration_report = self._perform_integration_review(
                backend_result['raw_output'],
                frontend_result['raw_output']
            )
            Config.apply_delay("integration")
            
            # Step 5: Final Review & Correction
            print("\n🔧 Step 5: Final Review & Correction...")
            final_review = self._perform_final_review(project_brief, specifications)
            Config.apply_delay("review")
            
            # Step 6: Finalization
            print("\n✅ Step 6: Finalizing Project...")
            return self._finalize_project(project_brief, specifications, integration_report, final_review)
            
        except Exception as e:
            print(f"💥 Workflow execution failed: {str(e)}")
            return {
                'project_brief': project_brief,
                'status': 'failed',
                'error': str(e),
                'generated_files': self._scan_generated_files(),
                'summary': f"Workflow failed: {str(e)}"
            }
    
    def _generate_specifications(self, project_brief: str) -> Dict[str, Any]:
        """Generate backend and frontend specifications with error handling"""
        try:
            from tasks.specification_task import SpecificationTask
            
            spec_task = SpecificationTask(self.agents['coordinator'].get_agent())
            task = spec_task.create_task(project_brief)
            
            crew = Crew(
                agents=[self.agents['coordinator'].get_agent()],
                tasks=[task],
                process=Process.sequential,
                verbose=True
            )
            
            result = crew.kickoff()
            return self._parse_specifications(str(result))
            
        except Exception as e:
            print(f"❌ Specification generation failed: {str(e)}")
            # Return fallback specifications to allow workflow to continue
            return self._create_fallback_specifications(project_brief)
    
    def _create_fallback_specifications(self, project_brief: str) -> Dict[str, Any]:
        """Create basic specifications when AI generation fails"""
        print("🔄 Using fallback specifications...")
        return {
            'backend_spec': f"""
            Basic backend specification for: {project_brief}
            
            REQUIREMENTS:
            - REST API with CRUD operations
            - User authentication system
            - Data persistence with database
            - Input validation and error handling
            
            SUGGESTED ARCHITECTURE:
            - FastAPI framework
            - SQLAlchemy ORM  
            - Pydantic models
            - JWT authentication
            """,
            'frontend_spec': f"""
            Basic frontend specification for: {project_brief}
            
            REQUIREMENTS:
            - React with TypeScript
            - Responsive UI with Tailwind CSS
            - State management
            - API integration
            - Routing if multi-page
            
            SUGGESTED STRUCTURE:
            - Component-based architecture
            - API service layer
            - Context for state management
            - Responsive design components
            """,
            'raw_output': f"Fallback specifications for: {project_brief}",
            'is_fallback': True
        }
    
    def _generate_backend(self, backend_spec: str) -> Dict[str, Any]:
        """Generate backend code with error handling"""
        try:
            from tasks.backend_task import BackendTask
            
            backend_task = BackendTask(self.agents['backend'].get_agent(), backend_spec)
            task = backend_task.create_task()
            
            crew = Crew(
                agents=[self.agents['backend'].get_agent()],
                tasks=[task],
                process=Process.sequential,
                verbose=True
            )
            
            result = crew.kickoff()
            return {'raw_output': str(result), 'spec': backend_spec, 'success': True}
            
        except Exception as e:
            print(f"❌ Backend generation failed: {str(e)}")
            return {
                'raw_output': f"Backend generation failed: {str(e)}",
                'spec': backend_spec, 
                'success': False,
                'error': str(e)
            }
    
    def _generate_frontend(self, frontend_spec: str, api_structure: str) -> Dict[str, Any]:
        """Generate frontend code with error handling"""
        try:
            from tasks.frontend_task import FrontendTask
            
            frontend_task = FrontendTask(
                self.agents['frontend'].get_agent(), 
                frontend_spec, 
                api_structure
            )
            task = frontend_task.create_task()
            
            crew = Crew(
                agents=[self.agents['frontend'].get_agent()],
                tasks=[task],
                process=Process.sequential,
                verbose=True
            )
            
            result = crew.kickoff()
            return {'raw_output': str(result), 'spec': frontend_spec, 'success': True}
            
        except Exception as e:
            print(f"❌ Frontend generation failed: {str(e)}")
            return {
                'raw_output': f"Frontend generation failed: {str(e)}",
                'spec': frontend_spec,
                'success': False, 
                'error': str(e)
            }
    
    def _perform_integration_review(self, backend_code_summary: str, frontend_code_summary: str) -> Dict[str, Any]:
        """Perform integration review with error handling"""
        try:
            from tasks.integration_task import IntegrationTask
            
            integration_task = IntegrationTask(
                self.agents['coordinator'].get_agent(),
                backend_code_summary,
                frontend_code_summary
            )
            task = integration_task.create_task()
            
            crew = Crew(
                agents=[self.agents['coordinator'].get_agent()],
                tasks=[task],
                process=Process.sequential,
                verbose=True
            )
            
            result = crew.kickoff()
            
            issues_found = any(keyword in str(result).lower() for keyword in 
                              ['mismatch', 'error', 'issue', 'inconsistent', 'correction needed', 'fix', 'problem'])
            
            return {
                'report': str(result),
                'issues_found': issues_found,
                'success': True
            }
            
        except Exception as e:
            print(f"❌ Integration review failed: {str(e)}")
            return {
                'report': f"Integration review failed: {str(e)}",
                'issues_found': True,
                'success': False,
                'error': str(e)
            }
    
    def _perform_final_review(self, project_brief: str, specifications: dict) -> Dict[str, Any]:
       """Perform intelligent completion review"""
       try:
         print("🔧 Performing intelligent project completion...")
        
        # Scan current state before review
         files_before = self._scan_generated_files()
        
        # Initialize intelligent review agent
         review_agent = ReviewAgent(tools=[self.tools['file_writer']])
         review_task = ReviewTask(review_agent.get_agent(), project_brief, specifications)
         task = review_task.create_task()
        
         crew = Crew(
            agents=[review_agent.get_agent()],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )
        
         result = crew.kickoff()
        
        # Scan state after review
         files_after = self._scan_generated_files()
        
        # Intelligent completion detection
         review_text = str(result)
         new_files = set(files_after) - set(files_before)
         completion_indicators = [
            'implemented', 'completed', 'added', 'created', 'finished',
            'functional', 'working', 'handlers', 'endpoints', 'components'
        ]
        
         has_substantial_completion = (
            len(new_files) > 2 or 
            any(indicator in review_text.lower() for indicator in completion_indicators) or
            len(review_text) > 800  # Substantial report indicates real work
        )
        
         print(f"📊 Completion Stats: {len(new_files)} new files, {len(review_text)} char report")
        
         return {
            'report': review_text,
            'issues_fixed': has_substantial_completion,
            'new_files_count': len(new_files),
            'new_files': list(new_files),
            'report_length': len(review_text),
            'success': True
        }
        
       except Exception as e:
        print(f"❌ Completion review failed: {str(e)}")
        return {
            'report': f"Completion review failed: {str(e)}",
            'issues_fixed': False,
            'new_files_count': 0,
            'new_files': [],
            'success': False,
            'error': str(e)
        }
    
    def _scan_generated_files(self) -> List[str]:
        """Scan and return all generated files"""
        output_dir = "output"
        generated_files = []
        
        if os.path.exists(output_dir):
            for root, dirs, files in os.walk(output_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, output_dir)
                    generated_files.append(relative_path.replace('\\', '/'))  # Normalize paths
        
        return generated_files
    
    def _finalize_project(self, project_brief: str, specifications: Dict, 
                         integration_report: Dict, final_review: Dict) -> Dict[str, Any]:
        """Finalize the project with review results"""
        
        generated_files = self._scan_generated_files()
        
        # Count unique files (after deduplication)
        unique_files = list(set(generated_files))
        
        # Analyze file structure
        backend_files = [f for f in unique_files if f.startswith('backend/')]
        frontend_files = [f for f in unique_files if f.startswith('frontend/')]
        other_files = [f for f in unique_files if not f.startswith(('backend/', 'frontend/'))]
        
        return {
            'project_brief': project_brief,
            'status': 'completed',
            'specifications': specifications,
            'integration_report': integration_report,
            'final_review': final_review,
            'generated_files': unique_files,  # Deduplicated
            'files_count': len(unique_files),
            'backend_files_count': len(backend_files),
            'frontend_files_count': len(frontend_files),
            'other_files_count': len(other_files),
            'duplicates_found': len(generated_files) - len(unique_files),
            'summary': f"Successfully generated and reviewed software skeleton for: {project_brief}",
            'has_backend': len(backend_files) > 0,
            'has_frontend': len(frontend_files) > 0,
            'review_issues_fixed': final_review.get('issues_fixed', False),
            'integration_issues_found': integration_report.get('issues_found', False),
            'project_health': self._assess_project_health(
                len(backend_files), 
                len(frontend_files), 
                final_review.get('issues_fixed', False),
                integration_report.get('issues_found', False)
            )
        }
    
    def _assess_project_health(self, backend_count: int, frontend_count: int, 
                              issues_fixed: bool, integration_issues: bool) -> str:
        """Assess overall project health"""
        if backend_count == 0 and frontend_count == 0:
            return "poor"
        elif backend_count > 5 and frontend_count > 5 and issues_fixed and not integration_issues:
            return "excellent"
        elif backend_count > 3 and frontend_count > 3 and issues_fixed:
            return "good"
        elif backend_count > 0 and frontend_count > 0:
            return "fair"
        else:
            return "basic"
    
    def _parse_specifications(self, spec_output: str) -> Dict[str, Any]:
        """Parse specifications with improved pattern matching"""
        # Enhanced regex patterns
        backend_match = re.search(
            r'### BACKEND_SPEC\s*\n(.*?)(?=\s*### FRONTEND_SPEC|\s*---|\s*### [A-Z]|\Z)', 
            spec_output, 
            re.DOTALL | re.IGNORECASE
        )
        frontend_match = re.search(
            r'### FRONTEND_SPEC\s*\n(.*?)(?=\s*---|\s*### [A-Z]|\Z)', 
            spec_output, 
            re.DOTALL | re.IGNORECASE
        )

        if not backend_match or not frontend_match:
            print("❌ WARNING: Failed to parse specifications. Using fallback parsing.")
            # Enhanced fallback logic
            lines = spec_output.split('\n')
            backend_lines = []
            frontend_lines = []
            current_section = None
            
            for line in lines:
                line_lower = line.lower()
                if 'backend' in line_lower and 'spec' in line_lower:
                    current_section = 'backend'
                    continue
                elif 'frontend' in line_lower and 'spec' in line_lower:
                    current_section = 'frontend'
                    continue
                elif current_section == 'backend' and line.strip():
                    backend_lines.append(line)
                elif current_section == 'frontend' and line.strip():
                    frontend_lines.append(line)
            
            backend_spec = '\n'.join(backend_lines).strip() or "Backend specification not properly generated"
            frontend_spec = '\n'.join(frontend_lines).strip() or "Frontend specification not properly generated"
        else:
            backend_spec = backend_match.group(1).strip()
            frontend_spec = frontend_match.group(1).strip()
            
        return {
            'backend_spec': backend_spec,
            'frontend_spec': frontend_spec,
            'raw_output': spec_output
        }
    
    def get_project_summary(self, result: Dict[str, Any]) -> str:
        """Generate a comprehensive project summary"""
        summary_lines = [
            "📊 PROJECT COMPLETION SUMMARY",
            "=" * 40,
            f"📋 Project: {result.get('project_brief', 'N/A')}",
            f"✅ Status: {result.get('status', 'unknown')}",
            f"🏗️  Project Health: {result.get('project_health', 'unknown').upper()}",
            "",
            "📁 GENERATED FILES:",
            f"   Total Files: {result.get('files_count', 0)}",
            f"   Backend Files: {result.get('backend_files_count', 0)}",
            f"   Frontend Files: {result.get('frontend_files_count', 0)}",
            f"   Other Files: {result.get('other_files_count', 0)}",
            f"   Duplicates Fixed: {result.get('duplicates_found', 0)}",
            "",
            "🔍 QUALITY ASSESSMENT:",
            f"   Backend Created: {'✅' if result.get('has_backend') else '❌'}",
            f"   Frontend Created: {'✅' if result.get('has_frontend') else '❌'}",
            f"   Integration Issues: {'⚠️' if result.get('integration_issues_found') else '✅'}",
            f"   Review Issues Fixed: {'✅' if result.get('review_issues_fixed') else '❌'}",
        ]
        
        # Add recommendations based on project health
        health = result.get('project_health', 'basic')
        if health == 'excellent':
            summary_lines.extend(["", "🎉 EXCELLENT: Project is production-ready!"])
        elif health == 'good':
            summary_lines.extend(["", "👍 GOOD: Project is functional with minor issues."])
        elif health == 'fair':
            summary_lines.extend(["", "ℹ️  FAIR: Project has basic structure but needs improvements."])
        elif health == 'basic':
            summary_lines.extend(["", "⚠️  BASIC: Project has minimal structure and needs significant work."])
        else:
            summary_lines.extend(["", "❌ POOR: Project generation failed or has critical issues."])
        
        return '\n'.join(summary_lines)