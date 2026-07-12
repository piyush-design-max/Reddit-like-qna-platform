from datetime import date, datetime
from typing import List

from sqlalchemy import Column, Integer, ForeignKey
from sqlmodel import SQLModel, Field, Relationship
from enum import Enum


class Answers(SQLModel, table=True):
    answer_id: int = Field(primary_key=True)
    content: str = Field(nullable=False)
    user_id: int = Field(nullable=False, foreign_key="user.user_id")
    question_id: int = Field(nullable=False, foreign_key="questions.question_id")
    created_at: date = Field(default_factory=datetime.utcnow, nullable=False)

    question : "Questions" = Relationship(back_populates="answers")
    user : "User" = Relationship(back_populates="answer")

class User(SQLModel, table=True):
    user_id: int = Field(primary_key=True)
    username: str = Field(nullable=False, unique=True)
    password: str = Field(nullable=False)
    created_at: date = Field(default_factory=datetime.utcnow, nullable=False)

    question : List["Questions"] = Relationship(back_populates="user")
    answer : List[Answers] = Relationship(back_populates="user")


class Questions(SQLModel, table=True):
    question_id: int = Field(primary_key=True)
    title: str = Field(nullable=False)
    content: str = Field(nullable=False)
    user_id: int = Field(nullable=False, foreign_key="user.user_id")
    created_at: date = Field(default_factory=datetime.utcnow, nullable=False)
    vote : int = Field(default=0)
    ai_overview : str = Field(nullable=True)


    answers : List[Answers] = Relationship(back_populates="question")
    user : User = Relationship(back_populates="question")

class Votes(SQLModel, table=True):
    question_id: int = Field(sa_column=Column(Integer, ForeignKey("questions.question_id", ondelete="CASCADE"), primary_key=True))
    user_id: int = Field(sa_column=Column(Integer, ForeignKey("user.user_id", ondelete="CASCADE"), primary_key=True))

