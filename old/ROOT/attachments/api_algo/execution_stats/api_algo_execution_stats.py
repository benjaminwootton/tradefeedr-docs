## tradefeedr library
from tradefeedr_public_content.v1.generic.tradefeedr_api import TradefeedrApi  

## need pandas to translate JSON results from API
import pandas as pd 

## create API object 
tf_api_object = TradefeedrApi(demo=False)

## options
options = {
    "groupby": ["LP"],
    "select": [
        "TradeQuantityUSD", # sum 
        "SpreadPnLPM",      # TradeQuantityUSD-weighted average 
        "DecayPM1s",        # TradeQuantityUSD-weighted average
        "Symbol",           # cannot aggregate - returns None 
        "ExecVenue",        # cannot aggregate - returns None
        "Mid0",             # cannot aggregate - returns None
        "Price",            # cannot aggregate - returns None
        {"function": "sum", "var": "TradeQuantityUSD", "name": "TotalVolume"},      # explicit aggregation function 
        {"function": "avg", "var": "Price", "name": "AvgPrice"},                    # explicit aggregation function 
    ],
    "filter": [
        {"function": "within", "var": "Date", "pars": ["2014-01-01", "2021-11-30"]},
        {"function": "within", "var": "TradeTime", "transform": "time", "pars": ["12:00:00", "14:00:00"]},
        {"function": "in", "var": "Symbol", "pars": ["EURUSD", "USDJPY"]}, 
        {"function": "eq", "var": "ParentChild", "par": "Child"}, 
    ],
}

# this is api end-point which returns execution stats
endpoint = "v1/fx/algo/execution-stats"

## call the API 
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response['result'])
data_frame