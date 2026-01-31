# Bilateral Market Share

## Introduction

The `v1_fx_rfs_bilateral-market-share` endpoint is designed to study the evolution of the `MarketShare` over a period of days. You can apply a `filter` to the underlying data on the fields outlined at the end of this notebook.
For example, you can see how their `MarketShare` varied over the last year for a specific `LP` and selected `Symbol`/s.
The data is anonymized by masking the `LP` names. 

Endpoint allows you to query `MarketShare` history by `Date`.

Refer to [Bilateral Sharing](../analytics/bilateral-sharing.md) page for details on how bilateral sharing works.

## API Specification

The API endpoint requires a JSON object representing query logic similar to SQL and containing the following fields:

- `select`  - which fields should be returned in the end result. For example `Date` or `MarketShare`.
- `filter`  - how the underlying data should be filtered

## Example 
**Note**: For display purposes we have limited the number of rows to 5 and and columns to 10.

### Default Results

When no options are passed the endpoint returns your `MarketShare` by `Date`.
The result set also contains columns `CreatedBy` (you) and `CreatedFor` ( client the view was created for).
For example if `CreatedFor` is LP1, LP1 results are unmaksed and all other names are masked.

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
}

# this is api end-point which returns bilateral market share
endpoint =  "v1/fx/rfs/bilateral-market-share"

## call the API
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response["result"])
# data_frame = data_frame.set_index("Date")
data_frame
```
```
#### Results

![api_rfs_bilateral_market_share_ex1.png](assets/images/api_rfs_bilateral/market_share/api_rfs_bilateral_market_share_ex1.png)

#### Figure

```python
```
# import plotly libary
import plotly.express as px

# Modify dataframe
data_frame = data_frame[data_frame.LP=="LP1masked"]

# Plot figure
fig = px.line(data_frame, x="Date", y="MarketShare", title="LP1masked MarketShare Plot")
fig.show()
```
```
### LP Market Share Analysis 1

This example shows you how to apply the `filter` parameter to obtain the masked results.
We apply a filter on the `CreatedFor` column to create a view for a single `LP`.

Results are only meaningful if one `CreatedFor` variable is selected, as shown below.

**Note**: In the demo data `CreatedFor` is an empty string. Change the parameter in the code cell below when using actual data.

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
        {"function": "eq", "var": "CreatedFor", "par": ""},
        {"function": "within", "var": "Date", "par": ["2017-02-01", "2017-02-10"]}
    ]
}

# this is api end-point which returns bilateral market share
endpoint =  "v1/fx/rfs/bilateral-market-share"

## call the API
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response["result"])
# data_frame = data_frame.set_index("Date")
data_frame
```
```
#### Results

![api_rfs_bilateral_market_share_ex2.png](assets/images/api_rfs_bilateral/market_share/api_rfs_bilateral_market_share_ex2.png)

#### Figure

```python
```
# import plotly libary
import plotly.express as px

# Plot figure
fig = px.line(data_frame, x="Date", y="MarketShare", title="LP Market Share Analysis 1", color="LP")
fig.show()
```
```
### LP Market Share Analysis 2

This example shows you how to apply the `filter` parameter to highlight the market share of selected names.

**Note ** : The use of `TRADEFEEDR` is for demo purposes only, this will differ when demo data is turned off. The user will need to change this to thier own `LP` name.

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
        {"function": "eq", "var": "CreatedFor", "par": ""},
        {"function": "in", "var": "LP", "pars": ["TRADEFEEDR","LP1masked"]},
        {"function": "within", "var": "Date", "par": ["2017-02-01", "2017-02-10"]}
    ]
}

# this is api end-point which returns bilateral market share
endpoint =  "v1/fx/rfs/bilateral-market-share"

## call the API
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response["result"])
# data_frame = data_frame.set_index("Date")
data_frame
```
```
#### Results

![api_rfs_bilateral_market_share_ex3.png](assets/images/api_rfs_bilateral/market_share/api_rfs_bilateral_market_share_ex3.png)

#### Figure

```python
```
# import plotly libary
import plotly.express as px

# Plot figure
fig = px.line(data_frame, x="Date", y="MarketShare", title="LP Market Share Analysis 2", color="LP")
fig.show()
```
```
## Field Definitions

```csv
Name,Description
Date,Date corresponding to TradeTime
CreatedBy,The user generating the report
CreatedFor,Who the report is intended for and all other names are masked
LP,Executing LP - counterparty to the trade.
MarketShare,Percentage TradeQuantityUSD traded by an LP
```