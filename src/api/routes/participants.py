from datetime import datetime, timezone
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ...db.models import Participant
from ...db.session import get_db_session

router = APIRouter(prefix="/participants", tags=["participants"])


@router.post("")
async def create_or_get_participant(
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    participant = Participant()
    participant.created_at = datetime.now(tz=timezone.utc)
    session.add(participant)
    await session.commit()
    return {"id": participant.id}


