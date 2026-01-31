# Market Data

## Introduction
The `v1/fx/algo/market-data` endpoint returns all relevant market data around an algo run - specified by `ParentOrderID`. 

- If for a single cross, only market data for one cross will be returned
- If multiple crosses - will also be returned and identified by `Symbol` column

## API Specification
The API endpoint requires a JSON object representing query logic similar to SQL and containing the following fields:

- `filter`  - how the underlying data should be filtered

**Note:** `ParentOrderID` is the only valid filter field for this endpoint

## Example 
**Note**: For display purposes we have limited the number of rows to 5 and and columns to 10.

### Market Data for a `ParentOrderID`

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
      "filter": [
          {"function": "eq", "var": "ParentOrderID", "par": "20180921-A07"}
       ]
}

# this is api end-point which returns market data
endpoint = "v1/fx/algo/market-data"

## call the API
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response["result"])

## translate Time to human readable time
df.Time = pd.to_datetime(df.Time, unit="ms" if str(df["Time"].dtype) == "int64" else None)
# data_frame = data_frame.set_index("Time")
display(HTML("<hr><h5>Market Data Table </h5>")
data_frame
```
```
#### Results

![api_algo_market_data_ex1.png](assets/images/api_algo/market_data/api_algo_market_data_ex1.png)

#### Figure

```python
```
## Obtain Execution Data for 20180921-A07
from tradefeedr_public_content.v1.generic.tradefeedr_api import TradefeedrApi

## need pandas to translate JSON results from API
import pandas as pd

# import plotly libary
import plotly.express as px
import plotly.graph_objs as go

## create API object
tf_api_object = TradefeedrApi(demo=True)

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
        {"function": "eq", "var": "ParentOrderID", "par": "20180921-A07"}
    ]
}

# this is api end-point which returns parent order stats one algo run per row
endpoint = "v1/fx/algo/event-history"

## call the API
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame_ex = pd.DataFrame(response["result"])
data_frame_ex = data_frame_ex.set_index("ParentChild")

## translate TradeTime and ArrivalTime to human readable time
data_frame_ex["TradeTime"] = pd.to_datetime(data_frame_ex["TradeTime"], unit="ms")
data_frame_ex["ArrivalTime"] = pd.to_datetime(data_frame_ex["ArrivalTime"], unit="ms")
data_frame_ex  = data_frame_ex.sort_values(by="ArrivalTime", ascending = False)

# Query from previous example
## options
options = {
      "filter": [
          {"function": "eq", "var": "ParentOrderID", "par": "20180921-A07"}
       ]
}

# this is api end-point which returns market data
endpoint = "v1/fx/algo/market-data"

## call the API
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response["result"])

## translate Time to human readable time
data_frame.Time = pd.to_datetime(data_frame.Time, unit="ms")

# Plot figure for market data
fig = px.line(data_frame, x="Time", y="Mid",
              title="Market Data and Execution Data For POID: 20180921-A07")

fig["data"][0]["name"] = "Mid"
fig["data"][0]["showlegend"] = True

# Update figure with execution prices
fig.add_trace(go.Scatter(y=data_frame_ex["Price"], x=data_frame_ex["ArrivalTime"], mode="markers", name="Execution Price"))

fig.show()
```
```
## Field Definitions

```csv
Name,Description
Mid,Tradefeedr Mid Price
Time,Time for Tradefeedr Mid Price
Symbol,Currency pair of ParentOrderID. For example: EURUSD
```