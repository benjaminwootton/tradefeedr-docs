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
        {"function": "sum", "var": "TradeQuantityUSD", "name": "TotalVolume"},
        {"function": "avg", "var": "TradeQuantityUSD", "name": "AvgTradeSize"},
        {"function": "dev", "var": "TradeQuantityUSD", "name": "DevTotalSize"},
        {"function": "max", "var": "TradeQuantityUSD", "name": "MaxTradeSize"},
        {"function": "min", "var": "TradeQuantityUSD", "name": "MinTradeSize"},
        {"function": "count", "var": "TradeQuantityUSD", "name": "NumberOfTrades"},
        {"function": "first", "var": "TradeTime", "name": "FirstTime"},
        {"function": "last", "var": "TradeTime", "name": "LastTime"}
    ],
    "filter": [
        {"function": "eq", "var": "Symbol", "par": "EURUSD"},
        {"function": "eq", "var": "ParentChild", "par": "Child"}
    ],
}

# this is api end-point which returns execution stats
endpoint = "v1/fx/algo/execution-stats"

## call the API
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response["result"])
# data_frame = data_frame.set_index("AlgoVendor")
data_frame