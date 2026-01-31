# Outrights Execution Stats

## Introduction
The `v1/fx/rfq-outrights/execution-stats` endpoint can be used to query across the entire execution history. 
The query returns a table with the metrics (fields) selected by you as columns. The rows are defined by `groupby` statements. 

You can review the outrights RFQs on a trade by trade level or an aggregated one by using the `groupby` query. You can review the `SecondBestPrice`,`BestBid`,`BestAsk` in the panel of `LP` s   and compare it to the `Price` that particular `LP` is quoting. This endpoint also displays the `NumLPs` that where in the stack at the time the outright RFQ was requested.

The endpoint is designed to study general execution quality of the outrights RFQ trades. 

## API Specification

The API endpoint requires a JSON object representing query logic similar to SQL and containing the following fields:

- `groupby` - which fields the results will be aggregated by
- `select`  - which fields should be returned in the end result. For example `BestBid`
- `filter`  - how the underlying data should be filtered

## Example 
**Note**: For display purposes we have limited the number of rows to 5 and and columns to 10.

### Only `LP` in `groupby`

**Note:** Aggregation is different depending on `select` and `groupby` fields. Only `TradeQuantityUSD` and `Price` have a default aggregation logic assigned to it.
However, you may define a function in the select option to aggregate the fields as they wish to.

In the example below we groupby `LP`, numerical fields such as `Price` return `None` as we aggregate across `Symbol` and `Side`. The aggregation of these results do not return a meaningful result.

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
    "select": [
        "TradeQuantityUSD", # sum
        "Symbol",           # cannot aggregate - returns None
        "Side",             # cannot aggregate - returns None
        "Price",            # cannot aggregate - returns None
        "NumLPs",           # default aggregation not defined - returns None, need to use user defined function to aggregate
        "SecondBestPrice",  # default aggregation not defined - returns None, need to use user defined function to aggregate
        "BestBid",          # default aggregation not defined - returns None, need to use user defined function to aggregate
        "BestAsk",          # default aggregation not defined - returns None, need to use user defined function to aggregate
        {"function": "sum", "var": "TradeQuantityUSD", "name": "TotalVolume"}       # explicit aggregation function
    ],
    "filter": [
        {"function": "within", "var": "Date", "pars": ["2014-01-01", "2021-11-30"]},
        {"function": "within", "var": "TradeTime", "transform": "time", "pars": ["12:00:00", "14:00:00"]}
    ],
}

# this is api end-point which returns RFQ outrights execution stats
endpoint =  "v1/fx/rfq-outrights/execution-stats"

## call the API
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response["result"])
# data_frame = data_frame.set_index("LP")
data_frame
```
```
#### Results

![api_rfq_swaps_execution_stats_ex1.png](assets/images/api_rfq/outrights/execution_stats/api_rfq_outrights_execution_stats_ex1.png)

### `LP`, `Symbol` and `Side` in `groupby`

**Note:** In this case as we are applying a `groupby` by `Symbol` and `Side`.`Price` is specified in `select`. It is returned as weighted average across `groupby` categories with `TradeQuantityUSD` being the weights. In this case the results are not `None` as we are not aggregating across different `Symbol` and `Side` values.

`NumLPs` is still returned as `None` because you must define the aggregation logic.

The following aggregation logic being applied:

- `TradeQuantityUSD` -> sum (Highlighted by the case that TradeQuantityUSD and TotalVolume are equal)
-  `Price` -> weighted average
- `NumLPs`, `BestBid`, `BestAsk`, `SecondBestPrice` ->  `None`, you need to define  aggregation logic

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
        "Side"
    ],
  "select": [
        "TradeQuantityUSD", # sum
        "Price",            # wavg of TradeQuantityUSD
        "NumLPs",           # default aggregation not defined - returns None, need to use user defined function to aggregate
        "SecondBestPrice",  # default aggregation not defined - returns None, need to use user defined function to aggregate
        "BestBid",          # default aggregation not defined - returns None, need to use user defined function to aggregate
        "BestAsk",          # default aggregation not defined - returns None, need to use user defined function to aggregate
        {"function": "sum", "var": "TradeQuantityUSD", "name": "TotalVolume"},               # explicit aggregation function
        {"function": "wavg", "var": ["TradeQuantityUSD", "Price"], "name": "wavgPrice"}      # explicit aggregation function
    ],
    "filter": [
        {"function": "within", "var": "Date", "pars": ["2014-01-01", "2021-11-30"]},
        {"function": "within", "var": "TradeTime", "transform": "time", "pars": ["12:00:00", "14:00:00"]},
    ],
}

# this is api end-point which returns RFQ outrights execution stats
endpoint =  "v1/fx/rfq-outrights/execution-stats"

## call the API
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response["result"])
# data_frame = data_frame.set_index("LP")
data_frame
```
```
#### Results

![api_rfq_swaps_execution_stats_ex2.png](assets/images/api_rfq/outrights/execution_stats/api_rfq_outrights_execution_stats_ex2.png)

### `TradeID` present in `groupby`

Applying a `groupby` with the field including a unique identifier results in no aggregation taking place, as the `groupby` field is unique to every row.

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
        "TradeID"
    ],
    "select": [
        "TradeQuantityUSD",
        "Symbol",
        "Side",
        "Price",
        "NumLPs",
        "SecondBestPrice",
        "BestBid",
        "BestAsk",
        {"function": "sum", "var": "TradeQuantityUSD", "name": "TotalVolume"}
    ],
    "filter": [
        {"function": "within", "var": "Date", "pars": ["2014-01-01", "2021-11-30"]},
        {"function": "within", "var": "TradeTime", "transform": "time", "pars": ["12:00:00", "14:00:00"]},
    ],
}

# this is api end-point which returns RFQ outrights execution stats
endpoint =  "v1/fx/rfq-outrights/execution-stats"

## call the API
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response["result"])
# data_frame = data_frame.set_index("TradeID")
data_frame
```
```
#### Results

![api_rfq_outrights_execution_stats_ex3.png](assets/images/api_rfq/outrights/execution_stats/api_rfq_outrights_execution_stats_ex3.png)

#### Figure

```python
```
# import plotly libary
import plotly.express as px

# Plot figure
fig= px.scatter(data_frame.head(1), x="TradeID", y=["Price", "SecondBestPrice"],
                title="TradeID:Trade_00001 Price Comparison")
fig.show()
```
```
### User defined field names

You can apply aggregation functions (such as `sum`, `avg`, `dev`,`max`,`min`,`count`,`first` and `last`, aggregation functions documented towards the end of this document) to the same variable (`TradeQuantityUSD`). 

In this example we conduct a `LP` analysis where we group the results by `LP` and `Symbol`. This is to review the differences in the traded volume and the price differentials between `LP` s.
Below we have applied transformation functions to both the `Price` and `TradeQuantityUSD` fields.

```python
```
## tradefeedr library
from tradefeedr_public_content.v1.generic.tradefeedr_api import TradefeedrApi

## need pandas to translate JSON results from API
import pandas as pd

## create API object
tf_api_object = TradefeedrApi(demo=True)

## options
options =  {
    "groupby":[
        "LP",
        "Symbol",
        "Side"
    ],
    "select":[
        {"function": "sum", "var": "TradeQuantityUSD", "name": "TotalVolume"},      # explicit aggregation function
        {"function": "avg", "var": "TradeQuantityUSD", "name": "AvgTicketSize"},
        {"function": "max", "var": "TradeQuantityUSD", "name": "MaxTicketSize"},
        {"function": "min", "var": "TradeQuantityUSD", "name": "MinTicketSize"},
        {"function": "max", "var": "Price", "name": "MaxPrice"},
        {"function": "min", "var": "Price", "name": "MinPrice"},
        "Price",
        {"function": "dev", "var": "Price", "name": "StdPrice"},
        {"function": "avg", "var": "NumLPs", "name": "AvgNumLPs"},
    ],
    "filter": [
        {"function": "within", "var": "Date", "pars": ["2014-01-01", "2021-11-30"]},
        {"function": "within", "var": "TradeTime", "transform": "time", "pars": ["12:00:00", "14:00:00"]},
        {"function": "in", "var": "Symbol", "pars": ["EURUSD", "USDJPY"]},
    ],
}

# this is api end-point which returns RFQ outrights execution stats
endpoint =  "v1/fx/rfq-outrights/execution-stats"

## call the API
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response["result"])
# data_frame = data_frame.set_index("LP")
data_frame
```
```
#### Results

![api_rfq_swaps_execution_stats_ex4.png](assets/images/api_rfq/outrights/execution_stats/api_rfq_outrights_execution_stats_ex4.png)

### Available filter functions

The JSON Query accepts an array of filters which must be defined simultaneously. Negative operators such as `not_in` and `not_eq` allow to exclude specific sets of observations (for example outliers) from consideration. 

Filters are frequently used in cases where we are dealing with big datasets: An example of this would be to select a sub-set of data and apply a set of aggregations to it.
Example below filters the data for a sub-selection of currency pairs, dates, trade times, trade size over $ 10m where the `Side` is Sell `S`.

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
        "Symbol",
        "LP",
        "Side"
    ],
    "select": [
        "TradeQuantityUSD",   # spread paid by client, implicit aggregation is TradeQuantityUSD-weighted average
    ],
    "filter": [
        {"function": "not_in", "var": "Symbol", "pars": ["EURUSD", "USDJPY", "GBPUSD"]},
        {"function": "gt", "var": "TradeQuantityUSD", "par": 1e7},   # greater than
        {"function": "not_eq", "var": "Side", "par": "B"},
        {"function": "within", "var": "Date", "pars": ["2014-01-01", "2021-11-30"]},
        {"function": "within", "var": "TradeTime", "transform": "time", "pars": ["08:00:00", "17:00:00"]}
    ],
}

# this is api end-point which returns RFQ outrights execution stats
endpoint =  "v1/fx/rfq-outrights/execution-stats"

## call the API
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response["result"])
# data_frame = data_frame.set_index("Symbol")
data_frame
```
```
#### Results

![api_rfq_swaps_execution_stats_ex5.png](assets/images/api_rfq/outrights/execution_stats/api_rfq_outrights_execution_stats_ex5.png)

### Histogram and Aggregation for different buckets

Each `groupby` variable  is rounded down to the nearest multiple of `par`. 

For example 11, 12, 19 all become 10 when par has a value of 10. These buckets are then used for aggregation across several buckets. The simplest example would be a histogram when the counts are presented. 

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
        "Side",
        {"function": "bar", "var": "TradeQuantityUSD", "par": 1e7}
    ],
    "select": [
        "Price"
    ],
    "filter": [
        {"function": "within", "var": "Date", "pars": ["2014-01-01", "2021-11-30"]},
        {"function": "lt", "var": "TradeQuantityUSD", "par": 1e8},     # ignore order with zero traded quantity
        {"function": "eq", "var": "LP", "par": "LP_1"},
        {"function": "eq", "var": "Symbol", "par": "EURUSD"}
    ],
}

# this is api end-point which returns RFQ outrights execution stats
endpoint =  "v1/fx/rfq-outrights/execution-stats"

## call the API
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response["result"])
# data_frame = data_frame.set_index("LP")
data_frame
```
```
#### Results

![api_rfq_swaps_execution_stats_ex6.png](assets/images/api_rfq/outrights/execution_stats/api_rfq_outrights_execution_stats_ex6.png)

#### Figure

```python
```
# import plotly libary
import plotly.express as px

# Plot figure
fig = px.scatter(data_frame, x="TradeQuantityUSD", y="Price",
                 title="Bubble plot of Price and TradeQuantityUSD",
                 size="TradeQuantityUSD")
fig.show()
```
```
### Histogram (Buckets)

Group modification function `hist` (stands for histogram buckets) splits the incoming variable range (`TradeQuantityUSD` in the below example) into a number of buckets of the same size.  Variables in the `select` operator are aggregated within those buckets. 

**Note**: The resulting column created by applying `hist` in the groupby, returns the middle value of the bucket.

#### Histogram (Buckets) example 1

`hist` function returns the middle value of the bucket.

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
        "Side",
        {"function": "hist", "var": "TradeQuantityUSD", "par": 10}
    ],
    "select": [
        {"function": "min", "var": "Price", "name": "MinPrice"},
        {"function": "max", "var": "Price", "name": "MaxPrice"},
        "Price",
        {"function": "count", "var": "Symbol", "name": "Count"},
        {"function": "sum", "var": "TradeQuantityUSD", "name": "TotalVolume"},
        {"function": "avg", "var": "NumLPs", "name": "AvgNumLPs"}
    ],
    "filter": [
        {"function": "within", "var": "Date", "pars": ["2014-01-01", "2021-11-30"]},
        {"function": "gt", "var": "TradeQuantityUSD", "par": 0},     # ignore order with zero traded quantity
        {"function": "eq", "var": "Symbol", "par": "EURUSD"}
    ],
}

# this is api end-point which returns RFQ outrights execution stats
endpoint =  "v1/fx/rfq-outrights/execution-stats"

## call the API
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response["result"])
# data_frame = data_frame.set_index("LP")
data_frame
```
```
#### Results

![api_rfq_swaps_execution_stats_ex7.png](assets/images/api_rfq/outrights/execution_stats/api_rfq_outrights_execution_stats_ex7.png)

#### Figure

```python
```
# import plotly libary
import plotly.express as px

# Plot figure
fig = px.bar(data_frame, x="TradeQuantityUSD", y="Count", title="TradeQuantityUSD frequency plot")
fig.show()
```
```
#### Histogram (Buckets) example 2

`hist_range` function returns the range of the bucket.

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
        "Side",
        {"function": "hist_range", "var": "TradeQuantityUSD", "par": 10}
    ],
    "select": [
        "Price"
    ],
    "filter": [
        {"function": "within", "var": "Date", "pars": ["2014-01-01", "2021-11-30"]},
        {"function": "lt", "var": "TradeQuantityUSD", "par": 1e8},     # ignore order with zero traded quantity
        {"function": "eq", "var": "Symbol", "par": "EURUSD"}
    ],
}

# this is api end-point which returns RFQ outrights execution stats
endpoint =  "v1/fx/rfq-outrights/execution-stats"

## call the API
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response["result"])
# data_frame = data_frame.set_index("LP")
data_frame
```
```
#### Results

![api_rfq_swaps_execution_stats_ex9.png](assets/images/api_rfq/outrights/execution_stats/api_rfq_outrights_execution_stats_ex9.png)

#### Histogram (Buckets) example 3

`hist_index` function returns the index of the bucket.

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
        "Side",
        {"function": "hist_index", "var": "TradeQuantityUSD", "par": 10}
    ],
    "select": [
        "Price"
    ],
    "filter": [
        {"function": "within", "var": "Date", "pars": ["2014-01-01", "2021-11-30"]},
        {"function": "lt", "var": "TradeQuantityUSD", "par": 1e8},     # ignore order with zero traded quantity
        {"function": "eq", "var": "Symbol", "par": "EURUSD"}
    ],
}

# this is api end-point which returns RFQ outrights execution stats
endpoint =  "v1/fx/rfq-outrights/execution-stats"

## call the API
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response["result"])
# data_frame = data_frame.set_index("LP")
data_frame
```
```
#### Results

![api_rfq_swaps_execution_stats_ex10.png](assets/images/api_rfq/outrights/execution_stats/api_rfq_outrights_execution_stats_ex10.png)

### Percentile 

`percentile` returns the x percentile of the specified column.

In this example we return the value corresponding to the 25th, 50th, 75th, 90th and 100th percentile of `Price`.
You can query various percentiles in the `select` parameter and analyse distribution of the chosen metric.

**Warning**: This function is computationally intensive running on a large data set will results in a slower response time.

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
        "Side"
    ],
    "select": [
        "TradeQuantityUSD", # sum
        "Price",      # TradeQuantityUSD-weighted average
        {"name": "Price_Pct25", "function": "percentile", "var": "Price", "par": 25},
        {"name": "Price_Pct50", "function": "percentile", "var": "Price", "par": 50},
        {"name": "Price_Pct75", "function": "percentile", "var": "Price", "par": 75},
        {"name": "Price_Pct90", "function": "percentile", "var": "Price", "par": 90},
        {"name": "Price_Pct100", "function": "percentile", "var": "Price", "par": 100}
    ],
    "filter": [
        {"function": "within", "var": "Date", "pars": ["2014-01-01", "2021-11-30"]},
        {"function": "within", "var": "TradeTime", "transform": "time", "pars": ["12:00:00", "14:00:00"]}
    ]
}

# this is api end-point which returns RFQ outrights execution stats
endpoint =  "v1/fx/rfq-outrights/execution-stats"

## call the API
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response["result"])
# data_frame = data_frame.set_index("LP")
data_frame
```
```
#### Results

![api_rfq_swaps_execution_stats_ex11.png](assets/images/api_rfq/outrights/execution_stats/api_rfq_outrights_execution_stats_ex11.png)

#### Figure

```python
```
# import plotly libary
import plotly.express as px

# Modify dataframe
data_frame = data_frame.set_index("LP")
data_frame1 = data_frame[(data_frame.Symbol=="EURUSD") & (data_frame.Side=="B")]
data_frame2 = data_frame[(data_frame.Symbol=="EURUSD") & (data_frame.Side=="S")]

# Plot figure 1
fig = px.scatter(data_frame1, y=["Price","Price_Pct90"],
          title="Buying EURUSD Price by LP" )
fig.show()

# Plot figure 2
fig = px.scatter(data_frame2, y=["Price","Price_Pct90"],
          title="Selling EURUSD Price by LP" )
fig.show()
```
```
### Rank Percentile 

The `rank_percentile` function transforms the target column into a value in the range of [0;100].

This is applied in the `filter` option. You can use this function to apply an outlier filtering. `Price` results are filtered to only select values which fall within the 10th-90th percentile range.

**Warning**: This function is computationally intensive running on a large data set will results in a slower response time.

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
        "Side"
    ],
    "select": [
        "TradeQuantityUSD", # sum
        "Price",      # TradeQuantityUSD-weighted average
    ],
    "filter": [
        {"function": "within", "var": "Date", "pars": ["2014-01-01", "2021-11-30"]},
        {"function": "within", "var": "TradeTime", "transform": "time", "pars": ["12:00:00", "14:00:00"]},
        {"function": "within", "var": "Price", "transform": "rank_percentile", "pars": [10, 90]}
    ]
}

# this is api end-point which returns RFQ outrights execution stats
endpoint =  "v1/fx/rfq-outrights/execution-stats"

## call the API
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response["result"])
# data_frame = data_frame.set_index("LP")
data_frame
```
```
#### Results

![api_rfq_swaps_execution_stats_ex12.png](assets/images/api_rfq/outrights/execution_stats/api_rfq_outrights_execution_stats_ex12.png)

### `Price` deltas (minus transformation)

Applying the `minus` transformation to compute the difference between `Price` and `BestBid`.
This example filters the data to only include results where the difference between `Price` and `BestBid` is between 0 and 5bps.

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
        "TradeID",
        "Symbol",
    ],
    "select": [
        "TradeTime",
        "Account",
        {"function": "avg", "var": "NumLPs", "name": "AvgNumLPs"},
        "TradeQuantity",
        "Price",
        "BestBid",
    ],
    "filter": [
        {"function": "within", "var": "Date", "pars": ["2014-05-01", "2021-05-30"]},
        {"function": "within", "var": "TradeTime", "transform": "time", "pars": ["12:00:00", "14:00:00"]},
        {"function": "within", "var": ["Price", "BestBid"], "transform": "minus", "pars": [0, 0.0005]},
        {"function": "eq", "var": "Symbol", "par": "EURUSD"},
        {"function": "eq", "var": "ProductType", "par": "SPOT"},
        {"function": "eq", "var": "Side", "par": "B"}         # only consider buys
    ]
}

# this is api end-point which returns RFQ outrights execution stats
endpoint =  "v1/fx/rfq-outrights/execution-stats"

## call the API
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response["result"])
# data_frame = data_frame.set_index("LP")

## translate TradeTime to human readable time
data_frame["TradeTime"] = pd.to_datetime(data_frame["TradeTime"], unit="ms" if str(data_frame["TradeTime"].dtype) == "int64" else None)

data_frame
```
```
#### Results

![api_rfq_swaps_execution_stats_ex13.png](assets/images/api_rfq/outrights/execution_stats/api_rfq_outrights_execution_stats_ex13.png)

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