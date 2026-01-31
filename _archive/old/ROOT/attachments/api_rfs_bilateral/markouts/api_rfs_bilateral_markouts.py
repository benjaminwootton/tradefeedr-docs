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
        "OrderStatus"
    ],
    "select": [
        "TradeQuantityUSD", 
        "-5s",
        "-1s", 
        "0", 
        "5s", 
        "10s", 
        "30s",
        "1m", 
        "3m", 
        "5m" 
    ],
    "filter": [
        {"function": "eq", "var": "OrderStatus", "par": "F"},
        {"function": "gt", "var": "TradeQuantityUSD", "par": 1000000},
        {"function": "eq", "var": "MarkoutType", "par": "Markouts"},
        {"function": "eq", "var": "Symbol", "par": "EURUSD"}
   ]
}

# this is api end-point which returns bilateral markouts
endpoint  =  "v1/fx/rfs/bilateral-markouts"

## call the API 
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response['result'])
data_frame