
from typing import Dict, List, Optional, Union
from pathlib import Path
import json
import string

class Node():

    def __init__(self, name: str, parent: Optional["Node"] = None):
        """__init__

        Note:
            Another method to solve serialization issue is to inherit from Dict, but
            that will make `is_cyclic` returns True since 2 nodes with the same name and same children number
            are considered to be the same objects.
            Therefore, `from_dict()` is used to solve serialization.
        Args:
            name (str): The name of the node.
            parent (Optional["Node"], optional): The parent node. Defaults to None.
        """
        self.name = name
        self.parent = parent
        self.children = {}

    def add_child(self, child: Union[str, "Node"]) -> None:
        """add_child

        Args:
            child (Union[str, "Node"]): The child node to be added.

        Raises:
            TypeError: If the child is neither a Node nor a string.
        """
        if isinstance(child, str):
            child = Node(child, self)
            self.children[child.name] = child
        elif isinstance(child, Node):
            child.parent = self
            self.children[child.name] = child
        else:
            raise TypeError(f"child must be str or Node, not {type(child)}")

    def track_back(self) -> str:
        """track_back

        Returns:
            str: The string of the path from the root to the current node.
        """
        parent = self.parent
        result = self.name

        while parent is not None and parent.name != "root":
            result = f"{parent.name} {result}"
            parent = parent.parent

        for punc in string.punctuation:
            result = result.replace(f" {punc} ", punc)
        return result

    @staticmethod
    def from_dict(tree_dict: Dict):
        """from_dict transforms a serialized tree dictionary to a tree structure, serves as an adapter.
        Args:
            tree_dict (Dict): The serialized tree dictionary.
        Returns:
            Node: The decoded tree structure.
        """
        node = Node(tree_dict['name'], tree_dict['children'])
        node.children = {k: Node.from_dict(v) for k, v in tree_dict['children'].items()}
        return node

    @staticmethod
    def to_dict(node: "Node"):
        """to_dict transforms a tree structure to a serialized tree dictionary, serves as an adapter.
        Returns:
            Dict: The serialized tree dictionary.
        """
        print(node, type(node))
        return {
            'name': node.name,
            'children': {k: Node.to_dict(v)
                         for k, v in node.children.items()}
        }

    def __repr__(self): # magic function
        return f"{self.name}|{len(self.children)}"

    def __getitem__(self, key):
        return self.children[key]

    def __setitem__(self, key: str, value):
        self.children[key] = value

    def __contains__(self, key):
        return key in self.children


# ==============================================
def json2tree(path: Union[str, Path]) -> Dict:
    """load_json

    Args:
        path (Union[str, Path]): The path to the json file.

    Returns:
        Dict: The loaded json file.
    """
    with open(path, "r", encoding="utf-8") as f:
        return Node.from_dict(json.loads(f.read()))


def tree2json(node: Node, path: Union[str, Path]) -> None:
    """save_json

    Args:
        node_dict (Dict): The dictionary to be saved.
        path (Union[str, Path]): The path to the json file.
    """
    with open(path, "w", encoding="utf-8") as f:

        jsonstr = json.dumps(Node.to_dict(node))
        f.write(jsonstr)


# ==============================================

