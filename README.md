# Genderalize

Genderalize is a small _alpha-quality_ utility for detecting the use of simple gender generalizations.
Gender generalization is one of several forms of gender bias defined in [Proposed Taxonomy for Gender Bias in Text; A Filtering Methodology for the Gender Generalization Subtype](https://www.semanticscholar.org/paper/Proposed-Taxonomy-for-Gender-Bias-in-Text%3B-A-for-Hitti-Jang/f05b9b663f1461ef2e20be5d2e8d2116a5a44f94).

This utility detects gender generalizations of the form

> The astronaut drank his coffee.

where a gender-specific pronoun ("his") was used with a gender neutral noun (astronaut). It also presents functions to replace gendered pronouns, turning the above text into

> The astronaut drank her coffee.

A sentence is identified as a gender generalization if it:

- includes any gender-specific pronoun,
- but no person names
- and no gender-specific nouns.

This is conservative in the sense that it will not detect all gender generalizations but is unlikely to classify something as a generalization that is not one.

## Usage

### CLI

A [typer](typer.tiangolo.com/) CLI is included, which, once installed, has two functions.

The first is detection of gender generalizations:

```
genderalize detect "The ballet dancer tied her shoes"
=> True # this is a gender generalization

genderalize detect "The ballerina tied her shoes"
=> False # this is not, since ballerina is gendered
```

The second is to replace male and female pronouns in a gender generalization:

```
genderalize change m "The ballet dancer tied her shoes"
=> "The ballet dancer tied her shoes"

genderalize change f "The fireman wore his hat"
=> "The fireman wore his hat"
```

Notice in the second example, the output is unchanged.
Fireman is a gendered term, so this is not a gender generalization in the sense that it is referred to in this utility.

Further instructions for the CLI can be obtained with the CLI itself:

```
genderalize --help
```

### API

A small REST API is also provided using [FastAPI](https://fastapi.tiangolo.com/).
The API can be served with

```
uvicorn genderalize.api:app --reload
```

This exposes three endpoints on `localhost:8000` (by default).
The endpoints are:

- `/status` - this always returns green, and should be used only to test that the endpoint is accessible.
- `/biases` - this expects some input text and returns a response of the form `{generalization: True}` if the text is a gender generalization.
- `/biases/generalizations/{m,f}` - expects input text, and converts the pronoun to the specified m/f gender if the text is a gender generalization.

Specific request and response forms can be viewed in the auto-generated documentation at `localhost:8000/docs`.

### Library

The CLI is built using the included `genderalize` library. It is composed of custom [spaCy](https://spacy.io/) (v2) pipeline components for identifying gender generalizations, and some functions for replacing gendered pronouns.

## Installation

This repository is intended to be installed via [Poetry](https://python-poetry.org/).
To install, clone the repository, and run `poetry install` inside it (this may require you to first [install Poetry](https://python-poetry.org/docs/#installation)).

A `requirements.txt` file is provided, which should enable installation in other python 3 environments.

## Conventions

The repo uses default configurations of

- [black](https://github.com/psf/black) for code formatting,
- [pytest](https://docs.pytest.org/en/stable/) for testing, and
- [pylint](http://pylint.pycqa.org/en/latest/) for linting.

## Data

The word gender dictionary in `genderalize/words.json` is derived from [ecmonsen/gendered_words](https://github.com/ecmonsen/gendered_words), which is licensed under [Creative Commons Attribution 3.0](https://creativecommons.org/licenses/by/3.0/us/), and WordNet content is licensed under the [WordNet License](https://wordnet.princeton.edu/license-and-commercial-use).

## Known limitations

Aside from detecting only gender generalizations and not other forms of gender bias in text, there are several clear limitations to the utility (and likely many less obvious failings).

### Non-binary gender

Gender is non-binary. Pronoun replacement works only for male (he/him) and female (she/her) gendered pronouns. Truly neutralizing sentences with singular they/them pronouns presents a harder technical challenge, but would be worthy work.

### Entity resolution

No attempt at entity resolution is made. In principle it would be possible to detect more, and more granular gender generalizations by resolving to which entity in a sentence gendered pronouns apply.

### Lemmatization

No lemmatization (including plurals). The detection of gendered nouns relies on a dictionary, which does not include all forms of the nouns. For instance, "Ballerinas" will not be detected as gendered, but "Ballerina" will.

### Long contexts

By design, the tool works only for simple, _independent_ documents. No attempt at capturing long context is made. Some things that may not be generalizations, because the gender of the subject is known, will be detected as such, because it is not known within the short context of a single sentence (or whatever document is passed).

### Statistical errors

The library is subject to the usual limitations of a statistical model, and gendered pronoun replacement is particularly vulnerable to mis-tagging the part-of-speech. For instance, one test case (in `tests/test_replace_pronouns.py` is to transform the sentence

> "The astronaut loved her shiny new helmet. It was just hers."

into

> "The astronaut loved his shiny new helmet. It was just his."

This works. However, the converse, transforming

> "The astronaut loved his shiny new helmet. It was just his."

into

> "The astronaut loved her shiny new helmet. It was just hers."

fails, because the `en_core_web_sm` model mis-tags the final "his" in the input sentence as a personal pronoun (`PRP`) instead of a possessive determiner (`PRP$`). Language is hard. It's possible larger models (this project uses spaCy's `en_core_web_sm` model) could improve this (at the cost of increased memory and compute usage).
