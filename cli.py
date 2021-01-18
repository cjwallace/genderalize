import json
import sys

import en_core_web_sm

from genderalize import GenderMatcher, gender_generalization_matcher, gendered_dict


def main(sentence):
    nlp = en_core_web_sm.load()

    gender_component = GenderMatcher(nlp, gendered_dict)
    nlp.add_pipe(gender_component)
    nlp.add_pipe(gender_generalization_matcher)

    for doc in nlp.pipe(sentence):
        print(doc)
        print("has_person: ", doc._.has_person)
        print("has_gendered_pronouns: ", doc._.has_gendered_pronouns)
        print("has_gendered_nouns: ", doc._.has_gendered_nouns)
        print("is gender_generalization: ", doc._.is_gender_generalization)
        print()


if __name__ == "__main__":
    main(sys.argv[1:])
