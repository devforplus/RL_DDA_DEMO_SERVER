from datetime import datetime, timezone
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ...db.models import Participant
from ...db.session import get_db_session
from ..schemas import ConsentAcceptRequest

router = APIRouter(prefix="/consent", tags=["consent"])


@router.post("/accept")
async def accept_consent(
    body: ConsentAcceptRequest,
    session: AsyncSession = Depends(get_db_session),
) -> dict:
    stmt = select(Participant).where(Participant.id == body.participant_id)
    res = await session.execute(stmt)
    participant = res.scalar_one()
    participant.consent_version = body.consent_version
    participant.consent_accepted_at = datetime.now(tz=timezone.utc)
    await session.commit()
    return {"ok": True}


