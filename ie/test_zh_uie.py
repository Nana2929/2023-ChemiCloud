from paddlenlp import Taskflow
import opencc
from typing import Union, List, Dict
from utils import t2sconvert

schema ={
    "機構":[],
    "化學物質":[
        "治癌物",
        "農藥"],
    "產品":[],
    "時間":[]
}

# UIESentaTask # Google 計畫可以用
# https://github.com/PaddlePaddle/PaddleNLP
text = "哈根達斯香草冰淇淋再被驗出致癌物環氧乙烷"
text = t2sconvert(text)
schema = t2sconvert(schema)
ie = Taskflow('information_extraction', schema=schema)
ner_uiebase_ = ie(text)
print(ner_uiebase_)