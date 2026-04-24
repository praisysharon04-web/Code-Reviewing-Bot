"""
src/llm_provider.py - LLM API handlers
Free option: MockProvider uses smart rule-based analysis (no API key needed!)
Paid options: OpenAI, Claude, Hugging Face
"""
import os
import re
import ast
import json
from abc import ABC, abstractmethod
from typing import Optional


class LLMProvider(ABC):
    """Base class for LLM providers"""
    @abstractmethod
    async def generate(self, prompt: str, max_tokens: int = 1000) -> str:
        pass


class MockProvider(LLMProvider):
    """
    Completely FREE rule-based code reviewer.
    No API key, no internet, no cost — works 100% offline.
    Analyzes your actual code and gives real feedback.
    """

    async def generate(self, prompt: str, max_tokens: int = 1000) -> str:
        code = self._extract_code(prompt)
        lang = self._detect_lang(prompt)
        return self._analyze_code(code, lang)

    def _extract_code(self, prompt: str) -> str:
        match = re.search(r'```(?:\w+)?\n(.*?)```', prompt, re.DOTALL)
        if match:
            return match.group(1).strip()
        if "CODE TO REVIEW:" in prompt:
            return prompt.split("CODE TO REVIEW:")[-1].strip()
        return prompt.strip()

    def _detect_lang(self, prompt: str) -> str:
        for lang in ["python", "javascript", "java", "cpp", "rust", "go", "typescript"]:
            if lang in prompt.lower():
                return lang
        return "unknown"

    def _analyze_code(self, code: str, lang: str) -> str:
        lines = code.split("\n")
        issues = []
        suggestions = []
        security_issues = []
        recommendations = []
        improvements = []
        refactoring = []

        # ── General checks ──────────────────────────────────────────
        long_lines = [i+1 for i, l in enumerate(lines) if len(l) > 100]
        if long_lines:
            issues.append(f"Lines {long_lines[:3]} exceed 100 characters — consider breaking them up")

        todos = [i+1 for i, l in enumerate(lines) if re.search(r'\b(TODO|FIXME|HACK|XXX)\b', l, re.I)]
        if todos:
            issues.append(f"Unresolved TODO/FIXME found at line(s) {todos[:3]}")

        if re.search(r'(password|secret|api_key|token|passwd)\s*=\s*["\'].+["\']', code, re.I):
            security_issues.append("Hardcoded secret/password detected — use environment variables instead")

        magic = re.findall(r'(?<!["\'\w])\b(?!0|1)\d{2,}\b(?!["\'\w])', code)
        if len(magic) > 2:
            suggestions.append("Magic numbers detected — extract them into named constants")

        func_lengths = self._get_function_lengths(lines, lang)
        long_funcs = [f for f, l in func_lengths.items() if l > 30]
        if long_funcs:
            issues.append(f"Function(s) {long_funcs[:2]} are too long (>30 lines) — split into smaller functions")

        deep_nest = [i+1 for i, l in enumerate(lines) if len(l) - len(l.lstrip()) >= 16]
        if deep_nest:
            issues.append(f"Deep nesting at line(s) {deep_nest[:3]} — consider early returns or helper functions")

        non_empty = [l.strip() for l in lines if l.strip()]
        dupes = set(l for l in non_empty if non_empty.count(l) > 1 and len(l) > 10)
        if dupes:
            issues.append(f"Duplicate code: '{list(dupes)[0][:40]}' — extract to a function")

        if re.search(r'except\s*:', code) or re.search(r'catch\s*\(\w+\)\s*\{\s*\}', code):
            security_issues.append("Empty except/catch block — always handle or log exceptions")

        if lang == "python" and re.search(r'\bprint\s*\(', code):
            suggestions.append("Found print() statements — use logging module for production code")

        if lang in ["javascript", "typescript"] and "console.log" in code:
            suggestions.append("Found console.log() — remove before production")

        # ── Python-specific ──────────────────────────────────────────
        if lang == "python":
            funcs_without_docs = self._python_missing_docstrings(code)
            if funcs_without_docs:
                suggestions.append(f"Functions missing docstrings: {funcs_without_docs[:3]}")

            if re.search(r'def \w+\([^)]*=\s*[\[\{]', code):
                security_issues.append("Mutable default argument (e.g. def f(x=[])) — use None instead")

            funcs = re.findall(r'def (\w+)\(', code)
            typed = re.findall(r'def \w+\([^)]*:\s*\w', code)
            if funcs and len(typed) < len(funcs) // 2:
                suggestions.append("Many functions missing type hints — add them for better readability")

            if re.search(r'except\s*:', code):
                issues.append("Bare 'except:' clause — catch specific exceptions instead")

            if re.search(r'^global\s+\w+', code, re.MULTILINE):
                suggestions.append("Global variables detected — consider using classes or parameters")

        # ── JavaScript/TypeScript ────────────────────────────────────
        if lang in ["javascript", "typescript"]:
            if "var " in code:
                suggestions.append("'var' used — prefer 'const' or 'let'")
            if "==" in code and "===" not in code:
                issues.append("Using '==' instead of '===' — use strict equality")
            if re.search(r'eval\s*\(', code):
                security_issues.append("eval() detected — dangerous, avoid using it")

        # ── Java ─────────────────────────────────────────────────────
        if lang == "java":
            if re.search(r'catch\s*\(\s*Exception\s+', code):
                suggestions.append("Catching generic Exception — catch specific exceptions")
            if "System.out.println" in code:
                suggestions.append("Use a logger instead of System.out.println")

        # ── Scoring ──────────────────────────────────────────────────
        score = 10
        score -= min(len(issues) * 1.5, 5)
        score -= min(len(security_issues) * 2, 4)
        score = max(1, round(score))

        severity = "none"
        if security_issues:
            severity = "high" if len(security_issues) >= 2 else "medium"
        elif issues:
            severity = "low"

        branch_keywords = len(re.findall(r'\b(if|elif|else|for|while|case|catch|except|and|or)\b', code))
        cyclomatic = "low" if branch_keywords <= 3 else "medium" if branch_keywords <= 10 else "high"

        readability = 10
        if long_lines: readability -= 1
        if deep_nest: readability -= 2
        readability = max(1, readability)

        what_it_does = self._summarize_code(code, lang, lines)
        time_complexity, space_complexity = self._estimate_complexity(code)

        if not improvements:
            improvements.append("Add input validation at function boundaries")
        if time_complexity != "O(1)":
            improvements.append(f"Time complexity is {time_complexity} — check if optimizable")
        if not refactoring:
            refactoring.append("Consider adding unit tests for each function")
        if long_funcs:
            refactoring.append("Break long functions into smaller single-responsibility functions")
        if not suggestions:
            suggestions.append("Code looks clean! Consider adding more inline comments")
        if not recommendations:
            recommendations.append("Add logging for important operations")
            recommendations.append("Consider edge cases: empty input, None values, large datasets")

        return json.dumps({
            "code_quality": {
                "score": score,
                "issues": issues if issues else ["No major issues found"],
                "suggestions": suggestions
            },
            "bugs_security": {
                "severity": severity,
                "issues": security_issues if security_issues else ["No security issues detected"],
                "recommendations": recommendations
            },
            "explanation": {
                "what_it_does": what_it_does,
                "main_purpose": f"A {lang} program with {len(lines)} lines and {len(re.findall(r'def |function |func ', code))} function(s)"
            },
            "optimization": {
                "time_complexity": time_complexity,
                "space_complexity": space_complexity,
                "improvements": improvements
            },
            "complexity": {
                "cyclomatic_complexity": cyclomatic,
                "readability_score": readability,
                "refactoring_suggestions": refactoring
            }
        })

    def _python_missing_docstrings(self, code: str):
        missing = []
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    if not (node.body and isinstance(node.body[0], ast.Expr) and
                            isinstance(node.body[0].value, ast.Constant)):
                        missing.append(node.name)
        except Exception:
            funcs = re.findall(r'def (\w+)\(', code)
            doc_funcs = re.findall(r'def \w+[^:]+:\s*"""', code)
            missing = funcs[len(doc_funcs):]
        return missing

    def _get_function_lengths(self, lines, lang):
        lengths = {}
        current_func = None
        start = 0
        for i, line in enumerate(lines):
            if re.match(r'\s*(def |function |func |public |private |protected )\w+', line):
                if current_func:
                    lengths[current_func] = i - start
                m = re.search(r'(\w+)\s*\(', line)
                current_func = m.group(1) if m else f"func_{i}"
                start = i
        if current_func:
            lengths[current_func] = len(lines) - start
        return lengths

    def _estimate_complexity(self, code: str):
        nested_loops = len(re.findall(r'for .* in .*:\s*\n(?:.*\n)*?.*for .* in ', code))
        loops = len(re.findall(r'\b(for|while)\b', code))
        recursion = bool(re.search(r'def (\w+).*\n(?:.*\n)*?.*\1\(', code))

        if nested_loops >= 2:
            time_c = "O(n³) or worse"
        elif nested_loops == 1:
            time_c = "O(n²)"
        elif recursion:
            time_c = "O(2^n) worst case — check for memoization"
        elif loops > 0:
            time_c = "O(n)"
        else:
            time_c = "O(1)"

        lists = len(re.findall(r'\[\]|\{\}|list\(|dict\(|set\(', code))
        space_c = "O(n)" if lists > 3 else "O(1)"
        return time_c, space_c

    def _summarize_code(self, code: str, lang: str, lines) -> str:
        funcs = re.findall(r'def (\w+)|function (\w+)|func (\w+)', code)
        func_names = [next(f for f in func if f) for func in funcs]
        classes = re.findall(r'class (\w+)', code)
        parts = []
        if classes:
            parts.append(f"Defines class(es): {', '.join(classes[:3])}")
        if func_names:
            parts.append(f"Contains function(s): {', '.join(func_names[:5])}")
        if re.search(r'import|require|use ', code):
            parts.append("Imports external dependencies")
        if re.search(r'open\(|read\(|write\(|File', code):
            parts.append("Performs file I/O operations")
        if re.search(r'requests\.|fetch\(|http|axios', code, re.I):
            parts.append("Makes HTTP/network requests")
        if re.search(r'SELECT|INSERT|UPDATE|DELETE', code, re.I):
            parts.append("Contains database queries")
        return " | ".join(parts) if parts else f"A {lang} script with {len(lines)} lines"


class OpenAIProvider(LLMProvider):
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self.api_url = "https://api.openai.com/v1/chat/completions"
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")

    async def generate(self, prompt: str, max_tokens: int = 1000) -> str:
        import aiohttp
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        payload = {"model": self.model, "messages": [{"role": "user", "content": prompt}],
                   "max_tokens": max_tokens, "temperature": 0.3}
        async with aiohttp.ClientSession() as session:
            async with session.post(self.api_url, json=payload, headers=headers) as resp:
                if resp.status != 200:
                    raise Exception(f"OpenAI API error: {resp.status}")
                data = await resp.json()
                return data["choices"][0]["message"]["content"]


class ClaudeProvider(LLMProvider):
    def __init__(self, api_key: Optional[str] = None, model: str = "claude-sonnet-4-20250514"):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.model = model
        self.api_url = "https://api.anthropic.com/v1/messages"
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")

    async def generate(self, prompt: str, max_tokens: int = 1000) -> str:
        import aiohttp
        headers = {"x-api-key": self.api_key, "anthropic-version": "2023-06-01",
                   "content-type": "application/json"}
        payload = {"model": self.model, "max_tokens": max_tokens,
                   "messages": [{"role": "user", "content": prompt}]}
        async with aiohttp.ClientSession() as session:
            async with session.post(self.api_url, json=payload, headers=headers) as resp:
                if resp.status != 200:
                    raise Exception(f"Claude API error: {resp.status}")
                data = await resp.json()
                return data["content"][0]["text"]


class HuggingFaceProvider(LLMProvider):
    def __init__(self, api_key: Optional[str] = None, model: str = "mistralai/Mistral-7B-Instruct-v0.1"):
        self.api_key = api_key or os.getenv("HUGGINGFACE_API_KEY")
        self.model = model
        self.api_url = f"https://api-inference.huggingface.co/models/{model}"
        if not self.api_key:
            raise ValueError("HUGGINGFACE_API_KEY not found in environment variables")

    async def generate(self, prompt: str, max_tokens: int = 1000) -> str:
        import aiohttp
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {"inputs": prompt, "parameters": {"max_new_tokens": max_tokens, "temperature": 0.3}}
        async with aiohttp.ClientSession() as session:
            async with session.post(self.api_url, json=payload, headers=headers) as resp:
                if resp.status != 200:
                    raise Exception(f"Hugging Face API error: {resp.status}")
                data = await resp.json()
                if isinstance(data, list):
                    return data[0].get("generated_text", "")
                return data.get("generated_text", "")


def get_llm_provider(provider_type: str = "mock", **kwargs) -> LLMProvider:
    providers = {
        "openai": OpenAIProvider,
        "claude": ClaudeProvider,
        "huggingface": HuggingFaceProvider,
        "mock": MockProvider
    }
    if provider_type not in providers:
        raise ValueError(f"Unknown provider: {provider_type}")
    if provider_type == "mock":
        return MockProvider()
    return providers[provider_type](**kwargs)