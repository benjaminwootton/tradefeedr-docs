## tradefeedr library
from tradefeedr_public_content.v1.generic.tradefeedr_api import TradefeedrApi

## need pandas to translate JSON results from API
import pandas as pd

## create API object
tf_api_object = TradefeedrApi(demo=True)

## options
options = {
    "groupby": [
        "LP"
    ],
    "select": [
        "TradeQuantityUSD", # sum
        "Symbol",           # cannot aggregate - returns None
        "Side",             # cannot aggregate - returns None
        "Price",            # cannot aggregate - returns None
        "NumLPs",           # default aggregation not defined - returns None, need to use user defined function to aggregate
        "SecondBestPrice",  # default aggregation not defined - returns None, need to use user defined function to aggregate
        "BestBid",          # default aggregation not defined - returns None, need to use user defined function to aggregate
        "BestAsk",          # default aggregation not defined - returns None, need to use user defined function to aggregate
        {"function": "sum", "var": "TradeQuantityUSD", "name": "TotalVolume"}       # explicit aggregation function
    ],
    "filter": [
        {"function": "within", "var": "Date", "pars": ["2014-01-01", "2021-11-30"]},
        {"function": "within", "var": "TradeTime", "transform": "time", "pars": ["12:00:00", "14:00:00"]}
    ],
}

# this is api end-point which returns RFQ outrights execution stats
endpoint =  "v1/fx/rfq-outrights/execution-stats"

## call the API
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response["result"])
# data_frame = data_frame.set_index("LP")
data_frame