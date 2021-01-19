import pytest
import en_core_web_sm
from spacy.tokens import Token

from genderalize import GenderMatcher


@pytest.fixture(scope="class")
def nlp_with_empty_matcher():
    nlp = en_core_web_sm.load()
    matcher = GenderMatcher(nlp)
    nlp.add_pipe(matcher)
    return nlp


@pytest.fixture(scope="class")
def nlp():
    nlp = en_core_web_sm.load()
    gendered_dict = {"he": "m", "she": "f", "they": "n", "actress": "f"}
    matcher = GenderMatcher(nlp, gendered_dict)
    nlp.add_pipe(matcher)
    return nlp


class TestGenderMatcherNoDict:
    def test_instantiating_GenderMatcher_creates_gender_attribute_in_global_token(
        self, nlp_with_empty_matcher
    ):
        assert Token.has_extension("gender")

    def test_GenderMatcher_with_no_dict_assigns_empty_gender_attribute(
        self, nlp_with_empty_matcher
    ):
        doc = nlp_with_empty_matcher("He she they.")
        assert all([token._.gender == "" for token in doc])


class TestGenderMatcherWithDict:
    def test_GenderMatcher_with_dict_assigns_m_f_n_attributes(self, nlp):
        doc = nlp("He she they.")
        assert doc[0]._.gender == "m"
        assert doc[1]._.gender == "f"
        assert doc[2]._.gender == "n"

    def test_GenderMatcher_matches_upper_case(self, nlp):
        doc = nlp("HE is uppercase.")
        assert doc[0]._.gender == "m"
        assert doc[1]._.gender == ""
        assert doc[2]._.gender == ""

    def test_GenderMatcher_matches_with_punctuation(self, nlp):
        doc = nlp("Who is she?")
        assert doc[2]._.gender == "f"

    def test_GenderMatcher_matches_nouns_and_pronouns(self, nlp):
        doc = nlp("She is an actress.")
        assert [token._.gender for token in doc] == ["f", "", "", "f", ""]
