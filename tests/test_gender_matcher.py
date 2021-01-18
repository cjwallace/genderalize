import pytest
import spacy
import en_core_web_sm
from spacy.tokens import Token

from genderalize import GenderMatcher


@pytest.fixture()
def nlp():
    nlp = en_core_web_sm.load()
    return nlp


@pytest.fixture()
def gendered_dict():
    return {"he": "m", "she": "f", "they": "n", "actress": "f"}


def test_instantiating_GenderMatcher_creates_gender_attribute_in_global_token(nlp):
    matcher = GenderMatcher(nlp)
    nlp.add_pipe(matcher)
    assert Token.get_extension("gender")


def test_GenderMatcher_with_no_dict_assigns_empty_gender_attribute(nlp):
    matcher = GenderMatcher(nlp)
    nlp.add_pipe(matcher)
    doc = nlp("He she they.")
    assert all([token._.gender == "" for token in doc])


def test_GenderMatcher_with_dict_assigns_m_f_n_attributes(nlp, gendered_dict):
    matcher = GenderMatcher(nlp, gendered_dict)
    nlp.add_pipe(matcher)
    doc = nlp("He she they.")
    assert doc[0]._.gender == "m"
    assert doc[1]._.gender == "f"
    assert doc[2]._.gender == "n"


def test_GenderMatcher_matches_upper_case(nlp, gendered_dict):
    matcher = GenderMatcher(nlp, gendered_dict)
    nlp.add_pipe(matcher)
    doc = nlp("HE is uppercase.")
    assert doc[0]._.gender == "m"
    assert doc[1]._.gender == ""
    assert doc[2]._.gender == ""


def test_GenderMatcher_matches_with_punctuation(nlp, gendered_dict):
    matcher = GenderMatcher(nlp, gendered_dict)
    nlp.add_pipe(matcher)
    doc = nlp("Who is she?")
    assert doc[2]._.gender == "f"


def test_GenderMatcher_matches_nouns_and_pronouns(nlp, gendered_dict):
    matcher = GenderMatcher(nlp, gendered_dict)
    nlp.add_pipe(matcher)
    doc = nlp("She is an actress.")
    assert [token._.gender for token in doc] == ["f", "", "", "f", ""]
