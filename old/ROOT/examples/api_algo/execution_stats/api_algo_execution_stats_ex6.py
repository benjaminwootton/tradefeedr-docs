## tradefeedr library
from tradefeedr_public_content.v1.generic.tradefeedr_api import TradefeedrApi

## need pandas to translate JSON results from API
import pandas as pd

## create API object
tf_api_object = TradefeedrApi(demo=True)

## options
options = {
    "groupby": [
        "AlgoVendor",  # this is the institution responsible for the overall execution of algo
        "LP",          # this is the actual LP for the child order -  can be same as AlgoVendor
        "ExecVenue",   # venue where trading takes place -  can be "CboeFX", "EuronextFX"
        "OrderType",   # this should be "Market" or "Limit" or "Aggressive" or "Passive"
        "LiqPool",     # this can be specific liquidity pool like "no last look"
        "AlgoUrgency"
    ],
    "select": [
        "TradeQuantityUSD",
        "SpreadPnLPM", # spread paid in $/m, see definition in the end of the doc
        "DecayPM1s",
        "DecayPM5s"
    ],
    "child_filter": [
        {"function": "eq", "var": "ParentChild", "par": "Child"}
    ],
    "parent_filter":[
        {"function": "within", "var": "Date", "pars": ["2014-01-01", "2021-11-30"]},
        {"function": "eq", "var": "Symbol", "par": "EURUSD" },
        {"function": "eq", "var": "LP", "par": "LP1"},
        {"function": "gt", "var": "TradeQuantityUSD", "par": 50000000}   # greater than
    ]
}

# this is api end-point which returns execution stats
endpoint = "v1/fx/algo/execution-stats"

## call the API
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response["result"])
# data_frame = data_frame.set_index("AlgoVendor")
data_frame