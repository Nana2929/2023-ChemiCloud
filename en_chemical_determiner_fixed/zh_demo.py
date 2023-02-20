import os
from pathlib import Path
from pprint import pprint
from en_chemical_determiner_fixed.src.en_determiner import EnChemicalDeterminer
from preprocess_utils.clean_dictionaries import clean_dictionaries as en_clean_dictionaries
from preprocess_utils.clean_zh_dictionaries import clean_dictionaries as zh_clean_dictionaries
import logging

logging.basicConfig(level=logging.INFO)


def main():
    dictionaries_dir = Path(__file__).parent.parent.parent / "data/dictionaries/chemical_determine"
    ch_cleaned_file = dictionaries_dir / "chemical_list_zh-cleaned.txt"

    if not (ch_cleaned_file).exists():
        zh_clean_dictionaries(dictionaries_dir=dictionaries_dir)
    determiner = EnChemicalDeterminer(dictionaries_dir=dictionaries_dir, lang='zh')

    articles = [
        "從當地時間週三（8月4日）起禁止遊客或民眾在所有海洋國家公園使用含以下4種化學成分的防曬產品，包括二苯甲酮（oxybenzone）、甲氧基肉桂酸辛酯 （octinoxate）、4-甲基亞苄基樟腦（4-methylbenzylid camphor ）以及對羥苯甲酸丁酯（butylparaben）；當局指出，「這些化學物質會破壞珊瑚礁生長，恐導致珊瑚白化現象」。",
    ]
    for article in articles:
        print(article)
        print(determiner.extract_chemical(article))
        print()


if __name__ == "__main__":
    main()