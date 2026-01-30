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
        "ExecVenue"
    ],
    "filter": [
        {"function": "like", "var": "ParentChild", "par": "Child"},
        {"function": "gt", "var": "TradeQuantityUSD", "par": 1000000},
        {"function": "like", "var": "MarkoutType", "par": "*AtZero*"},
        {"function": "eq", "var": "Symbol", "par": "EURUSD"}
    ]
}

# this is api end-point which returns markouts
endpoint  =  "v1/fx/rfs/markouts"

## call the API 
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response['result'])
data_frame