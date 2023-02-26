import os
from pathlib import Path
from pprint import pprint
from src.zh_determiner import ZhChemicalDeterminer
from preprocess_utils.clean_zh_dictionaries import clean_zh_dictionaries

import logging
logging.basicConfig(level=logging.INFO)


def main():
    dictionaries_dir = Path(__file__).parent.parent.parent / "data/dictionaries/chemical_determine"
    ch_cleaned_file = dictionaries_dir / "chemical_list_zh-cleaned.txt"

    if not (ch_cleaned_file).exists():
        clean_zh_dictionaries(dictionaries_dir=dictionaries_dir)
    determiner = ZhChemicalDeterminer(dictionaries_dir=dictionaries_dir)

    articles = [
        "從當地時間週三（8月4日）起禁止遊客或民眾在所有海洋國家公園使用含以下4種化學成分的\
            防曬產品，包括二苯甲酮（oxybenzone）、甲氧基肉桂酸辛酯 （octinoxate）、\
                4-甲基亞苄基樟腦（4-methylbenzylid camphor ）以及對羥苯甲酸丁酯（butylparaben）；\
                    當局指出，「這些化學物質會破壞珊瑚礁生長，恐導致珊瑚白化現象」。",
        "羥丙甲纖維素 鄰苯二甲酸酯 ( h pm cp )", "BPA 或雙酚 A 是一種聚合物或分子鏈，通常用於製造聚碳酸酯塑料製品",
        "一批由韓國出口的「NONGSHIM農心超進化辛碗麵（豆腐泡菜味）」1128公斤，其調味粉包被檢出殘留農藥環氧乙烷",
        "另外，為維護青少年身體健康，免於新興精神活性物質的威脅，化學局也將尚未公告為毒品的物質1,4-丁二醇、海罌粟鹼，列為關注化學物質。而在爆裂物先驅化學物質方面，因應其物理特性，可能遭有心人士做成爆裂物或炸彈，將硝酸鈣、硝酸鈉、硝酸銨鈣、硝基甲烷、曡氮化鈉、過氯酸銨、過氯酸鈉及磷化鋁，一併納入關注化學物質管理。"
         , "有食安疑慮的物質共有五項，分別為一氧化鉛、四氧化三鉛、硫化鈉、硫氰酸鈉及β-荼（萘）酚。林松槿指出，過去曾有不肖廠商，將硫化鈉當成製作臭豆腐的原料",

    ]
    for article in articles:
        print(article)
        print(determiner.extract_chemical(article))
        print()


if __name__ == "__main__":
    main()