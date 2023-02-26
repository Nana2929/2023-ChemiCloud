from pathlib import Path
from typing import List, Optional, Union, Sequence
import abc
import logging
import tqdm

from src.Node import Node, json2tree, tree2json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaseChemicalDeterminer(abc.ABC):

    def __init__(self, lang:str, dictionaries_dir: Path, *args, **kwargs):
        """__init__

        Args:
            lang (str): The language of the chemical list. `en` and `zh` are supported.
            dictionaries_dir (str, optional): The dir to dictionaries. Defaults to None.

        """
        self.dictionaries_dir = dictionaries_dir  # Path
        self._lang = lang
        self.chemicals = open(
            self.dictionaries_dir /
            f"chemical_list_{self.lang}-cleaned.txt").read().split("\n")

    def __repr__(self) -> str:
        return f"<BaseChemicalDeterminer> #chemicals = {len(self.chemicals)}"

    @property
    @abc.abstractmethod
    def lang(self):
        pass

    @lang.setter
    @abc.abstractmethod
    def lang(self, lang):
        pass

    @staticmethod
    def is_cyclic(root: Node):
        """is_cyclic will check if the searching tree is cyclic.

        Args:
            root (Node): The root node of the searching tree.

        Returns:
            bool: True if the searching tree is cyclic, False otherwise.
        """
        visited = set()
        stack = [root]

        while stack:
            node = stack.pop()
            if node in visited:
                return True
            visited.add(node)
            stack.extend(node.children.values())
        return False

    @staticmethod
    def generate_searching_tree() -> Node:
        raise NotImplementedError

    @abc.abstractmethod
    def extract_chemical(
        self,
        article: str,
    ) -> List[str]:
        raise NotImplementedError

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
