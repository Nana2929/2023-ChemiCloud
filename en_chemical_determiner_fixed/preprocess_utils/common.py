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

def gen_zh_subwords(values: Set[str],
                    suffix_only = False,
                    min_len: int = 3,) -> Set[str]:
    """add_zh_subwords
        Args:
            values (Set[str]): The values to handle.
            suffix_only (bool): Whether to only add suffixes of the value.
            threshold (int): The threshold of the length of the subword.
        Yields:
            Iterator[Set[str]]: The subwords to use to expand the dictionary.
    """
    for value in values:
        matches = re.findall(r"[\u4e00-\u9fa5]+", value)
        if suffix_only and len(matches):
            if len(matches[-1]) > min_len:
                yield matches[-1]
        else:
            for match in matches:
                if len(match) > min_len:
                    yield match
