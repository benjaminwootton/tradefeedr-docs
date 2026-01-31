## tradefeedr library
from tradefeedr_public_content.v1.generic.tradefeedr_api import TradefeedrApi  

## need pandas to translate JSON results from API
import pandas as pd 

## create API object 
tf_api_object = TradefeedrApi(demo=False)

## options
options = {
    "select": [
        "ParentChild",
        "ParentOrderID",
        "TradeID",
        "Symbol",
        "Side",
        "TradeCcy",
        "TradeQuantityUSD",
        "OrderQuantity", 
        "Price",
        "OrderType",
        "ExecVenue",
        "Mid0",
        "Mid1s",
        "DecayPM1s",
        "SpreadPnLPM",
        "ArrivalTime",
        "TradeTime"
    ],
    "filter": [
        {"function": "eq", "var": "ParentOrderID", "par": "20180903-A00"}
    ]
}

# this is api end-point which returns parent order stats one algo run per row  
endpoint = "v1/fx/algo/event-history"

## call the API 
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response['result'])

## translate TradeTime and ArrivalTime to human readable time
data_frame["TradeTime"] = pd.to_datetime(data_frame["TradeTime"], unit="ms")
data_frame["ArrivalTime"] = pd.to_datetime(data_frame["ArrivalTime"], unit="ms")
data_frame = data_frame.sort_values(by=ArrivalTime", ascending=False)
data_frame