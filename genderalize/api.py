# pylint: disable=no-name-in-module
# ^ for pydantic

from enum import Enum

import en_core_web_sm
from fastapi import FastAPI
from pydantic import BaseModel

from genderalize import (
    GenderMatcher,
    gender_generalization_matcher,
    gendered_dict,
    replace_pronouns,
)


class Text(BaseModel):
    text: str

    class Config:
        schema_extra = {"example": {"text": "The astronaut drank his coffee."}}


class Biases(BaseModel):
    generalization: bool


class Gender(str, Enum):
    m = "m"
    f = "f"


app = FastAPI()


def process_text(text: str):
    nlp = en_core_web_sm.load()

    gender_component = GenderMatcher(nlp, gendered_dict)
    nlp.add_pipe(gender_component)
    nlp.add_pipe(gender_generalization_matcher)

    doc = nlp(text)
    return doc, nlp


@app.get("/status")
def status():
    return {"status": "green"}


@app.post("/biases", response_model=Biases)
def biases(text: Text):
    doc, _ = process_text(text.text)
    return {"generalization": doc._.is_gender_generalization}


@app.post("/biases/generalizations/{gender}", response_model=Text)
def generalization(text: Text, gender: Gender) -> Text:
    doc, nlp = process_text(text.text)
    if doc._.is_gender_generalization:
        doc = replace_pronouns(nlp, doc, gender)
    return {"text": doc.text}
