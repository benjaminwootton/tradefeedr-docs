## tradefeedr library
from tradefeedr_public_content.v1.generic.tradefeedr_api import TradefeedrApi  

## need pandas to translate JSON results from API
import pandas as pd 

## create API object 
tf_api_object = TradefeedrApi(demo=False)

## options
options = {
    "groupby": [
        "LP"
    ],
    "select": [
        "TradeQuantityUSD", # sum 
        "SpreadPnLPM",      # TradeQuantityUSD-weighted average 
        "DecayPM1s",        # TradeQuantityUSD-weighted average
    ],
    "filter": [
        {"function": "within", "var": "Date", "pars": ["2017-01-01", "2017-04-01"]},
        {"function": "within", "var": "TradeTime", "transform": "time", "pars": ["12:00:00", "14:00:00"]},
        {"function": "within", "var": "DecayPM1s", "transform": "rank_percentile", "pars": [10, 90]}
    ]
}

# this is api end-point which returns execution stats
endpoint  = "v1/fx/rfs/execution-stats"

## call the API 
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response['result'])
data_frame