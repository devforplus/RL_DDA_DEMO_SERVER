from datetime import datetime, timezone
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ...config import settings
from ...db.models import Participant, Session
from ...db.session import get_db_session
from ...security.ingest_token import sign_ingest_token
from ..schemas import SessionStartRequest, SessionStartResponse, SessionEndRequest

router = APIRouter(prefix="/session", tags=["sessions"])


@router.post("/start", response_model=SessionStartResponse)
async def start_session(
    body: SessionStartRequest,
    db: AsyncSession = Depends(get_db_session),
) -> SessionStartResponse:
    stmt = select(Participant).where(Participant.id == body.participant_id)
    res = await db.execute(stmt)
    _ = res.scalar_one()

    s = Session(
        participant_id=body.participant_id,
        mode=body.mode,
        agent_skill=body.agent_skill,
        game_version=body.game_version,
        model_version=body.model_version,
        seed=body.seed,
        started_at=datetime.now(tz=timezone.utc),
    )
    db.add(s)
    await db.commit()
    token = sign_ingest_token(settings.ingest_secret, s.id, ttl_seconds=3600)
    return SessionStartResponse(session_id=s.id, ingest_token=token)


@router.post("/end")
async def end_session(
    body: SessionEndRequest,
    db: AsyncSession = Depends(get_db_session),
) -> dict:
    stmt = select(Session).where(Session.id == body.session_id)
    res = await db.execute(stmt)
    s = res.scalar_one()
    s.ended_at = datetime.now(tz=timezone.utc)
    s.duration_ms = body.duration_ms
    s.result = body.result
    await db.commit()
    return {"ok": True}


