from pytrends.request import TrendReq
import json
from datetime import datetime

def keywords (keyword):

    keywords = []
    keywords.append(keyword)
    timeframe = 'today 1-y'
    pytrends = TrendReq(hl='es-419', tz=360)
    kw_list = keywords
    pytrends.build_payload(kw_list, cat=0, timeframe=timeframe, geo='MX')

    keywords = pytrends.related_queries()
    keywords = keywords['Formica']['top']

    kwords = keywords['query']
    values = keywords['value']

    words = []
    for i in range(len(kwords)):
        record = {}
        record['text'] = kwords[i]
        record['value'] = values[i]
        words.append(record)

    return words




