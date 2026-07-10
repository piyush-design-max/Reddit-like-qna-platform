from fastapi import status, HTTPException, Depends, APIRouter
from ..database import get_db
from sqlmodel import Session, select
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import models, schemas, utils, oauth2

router = APIRouter()


@router.post("/register")
def register(details: schemas.RegisterUser, db: Session = Depends(get_db)):
    hashed_password = utils.hash(details.password)
    new_user = models.User(username=details.username, password=hashed_password)
    db.add(new_user)
    db.commit()
    return {"user successfully registered"}


@router.post("/login")
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    statement = select(models.User).where(models.User.username == user_credentials.username)
    user = db.exec(statement).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="invalid credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="invalid credentials")

    access_token = oauth2.create_access_token(data={"user_id": user.user_id})
    return {"access_token": access_token, "token_type": "bearer"}
