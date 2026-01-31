# Swaps Execution Stats

## Introduction
The `v1/fx/rfq-swaps/execution-stats` can be used to query across the entire execution history. The query returns a table with the metrics (fields) selected by you as columns. The rows are defined by `groupby` statements. 
You can review the swaps RFQs on a trade by trade level or an aggregated one by using the `groupby` query. 
This endpoint also displays the `NumLPs` that where in the stack at the time the swaps RFQ was requested.

The endpoint is designed to study general execution quality of the swaps RFQ trades. 

## API Specification

The API endpoint requires a JSON object representing query logic similar to SQL and containing the following fields:

- `groupby` - which fields the results will be aggregated by
- `select`  - which fields should be returned in the end result. For example `NearPrice`
- `filter`  - how the underlying data should be filtered

## Example 
**Note**: For display purposes we have limited the number of rows to 5 and and columns to 10.

### `TradeID` present in `groupby`

Applying a `groupby` with the field including a unique identifier results in no aggregation taking place, as the `groupby` field is unique to every row.

**Note:** This endpoint does not have any default aggregation logic you must define the aggregation functions. 

Please refer to [v1/fx/rfq-outrights/execution-stats](api-rfq/api-rfq-outrights-execution-stats.md) to see more examples.

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
        "TradeID",
        "LP",
        "Symbol",
        "Side"
    ],
    "select": [
        "Account",
        "ProductType",
        "NumLPs",
        "NearPrice",
        "FarPrice",
        "NearTradeQuantity",
        "FarTradeQuantity",
        "NearValueDate",
        "FarValueDate"
    ],
    "filter": [
        {"function": "within", "var": "Date", "pars": ["2014-01-01", "2021-11-30"]},
        {"function": "within", "var": "TradeTime", "transform": "time", "pars": ["12:00:00", "14:00:00"]},
    ],
}

# this is api end-point which returns RFQ swaps execution stats
endpoint =  "v1/fx/rfq-swaps/execution-stats"

## call the API
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response["result"])
# data_frame = data_frame.set_index("TradeID")
data_frame
```
```
#### Results

![api_rfq_swaps_execution_stats_ex1.png](assets/images/api_rfq/swaps/execution_stats/api_rfq_swaps_execution_stats_ex1.png)

#### Figure

```python
```
# import plotly libary
import plotly.express as px

# Modify dataframe
data_frame = data_frame.groupby("LP").sum()
data_frame = data_frame.sort_values(by="NearTradeQuantity", ascending=False)

# Plot figure
fig = px.bar(data_frame, y="NearTradeQuantity", title="Swaps RFQ NearTradeQuantity by LP")
fig.show()
```
```
Refer to [v1/fx/rfq-outrights/execution-stats](api-rfq/api-rfq-outrights-execution-stats.md) for more examples on how to use the endpoint.

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
NearPrice,Price of the near leg
FarPrice,Price of the far leg
NearTradeQuantity,Neg leg traded quantity expressed in TradeCurrency
FarTradeQuantity,Far leg traded quantity expressed in TradeCurrency
NearValueDate,Settlement date of the near leg
FarValueDate,Settlement date of the far leg
```

### Aggreggation Functions (for `select` if `groupby` is present)

[%header,format=csv, cols=["60%", "40%"]]

```csv
Function,Description,Example
sum,sum,"{""function"":""sum"",""var"":""TradeQuantityUSD"",""name"":""TotalVolume""},"
avg,average,"{""function"":""avg"",""var"":""TradeQuantityUSD"",""name"":""AvgTradeSize""}"
wavg,weighted average,"{""function"": ""wavg"", ""var"": [""TradeQuantityUSD"", ""Price""], ""name"": ""wavgPrice""}"
dev,standard deviation,"{""function"":""dev"",""var"":""TradeQuantityUSD"",""name"":""DevTotalSize""},"
max,maximum,"{""function"":""max"",""var"":""TradeQuantityUSD"",""name"":""MaxTradeSize""},"
min,minimum,"{""function"":""min"",""var"":""TradeQuantityUSD"",""name"":""MinTradeSize""},"
count,count,"{""function"":""count"",""var"":""TradeQuantityUSD"",""name"":""NumberOfTrades""},"
first,first observation,"{""function"":""first"",""var"":""TradeTime"",""name"":""FirstTime""}"
last,last observation,"{""function"":""last"", ""var"":""TradeTime"",""name"":""LastTime""}"
percentile,returns the x percentile of the specified column	,"{""function"": ""percentile"", ""var"": ""SpreadPnLPM"", ""par"": 90}"
```

### Modification Functions (for `filter` and `groupby` )

[%header,format=csv, cols=["60%", "40%"]]

```csv
Function,Description,Example
eqx,"applied to sting variables,returns the value of parament if variable is equal to parameter and “Other” otherwise","{""function"":""eqx"",""par"":""LP1"",""var"":""LP""}"
bar,"rounds the variable down to the nearest multiple of the parameter, used to group to generate equal spaced buckets","{""function"":""bar"",""par"":""10"",""transform"":""minute"",""var"":""TradeTime""}"
minute,take the minute component from the variable,"{""function"":""bar"",""par"":""10"",""transform"":""minute"",""var"":""TradeTime""}"
in,"returns True if the variable is in the List and False otherwise, mainly for filters","{""function"":""in"",""var"":""Symbol"",""pars"":[""EURUSD"",""USDJPY""]},"
within,"within, variable within a provided range","{""function"":""within"",""var"":""date"",""pars"":[""2014-01-01"",""2021-11-30""]},"
gt,return True if the variable is greater than its parameter and False otherwise,"{""function"":""gt"",""var"":""TradeQuantityUSD"",""par"":1000000}, # greater than"
lt,return True if the variable is less than its paramer and False otherwise,"{""function"":""lt"",""var"":""SpreadPnLPM"",""par"":300}, # less than"
eq,returns True is the variable is equal to function parameter and false otherwise,"{""function"":""eq"",""var"":""Symbol"",""par"":""EURUSD""}"
hist,"split the variable into categories with N equally spaced buckets, typically used in group-by to produce histograms","{""function"":""hist"",""var"":""SpreadPnLPM"",""par"":""10""}"
hist_label,"split the variable into categories with N equally spaced buckets, function returns the bucket with the bucket number","{""function"":""hist_label"",""var"":""SpreadPnLPM"",""par"":""10""}"
hist_range,"split the variable into categories with N equally spaced buckets, function returns the range of the bucket","{""function"":""hist_range"",""var"":""SpreadPnLPM"",""par"":""10""}"
hist_index,"split the variable into categories with N equally spaced buckets, function returns the index of the bucket","{""function"":""hist_index"",""var"":""SpreadPnLPM"",""par"":""10""}"
like,matches string based on wild card pattern,"{""function"":""like"",""var"":""Symbol"",""pars"":""*USD""}"
not_eq,not equal. To exclude variables,"{""function"":""not_eq"",""var"":""Symbol"",""par"":""EURUSD""}"
not_in,"not in. returns False if the variable is in the List and True otherwise, mainly for filters","{""function"":""not_in"",""var"":""Symbol"",""pars"":[""EURUSD"",""USDJPY""]}"
rank_percentile,function transforms the target column into a value in the range of [0;100],"{""function"": ""within"", ""var"": ""DecayPM1s"", ""transform"": ""rank_percentile"", ""pars"": [10, 90]}"
diff_millis,"function takes two time columns x,y and performs an subtraction x-y results are in milliseconds","{""function"": ""within"", ""var"": [""TradeTime"", ""ArrivalTime""], ""transform"": ""diff_millis"", ""pars"": [0, 500]}"
diff_nanos,"function takes two time columns x,y and performs an subtraction x-y results are in nanoseconds","{""function"": ""within"", ""var"": [""TradeTime"", ""ArrivalTime""], ""transform"": ""diff_nanos"", ""pars"": [0, 500]}"
minus,"function takes two columns x,y and performs an subtraction x-y.","{""function"": ""within"", ""var"": [""OrderExecutionScore"", ""OrderReversalScore""], ""transform"": ""minus"", ""pars"": [0, 500]}"
plus,"function takes two columns x,y and performs an additon x+y.","{""function"": ""within"", ""var"": [""OrderExecutionScore"", ""OrderReversalScore""], ""transform"": ""plus"", ""pars"": [80, 150]}"
```