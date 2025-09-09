from fastapi import APIRouter

router = APIRouter(prefix="/session", tags=["sessions"])


@router.post("/start")
async def start_session() -> dict:
    # Placeholder implementation
    return {"session_id": "todo", "ingest_token": "todo"}


@router.post("/end")
async def end_session() -> dict:
    # Placeholder implementation
    return {"ok": True}


