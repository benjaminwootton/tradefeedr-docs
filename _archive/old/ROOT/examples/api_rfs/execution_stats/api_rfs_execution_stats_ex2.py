## tradefeedr library
from tradefeedr_public_content.v1.generic.tradefeedr_api import TradefeedrApi

## need pandas to translate JSON results from API
import pandas as pd

## create API object
tf_api_object = TradefeedrApi(demo=True)

## options
options = {
    "groupby": [
        "Symbol",
        "Side"
    ],
    "select": [
        "TradeQuantityUSD",
        "SpreadPnLPM",
        "DecayPM1s",
        "ExecVenue",
        "LP",
        "Mid0",
        "Price",
        {"function": "sum", "var": "TradeQuantityUSD", "name": "TotalVolume"},
        {"function": "avg", "var": "Price", "name": "AvgPrice"}
    ],
    "filter": [
        {"function": "within", "var": "Date", "pars": ["2014-01-01", "2021-11-30"]},
        {"function": "within", "var": "TradeTime", "transform": "time", "pars": ["12:00:00", "14:00:00"]},
        {"function": "in", "var": "Symbol", "pars": ["EURUSD", "USDJPY"]}
    ],
}

# this is api end-point which returns execution stats
endpoint = "v1/fx/rfs/execution-stats"

## call the API
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response["result"])
# data_frame = data_frame.set_index("Symbol")
data_frame