from fastapi import FastAPI
from . import models
from .database import engine
from .routers import auth,questions,vote

models.SQLModel.metadata.create_all(engine)
app = FastAPI()

app.include_router(auth.router)
app.include_router(questions.router)
app.include_router(vote.router)


@app.get("/")
def root():
    return {"message": "reddit style Q/A platform"}
