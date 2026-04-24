"""
api/main.py - FastAPI server for Code Reviewer Bot

Endpoints:
- POST /review - Submit code for review
- GET /review/{review_id} - Get review result
- GET /health - Health check
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import uuid
import json
import os
import asyncio
from datetime import datetime
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src_reviewer import CodeReviewer
from src_llm_provider import get_llm_provider


# ============ Data Models ============

class ReviewRequest(BaseModel):
    """Request model for code review"""
    code: str
    language: Optional[str] = None  # Optional hint about language
    detailed: bool = True


class ReviewResponse(BaseModel):
    """Response model for code review"""
    review_id: str
    status: str
    detected_language: str
    code_length: int
    review: Dict[str, Any]
    timestamp: str


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str


# ============ Initialize FastAPI ============

app = FastAPI(
    title="Smart Code Reviewer Bot",
    description="AI-powered code review service",
    version="1.0.0"
)

# Add CORS middleware (allows requests from web UIs)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
try:
    # Try to use real LLM provider, fall back to mock
    llm_provider = get_llm_provider(
        os.getenv("LLM_PROVIDER", "mock")
    )
except Exception as e:
    print(f"Warning: Could not initialize LLM provider: {e}")
    print("Falling back to mock provider...")
    llm_provider = get_llm_provider("mock")

reviewer = CodeReviewer(llm_provider)

# In-memory storage for reviews (use database in production)
reviews_store: Dict[str, Dict[str, Any]] = {}


# ============ API Endpoints ============

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        version="1.0.0"
    )


@app.post("/review", response_model=ReviewResponse)
async def submit_review(request: ReviewRequest):
    """
    Submit code for review
    
    Args:
        request: ReviewRequest with code snippet
        
    Returns:
        ReviewResponse with review results
        
    Example:
        POST /review
        {
            "code": "def hello(): print('world')",
            "detailed": true
        }
    """
    # Validate request
    if not request.code or len(request.code.strip()) == 0:
        raise HTTPException(status_code=400, detail="Code cannot be empty")
    
    if len(request.code) > 10000:
        raise HTTPException(
            status_code=400,
            detail="Code too long (max 10,000 characters)"
        )
    
    # Generate unique review ID
    review_id = str(uuid.uuid4())[:8]
    
    try:
        # Perform review
        result = await reviewer.review_code(
            code=request.code,
            detailed=request.detailed
        )
        
        # Prepare response
        response = ReviewResponse(
            review_id=review_id,
            status=result.get("status", "completed"),
            detected_language=result.get("detected_language", "unknown"),
            code_length=result.get("code_length", 0),
            review=result.get("review", {}),
            timestamp=datetime.utcnow().isoformat()
        )
        
        # Store review (for later retrieval)
        reviews_store[review_id] = response.dict()
        
        return response
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Review failed: {str(e)}"
        )


@app.get("/review/{review_id}")
async def get_review(review_id: str):
    """
    Retrieve a previously submitted review
    
    Args:
        review_id: ID of the review
        
    Returns:
        Review details
    """
    if review_id not in reviews_store:
        raise HTTPException(status_code=404, detail="Review not found")
    
    return reviews_store[review_id]


@app.get("/reviews")
async def list_reviews(limit: int = 10):
    """
    List recent reviews
    
    Args:
        limit: Maximum number of reviews to return
        
    Returns:
        List of recent reviews
    """
    # Return last N reviews
    recent = dict(list(reviews_store.items())[-limit:])
    return {
        "total": len(reviews_store),
        "returned": len(recent),
        "reviews": recent
    }


@app.post("/batch-review")
async def batch_review(codes: list[str]):
    """
    Batch review multiple code snippets
    
    Args:
        codes: List of code snippets
        
    Returns:
        List of review results
    """
    if len(codes) > 100:
        raise HTTPException(
            status_code=400,
            detail="Batch size too large (max 100)"
        )
    
    results = []
    for code in codes:
        result = await reviewer.review_code(code)
        results.append(result)
    
    return {
        "total": len(codes),
        "results": results
    }


# ============ Root Endpoint ============

@app.get("/")
async def root():
    """Root endpoint with API documentation"""
    return {
        "name": "Smart Code Reviewer Bot",
        "version": "1.0.0",
        "endpoints": {
            "POST /review": "Submit code for review",
            "GET /review/{review_id}": "Get review by ID",
            "GET /reviews": "List recent reviews",
            "POST /batch-review": "Batch review multiple codes",
            "GET /health": "Health check",
            "GET /docs": "API documentation (Swagger UI)"
        }
    }


# ============ Error Handlers ============

@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    return HTTPException(status_code=400, detail=str(exc))


# ============ Startup/Shutdown ============

@app.on_event("startup")
async def startup_event():
    """Runs on server startup"""
    print("🚀 Code Reviewer Bot API started")
    print(f"📝 Using LLM provider: {type(llm_provider).__name__}")


@app.on_event("shutdown")
async def shutdown_event():
    """Runs on server shutdown"""
    print("🛑 Code Reviewer Bot API stopped")


# ============ Run Server ============

if __name__ == "__main__":
    import uvicorn
    
    # Run: python api/main.py
    # Or: uvicorn api.main:app --reload
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=True
    )
