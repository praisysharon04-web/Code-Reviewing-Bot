"""
src/reviewer.py - Core code review logic

This module handles:
- Code language detection
- LLM prompt engineering
- Review generation
- Result formatting
"""

import re
from typing import Dict, Any
from enum import Enum


class ProgrammingLanguage(Enum):
    """Supported programming languages"""
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    JAVA = "java"
    CPLUS = "cpp"
    CSHARP = "csharp"
    GO = "go"
    RUST = "rust"
    TYPESCRIPT = "typescript"
    UNKNOWN = "unknown"


class CodeReviewer:
    """Main code reviewer class"""
    
    def __init__(self, llm_provider):
        """
        Initialize reviewer with LLM provider
        
        Args:
            llm_provider: Instance of LLM provider (OpenAI, Claude, Hugging Face, etc.)
        """
        self.llm = llm_provider
        self.review_categories = [
            "code_quality",
            "bugs_security",
            "explanation",
            "optimization",
            "complexity"
        ]
    
    def detect_language(self, code: str) -> ProgrammingLanguage:
        """
        Detect programming language from code snippet
        
        Args:
            code: Code string
            
        Returns:
            ProgrammingLanguage enum
        """
        code_lower = code.lower()
        
        # Language detection patterns
        patterns = {
            ProgrammingLanguage.PYTHON: [r"^import|^from|^def |^class ", r"print\("],
            ProgrammingLanguage.JAVASCRIPT: [r"const |let |var |function", r"console\.log"],
            ProgrammingLanguage.JAVA: [r"public class|public static void main"],
            ProgrammingLanguage.CPLUS: [r"#include|using namespace|int main\(\)"],
            ProgrammingLanguage.RUST: [r"fn main|use std|let mut"],
            ProgrammingLanguage.GO: [r"package main|func main\(\)|import \("],
            ProgrammingLanguage.TYPESCRIPT: [r": string|: number|: any|interface "],
        }
        
        for lang, patterns_list in patterns.items():
            if any(re.search(p, code_lower) for p in patterns_list):
                return lang
        
        return ProgrammingLanguage.UNKNOWN
    
    def generate_review_prompt(self, code: str, language: ProgrammingLanguage) -> str:
        """
        Generate detailed prompt for LLM to review code
        
        Args:
            code: Code to review
            language: Detected language
            
        Returns:
            Formatted prompt string
        """
        lang_name = language.value if language != ProgrammingLanguage.UNKNOWN else "code"
        
        prompt = f"""You are an expert code reviewer. Review the following {lang_name} code.

IMPORTANT: Respond ONLY with valid JSON (no markdown, no extra text). Use this exact structure:
{{
    "code_quality": {{"score": 1-10, "issues": ["issue1", "issue2"], "suggestions": ["suggestion1"]}},
    "bugs_security": {{"severity": "none/low/medium/high", "issues": ["issue1"], "recommendations": ["recommendation1"]}},
    "explanation": {{"what_it_does": "brief explanation", "main_purpose": "what the code achieves"}},
    "optimization": {{"time_complexity": "O(...)", "space_complexity": "O(...)", "improvements": ["improvement1"]}},
    "complexity": {{"cyclomatic_complexity": "low/medium/high", "readability_score": 1-10, "refactoring_suggestions": ["suggestion1"]}}
}}

CODE TO REVIEW:
```{lang_name}
{code}
```

Respond with ONLY the JSON object, no additional text."""
        
        return prompt
    
    def parse_review(self, llm_response: str) -> Dict[str, Any]:
        """
        Parse LLM response to structured review
        
        Args:
            llm_response: Raw response from LLM
            
        Returns:
            Structured review dictionary
        """
        import json
        
        try:
            # Try to extract JSON from response
            json_match = re.search(r'\{.*\}', llm_response, re.DOTALL)
            if json_match:
                review = json.loads(json_match.group())
                return review
            else:
                # Fallback if JSON not found
                return {
                    "error": "Could not parse LLM response",
                    "raw_response": llm_response[:500]
                }
        except json.JSONDecodeError as e:
            return {
                "error": f"JSON parsing failed: {str(e)}",
                "raw_response": llm_response[:500]
            }
    
    async def review_code(self, code: str, detailed: bool = True) -> Dict[str, Any]:
        """
        Main method to review code
        
        Args:
            code: Code snippet to review
            detailed: Whether to include detailed analysis
            
        Returns:
            Review result dictionary
        """
        # Validate code length
        if len(code.strip()) == 0:
            return {"error": "Empty code provided"}
        
        if len(code) > 10000:
            return {
                "error": "Code too long (max 10,000 characters)",
                "provided_length": len(code)
            }
        
        # Detect language
        language = self.detect_language(code)
        
        # Generate prompt
        prompt = self.generate_review_prompt(code, language)
        
        # Get LLM response
        try:
            llm_response = await self.llm.generate(prompt)
        except Exception as e:
            return {
                "error": f"LLM API error: {str(e)}"
            }
        
        # Parse review
        review = self.parse_review(llm_response)
        
        # Add metadata
        result = {
            "status": "success",
            "detected_language": language.value,
            "code_length": len(code),
            "review": review
        }
        
        return result


# Example usage (for testing locally)
if __name__ == "__main__":
    # Test language detection
    python_code = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
"""
    
    reviewer = CodeReviewer(None)  # Will fail without LLM provider, but shows structure
    lang = reviewer.detect_language(python_code)
    print(f"Detected language: {lang.value}")
    print(f"Prompt generated: {len(reviewer.generate_review_prompt(python_code, lang))} chars")
