# Bilateral Markouts

## Introduction
The `v1_fx_rfs_bilateral-markouts` endpoint is used to study the markouts. It returns the aggregated markout curves information in a number of tables.
The data is anonymized by masking the `LP` names. 

These tables include: 

- `Markout` - Markout Curves starting at SpreadPNL at time zero. Those curve represent the PnL of counterparty.
- `MarkoutsAtZero`  - Markout Curves starting at 0 at time 0. Those curves represent price impact curves and do not include Spread Paid.
- `MarkoutsAtZeroAverage` - Average (as opposed to weighted average) version of MarkoutsAtZero.
- `Volatilities` - Standard deviation of each markout point for confidence intervals.

Mark-out Curves represent market dynamics before and after each trading event (fill, reject or order placement).

Refer to [RFS Bilateral Sharing](../analytics/bilateral-sharing.md) page for details on how bilateral sharing works.

## API Specification

The API endpoint requires a JSON object representing query logic similiar to SQL and containing the following fields:

- `groupby` - what fields to aggregate markouts by
- `select`  - which fields should be returned in the end result.
- `filter`  - how the underlying data should be filtered

**Note:** This API endpoint is similar to the [v1/fx/rfs/markouts](api-rfs/api-rfs-markouts.md) endpoint. The difference is that this API endpoint sources aggregated data and masks the `LP` names.

## Example 
For more examples and markout definitions refer to [v1/fx/rfs/markouts](api-rfs/api-rfs-markouts.md)

**Note**: For display purposes we have limited the number of rows to 5 and and columns to 10.

### By LP, Symbol and OrderStatus

In this example we query for the PnL curves `Markouts` and select the points in time of the markout curve.
Then filter for Fills only.

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
        "OrderStatus"
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
        {"function": "eq", "var": "OrderStatus", "par": "F"},
        {"function": "gt", "var": "TradeQuantityUSD", "par": 1000000},
        {"function": "eq", "var": "MarkoutType", "par": "Markouts"},
        {"function": "eq", "var": "Symbol", "par": "EURUSD"}
   ]
}

# this is api end-point which returns bilateral markouts
endpoint =  "v1/fx/rfs/bilateral-markouts"

## call the API
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response["result"])
# data_frame = data_frame.set_index("LP")
data_frame
```
```
#### Results

![api_rfs_bilateral_markouts_ex1.png](assets/images/api_rfs_bilateral/markouts/api_rfs_bilateral_markouts_ex1.png)

#### Figure

```python
```
# import plotly libary
import plotly.express as px

# Modify dataframe
data_frame = data_frame.set_index("LP")

# Plot figure
fig = px.line(data_frame.iloc[:,3:].T, title="Markout Curves")
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