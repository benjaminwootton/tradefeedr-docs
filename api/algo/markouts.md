# Markouts

## Introduction
The `v1/fx/algo/markouts` endpoint returns the markout curves information in a number of tables.

These tables include: 

- `Markout` - Markout Curves starting at SpreadPNL at time zero. Those curve represent the PnL of counterparty
- `MarkoutsAtZero`  - Markout Curves starting at 0 at time 0. Those curves represent price impact curves and do not include Spread Paid
- `MarkoutsAtZeroAverage` - Average (as opposed to weighted average) version of MarkoutsAtZero
- `Volatilities` - Standard deviation of each markout point for confidence intervals

Mark-out Curves represent market dynamics before and after each trading event (fill, reject or order placement). This market dynamics is typically aggregated across different categories such as `Symbol` `LP`, `ExecVenue` and `ParentOrderID` but it is possible to extract markout curves for each trading event as well.

## API Specification
The API endpoint requires a JSON object representing query logic similiar to SQL and containing the following fields:

- `groupby` - what fields to aggregate markouts by
- `filter`  - how the underlying data should be filtered
- `child_filter` - how the child orders should be filtered
- `parent_filter` - how the parent orders should be filtered

## Markout Definitions

Mark-out Curves represent PnL (in dollar/m traded) earned by the counterparty of your trades. Market Impact Curves represent your PnL from inception (using mid and ignoring the spread). Tradefeedr supports both.    

Mark-out curves are calculated for each trade and aggregated across by `LP`, `Account`, `Symbol` traded etc. The aggregation weights for are proportional to Trade sizes.  Direction is adjusted for Side (buy or sell).

Mark-out curve at time 0 represents Spread paid on a trade (in dollar/m) - so called Inception PnL for market maker.
Mark-out curve at 30s represents PnL left for the market maker 30s after the trade is done. The PnL is marked-to-market using Tradefeedr mid.              

For example, if spread paid is 25 dollar/m and mid-price move is 10 dollar/m against LP then the mark-out curve will show 15 dollar/m. 

Effectively, mark-out curve at time X can be thought as an approximation of market maker PnL if the trade is covered at time X at mid.
Typically (but not always) mark-out curves are downward sloping meaning that less spread PnL is left LP as time goes by. 

Downward sloping mark-out curve means that your trades have positive momentum, spot goes UP after BUY trade and DOWN after SELL. 

We also present dynamics before the trade time.  It has the same interpretation.
 Downward sloping curve from -10s to 0 means spot was going UP before BUY trade happened (DOWN before sell trade happened). 

## Examples 
**Note**: For display purposes we have limited the number of rows to 5 and and columns to 10.

### Markouts by ParentOrderID

In this example we have queried the API for a single ParentOrderID.
Using this data we have created a markouts plot with volatility bands.
Where the `MarkoutType` equal to `Volatilities` is being used to construct the confidence intervals.

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
    "groupby": ["ParentOrderID"],
    "filter": [
        {"function": "like", "var": "ParentChild", "par": "Child"},
        {"function": "like", "var": "ParentOrderID", "par": "20180921-A00"},
    ],
}

# this is api end-point which returns markouts
endpoint = "v1/fx/algo/markouts"

## call the API
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response["result"])
# data_frame = data_frame.set_index("ParentOrderID")
data_frame
```
```
#### Results

![api_algo_markouts_ex1.png](assets/images/api_algo/markouts/api_algo_markouts_ex1.png)

#### Figure

```python
```
# import plotly libary
import plotly.express as px
import plotly.graph_objs as go

# Modify dataframe
data_frame = data_frame.set_index("MarkoutType").iloc[:,3:].T
data_frame = data_frame[["Markouts", "Volatilities"]]

# Plot figure
fig = px.line(data_frame, y="Markouts", title ="Markouts with Volatility Bands For POID:20180921-A00")

fig["data"][0]["name"] = "Markouts"
fig["data"][0]["showlegend"] = True

fig.add_trace(go.Scatter(y=data_frame["Markouts"]-data_frame["Volatilities"], x=data_frame.index, mode="lines",
                         fill="tonexty", name="Confidence Interval 2"))
fig.add_trace(go.Scatter(y=data_frame["Markouts"]+data_frame["Volatilities"], x=data_frame.index, mode="lines",
                         fill="tonexty", name="Confidence Interval 1"))
fig.show()
```
```
### Using the child and parent filters

We obtain the same results as above using a filter on the child orders and a filter on the parent orders.

- The `parent_filter` is applied to the parent orders, in this case we filter the parent orders such that the ParentOrderID equal to 20180921-A00.
- The `child_filter` is applied to return only markouts on the child orders.

For markouts to have a meaningful result we must look at the child orders only. As child rows reflect the actions of AlgoVendor, the institution responsible for algo execution. This includes child fills, order placements and rejects.

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
    "groupby": [
        "ParentOrderID"
    ],
    "child_filter": [
        {"function": "like", "var": "ParentChild", "par": "Child"}
    ],
    "parent_filter":[
        {"function": "like", "var": "ParentOrderID", "par": "20180921-A00"},
    ]
}

# this is api end-point which returns markouts
endpoint = "v1/fx/algo/markouts"

## call the API
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response["result"])
# data_frame = data_frame.set_index("ParentOrderID")
data_frame
```
```
#### Results

![api_algo_markouts_ex2.png](assets/images/api_algo/markouts/api_algo_markouts_ex2.png)

#### Figure

```python
```
# import plotly libary
import plotly.express as px

# Modify dataframe
data_frame = data_frame.set_index("MarkoutType").iloc[:,3:].T
data_frame = data_frame[["Markouts"]]

# Plot figure
fig = px.line(data_frame, y="Markouts",
              title="Markouts Using Child and Parent Filters For POID:20180921-A00")

fig["data"][0]["name"] = "Markouts"
fig["data"][0]["showlegend"] = True

fig.show()
```
```
### Venue Analysis

In this example we use the `child_filter` to filter for child orders, that have traded more than $10M and to specify the type of markouts we want to view.

The `parent_filter` is used to filter for large trades greater than $100M, for only EURUSD trades and which `LP` we want to review the markout of.

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
    "groupby": [
        "ParentOrderID",
        "Symbol",
        "LP",
        "ExecVenue"
    ],
    "child_filter": [
        {"function": "like", "var": "ParentChild", "par": "Child"},
        {"function": "like", "var": "MarkoutType", "par": "**AtZero**"}
    ],
    "parent_filter":[
        {"function": "gt", "var": "TradeQuantityUSD", "par": 100000000},
        {"function": "eq", "var": "LP", "par": "LP3"},
        {"function": "eq", "var": "Symbol", "par": "EURUSD"}
    ]
}

# this is api end-point which returns markouts
endpoint = "v1/fx/algo/markouts"

## call the API
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response["result"])
# data_frame = data_frame.set_index("ParentOrderID")
data_frame
```
```
#### Results

![api_algo_markouts_ex3.png](assets/images/api_algo/markouts/api_algo_markouts_ex3.png)

#### Figures

```python
```
# import plotly libary
import plotly.express as px

# Modify dataframe
data_frame = data_frame[data_frame.ParentOrderID=="20180903-A03"]

df1 = data_frame[data_frame.MarkoutType=="MarkoutsAtZero"]
df1 = df1.set_index("ExecVenue").iloc[:,6:]

df2 = data_frame[data_frame.MarkoutType=="MarkoutsAtZeroAverage"]
df2 = df2.set_index("ExecVenue").iloc[:,6:]

# Plot figure 1
fig = px.line(df1.T, title ="MarkoutsAtZero by ExecVenue For POID:20180903-A03")
fig.show()

# Plot figure 2
fig = px.line(df2.T, title ="MarkoutsAtZero by ExecVenue For POID:20180903-A03")
fig.show()
```
```
## Field Definitions

Refer to [Analytics Algo](../analytics/algo.md) page for details and formula.

```csv
Name,Description
Markouts,Markout Curves starting at SpreadPNL at time zero. Those curve represent the PnL of counterparty
MarkoutsAtZero,Markout Curves starting at 0 at time 0. Those curves represent price impact curves and do not include Spread Paid.
MarkoutsAtZeroAverage,Average (as opposed to weighted average) version of MarkoutsAtZero.
Volatilities,Standard deviation of each markout point for confidence intervals
```