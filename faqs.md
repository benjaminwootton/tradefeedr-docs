# FAQs

This page contains frequently asked questions.

## 1. How to obtain stack information for a single trade? 

```python
```
## tradefeedr library
from tradefeedr_public_content.v1.generic.tradefeedr_api import TradefeedrApi

## need pandas to translate JSON results from API
import pandas as pd

## create API object
tf_api_object = TradefeedrApi(demo=True)

## options
options = {
    'select':[
        "Date",
        "TradeTime",
        "TradeID",
        "Symbol",
        "Side",
        "LP",
        "Account",
      #  "SubAccount",
      #  "OrderID",
      #  "Trader",
      #  "TradeCcy",
      #  "ProductType",
      #  "NumLPs",
      #  "NearPrice",
      #  "FarPrice",
      #  "NearTradeQuantity",
      #  "FarTradeQuantity",
      #  "NearForwardPoints",
      #  "FarForwardPoints",
        "NearStack",
        "FarStack",
      #  "ProductType"

    ],
    'filter': [
        {"function":"within","var":"Date","pars":["2021-04-02", "2021-06-30"]},
        {'function': "eq", "variable": "TradeID", "par": "Trade_00059"}
    ],
}
# this is api end-point which returns RFQ swaps execution history
endpoint =  "v1/fx/rfq-swaps/execution-history"

## call the API
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response["result"])

## translate TradeTime to human readable time
data_frame["TradeTime"] = pd.to_datetime(data_frame["TradeTime"], unit="ms" if str(data_frame["TradeTime"].dtype) == "int64" else None)
# data_frame = data_frame.set_index("Date")
data_frame
```
```
### Results

![faqs_ex1.png](assets/images/faqs/faqs_ex1.png)