import spacy
from spacy.matcher import PhraseMatcher
from spacy.tokens import Doc, Span, Token


class GenderMatcher:
    """
    spaCy matcher for dictionary-based annotation of word genders.
    """

    name = "gender_matcher"

    def __init__(self, nlp, gender_dict=dict()):
        self.gender_dict = gender_dict

        patterns = nlp.pipe(self.gender_dict.keys())
        self.matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
        self.matcher.add("GENDERED", None, *patterns)

        Token.set_extension("gender", default="", force=True)

    def __call__(self, doc):
        """
        Call mutates the doc object, adding "gender" attributes to tokens.
        """

        matches = self.matcher(doc)

        for _, start, end in matches:
            match = Span(doc, start, end)

            for token in match:
                token._.set("gender", self.gender_dict[token.text.lower()])

        return doc


def gender_generalization_matcher(doc):
    """
    spaCy pipeline component that sets four Doc-level attributes:

    - has_person: the Doc contains a named person
    - has_gendered_pronouns: the Doc contains words like he/him/she/herself
    - any_gendered_nouns: the Doc contains gendered nouns like Aunt or policeman.
    - is_gender_generalization: the Doc contains gendered pronouns,
                                but no people or gendered nouns.
    """

    Doc.set_extension("has_person", getter=has_person, force=True)
    Doc.set_extension("has_gendered_pronouns", getter=has_gendered_pronouns, force=True)
    Doc.set_extension("has_gendered_nouns", getter=has_gendered_nouns, force=True)
    Doc.set_extension(
        "is_gender_generalization", getter=is_gender_generalization, force=True
    )

    return doc


def has_person(doc):
    """
    Doc-level spaCy attribute getter, which returns True if
    any named entity in the Doc is a PERSON.
    """
    return any([ent.label_ == "PERSON" for ent in doc.ents])


def has_gendered_pronouns(doc):
    """
    Doc-level spaCy attribute getter, which returns True if
    there are any pronouns (tag_ "PRP" or "PRP$") in the Doc
    with a "m" or "f" gender.
    """
    pronoun_genders = [token._.gender for token in doc if token.tag_ in ["PRP", "PRP$"]]
    has_gendered_pronoun = any([g in ["m", "f"] for g in pronoun_genders])
    return has_gendered_pronoun


def has_gendered_nouns(doc):
    """
    Doc-level spaCy attribute getter, which returns True if
    any Token with a NOUN pos_ tag is of "m" or "f" gender.
    """
    noun_genders = [token._.gender for token in doc if token.pos_ in ["NOUN", "PROPN"]]
    has_gendered_noun = any([g in ["m", "f"] for g in noun_genders])
    return has_gendered_noun


def is_gender_generalization(doc):
    """
    Doc-level spaCy attribute getter, which returns True if
    there are gendered pronouns, but there are no people or
    gendered nouns in the Doc.
    """
    return (
        doc._.has_gendered_pronouns
        and not doc._.has_person
        and not doc._.has_gendered_nouns
    )
