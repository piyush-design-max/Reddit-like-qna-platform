from datetime import date
from typing import Optional, Literal, List
from sqlmodel import SQLModel


class RegisterUser(SQLModel):
    username: str
    password: str


class askQuestion(SQLModel):
    title: str
    content: str

class Response_question(SQLModel):
    question_id: int
    title: str
    content: str
    created_at: date
    user : response_search_user

class Vote(SQLModel):
    question_id :int
    response : Literal["upvote","downvote"]

class Delete(SQLModel):
    id : int
    type : Literal["question","answer",]

class response_search_user(SQLModel):
    username : str

class response_answer(SQLModel):
    content : str
    created_at : date
    user : response_search_user

class response_questionbyid(SQLModel):
    question_id: int
    title: str
    content: str
    created_at: date
    user: response_search_user
    answers : List[response_answer]

class Postanswer(SQLModel):
    content: str

class TokenData(SQLModel):
    id: Optional[int] = None



