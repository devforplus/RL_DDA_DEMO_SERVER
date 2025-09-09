from fastapi import APIRouter, Depends

router = APIRouter(prefix="/participants", tags=["participants"])


@router.post("")
async def create_or_get_participant() -> dict:
    # Placeholder implementation
    return {"id": "todo"}


