pronoun_pairs = {
    "PRP$": {
        "he": "she",
        "himself": "herself",
        "him": "her",
        "his": "her",
        "she": "he",
        "herself": "hisself",
        "her": "his",
        "hers": "his",
    },
    "PRP": {
        "he": "she",
        "himself": "herself",
        "him": "her",
        "his": "hers",
        "she": "he",
        "herself": "hisself",
        "her": "him",
        "hers": "his",
    },
}


def lookup_pronoun(token):
    """
    Look up personal (PRP) or possessive (PRP$) pronoun.
    """
    return pronoun_pairs[token.tag_][token.text.lower()]


def correct_capitalization(token, pronoun):
    """
    If the original pronoun was capitalized, capitalize the new pronoun.
    """
    if token.text[0].isupper():
        pronoun = pronoun.capitalize()

    return pronoun


def append_correct_whitespace(token, pronoun):
    """
    If the original pronoun was followed by whitespace, append whitespace to new pronoun.
    """
    if token.text_with_ws != token.text:
        whitespace = token.text_with_ws[-1]
        pronoun = pronoun + whitespace
    return pronoun


def create_new_pronoun(token):
    """
    Lookup the new pronoun, handling capitalization and trailing whitespace.
    """
    new_pronoun = lookup_pronoun(token)
    new_pronoun = correct_capitalization(token, new_pronoun)
    new_pronoun = append_correct_whitespace(token, new_pronoun)
    return new_pronoun


def should_replace_pronoun(token, target_gender):
    """
    Determine if the word is a pronoun, with male or female gender,
    and whether the gender is different from the target gender.
    """
    return (
        (token.tag_ in ["PRP", "PRP$"])
        and (token._.gender in ["m", "f"])
        and (token._.gender != target_gender)
    )


def replace_pronoun_at_start_of_doc(nlp, doc, token, pronoun):
    return nlp.make_doc(f"{pronoun}" + doc[token.i + 1 :].text_with_ws)


def replace_pronoun_in_middle_of_doc(nlp, doc, token, pronoun):
    return nlp.make_doc(
        doc[: token.i].text_with_ws + f"{pronoun}" + doc[token.i + 1 :].text_with_ws
    )


def replace_pronouns(nlp, doc, target_gender):
    """
    Replace the pronouns in a sentence with pronouns of target_gender,
    if they are different to target_gender.
    """

    for token in doc:
        if should_replace_pronoun(token, target_gender):
            new_pronoun = create_new_pronoun(token)

            if token.i == 0:
                doc = replace_pronoun_at_start_of_doc(nlp, doc, token, new_pronoun)
            else:
                doc = replace_pronoun_in_middle_of_doc(nlp, doc, token, new_pronoun)
    return doc
