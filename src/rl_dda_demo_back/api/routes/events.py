from fastapi import APIRouter

router = APIRouter(prefix="/events", tags=["events"])


@router.post("/batch")
async def ingest_events_batch() -> dict:
    # Placeholder implementation
    return {"accepted": True}


