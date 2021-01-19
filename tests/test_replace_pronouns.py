import pytest
import en_core_web_sm

from genderalize import (
    GenderMatcher,
    gender_generalization_matcher,
    gendered_dict,
    replace_pronouns,
)


@pytest.fixture(scope="module")
def nlp():
    nlp = en_core_web_sm.load()
    matcher = GenderMatcher(nlp, gendered_dict)
    nlp.add_pipe(matcher)
    nlp.add_pipe(gender_generalization_matcher)
    return nlp


def test_replace_pronouns_leaves_empty_string_unchanged(nlp):
    doc = nlp("")
    replaced = replace_pronouns(nlp, doc, "f")
    assert replaced.text == doc.text


def test_replace_pronouns_single_she_to_he(nlp):
    doc = nlp("Is she an astronaut?")
    replaced = replace_pronouns(nlp, doc, "m")
    assert replaced.text == "Is he an astronaut?"


def test_replace_pronouns_start_of_sentence(nlp):
    doc = nlp("She is an astronaut.")
    replaced = replace_pronouns(nlp, doc, "m")
    assert replaced.text == "He is an astronaut."


def test_replace_pronouns_end_of_sentence(nlp):
    doc = nlp("I like him.")
    replaced = replace_pronouns(nlp, doc, "f")
    assert replaced.text == "I like her."


def test_replace_pronouns_multiple_pronouns(nlp):
    doc = nlp("The thing about her is she is a human.")
    replaced = replace_pronouns(nlp, doc, "m")
    assert replaced.text == "The thing about him is he is a human."


def test_replace_pronouns_respects_target_gender(nlp):
    doc = nlp("He might change.")
    replaced = replace_pronouns(nlp, doc, "m")
    assert replaced.text == doc.text

    replaced = replace_pronouns(nlp, doc, "f")
    assert replaced.text == "She might change."

    doc = nlp("He for she.")
    replaced = replace_pronouns(nlp, doc, "f")
    assert replaced.text == "She for she."


def test_replace_pronouns_possessive_determiner_pronouns(nlp):
    doc = nlp("It was his apple.")
    replaced = replace_pronouns(nlp, doc, "f")
    assert replaced.text == "It was her apple."


def test_replace_prononouns_possessive_personal_pronouns(nlp):
    doc = nlp("The apple was his.")
    replaced = replace_pronouns(nlp, doc, "f")
    assert replaced.text == "The apple was hers."


def test_replace_pronouns_personal_and_possessive_pronouns(nlp):
    doc = nlp("The astronaut loved her shiny new helmet. It was just hers.")
    replaced = replace_pronouns(nlp, doc, "m")
    assert replaced.text == "The astronaut loved his shiny new helmet. It was just his."
