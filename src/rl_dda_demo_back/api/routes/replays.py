from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ...db.models import Replay
from ...db.session import get_db_session
from ...storage.s3 import S3Client

router = APIRouter(prefix="/replays", tags=["replays"])


@router.get("/{replay_id}")
async def get_replay(replay_id: str, db: AsyncSession = Depends(get_db_session)) -> dict:
    res = await db.execute(select(Replay).where(Replay.id == replay_id))
    replay = res.scalar_one_or_none()
    if not replay:
        raise HTTPException(status_code=404, detail="replay not found")

    key = replay.storage_url
    s3 = S3Client()
    signed = s3.presign_get(key)
    return {
        "id": replay.id,
        "session_id": replay.session_id,
        "frames_count": replay.frames_count,
        "duration_ms": replay.duration_ms,
        "compression": replay.compression,
        "schema_version": replay.schema_version,
        "generated_by": replay.generated_by,
        "checksum": replay.checksum,
        "created_at": replay.created_at.isoformat() if replay.created_at else None,
        "url": signed.url,
        "expires_in": signed.expires_in,
    }


