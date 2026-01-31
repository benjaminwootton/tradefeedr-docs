## tradefeedr library
from tradefeedr_public_content.v1.generic.tradefeedr_api import TradefeedrApi  

## need pandas to translate JSON results from API
import pandas as pd 

## create API object 
tf_api_object = TradefeedrApi(demo=False)

## options
options = {
    "groupby": [
        "TradeID"
    ],
    "select": [
        "TradeQuantityUSD",
        "SpreadPnLPM",
        "DecayPM1s",
        "Symbol",
        "LP",
        "Side",
        "ExecVenue",
        "Mid0",
        "Price",
        {"function": "sum", "var": "TradeQuantityUSD", "name": "TotalVolume"}, 
        {"function": "avg", "var": "Price", "name": "AvgPrice"} 
    ],
    "filter": [
        {"function": "within", "var": "Date", "pars": ["2014-01-01", "2021-11-30"]},
        {"function": "within", "var": "TradeTime", "transform": "time", "pars": ["12:00:00", "14:00:00"]},
        {"function": "in", "var": "Symbol", "pars": ["EURUSD", "USDJPY"]}, 
        {"function": "eq", "var": "ParentChild", "par": "Child"}
    ],
}

# this is api end-point which returns execution stats
endpoint = "v1/fx/algo/execution-stats"

## call the API 
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response['result'])
data_frame