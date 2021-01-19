# Genderalize

Genderalize is a small module for detecting the use of simple gender generalizations.
Gender generalization is one of several forms of gender bias defined in [Proposed Taxonomy for Gender Bias in Text; A Filtering Methodology for the Gender Generalization Subtype](https://www.semanticscholar.org/paper/Proposed-Taxonomy-for-Gender-Bias-in-Text%3B-A-for-Hitti-Jang/f05b9b663f1461ef2e20be5d2e8d2116a5a44f94).

This utility detects gender generalizations of the form

> The astronaut drank his coffee.

where a gender-specific pronoun ("his") was used with a gender neutral term. It also presents functions to replace gendered pronouns.

A sentence is identified as a gender generalization if it includes any gender-specific pronoun, but no person names or gender-specific nouns.
This is conservative in the sense that it will not detect all gender generalizations but is unlikely to classify something as a generalization that is not one.

The utility is composed of custom [spaCy](https://spacy.io/) (v2) pipeline components for identifying gender generalizations, and some functions for replacing gendered pronouns.
A small CLI script is included, which may be used as:

```
python cli.py "One sentence" "Another sentence" "And so on"
```

### Setup

Clone this repository, and start a python3 virtual environment by your preferred means.
Within that environment, run:

```bash
pip install -r requirements.txt
```

#### Conventions

The repo uses [black](https://github.com/psf/black) for code fomatting, [pytest](https://docs.pytest.org/en/stable/) for testing and [pylint](http://pylint.pycqa.org/en/latest/) for linting.

### Data

The word gender dictionary in `genderalize/words.json` is derived from [ecmonsen/gendered_words](https://github.com/ecmonsen/gendered_words), which is licensed under [Creative Commons Attribution 3.0](https://creativecommons.org/licenses/by/3.0/us/), and WordNet content is licensed under the [WordNet License](https://wordnet.princeton.edu/license-and-commercial-use).

### Known limitations

#### Non-binary gender

Gender is non-binary. Pronoun replacement works only for male (he/him) and female (she/her) gendered pronouns. Truly neutralizing sentences with singular they/them pronouns presents a harder technical challenge, but would be worthy work.

#### Entity resolution

No attempt at entity resolution is made. In principle it would be possible to detect more generalizations by resolving to which entity in a sentence gendered pronouns apply.

#### Lemmatization

No lemmatization (including plurals). The detection of gendered nouns relies on a dictionary, which does not include all forms of the nouns. For instance, "Ballerinas" will not be detected as gendered, but "Ballerina" will.

#### Long contexts

By design, the tool works only for simple, _independent_ documents. No attempt at capturing long context is made. Some things that may not be generalizations, because the gender of the subject is known, will be detected as such, because it is not known within the short context of a single sentence (or whatever document is passed).

#### Statistical errors

The library is subject to the usual limitations of a statistical model, and gendered pronoun replacement is particularly vulnerable to mis-tagging the part-of-speech. For instance, one test case (in `tests/test_replace_pronouns.py` is to transform the sentence

> "The astronaut loved her shiny new helmet. It was just hers."

into

> "The astronaut loved his shiny new helmet. It was just his."

This works. However, the converse, transforming

> "The astronaut loved his shiny new helmet. It was just his."

into

> "The astronaut loved her shiny new helmet. It was just hers."

fails, because the `en_core_web_sm` model mis-tags the final "his" in the input sentence as a personal pronoun (`PRP`) instead of a possessive determiner (`PRP$`). Language is hard, and it's possible larger models will solve this (at the cost of increased memory and compute usage).
