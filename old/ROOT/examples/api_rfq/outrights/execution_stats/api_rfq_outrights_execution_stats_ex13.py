## tradefeedr library
from tradefeedr_public_content.v1.generic.tradefeedr_api import TradefeedrApi

## need pandas to translate JSON results from API
import pandas as pd

## create API object
tf_api_object = TradefeedrApi(demo=True)

## options
options = {
    "groupby": [
        "LP",
        "TradeID",
        "Symbol",
    ],
    "select": [
        "TradeTime",
        "Account",
        {"function": "avg", "var": "NumLPs", "name": "AvgNumLPs"},
        "TradeQuantity",
        "Price",
        "BestBid",
    ],
    "filter": [
        {"function": "within", "var": "Date", "pars": ["2014-05-01", "2021-05-30"]},
        {"function": "within", "var": "TradeTime", "transform": "time", "pars": ["12:00:00", "14:00:00"]},
        {"function": "within", "var": ["Price", "BestBid"], "transform": "minus", "pars": [0, 0.0005]},
        {"function": "eq", "var": "Symbol", "par": "EURUSD"},
        {"function": "eq", "var": "ProductType", "par": "SPOT"},
        {"function": "eq", "var": "Side", "par": "B"}         # only consider buys
    ]
}

# this is api end-point which returns RFQ outrights execution stats
endpoint =  "v1/fx/rfq-outrights/execution-stats"

## call the API
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response["result"])
# data_frame = data_frame.set_index("LP")

## translate TradeTime to human readable time
data_frame["TradeTime"] = pd.to_datetime(data_frame["TradeTime"], unit="ms" if str(data_frame["TradeTime"].dtype) == "int64" else None)

data_frame