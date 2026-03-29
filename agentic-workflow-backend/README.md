# Agentic Workflow Backend - Employee Onboarding System
A multi-agent backend for autonomous employee onboarding workflows using LangGraph and Claude API.

## Features
- 5 specialized agents with LangGraph orchestration
- Few-shot learning for each agent
- Real-time WebSocket streaming updates
- Token optimization (caching, feedback loops, prompt adjustment)
- Error handling and retry mechanisms
- Mock external systems (AD, Calendar, Email)

## Setup

1. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure .env:
   ```bash
   cp .env.example .env
   # Add your ANTHROPIC_API_KEY
   ```

4. Run server:
   ```bash
   python -m uvicorn app.main:app --reload
   ```

## API Endpoints

- `POST /api/workflow/onboard` - Start employee onboarding
- `WS /workflow/stream/{workflow_id}` - WebSocket for real-time updates
- `GET /api/workflow/{workflow_id}` - Get workflow status
- `GET /api/logs/{workflow_id}` - Get audit logs
