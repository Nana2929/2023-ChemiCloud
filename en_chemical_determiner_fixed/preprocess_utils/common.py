from typing import Set
from functools import partial
import unicodedata
import string
import re


def full_to_half(values: Set[str]) -> Set[str]:
    """full_to_half convert full-width characters to half-width characters.

    Args:
        values (Set[str]): The values to handle.

    Returns:
        Set[str]: The values after handling.
    """
    f2h = partial(unicodedata.normalize, "NFKC")
    return set(map(f2h, values))


def handle_punctuation(values: Set[str]) -> Set[str]:
    """handle_punctuation

    Args:
        values (Set[str]): The values to handle.

    Yields:
        Iterator[Set[str]]: The value after handling.
    """
    # remove redundant spaces
    space = lambda x: re.sub(r"\s+", " ", x)
    punctuation = set(string.punctuation).difference(
        {'-', '(', ')', '[', ']', '{', '}', ':', ',', ';', '|'})
    punctuation = "|".join(punctuation).replace("+", "\+").replace("*", "\*").replace(
        "?", "\?").replace("$", "\$").replace("^", "\^").replace(".", "\.").replace("?", "\?")
    print(punctuation)
    remove_punct = lambda x: re.sub(punctuation, "", x)

    for value in values:
        value = remove_punct(value)
        for punc in string.punctuation:
            value = re.sub('\\' + punc, f" {punc} ", value)
        value = space(value)
        # remove chinese
        yield value.strip()