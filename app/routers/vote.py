from fastapi import status, HTTPException, APIRouter
from .. import models, schemas, oauth2
from ..database import getdb_dependency
from sqlmodel import select

router = APIRouter(
    prefix="/questions"
)


@router.post("/{id}/vote")
def vote(vote: schemas.Vote, id: int, db: getdb_dependency, current_user: oauth2.user_dependency):
    statement = select(models.Votes).where(models.Votes.user_id == current_user.user_id,
                                           models.Votes.question_id == vote.question_id)
    found_vote = db.exec(statement).first()
    if vote.response == "upvote":
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="user already voted")
        new_vote = models.Votes(user_id=current_user.user_id, question_id=vote.question_id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}
    if vote.response == "downvote":
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="user has not voted")
        db.delete(found_vote)
        db.commit()
        return {"message": "successfully deleted vote"}
