## tradefeedr library
from tradefeedr_public_content.v1.generic.tradefeedr_api import TradefeedrApi

## need pandas to translate JSON results from API
import pandas as pd

## create API object
tf_api_object = TradefeedrApi(demo=True)

## options
options = {
    "groupby": [
        {"function": "hist", "var": "DecayPM1m", "par": 10}
    ],
    "select": [
        {"function": "min", "var": "DecayPM1m", "name": "MinDecayPM1m"},
        {"function": "max", "var": "DecayPM1m", "name": "MaxDecayPM1m"},
        {"function": "count", "var": "Symbol", "name": "Count"},
        {"function": "min", "var": "TradeQuantityUSD", "name": "TotalVolume"}
    ],
    "filter": [
        {"function": "within", "var": "Date", "pars": ["2014-01-01", "2021-11-30"]},
        {"function": "eq", "var": "ParentChild", "par": "Child"},    # only consider child orders which represent the actual trading
        {"function": "eq", "var": "OrderStatus", "par": "F"},        # only consider fills
        {"function": "gt", "var": "TradeQuantityUSD", "par": 0},     # ignore order with zero traded quantity
        {"function": "eq", "var": "Symbol", "par": "EURUSD"}
    ],
}

# this is api end-point which returns execution stats
endpoint = "v1/fx/rfs/execution-stats"

## call the API
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response["result"])
# data_frame = data_frame.set_index("DecayPM1m")
data_frame