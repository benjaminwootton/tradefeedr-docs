# Markouts

## Introduction
This `v1/fx/rfs/markouts` endpoint returns the markout curves information in a number of tables.

These tables include: 

- `Markout` - Markout Curves starting at SpreadPNL at time zero. Those curve represent the PnL of counterparty
- `MarkoutsAtZero`  - Markout Curves starting at 0 at time 0. Those curves represent price impact curves and do not include Spread Paid.
- `MarkoutsAtZeroAverage` - Average (as opposed to weighted average) version of MarkoutsAtZero.
- `Volatilities` - Standard deviations of each markout point for confidence intervals

Mark-out Curves represent market dynamics before and after each trading event (fill, reject or order placement). 
This market dynamics is typically aggregated across different categories such as `Symbol` `LP`, 
and `ExecVenue` but it is possible to extract markout curves for each trading event as well.

## API Specification

The API endpoint requires a JSON object representing query logic similiar to SQL and containing the following fields:

- `groupby` - what fields to aggregate markouts by
- `select`  - which fields should be returned in the end result
- `filter`  - how the underlying data should be filtered

## Markout Definitions 

### `Markout`

Mark-out Curves represent PnL (in dollar/m traded) earned by the counterparty of your trades. Market Impact Curves represent your PnL from inception (using mid and ignoring the spread). Tradefeedr supports both.    

Mark-out curves are calculated for each trade and aggregated across by `LP`, `Account`, `Symbol` traded etc. The aggregation weights for are proportional to Trade sizes.  Direction is adjusted for Side (buy or sell)

Mark-out curve at time 0 represents Spread paid on a trade (in dollar/m) - so called Inception PnL for market maker.
Mark-out curve at 30s represents PnL left for the market maker 30s after the trade is done. The PnL is marked-to-market using Tradefeedr mid.              

For example, if spread paid is 25 dollar/m and mid-price move is 10 dollar/m against LP then the mark-out curve will show 15 dollar/m. 

Effectively, mark-out curve at time X can be thought as an approximation of market maker PnL if the trade is covered at time X at mid.
Typically (but not always) mark-out curves are downward sloping meaning that less spread PnL is left LP as time goes by. 

Downward sloping mark-out curve means that your trades have positive momentum, spot goes UP after BUY trade and DOWN after SELL. 

We also present dynamics before the trade time.  It has the same interpretation. Downward sloping curve from -10s to 0 means spot was going UP before BUY trade happened (DOWN before sell trade happened). 

### `MarkoutAtZero` 

These markout represnt your PnL marked to market at the mid Upward sloping markout curves mean your trades have positive momentum.

### `MarkoutAtZeroAverage` 

These markout represent your PnL marked to market at the mid. Unlike `MarkoutAtZero` the individual trade markouts are aggregated as average as opposed to weighted average. Upward sloping markout curves mean your trades have positive momentum.

###  `Volatility` 

These are the standard deviations of the `Markout` curves at the point in time.

## Examples 

**Note**: For display purposes we have limited the number of rows to 5 and and columns to 10.

### By LP

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
        "LP"
    ],
    "filter": [
        {"function": "like", "var": "ParentChild", "par": "Child"}
    ]
}

# this is api end-point which returns markouts
endpoint =  "v1/fx/rfs/markouts"

## call the API
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response["result"])
# data_frame = data_frame.set_index("LP")
data_frame
```
```
#### Results

![api_rfs_markouts_ex1.png](assets/images/api_rfs/markouts/api_rfs_markouts_ex1.png)

#### Figure

```python
```
# import plotly libary
import plotly.express as px

# Modify dataframe
data_frame = data_frame[data_frame.MarkoutType=="Markouts"]
data_frame = data_frame.set_index("LP")

# Plot figure
fig = px.line(data_frame.iloc[:,3:].T, title="Markouts by LP")
fig.update_xaxes(title="Time")
fig.update_yaxes(title="Markouts")
fig.show()
```
```
###  By LP (Volatility Curves)

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
        "LP"
    ],
    "filter": [
        {"function": "like", "var": "ParentChild", "par": "Child"},
        {"function": "eq", "var": "MarkoutType", "par": "Volatilities"}
    ]
}

# this is api end-point which returns markouts
endpoint =  "v1/fx/rfs/markouts"

## call the API
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response["result"])
# data_frame = data_frame.set_index("LP")
data_frame
```
```
#### Results

![api_rfs_markouts_ex2.png](assets/images/api_rfs/markouts/api_rfs_markouts_ex2.png)

#### Figure

```python
```
# import plotly libary
import plotly.express as px

# Modify dataframe
data_frame = data_frame.set_index("LP")

# Plot figure
fig = px.line(data_frame.iloc[:,3:].T, title="Volatilities by LP")
fig.update_xaxes(title="Time")
fig.update_yaxes(title="Volatilities")
fig.show()
```
```
### By LP, Symbol and execution venue

In this example we query for the impact curves `MarkoutsAtZero` and `MarkoutsAtZeroAverage`. 

Then we conduct an LP and venue analysis for EURUSD for trades greater than $1M in size.

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
        "LP",
        "Symbol",
        "ExecVenue"
    ],
    "filter": [
        {"function": "like", "var": "ParentChild", "par": "Child"},
        {"function": "gt", "var": "TradeQuantityUSD", "par": 1000000},
        {"function": "like", "var": "MarkoutType", "par": "**AtZero**"},
        {"function": "eq", "var": "Symbol", "par": "EURUSD"}
    ]
}

# this is api end-point which returns markouts
endpoint =  "v1/fx/rfs/markouts"

## call the API
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response["result"])
# data_frame = data_frame.set_index("LP")
data_frame
```
```
#### Results

![api_rfs_markouts_ex3.png](assets/images/api_rfs/markouts/api_rfs_markouts_ex3.png)

### Figures

```python
```
# import plotly libary
import plotly.express as px

# Modify dataframe
data_frame = data_frame.set_index("LP")

# Plot figure 1
fig = px.line(data_frame[data_frame.MarkoutType=="MarkoutsAtZero"].iloc[:,5:].T, title="MarkoutsAtZero by LP")
fig.update_xaxes(title="Time")
fig.update_yaxes(title="MarkoutsAtZero")
fig.show()

# Plot figure 2
fig = px.line(data_frame[data_frame.MarkoutType=="MarkoutsAtZeroAverage"].iloc[:,5:].T, title="MarkoutsAtZeroAverage by LP")
fig.update_xaxes(title="Time")
fig.update_yaxes(title="MarkoutsAtZeroAverage")
fig.show()
```
```
### By LP, Symbol and execution venue with select filter

In this example we query for the PnL curves `Markouts` and select the points in time of the markout curve.

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
        "LP",
        "Symbol",
        "ExecVenue"
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
        {"function": "like", "var": "ParentChild", "par": "Child"},
        {"function": "gt", "var": "TradeQuantityUSD", "par": 1000000},
        {"function": "eq", "var": "MarkoutType", "par": "Markouts"},
        {"function": "eq", "var": "Symbol", "par": "EURUSD"}
   ]
}

# this is api end-point which returns markouts
endpoint =  "v1/fx/rfs/markouts"

## call the API
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response["result"])
# data_frame = data_frame.set_index("LP")
data_frame
```
```
#### Results

![api_rfs_markouts_ex4.png](assets/images/api_rfs/markouts/api_rfs_markouts_ex4.png)

#### Figure

```python
```
# import plotly libary
import plotly.express as px

# Modify dataframe
data_frame = data_frame.head()
data_frame = data_frame.set_index("LP")

# Plot figure
fig = px.line(data_frame.iloc[:,3:].T, title="Markout Curve")
fig.update_xaxes(title="Time")
fig.update_yaxes(title="Markouts")
fig.show()
```
```
## Field Definitions

Refer to [Analytics RFS](../analytics/rfs.md) page for details and formula.

```csv
Name,Description
Markouts,Markout Curves starting at SpreadPNL at time zero. Those curve represent the PnL of counterparty
MarkoutsAtZero,Markout Curves starting at 0 at time 0. Those curves represent price impact curves and do not include Spread Paid.
MarkoutsAtZeroAverage,Average (as opposed to weighted average) version of MarkoutsAtZero.
Volatilities,Standard deviationof each markout point for confidence intervals
```