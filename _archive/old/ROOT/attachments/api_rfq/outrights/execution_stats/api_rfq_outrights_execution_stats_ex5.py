## tradefeedr library
from tradefeedr_public_content.v1.generic.tradefeedr_api import TradefeedrApi  

## need pandas to translate JSON results from API
import pandas as pd 

## create API object 
tf_api_object = TradefeedrApi(demo=False)

## options
options = {
    "groupby": [
        "Symbol",
        "LP",
        "Side"
    ],
    "select": [
        "TradeQuantityUSD",   # spread paid by client, implicit aggregation is TradeQuantityUSD-weighted average
    ],
    "filter": [
        {"function": "not_in", "var": "Symbol", "pars": ["EURUSD", "USDJPY", "GBPUSD"]}, 
        {"function": "gt", "var": "TradeQuantityUSD", "par": 1e7},   # greater than
        {"function": "not_eq", "var": "Side", "par": "B"},
        {"function": "within", "var": "Date", "pars": ["2014-01-01", "2021-11-30"]},
        {"function": "within", "var": "TradeTime", "transform": "time", "pars": ["08:00:00", "17:00:00"]} 
    ],
}

# this is api end-point which returns RFQ outrights execution stats
endpoint  =  "v1/fx/rfq-outrights/execution-stats"

## call the API 
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response['result'])
data_frame