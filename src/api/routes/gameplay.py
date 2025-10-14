from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ...db.models import GamePlay
from ...db.session import get_db_session
from ..schemas import GamePlaySubmitRequest, GamePlaySubmitResponse

router = APIRouter(prefix="/gameplay", tags=["gameplay"])


@router.post("", response_model=GamePlaySubmitResponse)
async def submit_gameplay(
    body: GamePlaySubmitRequest,
    db: AsyncSession = Depends(get_db_session),
) -> GamePlaySubmitResponse:
    """
    게임 플레이 데이터를 제출합니다.

    - **nickname**: 플레이어 닉네임
    - **score**: 최종 점수
    - **final_stage**: 도달한 최종 스테이지
    - **model_id**: 사용한 AI 모델 ID (beginner, intermediate, advanced)
    - **statistics**: 게임 통계 정보
    - **frames**: 프레임별 상세 데이터
    """
    try:
        # 프레임 데이터를 딕셔너리 리스트로 변환
        frames_data = [frame.model_dump() for frame in body.frames]

        # GamePlay 인스턴스 생성
        gameplay = GamePlay(
            nickname=body.nickname,
            score=body.score,
            final_stage=body.final_stage,
            model_id=body.model_id,
            total_frames=body.statistics.total_frames,
            play_duration=body.statistics.play_duration,
            enemies_destroyed=body.statistics.enemies_destroyed,
            shots_fired=body.statistics.shots_fired,
            hits=body.statistics.hits,
            deaths=body.statistics.deaths,
            frames_data=frames_data,
            created_at=datetime.now(tz=timezone.utc),
        )

        db.add(gameplay)
        await db.commit()
        await db.refresh(gameplay)

        return GamePlaySubmitResponse(
            id=gameplay.id,
            message="게임 플레이 데이터가 성공적으로 저장되었습니다.",
        )

    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"게임 플레이 데이터 저장 중 오류가 발생했습니다: {str(e)}",
        )

