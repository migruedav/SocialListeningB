from pytrends.request import TrendReq
from datetime import datetime
import json


def trends(keywords, timeframe):

    keywords = keywords.split(',')
    keywords = [i.strip() for i in keywords]


    pytrends = TrendReq(hl='es-419', tz=360)
    kw_list = keywords
    pytrends.build_payload(kw_list, cat=0, timeframe=timeframe, geo='MX')


    iot = pytrends.interest_over_time()
    iot = iot.drop(columns=['isPartial'])
    iot = iot.to_json(orient='table')
    iot = json.loads(iot)
    iot = iot['data']


    for i in iot:
        i['date'] = i['date'][:10]
        i['date'] = datetime.strptime(i['date'], '%Y-%m-%d').strftime('%b %d, %Y')

    ibr = pytrends.interest_by_region()

    ibr = ibr.to_json(orient='table')
    ibr = json.loads(ibr)
    ibr = ibr['data']

    return {'iot': iot, 'ibr': ibr}


