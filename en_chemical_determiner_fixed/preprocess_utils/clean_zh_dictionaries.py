import re
import string
import unicodedata
from typing import List, Union
from pathlib import Path
from functools import partial
import logging

from tokenizers import Tokenizer
from tokenizers.models import BPE
from tokenizers.trainers import BpeTrainer

from .common import full_to_half, handle_punctuation, gen_zh_subwords

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def bpe_tokenize(
    dictionaries_dir: Union[str, Path],
    # tokenizer_type='bpe',
    pretrained_path=None,
    vocab_size: int = 30000,
    min_frequency: int = 2,
    save_file: str = 'zh_{tokenizer_type}_tokenizer.json',
):
    dictionaries = load_dictionaries(dictionaries_dir)
    tokenizer_type = 'bpe'

    tokenizer = Tokenizer(BPE())
    if pretrained_path:
        logger.info(f'Load pretrained tokenizer from {pretrained_path}')
        tokenizer = Tokenizer.from_file(pretrained_path)
    else:
        logger.info(f'Train {tokenizer_type} tokenizer from scratch.')
        trainer = BpeTrainer(vocab_size=vocab_size,
                             min_frequency=min_frequency,
                             special_tokens=["[UNK]", "[CLS]", "[SEP]", "[PAD]", "[MASK]"])

        tokenizer.train_from_iterator(dictionaries, trainer=trainer)

        save_path = dictionaries_dir / save_file.format(tokenizer_type=tokenizer_type)
        tokenizer.save(str(save_path))

    # output = tokenizer.encode(
    #     "從當地時間週三（8月4日）起禁止遊客或民眾在所有海洋國家公園使用含以下4種化學成分的防曬產品，包括二苯甲酮（oxybenzone）、甲氧基肉桂酸辛酯 （octinoxate）、4-甲基亞苄基樟腦（4-methylbenzylid camphor ）以及對羥苯甲酸丁酯（butylparaben）；當局指出，「這些化學物質會破壞珊瑚礁生長，恐導致珊瑚白化現象」。"
    # )
    tokenized_outputs = tokenizer.encode_batch(list(dictionaries))
    tokenized_outputs = [' '.join(output.tokens) for output in tokenized_outputs]
    logger.info(f"preview tokenized_outputs: {tokenized_outputs[:5]}")

    return set(tokenized_outputs)


def load_dictionaries(dictionaries_dir: str) -> set:
    """load_dictionaries

    Args:
        dictionaries_dir (str): The dir to dictionaries.

    Returns:
        set: The set of dictionaries.
    """

    # Load dictionaries.

    dic = []
    paths: List[str] = list(map(str, dictionaries_dir.glob(f"*zh*.txt")))

    for path in paths:
        dic.extend([word.strip().lower() for word in open(path).readlines()])

    dic = set(dic)

    with open(dictionaries_dir / "dismiss.txt") as dismiss_file:
        dismiss_set = set(dismiss_file.read().replace("\n", "").split(","))

    dic -= dismiss_set
    return dic


def clean_zh_dictionaries(dictionaries_dir: str) -> List[str]:
    """clean_dictionaries clean and save the dictionaries.

    This function will clean the dictionaries and save
    the result in the same dir with name
    "chemical_list_en-cleaned.txt".

    Args:
        dictionaries_dir (str): The dir to dictionaries.
        lang (str): which language, supports `en`, `ch`
    """

    dicts = bpe_tokenize(dictionaries_dir)
    dicts = filter(lambda x: re.search(r'[a-zA-Z]', x), dicts)
    dicts = full_to_half(dicts)
    # add subwords
    tokens = gen_zh_subwords(dicts, suffix_only=True, min_len=4)
    dicts = dicts + tokens

    dicts = handle_punctuation(dicts)
    dicts = sorted(dicts)
    logger.info(f"Chemicals count: {len(dicts)}")

    # filter out empty strings
    with open(dictionaries_dir / f"chemical_list_zh-cleaned.txt", "w") as f:
        f.write("\n".join(filter(lambda x: len(x) > 1, dicts)))

    return dicts





if __name__ == "__main__":
    dictionries_dir = '/home/nanaeilish/projects/2023-chemicloud/en_chemical_determiner_fixed/data/dictionaries/chemical_determine'
    import pathlib
    dictionries_dir = pathlib.Path(dictionries_dir)
    clean_zh_dictionaries(dictionries_dir)
