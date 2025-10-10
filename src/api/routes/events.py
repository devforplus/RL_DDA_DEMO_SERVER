from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ...config import settings
from ...db.models import Event, Session
from ...db.session import get_db_session
from ...security.ingest_token import verify_ingest_token
from ..schemas import EventsBatchRequest

router = APIRouter(prefix="/events", tags=["events"])


@router.post("/batch")
async def ingest_events_batch(
    body: EventsBatchRequest,
    authorization: str | None = Header(default=None, alias="Authorization"),
    db: AsyncSession = Depends(get_db_session),
) -> dict:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="missing bearer token")
    token = authorization.split(" ", 1)[1]
    payload = verify_ingest_token(settings.ingest_secret, token)
    if payload.get("sid") != body.session_id:
        raise HTTPException(status_code=403, detail="session mismatch")

    # validate session exists
    res = await db.execute(select(Session.id).where(Session.id == body.session_id))
    if res.scalar_one_or_none() is None:
        raise HTTPException(status_code=404, detail="session not found")

    # insert events
    db.add_all(
        [
            Event(session_id=body.session_id, t_ms=e.t_ms, type=e.type, payload=e.payload)
            for e in body.events
        ]
    )
    await db.commit()
    return {"accepted": True, "count": len(body.events)}


