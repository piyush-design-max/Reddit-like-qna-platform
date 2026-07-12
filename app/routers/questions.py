from fastapi import status, HTTPException, APIRouter
from .. import models, schemas, oauth2, ai
from ..database import getdb_dependency
from sqlmodel import select
from typing import List, Optional

router = APIRouter(
    prefix="/questions"
)


# POST /questions — ask a question
# GET /questions — list all, sorted by votes or recent
# GET /questions/{id} — get question with all its answers (this needs a JOIN — real practice)
# POST /questions/{id}/answers — post an answer
# POST /questions/{id}/vote — upvote/downvote
# DELETE on your own questions/answers only — ownership enforcement again
# GET /questions/search?q= — search by keyword





@router.post("/")
def ask_question(question: schemas.askQuestion, db: getdb_dependency, current_user: oauth2.user_dependency):
    new_question = models.Questions(**question.dict(), user_id=current_user.user_id)
    db.add(new_question)
    db.commit()
    return {"Posted": question}


@router.get("/", response_model=List[schemas.Response_question])
def getallquestions(db: getdb_dependency, current_user: oauth2.user_dependency):
    statement = select(models.Questions)
    questions = db.exec(statement).all()
    return questions


@router.get("/search", response_model=List[schemas.Response_question])
def search(db : getdb_dependency , current_user : oauth2.user_dependency, q : Optional[str] = ""):
    statement = select(models.Questions).where(models.Questions.title.contains(q))
    questions = db.exec(statement).all()
    return questions

@router.get("/{id}", response_model=schemas.response_questionbyid)
def getByID(id: int, db: getdb_dependency, current_user: oauth2.user_dependency):
    statement = select(models.Questions).where(models.Questions.question_id == id)
    question = db.exec(statement).first()
    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"question with {id} not found")
    return question

@router.post("/{id}/answer")
def answer(answer : schemas.Postanswer,id : int,db : getdb_dependency, current_user : oauth2.user_dependency):
    new_answer = models.Answers(content=answer.content,user_id=current_user.user_id,question_id=id)
    db.add(new_answer)
    db.commit()
    ai.aicall(id,db)
    return {"Message":"answer submitted"}

@router.delete("/delete",status_code=status.HTTP_204_NO_CONTENT)
def delete(data : schemas.Delete, db :getdb_dependency, current_user : oauth2.user_dependency):
    if data.type == "question":
        statement = select(models.Questions).where(models.Questions.question_id==data.id,models.Questions.user_id==current_user.user_id)
        question = db.exec(statement).first()
        if not question:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="question does not exist")
        db.delete(question)
        db.commit()

    if data.type=="answer":
        statement=select(models.Answers).where(models.Answers.answer_id==data.id,models.Answers.user_id==current_user.user_id)
        answer = db.exec(statement).first()
        if not answer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="answer does not exits")
        db.delete(answer)
        db.commit()




