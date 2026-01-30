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
        "SpreadPnLPM",      # TradeQuantityUSD-weighted average
        "DecayPM1s",        # TradeQuantityUSD-weighted average
        {"name": "SpreadPnLPM_Pct25", "function": "percentile", "var": "SpreadPnLPM", "par": 25},
        {"name": "SpreadPnLPM_Pct50", "function": "percentile", "var": "SpreadPnLPM", "par": 50},
        {"name": "SpreadPnLPM_Pct75", "function": "percentile", "var": "SpreadPnLPM", "par": 75},
        {"name": "SpreadPnLPM_Pct90", "function": "percentile", "var": "SpreadPnLPM", "par": 90},
        {"name": "SpreadPnLPM_Pct100", "function": "percentile", "var": "SpreadPnLPM", "par": 100}
    ],
    "filter": [
        {"function": "within", "var": "Date", "pars": ["2014-01-01", "2021-11-30"]},
        {"function": "within", "var": "TradeTime", "transform": "time", "pars": ["12:00:00", "14:00:00"]}
    ]
}

# this is api end-point which returns execution stats
endpoint = "v1/fx/algo/execution-stats"

## call the API
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response["result"])
# data_frame = data_frame.set_index("LP")
data_frame