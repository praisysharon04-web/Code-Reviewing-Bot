"""
ui/app.py - Streamlit web interface for Code Reviewer Bot

Run with: streamlit run ui/app.py

Features:
- Code input with syntax highlighting
- Real-time review generation
- Beautiful result visualization
- Review history
"""

import streamlit as st
import requests
import json
from datetime import datetime
import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src_reviewer import CodeReviewer
from src_llm_provider import get_llm_provider


# ============ Streamlit Configuration ============

st.set_page_config(
    page_title="Code Reviewer Bot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 1.25rem;
    }
    .code-box {
        background-color: #f0f0f0;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #0066cc;
    }
    .issue {
        background-color: #ffe6e6;
        padding: 0.5rem;
        border-radius: 0.25rem;
        margin: 0.5rem 0;
        color: #8b0000 !important;
        font-weight: 500;
    }
    .suggestion {
        background-color: #e6f2ff;
        padding: 0.5rem;
        border-radius: 0.25rem;
        margin: 0.5rem 0;
        color: #003366 !important;
        font-weight: 500;
    }
    .success {
        background-color: #e6ffe6;
        padding: 0.5rem;
        border-radius: 0.25rem;
        color: #1a5c1a !important;
        font-weight: 500;
    }
    </style>
""", unsafe_allow_html=True)


# ============ Session State ============

if "reviews_history" not in st.session_state:
    st.session_state.reviews_history = []

if "current_review" not in st.session_state:
    st.session_state.current_review = None


# ============ Initialize Reviewer ============

@st.cache_resource
def get_reviewer():
    """Initialize code reviewer (cached)"""
    try:
        llm_provider = get_llm_provider(
            os.getenv("LLM_PROVIDER", "mock")
        )
    except:
        llm_provider = get_llm_provider("mock")
    
    return CodeReviewer(llm_provider)


reviewer = get_reviewer()


# ============ Helper Functions ============

def render_review_section(title: str, content: dict, severity: str = None):
    """Render a review section with formatting"""
    st.subheader(title)
    
    if severity:
        color_map = {
            "none": " green",
            "low": " yellow",
            "medium": " orange",
            "high": " red"
        }
        st.markdown(f"**Severity:** {color_map.get(severity, severity)}")
    
    # Score if present
    if "score" in content:
        score = content["score"]
        progress = score / 10
        st.progress(progress)
        st.write(f"Score: {score}/10")
    
    # Issues
    if "issues" in content and content["issues"]:
        st.write("**Issues:**")
        for issue in content["issues"]:
            st.markdown(f'<div class="issue"> {issue}</div>', unsafe_allow_html=True)
    
    # Recommendations/Suggestions
    if "recommendations" in content and content["recommendations"]:
        st.write("**Recommendations:**")
        for rec in content["recommendations"]:
            st.markdown(f'<div class="suggestion">💡 {rec}</div>', unsafe_allow_html=True)
    
    if "suggestions" in content and content["suggestions"]:
        st.write("**Suggestions:**")
        for sug in content["suggestions"]:
            st.markdown(f'<div class="suggestion">💡 {sug}</div>', unsafe_allow_html=True)
    
    # Improvements
    if "improvements" in content and content["improvements"]:
        st.write("**Improvements:**")
        for imp in content["improvements"]:
            st.markdown(f'<div class="suggestion">💡 {imp}</div>', unsafe_allow_html=True)
    
    # Refactoring suggestions
    if "refactoring_suggestions" in content and content["refactoring_suggestions"]:
        st.write("**Refactoring Suggestions:**")
        for ref in content["refactoring_suggestions"]:
            st.markdown(f'<div class="suggestion">💡 {ref}</div>', unsafe_allow_html=True)
    
    # Main purpose
    if "what_it_does" in content:
        st.write(f"**What it does:** {content['what_it_does']}")
    
    if "main_purpose" in content:
        st.write(f"**Main purpose:** {content['main_purpose']}")


# ============ Main UI ============

st.title("🤖 Smart Code Reviewer Bot")
st.write("Get AI-powered code reviews in seconds! Paste your code and get instant feedback.")

# Tabs
tab1, tab2, tab3 = st.tabs(["Code Review", "Analytics", "History"])


# ============ Tab 1: Code Review ============

with tab1:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Input Code")
        
        code_input = st.text_area(
            "Paste your code here:",
            height=300,
            placeholder="def hello():\n    print('Hello, World!')",
            key="code_input"
        )
        
        detailed = st.checkbox("Detailed review", value=True)
        review_button = st.button("Review Code", use_container_width=True)
    
    with col2:
        st.subheader("Settings")
        
        llm_choice = st.selectbox(
            "LLM Provider",
            ["Mock (Free, for testing)", "OpenAI", "Claude", "Hugging Face"],
            help="Mock = no API key needed, perfect for testing"
        )
        
        if llm_choice != "Mock (Free, for testing)":
            st.info("Make sure your API key is set in environment variables")
        
        st.write("---")
        st.markdown("**Tips for best results:**")
        st.markdown("""
        - Keep code snippets under 10,000 characters
        - Include complete, runnable examples
        - Remove sensitive information
        - Use standard indentation
        """)


# ============ Handle Review ============

if review_button:
    if not code_input.strip():
        st.error("Please paste some code first!")
    else:
        with st.spinner("Analyzing your code..."):
            try:
                # Run review
                result = asyncio.run(reviewer.review_code(code_input, detailed=detailed))
                
                st.session_state.current_review = {
                    "code": code_input,
                    "result": result,
                    "timestamp": datetime.now().isoformat()
                }
                
                # Store in history
                st.session_state.reviews_history.append(st.session_state.current_review)
                
                st.success("Review completed!")
            except Exception as e:
                st.error(f"Review failed: {str(e)}")


# ============ Display Review Results ============

if st.session_state.current_review:
    st.write("---")
    st.subheader("Review Results")
    
    result = st.session_state.current_review["result"]
    
    # Show status and metadata
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Status", result.get("status", "Unknown"))
    
    with col2:
        st.metric("Language", result.get("detected_language", "Unknown").title())
    
    with col3:
        st.metric("Code Length", f"{result.get('code_length', 0)} chars")
    
    st.write("---")
    
    # Display review details
    review = result.get("review", {})
    
    if "error" in review:
        st.error(f"❌ Error: {review['error']}")
    else:
        # Code Quality
        if "code_quality" in review:
            render_review_section(
                "✨ Code Quality",
                review["code_quality"]
            )
            st.write("---")
        
        # Bugs & Security
        if "bugs_security" in review:
            render_review_section(
                "Bugs & Security",
                review["bugs_security"],
                severity=review["bugs_security"].get("severity")
            )
            st.write("---")
        
        # Explanation
        if "explanation" in review:
            st.subheader("Code Explanation")
            exp = review["explanation"]
            if "what_it_does" in exp:
                st.write(f"**What it does:** {exp['what_it_does']}")
            if "main_purpose" in exp:
                st.write(f"**Main purpose:** {exp['main_purpose']}")
            st.write("---")
        
        # Optimization
        if "optimization" in review:
            render_review_section(
                "⚡ Optimization",
                review["optimization"]
            )
            st.write("---")
        
        # Complexity
        if "complexity" in review:
            opt = review["complexity"]
            st.subheader("Complexity Analysis")
            
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Cyclomatic Complexity:** {opt.get('cyclomatic_complexity', 'N/A')}")
                st.write(f"**Readability Score:** {opt.get('readability_score', 'N/A')}/10")
            
            if "refactoring_suggestions" in opt:
                st.write("**Refactoring Suggestions:**")
                for sug in opt["refactoring_suggestions"]:
                    st.markdown(f"- {sug}")


# ============ Tab 2: Analytics ============

with tab2:
    st.subheader("Review Statistics")
    
    if st.session_state.reviews_history:
        total_reviews = len(st.session_state.reviews_history)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Reviews", total_reviews)
        
        with col2:
            avg_length = sum(r["result"].get("code_length", 0) 
                           for r in st.session_state.reviews_history) / total_reviews
            st.metric("Avg Code Length", f"{int(avg_length)} chars")
        
        with col3:
            languages = set(r["result"].get("detected_language", "Unknown") 
                          for r in st.session_state.reviews_history)
            st.metric("Languages Reviewed", len(languages))
        
        st.write("---")
        st.markdown("**Languages detected:**")
        lang_counts = {}
        for r in st.session_state.reviews_history:
            lang = r["result"].get("detected_language", "Unknown")
            lang_counts[lang] = lang_counts.get(lang, 0) + 1
        
        for lang, count in sorted(lang_counts.items()):
            st.write(f"- {lang.title()}: {count}")
    
    else:
        st.info("No reviews yet. Start reviewing code to see analytics!")


# ============ Tab 3: History ============

with tab3:
    st.subheader(" Review History")
    
    if st.session_state.reviews_history:
        for i, review in enumerate(reversed(st.session_state.reviews_history)):
            with st.expander(f"Review #{len(st.session_state.reviews_history) - i} - "
                           f"{review['result'].get('detected_language', 'Unknown').title()} "
                           f"({review['result'].get('code_length', 0)} chars)"):
                
                st.write("**Code reviewed:**")
                st.code(review["code"][:500] + "..." if len(review["code"]) > 500 
                       else review["code"],
                       language=review['result'].get('detected_language', 'text'))
                
                st.write(f"**Timestamp:** {review['timestamp']}")
    
    else:
        st.info("No review history yet!")
    
    # Clear history button
    if st.button("Clear History", use_container_width=True):
        st.session_state.reviews_history = []
        st.session_state.current_review = None
        st.rerun()


# ============ Footer ============

st.write("---")
st.markdown("""
<div style='text-align: center'>
    <p>Smart Code Reviewer Bot | Built with Streamlit & LLMs</p>
    <p style='font-size: 0.8rem; color: #666;'>
        For demonstration purposes. Always review AI feedback critically.
    </p>
</div>
""", unsafe_allow_html=True)
