## tradefeedr library
from tradefeedr_public_content.v1.generic.tradefeedr_api import TradefeedrApi  

## need pandas to translate JSON results from API
import pandas as pd 

## create API object 
tf_api_object = TradefeedrApi(demo=False)

## options
options = {
    "groupby": [ 
        "LP",
        "Symbol",
        "Side",
        {"function": "hist_label", "var": "NumLPs", "par": 10},
        {"function": "hist_label", "var": "TradeQuantityUSD", "par": 10}
    ],
    "select": [
        {"function": "min", "var": "Price", "name": "MinPrice"},
        {"function": "max", "var": "Price", "name": "MaxPrice"}, 
        "Price",
        {"function": "count", "var": "Symbol", "name": "Count"}, 
        {"function": "sum", "var": "TradeQuantityUSD", "name": "TotalVolume"}
    ],
    "filter": [
        {"function": "within", "var": "Date", "pars": ["2014-01-01", "2021-11-30"]},
        {"function": "gt", "var": "TradeQuantityUSD", "par": 0},     # ignore order with zero traded quantity 
        {"function": "eq", "var": "Side", "par": "B"}         # only consider buys
    ],
}

# this is api end-point which returns RFQ outrights execution stats
endpoint  =  "v1/fx/rfq-outrights/execution-stats"

## call the API 
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response['result'])
data_frame