import os
from pathlib import Path
from typing import Dict, Any
from crewai.tools import BaseTool
from pydantic import Field

class FileWriterTool(BaseTool):
    name: str = "File Writer"
    description: str = "Writes code files to the specified directory structure with proper path handling"
    output_dir: str = Field(default="output", description="Base directory where files will be written")

    def _run(self, file_path: str, content: str, overwrite: bool = True, subfolder: str = "") -> Dict[str, Any]:
        try:
            # Validate inputs
            if not file_path or not file_path.strip():
                return {
                    "success": False,
                    "error": "File path cannot be empty",
                    "path": ""
                }
            
            if content is None:
                content = ""
            
            # **FIX: Proper path construction to avoid double folders**
            if subfolder:
                # Clean subfolder path (remove leading/trailing slashes)
                subfolder = subfolder.strip().strip('/').strip('\\')
                output_path = Path(self.output_dir) / subfolder
            else:
                output_path = Path(self.output_dir)
            
            output_path.mkdir(parents=True, exist_ok=True)

            # **FIX: Clean file path properly**
            file_path = file_path.strip().lstrip('/').lstrip('\\')
            
            # **FIX: Prevent double subfolder names**
            if subfolder and file_path.startswith(subfolder):
                file_path = file_path[len(subfolder):].lstrip('/').lstrip('\\')
            
            full_path = output_path / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)

            if full_path.exists() and not overwrite:
                return {
                    "success": False,
                    "error": f"File {file_path} already exists and overwrite is False",
                    "path": str(full_path)
                }

            # Write file with proper encoding
            full_path.write_text(content, encoding='utf-8')

            return {
                "success": True,
                "message": f"Successfully wrote file: {file_path}",
                "path": str(full_path),
                "file_size": len(content),
                "subfolder": subfolder,
                "directory": str(output_path),
                "relative_path": f"{subfolder}/{file_path}" if subfolder else file_path
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to write file {file_path}: {str(e)}",
                "path": str(full_path) if 'full_path' in locals() else file_path
            }