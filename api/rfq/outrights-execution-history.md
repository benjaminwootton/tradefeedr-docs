# Outrights Execution History

## Introduction
The `v1/fx/rfq-outrights/execution-history` endpoint is used to query all trading events for outrights RFQ . It should be used when you require a detailed analysis and understanding of the execution. 
The endpoint allows selection of multiple metrics (fields) such as `BestBid`, `BestAsk`, `NumLPs` etc. 

## API Specification

The API endpoint requires a JSON object representing query logic similar to SQL and containing the following fields:

- `select`  - which fields should be returned in the end result. For example `BestBid`
- `filter`  - how the underlying data should be filtered

## Example 
**Note**: For display purposes we have limited the number of rows to 5 and and columns to 10.

### Select Metrics (Fields) for a Date Range

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
```
```
#### Results

![api_rfq_outrights_execution_history_ex1.png](assets/images/api_rfq/outrights/execution_history/api_rfq_outrights_execution_history_ex1.png)

#### Figure

```python
```
# import plotly libary
import plotly.express as px

# Modify dataframe
data_frame=data_frame.groupby("Date").sum()

# Plot figure
fig = px.line(data_frame, y="TradeQuantity", title="Daily Traded Volume")
fig.show()
```
```
## Field Definitions

[%header,format=csv, cols=["60%", "40%"]]

```csv
Name,Description
Date,Date corresponding to TradeTime
TradeTime,TradeTime - Time (GMT) when the trade was filled
TradeID,"Unique identifier for a trading event. Event can fill, order submission, reject or other event related to trading workflow"
Symbol,Currency pair. For example EURUSD.
Side,"Trade side. ""B” for buy and ""S” for sell."
LP,Executing LP - counterparty to the trade.
Account,Name of the underlying client this ParentOrderID executed on behalf of
SubAccount,SubAccount associated with this ParentOrderID
OrderID,Unique identifier for the order
Trader,The name of a trader associated with this TradeID
TradeCcy,"Denomination Currency for TradeQuantity and OrderQuantity. For example
    EUR."
ProductType,Type of product traded. For example SPOT
NumLPs,Total number of LPs in the stack
Price,Execution price of the trade
TradeQuantity,Traded quantity expressed in TradeCurrency
SecondBestPrice,The second best price in the stack
BestBid,The best Bid price in the stack
BestAsk,The best Ask price in the stack
ValueDate,Settlement date of the trade
```