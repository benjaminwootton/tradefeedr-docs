## tradefeed library
from tradefeedr_public_content.v1.generic.tradefeedr_api import TradefeedrApi

## need pandas to translate JSON results from API
import pandas as pd

## create API object
tf_api_object = TradefeedrApi(demo=True)

## options
options = {
    "select": [
        "Date",
        "ParentOrderID",
        "LP",
        "Side",
        "Symbol",
        "Duration",
        "TradeQuantityUSD",
        "AlgoName",
        "ArrivalMidPerfBPS",
        ],
    "filter": [
        {"function": "within", "var": "Date", "pars": ["2014-01-01", "2025-12-31"]},
        {"function": "eq", "var": "Symbol", "par": "EURUSD"},
        {"function": "within", "var": "ArrivalMidPerfBPS", "par": [-20,0]}
    ],
}

# this is api end-point which returns parent order stats one algo run per row
endpoint = "v1/fx/algo/parent-orders"

## call the API
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response["result"])
#data_frame = data_frame.set_index("Date")

## translate ArrivalTime to human readable time
data_frame.head()