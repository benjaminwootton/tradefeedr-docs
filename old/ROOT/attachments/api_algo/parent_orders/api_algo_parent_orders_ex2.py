## tradefeedr library
from tradefeedr_public_content.v1.generic.tradefeedr_api import TradefeedrApi  

## need pandas to translate JSON results from API
import pandas as pd 

## create API object 
tf_api_object = TradefeedrApi(demo=False)

## options
performance_metric = ["ArrivalMidPerfBPS", "ArrivalMidPerfNetBPS", "TWAPMidPerfBPS", "TWAPMidPerfBPS"][0]
options = {
    "select": [
        "Date",
        "ParentOrderID",
        "ArrivalTime",
        "NumChildEvents",
        "NumParentEvents",
        "Side",
        "Symbol",
        "Duration",
        "TradeQuantityUSD",
        "AlgoName",
        "LP",
        "ArrivalPrice", 
        "AllInPrice",
        "ArrivalMidPerfBPS",
        "ArrivalMidPerfNetBPS",
        "TWAPMidPerfBPS",
        "TWAPMidPerfNetBPS"
        ],
    "filter": [
        {"function": "within", "var": "Date", "pars": ["2014-01-01", "2025-12-31"]},
        {"function": "eq", "var": "Symbol", "par": "EURUSD"}, 
        {"function": "lt", "var": performance_metric, "par": 100}       
    ],
}

# this is api end-point which returns parent order stats one algo run per row  
endpoint = "v1/fx/algo/parent-orders"

## call the API 
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response['result'])

## translate ArrivalTime to human readable time
data_frame['ArrivalTime'] = pd.to_datetime(data_frame['ArrivalTime'], unit='ms')
data_frame = data_frame.sort_values(by=ArrivalTime", ascending=False)
data_frame