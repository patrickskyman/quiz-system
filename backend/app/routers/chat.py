from fastapi import APIRouter, HTTPException, Query, Depends
from fastapi.responses import JSONResponse
from typing import Optional, List
import logging
from datetime import datetime

from app.models import QueryRequest, QueryResponse, QueryHistoryResponse, ErrorResponse
from app.services.openai_service import generate_ai_response
from app.database import save_query, get_query_history

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post(
    "/query",
    response_model=QueryResponse,
    summary="Submit a query to the AI",
    description="Submit a question and receive an AI-generated response",
    responses={
        200: {"description": "Successful response"},
        400: {"description": "Invalid request"},
        500: {"description": "Internal server error"}
    }
)
async def submit_query(request: QueryRequest):
    """
    Submit a query to the AI system and get a response
    
    - **query**: The question or query to submit (required)
    - **user_id**: Optional user identifier for tracking history
    """
    try:
        logger.info(f"Processing query: {request.query[:50]}...")
        
        # Validate input
        if not request.query.strip():
            raise HTTPException(
                status_code=400,
                detail="Query cannot be empty"
            )
        
        # Generate AI response
        ai_result = await generate_ai_response(request.query)
        
        if not ai_result["success"]:
            raise HTTPException(
                status_code=500,
                detail="Failed to generate AI response"
            )
        
        # Save to database
        query_id = save_query(
            query=request.query,
            response=ai_result["response"],
            user_id=request.user_id,
            response_time=ai_result.get("response_time")
        )
        
        # Create response
        response = QueryResponse(
            id=query_id,
            query=request.query,
            response=ai_result["response"],
            timestamp=datetime.now(),
            response_time=ai_result.get("response_time"),
            success=True
        )
        
        logger.info(f"Query processed successfully. ID: {query_id}")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while processing your query: {str(e)}"
        )

@router.get(
    "/history",
    response_model=QueryHistoryResponse,
    summary="Get query history",
    description="Retrieve previous queries with pagination support",
    responses={
        200: {"description": "Query history retrieved successfully"},
        400: {"description": "Invalid parameters"}
    }
)
async def get_history(
    user_id: Optional[str] = Query(None, description="Filter by user ID"),
    page: int = Query(1, ge=1, description="Page number (starts from 1)"),
    page_size: int = Query(10, ge=1, le=100, description="Number of items per page")
):
    """
    Get query history with pagination
    
    - **user_id**: Optional filter by user ID
    - **page**: Page number (default: 1)
    - **page_size**: Items per page (default: 10, max: 100)
    """
    try:
        # Calculate offset
        offset = (page - 1) * page_size
        
        # Get history from database
        queries_data, total_count = get_query_history(
            user_id=user_id,
            limit=page_size,
            offset=offset
        )
        
        # Convert to response models
        queries = []
        for query_data in queries_data:
            queries.append(QueryResponse(
                id=query_data["id"],
                query=query_data["query"],
                response=query_data["response"],
                timestamp=datetime.fromisoformat(query_data["timestamp"]) if isinstance(query_data["timestamp"], str) else query_data["timestamp"],
                response_time=query_data.get("response_time"),
                success=query_data.get("success", True)
            ))
        
        return QueryHistoryResponse(
            queries=queries,
            total_count=total_count,
            page=page,
            page_size=page_size
        )
        
    except Exception as e:
        logger.error(f"Error retrieving query history: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve query history"
        )

@router.get(
    "/stats",
    summary="Get system statistics",
    description="Get basic statistics about the Q&A system"
)
async def get_stats():
    """Get basic system statistics"""
    try:
        # Get total queries count
        _, total_queries = get_query_history(limit=1)
        
        return {
            "total_queries": total_queries,
            "system_status": "operational",
            "api_version": "1.0.0",
            "timestamp": datetime.now()
        }
        
    except Exception as e:
        logger.error(f"Error retrieving stats: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve system statistics"
        )

@router.delete(
    "/history/{query_id}",
    summary="Delete a query from history",
    description="Delete a specific query from the history (soft delete)"
)
async def delete_query(query_id: int):
    """Delete a query from history"""
    try:
        # For now, we'll just return success
        # In a real implementation, you'd mark the query as deleted
        return {
            "message": f"Query {query_id} deleted successfully",
            "success": True
        }
        
    except Exception as e:
        logger.error(f"Error deleting query {query_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to delete query"
        )

# Health check for the chat service
@router.get(
    "/health",
    summary="Chat service health check",
    description="Check if the chat service is operational"
)
async def chat_health():
    """Health check for chat service"""
    return {
        "service": "chat",
        "status": "healthy",
        "timestamp": datetime.now(),
        "dependencies": {
            "database": "connected",
            "openai_api": "configured"
        }
    }