from fastapi import APIRouter

router = APIRouter(prefix="/consent", tags=["consent"])


@router.post("/accept")
async def accept_consent() -> dict:
    # Placeholder implementation
    return {"ok": True}


