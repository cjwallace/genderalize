import pytest
import spacy
import en_core_web_sm
from spacy.tokens import Doc

from genderalize import GenderMatcher, gender_generalization_matcher, gendered_dict


@pytest.fixture()
def nlp():
    nlp = en_core_web_sm.load()
    matcher = GenderMatcher(nlp, gendered_dict)
    nlp.add_pipe(matcher)
    nlp.add_pipe(gender_generalization_matcher)
    return nlp


def test_gender_generalization_matcher_assigns_attributes_to_global_Doc(nlp):
    nlp("Any text.")
    assert Doc.get_extension("has_person")
    assert Doc.get_extension("has_gendered_pronouns")
    assert Doc.get_extension("has_gendered_nouns")
    assert Doc.get_extension("is_gender_generalization")


def test_gender_generalization_matcher_has_person_with_names(nlp):
    docs = list(
        nlp.pipe(
            [
                "The wind cried Mary.",
                "Jason was an argonaut.",
                "Jolene took my man.",
                "Noether's theorem is a cornerstone of theoretical physics, and we owe it to Emmy Noether.",
                "Simon.",
            ]
        )
    )
    assert all([doc._.has_person for doc in docs])


def test_gender_generalization_matcher_has_person_without_names(nlp):
    docs = list(
        nlp.pipe(
            [
                "The wind cried often.",
                "A person was an argonaut.",
                "I took my man out.",
                "Noether's theorem is a cornerstone of theoretical physics.",
                "Xyzzyx",
            ]
        )
    )
    assert not any([doc._.has_person for doc in docs])


def test_gender_generalization_matcher_has_gendered_pronouns_with_pronouns(nlp):
    docs = list(
        nlp.pipe(
            [
                "He is a man.",
                "Bob thought highly of himself.",
                "She always wanted to be an actress.",
                "Her.",
                "A woman should have a room of her own.",
            ]
        )
    )
    assert all([doc._.has_gendered_pronouns for doc in docs])


def test_gender_generalization_matcher_has_gendered_pronouns_without_pronouns(nlp):
    docs = list(
        nlp.pipe(
            [
                "That dude is a man.",
                "They thought highly of theirself.",
                "Jenny always wanted to be an actress.",
                "Them.",
                "A person should have a room of their own.",
                "I can includes names like Bob and gendered nouns like Aunt just fine.",
                "Me, myself, and I.",
            ]
        )
    )
    assert not any([doc._.has_gendered_pronouns for doc in docs])


def test_gender_generalization_matcher_has_gendered_nouns_with_nouns(nlp):
    docs = list(
        nlp.pipe(
            [
                "Jenny always wanted to be an actress.",
                "I am an Uncle.",
                "My mother was a brave person.",
                "The fireman was brave.",
                "Sentences about men include a gendered noun.",
                "Fie, fi, fo, fum, I smell the blood on an Englishman!",
                "A ballerina should always carry their shoes.",
            ]
        )
    )
    print([ent.pos_ for ent in docs[1]])
    assert all([doc._.has_gendered_nouns for doc in docs])


def test_gender_generalization_matcher_has_gendered_nouns_without_nouns(nlp):
    docs = list(
        nlp.pipe(
            [
                "She is a her.",
                "The fire fighter was brave.",
                "The word 'actor' is considered gender neutral by this dictionary.",
                "Ballet dancers should always carry their shoes.",
                # does not yet lemmatize Ballerinas to ballerina
                "Ballerinas should always carry their shoes.",
            ]
        )
    )
    assert not any([doc._.has_gendered_nouns for doc in docs])


def test_gender_generalization_matcher_tags_positive_cases(nlp):
    docs = list(
        nlp.pipe(
            [
                "The programmer put down his laptop.",
                "The pilot cursed her luck.",
                "It's not often one forgets to tie his shoelaces.",
                "He is strong.",
                "I don't like him, he's a jerk.",
                "A nurse should look after her patients.",
            ]
        )
    )
    assert all([doc._.is_gender_generalization for doc in docs])


def test_gender_generalization_matcher_skips_negative_cases(nlp):
    docs = list(
        nlp.pipe(
            [
                "Women are more socially adept than men.",
                "Jason put down his coffee.",
                "My Great Aunt thinks highly of herself.",
                "A woman should have a room of her own.",
                "A nurse should look after the women in their care.",
            ]
        )
    )
    assert not any([doc._.is_gender_generalization for doc in docs])
