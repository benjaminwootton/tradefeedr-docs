## tradefeedr library
from tradefeedr_public_content.v1.generic.tradefeedr_api import TradefeedrApi

## need pandas to translate JSON results from API
import pandas as pd

## create API object
tf_api_object = TradefeedrApi(demo=True)

## options
options = {
    "select":[
        "Date",
        "Account",
        "TradeTime",
        "Symbol",
        "TradeCcy",
        "Side",
        "TradeQuantity",
        "ProductType"
    ],
    "filter":[
        {"function":"within","var":"Date","pars":["2021-04-02", "2021-06-30"]}
    ]
}

# this is api end-point which returns RFQ outrights execution history
endpoint =  "v1/fx/rfq-outrights/execution-history"

## call the API
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response["result"])

## translate TradeTime to human readable time
data_frame["TradeTime"] = pd.to_datetime(data_frame["TradeTime"], unit="ms" if str(data_frame["TradeTime"].dtype) == "int64" else None)

# data_frame = data_frame.set_index("Date")
data_frame