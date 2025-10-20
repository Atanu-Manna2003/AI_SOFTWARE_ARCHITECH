import ast
from typing import Dict, Any
from crewai.tools import BaseTool

class CodeLinterTool(BaseTool):
    name: str = "Code Linter"
    description: str = "Analyzes code for syntax errors, common issues, and provides improvement suggestions"

    def _run(self, code: str, language: str = "python") -> Dict[str, Any]:
        try:
            if language.lower() in ["python", "py"]:
                return self._lint_python(code)
            elif language.lower() in ["javascript", "js", "typescript", "ts"]:
                return self._lint_javascript(code)
            else:
                return self._lint_generic(code, language)
                
        except Exception as e:
            return {
                "valid_syntax": False,
                "issues": [f"Error during linting: {str(e)}"],
                "warnings": [],
                "suggestions": []
            }
    
    def _lint_python(self, code: str) -> Dict[str, Any]:
        issues = []
        warnings = []
        suggestions = []
        
        try:
            ast.parse(code)
            syntax_valid = True
        except SyntaxError as e:
            syntax_valid = False
            issues.append(f"Syntax error: {e.msg} at line {e.lineno}")
        
        # Check for common issues
        if "import *" in code:
            warnings.append("Wildcard import detected - consider importing specific names")
        
        if len(code.split('\n')) > 100:
            suggestions.append("Consider breaking down into smaller functions/modules")
            
        return {
            "valid_syntax": syntax_valid,
            "issues": issues,
            "warnings": warnings,
            "suggestions": suggestions
        }
    
    def _lint_javascript(self, code: str) -> Dict[str, Any]:
        issues = []
        warnings = []
        suggestions = []
        
        # Basic syntax checks
        if "==" in code:
            warnings.append("Consider using strict equality (===) instead of loose equality (==)")
        
        if "var " in code:
            suggestions.append("Consider using 'let' or 'const' instead of 'var' for better scoping")
        
        # Check for console.log
        if "console.log" in code:
            warnings.append("Found console.log statements - remove for production code")
        
        # Basic bracket matching
        open_braces = code.count('{')
        close_braces = code.count('}')
        if open_braces != close_braces:
            issues.append(f"Mismatched braces: {open_braces} opening vs {close_braces} closing")
        
        return {
            "valid_syntax": True,
            "issues": issues,
            "warnings": warnings,
            "suggestions": suggestions
        }
    
    def _lint_generic(self, code: str, language: str) -> Dict[str, Any]:
        return {
            "valid_syntax": True,
            "issues": [],
            "warnings": ["Language-specific linting not available"],
            "suggestions": ["Consider running language-specific linter for detailed analysis"]
        }