## tradefeedr library
from tradefeedr_public_content.v1.generic.tradefeedr_api import TradefeedrApi  

## need pandas to translate JSON results from API
import pandas as pd 

## create API object 
tf_api_object = TradefeedrApi(demo=False)

## options
options = {
    "select":[
        "Date",
        "Account",
        "TradeTime",
        "Symbol",
        "TradeCcy",
        "Side",
        "NearTradeQuantity",
        "ProductType"
    ],
    "filter":[
        {"function":"within","var":"Date","pars":['2021-04-02', '2021-06-30']}
    ]
}

# this is api end-point which returns RFQ swaps execution history
endpoint  =  "v1/fx/rfq-swaps/execution-history"

## call the API 
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response['result'])

## translate TradeTime to human readable time
data_frame["TradeTime"] = pd.to_datetime(data_frame["TradeTime"], unit="ms")
data_frame