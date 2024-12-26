from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session


app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class ChoiceBase(BaseModel):
    choice_text:str
    is_correct:bool

    class Config:
        from_attributes = True

class QuestionBase(BaseModel):
    question_text:str
    choices: List[ChoiceBase]

    class Config:
        from_attributes = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]



@app.get("/questions/{question_id}")
async def read_data(question_id:int, db: db_dependency):
    result =  db.query(models.Questions).filter(models.Questions.id == question_id).first()
    if result is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return result

@app.get("/choices/{question_id}")
async def read_data(question_id:int, db: db_dependency):
    result =  db.query(models.Choices).filter(models.Choices.question_id == question_id).all()
    return result

@app.post("/questions/")
async def create_question(question: QuestionBase, db: db_dependency):
    db_question = models.Questions(question_text=question.question_text)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    for choice in question.choices:
        db_choice = models.Choices(
            question_id=db_question.id,
            choice_text=choice.choice_text,
            is_correct=choice.is_correct,
        )
        db.add(db_choice)
    db.commit()
    db_question.choices
    return db_question