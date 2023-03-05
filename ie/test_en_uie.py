from pprint import pprint
from paddlenlp import Taskflow
schema = ['Person', 'Organization']
ie_en = Taskflow('information_extraction', schema=schema, model='uie-base-en')
pprint(ie_en('In 1997, Steve was excited to become the CEO of Apple.'))
# [{'Organization': [{'end': 53,
#                     'probability': 0.9998692302791312,
#                     'start': 48,
#                     'text': 'Apple'}],
# 'Person': [{'end': 14,
#             'probability': 0.9996516411866807,
#             'start': 9,
#             'text': 'Steve'}]}]