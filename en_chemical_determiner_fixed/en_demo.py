#%%
from pathlib import Path
from pprint import pprint
from src.en_determiner import EnChemicalDeterminer
from preprocess_utils.clean_dictionaries import clean_dictionaries
import logging

logging.basicConfig(level=logging.INFO)


def main():
    dictionaries_dir = Path(
        __file__).parent.parent.parent / "data/dictionaries/chemical_determine"

    if not (dictionaries_dir / "chemical_list_en-cleaned.txt").exists():
        clean_dictionaries(dictionaries_dir)
    determiner = EnChemicalDeterminer(dictionaries_dir=dictionaries_dir,
                                      lang='en')

    articles = [
        "Three common solvents—methylene chloride acetate N-methylpyrrolidone (NMP), and perchloroethylene—pose unreasonable risks to human health under multiple use scenarios, the US Environmental Protection Agency concludes in separate draft risk evaluations released within days of each other.",
        "this chemical 3-monochloorpropaan-1,2-diol is toxic.",
        "Ethylene oxide cyclic (EO) is a chemical that is used in the manufacture of electronic devices. It is a very common chemical in the electronics industry, and is used in a wide range of applications.",
        "No definition-ethylene oxide BG",
    ]
    for article in articles:
        print(article)
        print(determiner.extract_chemical(article))
        print()


if __name__ == "__main__":
    main()