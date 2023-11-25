import os
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Boolean,
    Float,
    DateTime,
    ForeignKey,
    Enum,
    CheckConstraint,
)
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime


engine = create_engine("sqlite:///cc.db", echo=True)  # Set echo to True for debugging

Base = declarative_base()


class CCCharacter(Base):
    __tablename__ = "cc_characters"

    key = Column(String, primary_key=True)
    name = Column(String)


class CCCard(Base):
    __tablename__ = "cc_cards"

    key = Column(String, primary_key=True)
    name = Column(String)


class CCArtifact(Base):
    __tablename__ = "cc_artifacts"

    key = Column(String, primary_key=True)
    name = Column(String)


class CCCharacterLinkedRun(Base):
    __tablename__ = "cc_character_linked_run"

    id = Column(Integer, primary_key=True)
    run_id = Column(
        Integer, ForeignKey("cc_runs.id")
    )  # related by internal id, not runId
    character_id = Column(Integer, ForeignKey("cc_characters.key"))


class CCCardLinkedRun(Base):
    __tablename__ = "cc_card_linked_run"
    __table_args__ = (CheckConstraint("upgrade IN ('None', 'A', 'B')"),)

    id = Column(Integer, primary_key=True)
    run_id = Column(
        Integer, ForeignKey("cc_runs.id")
    )  # related by internal id, not runId
    card_id = Column(Integer, ForeignKey("cc_cards.key"))
    upgrade = Column(String, default="None", nullable=False)


class CCArtifactLinkedRun(Base):
    __tablename__ = "cc_artifact_linked_run"

    id = Column(Integer, primary_key=True)
    run_id = Column(
        Integer, ForeignKey("cc_runs.id")
    )  # related by internal id, not runId
    artifact_id = Column(Integer, ForeignKey("cc_artifacts.key"))


class CCRun(Base):
    __tablename__ = "cc_runs"

    id = Column(Integer, primary_key=True)
    version = Column(Integer)
    won = Column(Boolean)
    duration = Column(Float)
    difficulty = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)
    runId = Column(String, unique=True, nullable=False)
    seed = Column(Integer)
    ship = Column(String)
    hullDamageTaken = Column(Integer)
    combatTurns = Column(Integer)


# Create the table in the database
Base.metadata.create_all(engine)
