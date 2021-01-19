from enum import Enum

import typer
import en_core_web_sm

from genderalize import (
    GenderMatcher,
    gender_generalization_matcher,
    gendered_dict,
    replace_pronouns,
)


class Gender(str, Enum):
    m = "m"
    f = "f"


app = typer.Typer()


@app.callback()
def callback():
    """
    A CLI for detecting and changing gender generalizations.
    """


def process_text(text: str):
    nlp = en_core_web_sm.load()

    gender_component = GenderMatcher(nlp, gendered_dict)
    nlp.add_pipe(gender_component)
    nlp.add_pipe(gender_generalization_matcher)

    doc = nlp(text)
    return doc, nlp


@app.command()
def detect(text: str):
    """
    Detect whether the input text is a gender generalization.
    Returns True when the text is a gender generalization, False otherwise.
    """
    doc, _ = process_text(text)
    typer.echo(str(doc._.is_gender_generalization))


@app.command()
def change(gender: Gender, text: str):
    """
    Set the gender (m|f) of a gender generalization.
    If the text is not a gender generalization, it is returned unchanged.
    """
    doc, nlp = process_text(text)
    if doc._.is_gender_generalization:
        doc = replace_pronouns(nlp, doc, gender)
    typer.echo(str(doc.text))
