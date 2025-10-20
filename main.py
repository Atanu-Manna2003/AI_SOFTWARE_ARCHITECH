import os
import shutil
from dotenv import load_dotenv
from agents.coordinator_agent import CoordinatorAgent
from agents.backend_agent import BackendAgent
from agents.frontend_agent import FrontendAgent
from tools.file_writer import FileWriterTool
from tools.code_linter import CodeLinterTool
from workflows.architect_workflow import ArchitectWorkflow

def setup_environment():
    """Setup output directory and ensure clean state"""
    output_dir = "output"
    
    # Create fresh output directory
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)
    print(f"📁 Created clean output directory: {output_dir}")

def main():
    # Load environment variables
    load_dotenv()
    
    if not os.getenv("GEMINI_API_KEY"):
        print("❌ Error: GEMINI_API_KEY not found in environment variables")
        print("Please create a .env file with your GEMINI_API_KEY")
        print("Get free API key from: https://aistudio.google.com/app/apikey")
        return
    
    # Setup environment
    setup_environment()
    
    print("🤖 AI Software Architect System")
    print("=" * 50)
    
    try:
        # Initialize tools
        file_writer = FileWriterTool()
        code_linter = CodeLinterTool()
        
        # Initialize agents with tools
        coordinator_agent = CoordinatorAgent(tools=[file_writer, code_linter])
        backend_agent = BackendAgent(tools=[file_writer, code_linter])
        frontend_agent = FrontendAgent(tools=[file_writer, code_linter])
        
        agents = {
            'coordinator': coordinator_agent,
            'backend': backend_agent,
            'frontend': frontend_agent
        }
        
        tools = {
            'file_writer': file_writer,
            'code_linter': code_linter
        }
        
        # Initialize workflow
        workflow = ArchitectWorkflow(agents, tools)
        
        # Project briefs
        project_briefs = [
            "Create a comprehensive food delivery platform with restaurant listings, menu management, order processing, and real-time order tracking. The system should support multiple user roles (customer, restaurant owner, delivery driver, admin) with complete order lifecycle management from browsing to delivery.",
        ]
        
        # Execute workflow for each brief
        for i, brief in enumerate(project_briefs, 1):
            print(f"\n🎯 Processing Project {i}: {brief}")
            print("-" * 60)
            
            try:
                result = workflow.execute(brief)
                
               # UPDATE THE RESULT DISPLAY SECTION:
                print(f"\n✅ Project {i} Completed!")
                print(f"📊 Status: {result['status']}")
                print(f"📁 Generated Files: {result.get('files_count', 0)}")
                print(f"🔧 Backend Created: {result.get('has_backend', False)}")
                print(f"🎨 Frontend Created: {result.get('has_frontend', False)}")
                print(f"🔄 Duplicates Fixed: {result.get('duplicates_found', 0)}")
                print(f"🔧 Review Issues Fixed: {result.get('review_issues_fixed', False)}")

# List generated files (deduplicated)
                if result.get('generated_files'):
                  print("\n📄 Clean File Structure:")
                  for file in sorted(result['generated_files']):
                    print(f"   📄 {file}")

                if result.get('final_review', {}).get('issues_fixed'):
                   print("✅ Final review completed and issues were fixed")
                else:
                  print("ℹ️  Final review completed")

                  print(f"\n📋 Summary: {result.get('summary', 'N/A')}")
            except Exception as e:
                print(f"❌ Error processing project {i}: {str(e)}")
                import traceback
                traceback.print_exc()
                continue
                
    except Exception as e:
        print(f"💥 Fatal error initializing system: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()