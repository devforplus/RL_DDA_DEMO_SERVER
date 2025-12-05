from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from ...db.models import GamePlay
from ...db.session import get_db_session
from ..schemas import (
    GamePlayRankingItem,
    GamePlayRankingResponse,
    GamePlaySubmitRequest,
    GamePlaySubmitResponse,
)

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


@router.get("/rankings", response_model=GamePlayRankingResponse)
async def get_rankings(
    page: int = Query(1, ge=1, description="페이지 번호 (1부터 시작)"),
    page_size: int = Query(10, ge=1, le=100, description="페이지당 항목 수 (최대 100)"),
    model_id: Optional[str] = Query(
        None, description="특정 모델로 필터링 (예: beginner, intermediate, advanced)"
    ),
    db: AsyncSession = Depends(get_db_session),
) -> GamePlayRankingResponse:
    """
    게임 플레이 랭킹을 조회합니다.

    - **page**: 페이지 번호 (1부터 시작)
    - **page_size**: 페이지당 항목 수 (기본 10, 최대 100)
    - **model_id**: 특정 모델로 필터링 (선택 사항)

    점수 기준 내림차순으로 정렬되며, 동점일 경우 먼저 등록된 순서로 정렬됩니다.
    """
    try:
        # 기본 쿼리 구성 - 랭킹에 필요한 컬럼만 선택 (frames_data 제외)
        base_query = select(
            GamePlay.id,
            GamePlay.nickname,
            GamePlay.score,
            GamePlay.final_stage,
            GamePlay.model_id,
            GamePlay.total_frames,
            GamePlay.play_duration,
            GamePlay.created_at,
        )
        count_query = select(func.count(GamePlay.id))

        # 모델별 필터링
        if model_id:
            base_query = base_query.where(GamePlay.model_id == model_id)
            count_query = count_query.where(GamePlay.model_id == model_id)

        # 전체 개수 조회
        total_result = await db.execute(count_query)
        total = total_result.scalar_one()

        # 랭킹 조회 (점수 내림차순, 동점일 경우 생성일 오름차순)
        offset = (page - 1) * page_size
        rankings_query = (
            base_query.order_by(desc(GamePlay.score), GamePlay.created_at)
            .limit(page_size)
            .offset(offset)
        )

        result = await db.execute(rankings_query)
        rows = result.all()

        # 랭킹 아이템 생성
        rankings = [
            GamePlayRankingItem(
                id=row.id,
                nickname=row.nickname,
                score=row.score,
                final_stage=row.final_stage,
                model_id=row.model_id,
                total_frames=row.total_frames,
                play_duration=row.play_duration,
                created_at=row.created_at.isoformat() if row.created_at else "",
                rank=offset + idx + 1,
            )
            for idx, row in enumerate(rows)
        ]

        return GamePlayRankingResponse(
            rankings=rankings,
            total=total,
            page=page,
            page_size=page_size,
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"랭킹 조회 중 오류가 발생했습니다: {str(e)}",
        )
