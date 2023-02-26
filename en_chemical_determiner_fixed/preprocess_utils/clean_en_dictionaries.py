import re
import string
import unicodedata
from typing import List, Set
from functools import partial

from .common import full_to_half, handle_punctuation


def load_dictionaries(dictionaries_dir: str) -> set:
    """load_dictionaries

    Args:
        dictionaries_dir (str): The dir to dictionaries.

    Returns:
        set: The set of dictionaries.
    """
    # Load dictionaries.
    paths: List[str] = list(map(str, dictionaries_dir.glob(f"*en*.txt")))

    dic = []

    for path in paths:
        dic.extend([word.strip().lower() for word in open(path).readlines()])

    dic = set(dic)

    with open(dictionaries_dir / "dismiss.txt") as dismiss_file:
        dismiss_set = set(dismiss_file.read().replace("\n", "").split(","))

    dic -= dismiss_set

    return dic


def clean_en_dictionaries(dictionaries_dir: str) -> List[str]:
    """clean_dictionaries clean and save the dictionaries.

    This function will clean the dictionaries and save
    the result in the same dir with name
    "chemical_list_en-cleaned.txt".

    Args:
        dictionaries_dir (str): The dir to dictionaries.
        lang (str): which language, supports `en`, `ch`
    """
    dicts = load_dictionaries(dictionaries_dir=dictionaries_dir)
    dicts = filter(lambda x: re.search(r'[a-zA-Z]', x), dicts)
    dicts = full_to_half(dicts)
    dicts = handle_punctuation(dicts)
    dicts = sorted(dicts)
    # filter out the empty strings
    with open(dictionaries_dir / f"chemical_list_en-cleaned.txt", "w") as f:
        f.write("\n".join(filter(lambda x: len(x) > 1, dicts)))

    return dicts
