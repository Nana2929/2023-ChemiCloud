# use ckip word segmenter
from ckiptagger import data_utils, construct_dictionary, WS, POS, NER
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional
from src.base_determiner import BaseChemicalDeterminer

import re
import string

ckip_data_path = './src/data'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
class ZhChemicalDeterminer(BaseChemicalDeterminer):
    def __init__(self, dictionaries_dir: Path, *args, **kwargs):
        """__init__

        Args:
            lang (str): The language of the chemical list. `en` and `zh` are supported.
            dictionaries_dir (str, optional): The dir to dictionaries. Defaults to None.

        """
        super().__init__(lang = 'zh', dictionaries_dir=dictionaries_dir)
        self.dictionaries_dir = dictionaries_dir  # Path
        self._lang = 'zh'
        self.chemicals = open(
            self.dictionaries_dir / "chemical_list_zh-cleaned.txt").read().split("\n")

    @property
    def lang(self):
        return self._lang

    @lang.setter
    def lang(self, lang):
        self._lang = lang

    def _construct_dictionary(self):
        weighted_dict = {}
        for chemical in self.chemicals:
            weighted_dict[chemical] = len(chemical.split())
        return weighted_dict

    def batch_extract_chemical(self, articles: List[str]) -> List[Dict[str, Any]]:
        ws = WS(ckip_data_path, disable_cuda= False)
        dictionary = construct_dictionary(self._construct_dictionary())
        result = []
        def process_single_article(article: str) -> List[str]:

            article = re.sub(r", |\. ", " ", article)
            for punc in string.punctuation:
                article = re.sub('\\' + punc, f" {punc} ", article)
            article = re.sub(r"\s+", " ", article)

            article = article.lower()
            return article

        articles = [process_single_article(article) for article in articles]
        ws_articles = ws(articles, coerce_dictionary=dictionary)
        for article, ws_article in zip(articles, ws_articles):
            seq_ids, chemicals = self._identify_positions(article, ws_article)
            result.append({"processed_text": article, "ws": ws_article, "chemicals": chemicals, "seq_ids": seq_ids})
        return result



    def extract_chemical(self, article: str) -> Dict[str, Any]:
        return self.batch_extract_chemical([article])

    def _identify_positions(self, article: str, ws_article: List[str]) -> List[str]:
        intersect= set(ws_article) & set(self.chemicals)
        seq_ids, chemicals = [], []
        for chemical in intersect:
            begin = article.find(chemical)
            end = begin + len(chemical)
            if begin < 0:
                continue
            seq_ids.append((begin, end))
            chemicals.append(chemical)

        compact = [(s, c) for s, c in zip(seq_ids, chemicals)]
        compact.sort(key=lambda x: x[0])
        seq_ids, chemicals = zip(*compact) if compact else ([], []) 

        return seq_ids, chemicals




    def __repr__(self) -> str:
        return f"<ZhChemicalDeterminer> #chemicals = {len(self.chemicals)}"
