from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Annotated

app = FastAPI()

class ChoiceBase(BaseModel):
    choice_text:str
    is_correct:bool

class QuestionBase(BaseModel):
    question_text:str
    choices: List[ChoiceBase]