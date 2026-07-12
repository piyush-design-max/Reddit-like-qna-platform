from groq import Groq
from .config import settings
from .database import getdb_dependency
from . import models
from sqlmodel import select

client = Groq(api_key=settings.groq_api_key)


def aicall(id: int, db=getdb_dependency):
    statement = select(models.Answers).where(models.Answers.question_id == id)
    answers = db.exec(statement).all()
    data = "\n\n".join([answer.content for answer in answers])
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": f"summarize these answers by users in 2-3 lines {data}"}]
    )
    question = db.exec(select(models.Questions).where(models.Questions.question_id == id)).first()
    question.ai_overview = response.choices[0].message.content
    db.add(question)
    db.commit()
