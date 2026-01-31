# PnL History

## Introduction

The `v1/fx/algo/pnl-history` endpoint should be used to understand the dynamics of the tick-by-tick algo PnL.
The PnL is split into AlgoVendor (Bank) PnL and algo user. The algo user can quantify the results of their actions such as setting algo limit price.  

Returns a table describing tick by tick decomposition of `SlippageToArrivalMid` into Slippage due to Bank (Algo Provider) and Slippage due to algo User (for a specific `ParentOrderID` supplied by a user).  

     
## API Specification
The API endpoint requires a JSON object representing query logic similar to SQL and containing the following fields:

- `filter`  - how the underlying data should be filtered

**Note:** `ParentOrderID` is the only valid filter field for this endpoint

## Example 
**Note**: For display purposes we have limited the number of rows to 5 and and columns to 10.

### PnL History for a ParentOrderID

This query returns an algo which does not contain a `LimitPrice`. Meaning that the algo is always active during the execution period.
Thus, there will not be any PnL attributed to the user.

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

# this is api end-point which returns parent order stats one algo run per row
endpoint = "v1/fx/algo/pnl-history"

## call the API
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response["result"])

## translate Time to human readable time
df["Time"] = pd.to_datetime(df["Time"], unit="ms" if str(df["Time"].dtype) == "int64" else None)
#data_frame = data_frame.set_index("Time")
data_frame
```
```
#### Results

![api_algo_pnl_history_ex1.png](assets/images/api_algo/pnl_history/api_algo_pnl_history_ex1.png)

#### Figures

Below figures illustrate the tick-by-tick algo PnL dynamics of an always active algo.
An algo which is constantly executing and assigns no user PnL.

```python
```
# import plotly libary
import plotly.express as px
import plotly.graph_objs as go

# Plot figure 1
fig = px.line(data_frame,
              y=["SlippageToArrivalMidPMUser","SlippageToArrivalMidPMBank"],
              x="Time",
              title="PnL Dynamics of an Active Algo")
fig.show()

# Plot figure 2
fig = px.line(data_frame, y=["Mid"], x="Time", title="Market data and LimitPrice Chart")
fig.add_trace(go.Scatter(x=data_frame["Time"], y=data_frame["LimitPrice"], mode="lines"))
fig.show()
```
```
### PnL History when LimitPrice is present

In this example we show how the PnL dynamics change when a `LimitPrice` is instructed by a user.
Now there is a user PnL in this case as the algo is following user instructions which determines if the algo is active or not.

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
          {"function": "eq", "var": "ParentOrderID", "par": "lim_20180904-A00"}
      ]
}

# this is api end-point which returns parent order stats one algo run per row
endpoint = "v1/fx/algo/pnl-history"

## call the API
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response["result"])

## translate Time to human readable time
df["Time"] = pd.to_datetime(df["Time"], unit="ms" if str(df["Time"].dtype) == "int64" else None)
#data_frame = data_frame.set_index("Time")
data_frame
```
```
#### Results

![api_algo_pnl_history_ex2.png](assets/images/api_algo/pnl_history/api_algo_pnl_history_ex2.png)

#### Figures

Below figures illustrate the tick-by-tick algo PnL dynamics of an always active algo.
An algo which is constantly executing and assigns no user PnL.

```python
```
# import plotly libary
import plotly.express as px
import plotly.graph_objs as go

# Plot figure 1
fig = px.line(data_frame,
              y=["SlippageToArrivalMidPMUser","SlippageToArrivalMidPMBank"],
              x="Time",
              title="PnL Dynamics of an Algo with a LimitPrice")
fig.show()

# Plot figure 2
fig = px.line(data_frame, y=["Mid"], x="Time", title="Market data and LimitPrice Chart ")
fig.add_trace(go.Scatter(x=data_frame["Time"], y=data_frame["LimitPrice"], mode="lines"))
fig.show()
```
```
## Field Definitions

```csv
Name,Description
Mid,Tradefeedr mid price
Time,time
LimitPrice,Algo LimitPrice set by the user and effective at time equal to “time”
IsActive,Whether the algo is active of not. The algo is active if the LimitPrice is not set or if the current market price is above (below) the LimitPrice for sell (buy) orders
SlippageToArrivalMidPM,Dynamics Total P&L of the algo in $/M using Arrival Price as the benchmark. Equals to the sum of SlippageToArrivalMidPMUser and SlippageToArrivalMidPMBank
SlippageToArrivalMidPMUser,"Algo P&L attributed to user the algo. P&L (positive or negative) can be attributed to algo user if they intervene in the normal course of algo execution by setting limit prices, stopping and restarting algo execution or doing other actions affecting algo performance. "
SlippageToArrivalMidPMBank,Algo P&L attributed to AlgoVendor
TradeQuantityRemainUSD,"Total Quantiy which is remained to be executed at the ""time"". Expressed in USD "
```