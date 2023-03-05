import os
import pandas as pd
from typing import Union, List, Dict
from pprint import pprint

from paddlenlp import Taskflow
from utils import t2sconvert, s2tconvert



root = '/paddle-test/2023-chemicloud/'
data_dir = os.path.join(root, 'data')
filename = '食品安全_重新整合.xlsx'
textcol = '新聞內容'
df = pd.read_excel(os.path.join(data_dir, filename))

df['simplified_text'] = df[textcol].apply(t2sconvert)
schema = {"機構": [], "化學物質": ["治癌物", "農藥"], "產品": [], "時間": []}
schema = t2sconvert(schema)
ie = Taskflow('information_extraction', schema=schema)
df['uie_base'] = df['simplified_text'].apply(ie)
for rid, row in df.iterrows():
    print(df[textcol])
    pprint(row['uie_base'])
    break



df.to_pickle(os.path.join(data_dir, '食品安全_ws_uie.csvpkl'))
