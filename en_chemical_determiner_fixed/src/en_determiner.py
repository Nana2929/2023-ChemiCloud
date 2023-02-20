import logging
from tqdm import tqdm
import re
from typing import List, Sequence, Union, Dict
import string
from pathlib import Path

from src.base_determiner import BaseChemicalDeterminer
from src.Node import Node, json2tree, tree2json

l = logging.getLogger(__name__)


class EnChemicalDeterminer(BaseChemicalDeterminer):

    def __init__(self, lang, dictionaries_dir: Path):
        """__init__

        Args:
            dictionaries_dir (str, optional): The dir to dictionaries. Defaults to None.
        """
        super().__init__(lang = lang, dictionaries_dir = dictionaries_dir)
        self.dictionaries_dir = dictionaries_dir  # Path
        self._lang = lang
        # filepath = dictionaries_dir / f"chemical_list_{lang}-cleaned.txt"
        # self.chemicals = open(filepath).read().split("\n")
        self.searching_tree = self._get_searching_tree()

    @property
    def lang(self):
        return self._lang

    @lang.setter
    def lang(self, lang):
        self._lang = lang

    @staticmethod
    def generate_searching_tree(
        chemicals: Sequence[str],
        json_path: str = None,
    ) -> Node:
        """generate_searching_tree

        This function will generate a searching tree from chemicals list
        and save it to json_path if json_path is not None.

        Args:
            chemicals (Sequence[str]): List of chemicals
            json_path (str, optional): Path to save the result in pickle format. Defaults to None.
                                    It is not recommended if the searching tree is large and deep (too slow).

        Returns:
            Node: The searching tree
        """
        root = Node('root')
        chemicals = sorted(chemicals)
        # chemicals = set(chemicals)
        l.info(f'Number of chemicals: {len(chemicals)}')

        for chemical in tqdm(chemicals,
                             desc="Generating searching tree",
                             total=len(chemicals)):
            words = chemical.split(' ')
            parent = root
            for word in words:
                if word in parent:  # if word's name in parent.children
                    parent = parent[
                        word]  # def __contains__(self, key): return key in self.children
                else:
                    current = Node(word, parent)
                    parent.add_child(current)
                    parent = current

            parent.add_child('<end>')

        if EnChemicalDeterminer.is_cyclic(root):
            raise RuntimeError("The searching tree is cyclic.")
        if json_path:
            l.info(f"Saving searching tree to {json_path}")
            tree2json(root, json_path)
        return root

    def extract_chemical(
        self,
        article: str,
    ) -> List[str]:
        """extract_chemical extract all chemicals which
        was defined at chemical_list_en-cleaned.txt from article

        Args:
            article (str): The article from which you want to extract chemicals

        Returns:
            List[str]: List of chemicals
        """
        result = []
        article = re.sub(r", |\. ", " ", article)

        for punc in string.punctuation:
            article = re.sub('\\' + punc, f" {punc} ", article)
        article = re.sub(r"\s+", " ", article)

        words = article.lower().split(' ')

        def continue_extract(
            wi: int,
            words: List[str],
            current_tree: Node,
        ) -> None:
            try:
                while current_tree and words[wi] in current_tree:
                    current_tree = current_tree[words[wi]]
                    if '<end>' in current_tree:
                        out = current_tree.track_back()
                        result.append(out)
                    wi += 1
                    if words[wi] in self.searching_tree:
                        continue_extract(
                            wi=wi,
                            words=words,
                            current_tree=self.searching_tree[words[wi]],
                        )
            except IndexError:
                return

        for wi, word in enumerate(words):

            if word not in self.searching_tree:
                continue

            continue_extract(
                wi=wi,
                words=words,
                current_tree=self.searching_tree,
            )

        return result

    def batch_extract_chemical(
        self,
        articles: List[str],
    ) -> List[List[str]]:
        """batch_extract_chemical

        Args:
            articles (List[str]): List of articles

        Returns:
            List[List[str]]: List of chemicals for each article
        """
        return [self.extract_chemical(article=article) for article in articles]
