"""FastAPI Main Application with WebSocket Streaming"""
from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any
import json
import asyncio
from datetime import datetime

from app.config import settings
from app.workflows.onboarding import create_onboarding_workflow

# Initialize FastAPI app
app = FastAPI(
    title="Agentic Workflow API",
    description="Multi-agent autonomous workflow system",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global workflow instance
workflow = create_onboarding_workflow()
active_connections: Dict[str, WebSocket] = {}


# Pydantic models
class EmployeeOnboardingRequest(BaseModel):
    name: str
    email: str
    department: str
    start_date: str = "2024-03-30"


class WorkflowStatusResponse(BaseModel):
    workflow_id: str
    status: str
    current_step: int
    logs: list


# REST Endpoints
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "environment": settings.environment}


@app.post("/api/workflow/onboard")
async def start_onboarding(request: EmployeeOnboardingRequest):
    """Start employee onboarding workflow"""
    import uuid

    try:
        employee_data = request.model_dump()
        workflow_id = f"onboard-{uuid.uuid4().hex[:8]}"

        # Create notification callback
        def notify_update(event_type: str, updated_state: Any):
            print(f"Workflow update: {event_type} for {workflow_id}")

        # Start workflow (non-blocking)
        asyncio.create_task(
            workflow.execute(employee_data, notify_update, workflow_id)
        )

        return {
            "status": "started",
            "workflow_id": workflow_id,
            "employee": employee_data["name"],
            "message": "Onboarding workflow initiated. Connect to WebSocket for updates.",
        }
    except Exception as e:
        import traceback
        print(f"Error starting workflow: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/workflow/{workflow_id}")
async def get_workflow_status(workflow_id: str):
    """Get workflow status"""
    if workflow_id not in workflow.workflows:
        raise HTTPException(status_code=404, detail="Workflow not found")

    state = workflow.workflows[workflow_id]
    return {
        "workflow_id": workflow_id,
        "status": state.status.value,
        "current_step": state.current_step,
        "logs_count": len(state.logs),
        "active_agent": state.active_agent,
    }


@app.get("/api/logs/{workflow_id}")
async def get_workflow_logs(workflow_id: str):
    """Get all logs for a workflow"""
    if workflow_id not in workflow.workflows:
        raise HTTPException(status_code=404, detail="Workflow not found")

    state = workflow.workflows[workflow_id]
    logs = [
        {
            "timestamp": log.timestamp,
            "type": log.type,
            "step_id": log.step_id,
            "step_name": log.step_name,
            "agent_id": log.agent_id,
            "agent_name": log.agent_name,
            "message": log.message,
            "reasoning": log.reasoning,
        }
        for log in state.logs
    ]
    return {"workflow_id": workflow_id, "logs": logs}


# WebSocket Endpoint
@app.websocket("/workflow/stream/{workflow_id}")
async def websocket_workflow_stream(websocket: WebSocket, workflow_id: str):
    """WebSocket endpoint for real-time workflow updates"""
    await websocket.accept()
    active_connections[workflow_id] = websocket

    try:
        while True:
            # Check if workflow exists and send updates
            if workflow_id in workflow.workflows:
                state = workflow.workflows[workflow_id]

                # Prepare update payload
                update = {
                    "workflow_id": workflow_id,
                    "status": state.status.value,
                    "current_step": state.current_step,
                    "active_agent": state.active_agent,
                    "logs": [
                        {
                            "timestamp": log.timestamp,
                            "type": log.type,
                            "step_id": log.step_id,
                            "step_name": log.step_name,
                            "agent_id": log.agent_id,
                            "agent_name": log.agent_name,
                            "message": log.message,
                            "reasoning": log.reasoning,
                        }
                        for log in state.logs
                    ],
                }

                await websocket.send_json(update)

                # If workflow is complete, break
                if state.status.value in ["completed", "error", "escalated"]:
                    await asyncio.sleep(1)
                    break

            await asyncio.sleep(0.5)  # Poll interval

    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        del active_connections[workflow_id]


@app.get("/api/stats")
async def get_stats():
    """Get system statistics"""
    from app.optimization.token_cache import outcome_cache
    from app.optimization.prompt_optimizer import prompt_optimizer

    return {
        "cache_stats": outcome_cache.get_stats(),
        "prompt_performance": {
            agent: prompt_optimizer.get_performance_summary(agent)
            for agent in ["decision-making", "action-execution"]
        },
    }


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Agentic Workflow Backend",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "health": "/health",
            "start_workflow": "POST /api/workflow/onboard",
            "workflow_status": "GET /api/workflow/{workflow_id}",
            "workflow_logs": "GET /api/logs/{workflow_id}",
            "websocket": "WS /workflow/stream/{workflow_id}",
            "statistics": "GET /api/stats",
        },
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level=settings.log_level.lower(),
    )
