from typing import Union, List, Dict
import opencc


def t2sconvert(texts: Union[List, Dict, str])-> Union[List, Dict, str]:

    converter = opencc.OpenCC('t2s.json')
    if isinstance(texts, str):
        new_texts = converter.convert(texts)
    elif isinstance(texts, list):
        new_texts = []
        for i in range(len(texts)):
            new_texts.append(converter.convert(texts[i]))
    elif isinstance(texts, dict):
        new_texts = {}
        for key, value in texts.items():
            key = converter.convert(key)
            new_texts[key] = t2sconvert(value)
    assert len(texts) == len(new_texts)
    del texts
    return new_texts


def s2tconvert(texts: Union[List, Dict, str])-> Union[List, Dict, str]:

    converter = opencc.OpenCC('s2t.json')
    if isinstance(texts, str):
        new_texts = converter.convert(texts)
    elif isinstance(texts, list):
        new_texts = []
        for i in range(len(texts)):
            new_texts.append(converter.convert(texts[i]))
    elif isinstance(texts, dict):
        new_texts = {}
        for key, value in texts.items():
            key = converter.convert(key)
            new_texts[key] = s2tconvert(value)
    assert len(texts) == len(new_texts)
    del texts
    return new_texts