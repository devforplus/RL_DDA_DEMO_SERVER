from typing import Literal, Optional

from pydantic import BaseModel


class Participant(BaseModel):
    id: str


class SessionStartRequest(BaseModel):
    participant_id: str
    mode: Literal["human", "agent"]
    agent_skill: Optional[Literal["beginner", "intermediate", "advanced"]] = None
    game_version: Optional[str] = None
    model_version: Optional[str] = None
    seed: Optional[int] = None


class SessionStartResponse(BaseModel):
    session_id: str
    ingest_token: str


class SessionEndRequest(BaseModel):
    session_id: str
    duration_ms: Optional[int] = None
    result: Optional[dict] = None


class EventsBatchItem(BaseModel):
    t_ms: int
    type: str
    payload: dict


class EventsBatchRequest(BaseModel):
    session_id: str
    request_id: Optional[str] = None
    events: list[EventsBatchItem]


class GamePlayStatistics(BaseModel):
    total_frames: Optional[int] = None
    play_duration: Optional[float] = None
    enemies_destroyed: Optional[int] = None
    shots_fired: Optional[int] = None
    hits: Optional[int] = None
    deaths: Optional[int] = None


class GamePlayFrame(BaseModel):
    frame_number: int
    player_x: float
    player_y: float
    player_lives: int
    player_score: int
    current_weapon: int
    input_left: int
    input_right: int
    # 추가 필드는 프론트엔드에서 전송하는 모든 필드를 수용하도록 설정
    model_config = {"extra": "allow"}


class GamePlaySubmitRequest(BaseModel):
    nickname: str
    score: int
    final_stage: int
    model_id: Optional[str] = None
    statistics: GamePlayStatistics
    frames: list[GamePlayFrame]


class GamePlaySubmitResponse(BaseModel):
    id: str
    message: str


class GamePlayRankingItem(BaseModel):
    id: str
    nickname: str
    score: int
    final_stage: int
    model_id: Optional[str]
    created_at: str
    rank: int


class GamePlayRankingResponse(BaseModel):
    rankings: list[GamePlayRankingItem]
    total: int
    page: int
    page_size: int
