from typing import Literal, Optional

from pydantic import BaseModel


class Participant(BaseModel):
    id: str


class ConsentAcceptRequest(BaseModel):
    participant_id: str
    consent_version: str


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


