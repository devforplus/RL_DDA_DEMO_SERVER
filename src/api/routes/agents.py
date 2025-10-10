from fastapi import APIRouter

router = APIRouter(prefix="/agents", tags=["agents"])


@router.get("")
async def list_agents() -> list[dict]:
    # Static list for v1; can be moved to DB later
    return [
        {"id": "agent-beginner", "skill": "beginner", "model_version": "v1", "description": "초급 에이전트"},
        {"id": "agent-intermediate", "skill": "intermediate", "model_version": "v1", "description": "중급 에이전트"},
        {"id": "agent-advanced", "skill": "advanced", "model_version": "v1", "description": "고급 에이전트"},
    ]


