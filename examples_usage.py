"""
examples/usage_examples.py

Different ways to use the Smart Code Reviewer Bot
"""

import asyncio
import json
from typing import Dict, Any


# ============ Example 1: Direct Python Usage ============

async def example_1_direct_usage():
    """
    Use the reviewer directly in Python (no API server needed)
    """
    print("=" * 50)
    print("Example 1: Direct Python Usage")
    print("=" * 50)
    
    from src_reviewer import CodeReviewer
    from src_llm_provider import get_llm_provider
    
    # Initialize with mock provider (no API key needed)
    llm_provider = get_llm_provider("mock")
    reviewer = CodeReviewer(llm_provider)
    
    # Code to review
    code = """
def bubble_sort(arr):
    for i in range(len(arr)):
        for j in range(len(arr) - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

result = bubble_sort([64, 34, 25, 12, 22, 11, 90])
print(result)
    """
    
    # Get review
    result = await reviewer.review_code(code, detailed=True)
    
    print(f"\n✅ Review Status: {result['status']}")
    print(f"📊 Detected Language: {result['detected_language']}")
    print(f"📏 Code Length: {result['code_length']} characters")
    print(f"\n📋 Review Details:")
    print(json.dumps(result['review'], indent=2))
    
    return result


# ============ Example 2: Using the FastAPI Server ============

async def example_2_api_usage():
    """
    Use the reviewer via FastAPI REST API
    Run: python api/main.py
    """
    print("\n" + "=" * 50)
    print("Example 2: REST API Usage")
    print("=" * 50)
    
    import aiohttp
    
    url = "http://localhost:8000/review"
    
    code = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
    """
    
    payload = {
        "code": code,
        "detailed": True
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                if response.status == 200:
                    result = await response.json()
                    print(f"\n✅ Review ID: {result['review_id']}")
                    print(f"📊 Detected Language: {result['detected_language']}")
                    print(f"📋 Review Details:")
                    print(json.dumps(result['review'], indent=2))
                    return result
                else:
                    print(f"❌ API Error: {response.status}")
                    print(await response.text())
    
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        print("Make sure API server is running: python api/main.py")


# ============ Example 3: Batch Processing ============

async def example_3_batch_processing():
    """
    Review multiple code snippets at once
    """
    print("\n" + "=" * 50)
    print("Example 3: Batch Processing")
    print("=" * 50)
    
    from src_reviewer import CodeReviewer
    from src_llm_provider import get_llm_provider
    
    llm_provider = get_llm_provider("mock")
    reviewer = CodeReviewer(llm_provider)
    
    codes = [
        "def hello(): print('world')",
        """
def add(a, b):
    return a + b
        """,
        """
class Calculator:
    def __init__(self):
        self.result = 0
    
    def add(self, x):
        self.result += x
    
    def get_result(self):
        return self.result
        """
    ]
    
    print(f"\nReviewing {len(codes)} code snippets...\n")
    
    results = []
    for i, code in enumerate(codes, 1):
        print(f"📝 Snippet {i}/{len(codes)}: {len(code)} chars")
        result = await reviewer.review_code(code)
        results.append({
            "snippet": i,
            "language": result.get("detected_language"),
            "status": result.get("status")
        })
        print(f"   ✅ {result.get('status')}")
    
    print(f"\n📊 Summary:")
    for r in results:
        print(f"  Snippet {r['snippet']}: {r['language']} ({r['status']})")
    
    return results


# ============ Example 4: Switching LLM Providers ============

async def example_4_switch_providers():
    """
    Show how to switch between different LLM providers
    """
    print("\n" + "=" * 50)
    print("Example 4: Switching LLM Providers")
    print("=" * 50)
    
    from src_llm_provider import get_llm_provider
    
    code = "def hello(): print('world')"
    prompt = f"Review this code: {code}"
    
    providers = ["mock"]  # Only mock works without API keys
    # To use others, add API keys to .env:
    # providers = ["mock", "openai", "claude", "huggingface"]
    
    print(f"\nProviders available: {', '.join(providers)}\n")
    
    for provider_name in providers:
        try:
            print(f"📡 Testing {provider_name.upper()} provider...")
            provider = get_llm_provider(provider_name)
            response = await provider.generate(prompt, max_tokens=100)
            print(f"   ✅ Response received ({len(response)} chars)")
            print(f"   Preview: {response[:100]}...")
        except Exception as e:
            print(f"   ❌ Error: {str(e)[:50]}...")


# ============ Example 5: Language Detection ============

async def example_5_language_detection():
    """
    Demonstrate language detection
    """
    print("\n" + "=" * 50)
    print("Example 5: Language Detection")
    print("=" * 50)
    
    from src_reviewer import CodeReviewer
    from src_llm_provider import get_llm_provider
    
    reviewer = CodeReviewer(get_llm_provider("mock"))
    
    code_samples = {
        "Python": "def hello(): print('world')",
        "JavaScript": "function hello() { console.log('world'); }",
        "Java": "public class Hello { public static void main(String[] args) {} }",
        "C++": "#include <iostream> int main() { return 0; }",
        "Go": "package main; func main() { }",
    }
    
    print("\n🔍 Detecting languages:\n")
    
    for expected_lang, code in code_samples.items():
        detected = reviewer.detect_language(code)
        status = "✅" if detected.value.lower() in expected_lang.lower() else "❌"
        print(f"{status} {expected_lang}: Detected as {detected.value}")


# ============ Example 6: Performance Analysis ============

async def example_6_performance_metrics():
    """
    Show metrics about the reviewer performance
    """
    print("\n" + "=" * 50)
    print("Example 6: Performance Metrics")
    print("=" * 50)
    
    import time
    from src_reviewer import CodeReviewer
    from src_llm_provider import get_llm_provider
    
    reviewer = CodeReviewer(get_llm_provider("mock"))
    
    code = """
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    return result
    """
    
    print(f"\n⏱️  Timing review for {len(code)} character code...\n")
    
    start = time.time()
    result = await reviewer.review_code(code, detailed=True)
    elapsed = time.time() - start
    
    print(f"⏱️  Review completed in {elapsed:.2f} seconds")
    print(f"📊 Code metrics:")
    print(f"   - Code length: {len(code)} chars")
    print(f"   - Detected language: {result.get('detected_language')}")
    print(f"   - Review size: {len(json.dumps(result.get('review', {})))} chars")
    print(f"📈 Performance: {len(code)/elapsed:.0f} chars/sec")


# ============ Example 7: Error Handling ============

async def example_7_error_handling():
    """
    Show how to handle errors gracefully
    """
    print("\n" + "=" * 50)
    print("Example 7: Error Handling")
    print("=" * 50)
    
    from src_reviewer import CodeReviewer
    from src_llm_provider import get_llm_provider
    
    reviewer = CodeReviewer(get_llm_provider("mock"))
    
    # Test cases
    test_cases = [
        ("Empty code", ""),
        ("Very long code", "x = 1\n" * 10000),
        ("Valid code", "def hello(): pass"),
    ]
    
    print("\n🧪 Testing error cases:\n")
    
    for case_name, code in test_cases:
        print(f"Test: {case_name}")
        result = await reviewer.review_code(code)
        
        if "error" in result:
            print(f"  ❌ Error: {result['error']}")
        else:
            print(f"  ✅ Success: {result.get('status')}")


# ============ Main ============

async def main():
    """Run all examples"""
    
    print("\n")
    print("🤖 Smart Code Reviewer Bot - Usage Examples")
    print("=" * 50)
    
    # Run examples
    try:
        await example_1_direct_usage()
    except Exception as e:
        print(f"Example 1 error: {e}")
    
    try:
        await example_2_api_usage()
    except Exception as e:
        print(f"Example 2 error: {e}")
    
    try:
        await example_3_batch_processing()
    except Exception as e:
        print(f"Example 3 error: {e}")
    
    try:
        await example_4_switch_providers()
    except Exception as e:
        print(f"Example 4 error: {e}")
    
    try:
        await example_5_language_detection()
    except Exception as e:
        print(f"Example 5 error: {e}")
    
    try:
        await example_6_performance_metrics()
    except Exception as e:
        print(f"Example 6 error: {e}")
    
    try:
        await example_7_error_handling()
    except Exception as e:
        print(f"Example 7 error: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Examples completed!")
    print("=" * 50 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
