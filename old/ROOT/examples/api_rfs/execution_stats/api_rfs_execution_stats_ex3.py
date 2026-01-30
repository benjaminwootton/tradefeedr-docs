## tradefeedr library
from tradefeedr_public_content.v1.generic.tradefeedr_api import TradefeedrApi

## need pandas to translate JSON results from API
import pandas as pd

## create API object
tf_api_object = TradefeedrApi(demo=True)

## options
options = {
    "groupby": [
        "LP",          # this is the actual LP for the child order -  can be same as AlgoVendor
        "ExecVenue",   # venue where trading takes place -  can be "CboeFX", "EuronextFX"
        "Symbol",
        "OrderStatus"
    ],
    "select": [
        "TradeQuantityUSD",
        "SpreadPnLPM", # spread paid in $/m, see definition in the end of the doc
        "DecayPM1s",
        "DecayPM5s",
        "DecayPM30s",
        "DecayPM1m",
        "DecayPM5m"
    ],
    "filter": [
        {"function": "eq", "var": "ParentChild", "par": "Child"},
        {"function": "within", "var": "TradeTime", "transform": "time", "pars": ["12:00:00", "14:00:00"]},
        {"function": "within", "var": "Date", "pars": ["2017-01-01", "2017-12-31"]},
        {"function": "like", "var": "Symbol", "par": "USD*"}
    ]
}

# this is api end-point which returns execution stats
endpoint = "v1/fx/rfs/execution-stats"

## call the API
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response["result"])
# data_frame = data_frame.set_index("LP")
data_frame