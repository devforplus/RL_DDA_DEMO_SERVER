from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Optional

from sqlalchemy import (
    JSON,
    BigInteger,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


def uuid_pk() -> str:
    return uuid.uuid4().hex


class Participant(Base):
    __tablename__ = "participants"

    id: Mapped[str] = mapped_column(CHAR(32), primary_key=True, default=uuid_pk)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )
    locale: Mapped[Optional[str]] = mapped_column(String(16))
    user_agent_hash: Mapped[Optional[str]] = mapped_column(String(64))
    cohort: Mapped[Optional[str]] = mapped_column(String(32))

    sessions: Mapped[list[Session]] = relationship(back_populates="participant")


class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[str] = mapped_column(CHAR(32), primary_key=True, default=uuid_pk)
    participant_id: Mapped[str] = mapped_column(
        CHAR(32), ForeignKey("participants.id"), nullable=False, index=True
    )

    mode: Mapped[str] = mapped_column(String(8), nullable=False)  # 'human' | 'agent'
    agent_skill: Mapped[Optional[str]] = mapped_column(
        String(16)
    )  # beginner/intermediate/advanced
    game_version: Mapped[Optional[str]] = mapped_column(String(64))
    model_version: Mapped[Optional[str]] = mapped_column(String(64))
    seed: Mapped[Optional[int]] = mapped_column(Integer)

    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )
    ended_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    duration_ms: Mapped[Optional[int]] = mapped_column(Integer)
    result: Mapped[Optional[dict[str, Any]]] = mapped_column(JSON)

    participant: Mapped[Participant] = relationship(back_populates="sessions")
    events: Mapped[list[Event]] = relationship(back_populates="session")
    replay: Mapped[Optional[Replay]] = relationship(
        back_populates="session", uselist=False
    )


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(
        BigInteger().with_variant(BigInteger, "mysql"),
        primary_key=True,
        autoincrement=True,
    )
    session_id: Mapped[str] = mapped_column(
        CHAR(32), ForeignKey("sessions.id"), nullable=False, index=True
    )
    t_ms: Mapped[int] = mapped_column(Integer, nullable=False)
    type: Mapped[str] = mapped_column(String(32), nullable=False)
    payload: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)

    __table_args__ = (Index("ix_events_session_t", "session_id", "t_ms"),)

    session: Mapped[Session] = relationship(back_populates="events")


class Replay(Base):
    __tablename__ = "replays"

    id: Mapped[str] = mapped_column(CHAR(32), primary_key=True, default=uuid_pk)
    session_id: Mapped[str] = mapped_column(
        CHAR(32), ForeignKey("sessions.id"), nullable=False, unique=True
    )
    storage_url: Mapped[str] = mapped_column(Text, nullable=False)
    frames_count: Mapped[Optional[int]] = mapped_column(Integer)
    duration_ms: Mapped[Optional[int]] = mapped_column(Integer)
    compression: Mapped[Optional[str]] = mapped_column(String(16))
    schema_version: Mapped[Optional[str]] = mapped_column(String(16))
    generated_by: Mapped[Optional[str]] = mapped_column(String(16))
    checksum: Mapped[Optional[str]] = mapped_column(String(64))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )

    session: Mapped[Session] = relationship(back_populates="replay")


class Experiment(Base):
    __tablename__ = "experiments"

    id: Mapped[str] = mapped_column(CHAR(32), primary_key=True, default=uuid_pk)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    config: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )


class Assignment(Base):
    __tablename__ = "assignments"

    id: Mapped[str] = mapped_column(CHAR(32), primary_key=True, default=uuid_pk)
    experiment_id: Mapped[str] = mapped_column(
        CHAR(32), ForeignKey("experiments.id"), nullable=False
    )
    participant_id: Mapped[str] = mapped_column(
        CHAR(32), ForeignKey("participants.id"), nullable=False
    )
    arm: Mapped[str] = mapped_column(String(32), nullable=False)
    assigned_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )


class GamePlay(Base):
    __tablename__ = "gameplays"

    id: Mapped[str] = mapped_column(CHAR(32), primary_key=True, default=uuid_pk)
    nickname: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    score: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    final_stage: Mapped[int] = mapped_column(Integer, nullable=False)
    model_id: Mapped[str] = mapped_column(String(32), nullable=False, index=True)

    # 통계 데이터
    total_frames: Mapped[Optional[int]] = mapped_column(Integer)
    play_duration: Mapped[Optional[float]] = mapped_column(Float)  # 초 단위
    enemies_destroyed: Mapped[Optional[int]] = mapped_column(Integer)
    shots_fired: Mapped[Optional[int]] = mapped_column(Integer)
    hits: Mapped[Optional[int]] = mapped_column(Integer)
    deaths: Mapped[Optional[int]] = mapped_column(Integer)

    # 프레임 데이터는 JSON으로 저장 (LONGTEXT 사용)
    frames_data: Mapped[Optional[list[dict[str, Any]]]] = mapped_column(JSON)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False, index=True
    )

    __table_args__ = (
        Index("ix_gameplays_score_created", "score", "created_at"),
        Index("ix_gameplays_model_score", "model_id", "score"),
    )