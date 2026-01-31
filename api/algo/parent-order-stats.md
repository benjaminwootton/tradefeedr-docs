# Parent Order Stats

## Introduction

The purpose of the `v1/fx/algo/parent-order-stats` endpoint is to provide standard algo performance metrics aggregated across user defined categories like currency pair or LP. For example, you can rank the trading performance of their algo vendors using a performance metric (list of those provided below) within specific time frame or for certain currency pairs.   

It returns a table with algo trading performance statistics, e.g. `ArrivalMidPerfBPS`. 
Each row contains algo trading performance aggregated by the specified `groupby` fields. 

## API Specification
The API endpoint requires a Query String. A Query String is a JSON object representing query logic in SQL-like fashion that contains the following fields:

- `groupby` - what columns should the result set be aggregated by
- `select`  - what columns should be returned in the result set
- `filter`  - what filters should be applied to the result set before they are returned
- `risk_price_benchmark` - see below explanation
- `notation` - see below explanation

You can specify `risk_price_benchmark` as an additional field in the Query. The four possible values are described below:

- `TradefeedrModel` - (Default) This is Tradefeedr risk transfer benchmark constructed from the data collected from individual algo runs and fitted to volatility, time of the day and trade size.
- `BankReported` - This is the benchmark reported by the algo provider. This is only available for those providers who submit this data. `None` is reported for others.
- `OwnRiskPriceStatic` - This is provided by you (via uploading spread matrices) for your own internal use.
- `OwnRiskPriceVolAdjusted` - This adjusts `OwnRiskPriceStatic` for volatility.

You can provide `notation` as a field in the Query. It is either `performance` or `slippage`. Setting `notation` to `performance` expresses the algo statistics in terms of basis points and 
expresses algo metrics in terms of performance (the higher the number the better).   Setting `notation` to `slippage` switches to slippage terminology 
(the lower the number the better).

Endpoint returns feilds like `SlippageToArrivalMidPM` and 
negative numbers imply a good outcome. This notation is consistent with original Implementation Shortfall terminology.  

## Examples 
**Note**: For display purposes we have limited the number of rows to 5 and and columns to 10.

### Return all available benchmarks (`performance`)

Refer to [Algo API](algo/README.md) page for page for details on aggregation logic.

**Note:** That in this example we `groupby` `LP` and removed the select query to return all available benchmarks.
This example uses the `TradefeedrModel` and `notation` is set to `performance`, as a result the algo stats are expressed in terms of basis points.

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
          {"function": "within", "var": "Date", "pars": ["2018-01-01", "2018-12-31"]},
          {"function": "eq", "var": "Symbol", "par": "EURUSD"},
          {"function": "within", "var": "ArrivalTime", "transform": "time", "pars": ["09:00:00", "20:00:00"]}
    ],
    "risk_price_benchmark": "TradefeedrModel",
    "notation": "performance"
}

# this is api end-point which returns parent order stats
endpoint = "v1/fx/algo/parent-order-stats"

## call the API
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response["result"])
# data_frame = data_frame.set_index("LP")
data_frame
```
```
#### Results

![api_algo_parent_order_stats_ex1.png](assets/images/api_algo/parent_order_stats/api_algo_parent_order_stats_ex1.png)

#### Figure

```python
```
# import plotly libary
import plotly.express as px

# Modify dataframe
data_frame = data_frame[data_frame["LP"].isin(["LP1","LP2","LP3"])]

# Plot figure
fig = px.pie(data_frame, values="TradeQuantityUSD", names=data_frame.index,
             title="TradeQuantityUSD by LP")
fig.show()
```
```
### Return all available benchmarks (`slippage`)

Refer to [Algo API](algo/README.md) page for page for details on aggregation logic.

**Note:** This is the same as the above example however, we are using `slippage` in the `notation` option.
Benchmarks returned are in slippage terminology.

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
          {"function": "within", "var": "Date", "pars": ["2018-01-01", "2018-12-31"]},
          {"function": "eq", "var": "Symbol", "par": "EURUSD"},
          {"function": "within", "var": "ArrivalTime", "transform": "time", "pars": ["09:00:00", "20:00:00"]}
    ],
    "risk_price_benchmark": "TradefeedrModel",
    "notation": "slippage"
}

# this is api end-point which returns parent order stats
endpoint = "v1/fx/algo/parent-order-stats"

## call the API
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response["result"])
# data_frame = data_frame.set_index("LP")
data_frame
```
```
#### Results

![api_algo_parent_order_stats_ex2.png](assets/images/api_algo/parent_order_stats/api_algo_parent_order_stats_ex2.png)

### Comparing algo performance metrics across LPs

Refer to [Algo API](algo/README.md) page for page for details on aggregation logic.

**Note:** In this example `notation` is set to `performance` as we are analysing the results in basis point terms. Changing the `notation` to `slippage` will result in no output being displayed.

This is due to the `select` option selecting fields which are only present when notation is in the `performance` setting.

It is important for algo user to know which algo vendor delivered better performance over specific time range. For the comparison to be meaningful a filter must be applied. 
Ensuring that we do not compare performance across different currencies or liquidity conditions. 

The example below compares risk adjusted performance `RiskTransferPricePerfIR` across three algo vendors (LP1 to LP3) for EURUSD. 
Additionally, a time filter can be applied to select only high liquidity periods.    

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
        "NumRuns",
        "TradeQuantityUSD",
        "ArrivalMidPerfBPS",
        "TWAPMidPerfBPS",
        "RiskTransferPricePerfBPS",
        "RiskTransferPricePerfBPSStdDev",
        "RiskTransferPricePerfIR"
    ],
    "filter": [
        {"function": "within", "var": "Date", "pars": ["2018-01-01", "2018-12-31"]},
        {"function": "eq", "var": "Symbol", "par": "EURUSD"},
        {"function": "within", "var": "ArrivalTime", "transform": "time", "pars": ["09:00:00", "20:00:00"]}
    ],
    "risk_price_benchmark": "TradefeedrModel",
    "notation": "performance"
}

# this is api end-point which returns parent order stats
endpoint = "v1/fx/algo/parent-order-stats"

## call the API
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response["result"])
# data_frame = data_frame.set_index("LP")
data_frame
```
```
#### Results

![api_algo_parent_order_stats_ex3.png](assets/images/api_algo/parent_order_stats/api_algo_parent_order_stats_ex3.png)

#### Figure

```python
```
# import plotly libary
import plotly.express as px

# Plot figure
fig = px.bar(data_frame, y="ArrivalMidPerfBPS", x="LP", title="Comparing algo performance metrics across LPs")
fig.update_layout(xaxis={"categoryorder":"total ascending"})
fig.show()
```
```
### Comparing different risk transfer price benchmarks

**Note:** Following examples are using the `performance` setting on the `notation` option as we are comparing the `RiskTransferPricePerfBPS`.

Risk transfer price benchmark is a zero risk alternative of algo execution: immediately crossing the spread. Tradefeedr provides a number of alternatives for algo benchmarking 
Option  `TradefeedrModel` calculates algo performance with respect to Tradefeer risk transfer model. The performance is aggregated across `groupby` categories.  

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
        "RiskTransferPricePerfBPS"
    ],
    "filter":[
        {"function": "within", "var": "Date", "pars": ["2018-01-01", "2018-12-31"]}
    ],
    "risk_price_benchmark": "TradefeedrModel",
    "notation" : "performance"
}

# this is api end-point which returns parent order stats
endpoint = "v1/fx/algo/parent-order-stats"

## call the API
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response["result"])
# data_frame = data_frame.set_index("LP")
data_frame
```
```
#### Results

![api_algo_parent_order_stats_ex4.png](assets/images/api_algo/parent_order_stats/api_algo_parent_order_stats_ex4.png)]

#### Figure

```python
```
# import plotly libary
import plotly.express as px

# Plot figure
fig = px.bar(data_frame, x="LP", y ="RiskTransferPricePerfBPS", title="Comparing different risk transfer price benchmarks")
fig.update_layout(xaxis={"categoryorder":"total ascending"})
fig.show()
```
```
### Select large orders in low volatility environment 

Performance may vary in low and high volatility environments, so selecting the correct environment for you may help to better estimate expected algo performance.

Example below only includes algo runs when the market volatility is below 10 percent (annualised).

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
        "NumRuns",
        "TradeQuantityUSD",
        "ArrivalMidPerfBPS",
        "TWAPMidPerfBPS",
        "RiskTransferPricePerfBPS"
    ],
    "filter": [
        {"function": "within", "var": "Date", "pars": ["2018-01-01", "2018-12-31"]},
        {"function": "within", "var": "ArrivalTime", "transform": "time", "pars": ["09:00:00", "14:00:00"]}, # order started between 9:00 to 14:00
        {"function": "gt", "var": "TradeQuantityUSD", "par": 100000000},  # algo size above $100mil
        {"function": "eq", "var": "Symbol", "par": "EURUSD"},
        {"function": "lt", "var": "DailyVolatilityPct", "par": 10}   # volatility below 10% (annualized)
    ],
    "risk_price_benchmark": "TradefeedrModel",
    "notation": "performance"
}

# this is api end-point which returns parent order stats
endpoint = "v1/fx/algo/parent-order-stats"

## call the API
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response["result"])
# data_frame = data_frame.set_index("LP")
data_frame
```
```
#### Results

![api_algo_parent_order_stats_ex5.png](assets/images/api_algo/parent_order_stats/api_algo_parent_order_stats_ex5.png)]

#### Figure

```python
```
# import plotly libary
import plotly.express as px

# Modify dataframe
data_frame = data_frame[data_frame["LP"].isin(["LP1","LP2","LP3"])]

# Plot figure
fig = px.pie(data_frame, values="TradeQuantityUSD", names=data_frame.index,
             title="TradeQuantityUSD by LP")
fig.show()
```
```
### Select orders wih a low performance metric

Conditional on bad execution outcome which algo vendor is likely to do worse? 

Example below compares algo performance across LPs, only selecting algo run where algo performance metrics (such as `ArrivalMidPerfBPS`) is below certain threshold. 

```python
```
## tradefeedr library
from tradefeedr_public_content.v1.generic.tradefeedr_api import TradefeedrApi

## need pandas to translate JSON results from API
import pandas as pd

## create API object
tf_api_object = TradefeedrApi(demo=True)

## options
performance_metric = ["ArrivalMidPerfBPS", "ArrivalMidPerfNetBPS", "TWAPMidPerfBPS", "TWAPMidPerfBPS"][3]
options = {
    "groupby": [
        "LP",
        "HourArrive"
    ],
    "select": [
        "NumRuns",
        "TradeQuantityUSD",
        "ArrivalMidPerfBPS",
        "TWAPMidPerfBPS",
        "RiskTransferPricePerfBPS"
    ],
    "filter": [
        {"function": "within", "var": "Date", "pars": ["2018-01-01", "2018-12-31"]},
        {"function": "within", "var": "ArrivalTime", "transform": "time", "pars": ["12:00:00", "14:00:00"]},
        {"function": "lt", "var":  performance_metric, "par": 100},
        {"function": "eq", "var": "Symbol", "par": "EURUSD"}
    ],
    "risk_price_benchmark": "TradefeedrModel",
    "notation" : "performance"
}

# this is api end-point which returns parent order stats
endpoint = "v1/fx/algo/parent-order-stats"

## call the API
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response["result"])
# data_frame = data_frame.set_index("LP")
data_frame
```
```
#### Results

![api_algo_parent_order_stats_ex6.png](assets/images/api_algo/parent_order_stats/api_algo_parent_order_stats_ex6.png)

###  Empty groupby

This is useful when only total number is required. 

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
    "groupby": [],
    "select": [
        "NumRuns",
        "TradeQuantityUSD",
        "ArrivalMidPerfBPS",
        "TWAPMidPerfBPS",
        "RiskTransferPricePerfBPS"
    ],
    "filter": [
        {"function": "within", "var": "Date", "pars": ["2018-01-01", "2018-12-31"]},
        {"function": "in", "var": "Symbol", "pars": ["EURUSD", "USDJPY"]}
    ],
    "risk_price_benchmark": "TradefeedrModel",
    "notation": "performance"
}

# this is api end-point which returns parent order stats
endpoint = "v1/fx/algo/parent-order-stats"

## call the API
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response["result"])
# data_frame = data_frame.set_index("NumRuns")
data_frame
```
```
#### Results

![api_algo_parent_order_stats_ex7.png](assets/images/api_algo/parent_order_stats/api_algo_parent_order_stats_ex7.png)

### Wildcard `*` search 

Filtering supports simple wildcard. In the example below we select all the currencies pairs which start with USD and group by currency pair to illustrate the result of the filtering. It is useful to aggregate across specific crosses. 

For example, if algo user would like to analyse results for all AUD crosses (EURAUD, AUDUSD etc). 

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
        "Account"
    ],
    "select": [
        "NumRuns",
        "TradeQuantityUSD",
        "ArrivalMidPerfBPS",
        "TWAPMidPerfBPS",
        "RiskTransferPricePerfBPS"
    ],
    "filter": [
        {"function": "like", "var": "Symbol", "par": "USD*"}
        #{"function": "like", "var": "ParentOrderID", "pars": "**201809**"},  # can search ParentOrderID by wildcard
        #{"function": "like", "var": "Account", "pars": "**Algo**"},  # can search  Account by wildcard
    ],
    "risk_price_benchmark": "TradefeedrModel",
    "notation": "performance"
}

# this is api end-point which returns parent order stats
endpoint = "v1/fx/algo/parent-order-stats"

## call the API
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response["result"])
# data_frame = data_frame.set_index("Symbol")
data_frame
```
```
#### Results

![api_algo_parent_order_stats_ex8.png](assets/images/api_algo/parent_order_stats/api_algo_parent_order_stats_ex8.png)

### Excluding Specific Variables

At times, you may wish to exclude certain currency pair(s) or/and certain liquidity provider(s) from analysis. 
The `not_in` function only applies to symbolic variables.

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
        "LP"
    ],
    "select": [
        "NumRuns",
        "TradeQuantityUSD",
        "ArrivalMidPerfBPS",
        "TWAPMidPerfBPS",
        "RiskTransferPricePerfBPS",
    ],
    "filter": [
        {"function": "not_in", "var": "Symbol", "pars": ["EURUSD", "USDJPY", "GBPUSD"]},
        {"function": "not_in", "var": "LP", "par": "LP3"}
    ],
    "risk_price_benchmark": "TradefeedrModel",
    "notation": "performance"
}

# this is api end-point which returns parent order stats
endpoint = "v1/fx/algo/parent-order-stats"

## call the API
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response["result"])
# data_frame = data_frame.set_index("Symbol")
data_frame
```
```
#### Results

![api_algo_parent_order_stats_ex9.png](assets/images/api_algo/parent_order_stats/api_algo_parent_order_stats_ex9.png)

### Intraday pattern of different performance metrics

Intraday execution pattern can be easily constructed across select time period/currencies. 

The `ArrivalTime` variable in the `groupby` below is transformed in `HH:MM` format and is then rounded down to the nearest multiple of `par`. 

For example, 11:20 becomes 11:00. 
The buckets such as 11:00 (including all times from 11:00 and 11:29) and 11:30 (including all times from 11:30 to 11:59) are then used for aggregation.  

```python
```
## tradefeedr library
from tradefeedr_public_content.v1.generic.tradefeedr_api import TradefeedrApi

## need pandas to translate JSON results from API
import pandas as pd
from time import strftime, gmtime

## create API object
tf_api_object = TradefeedrApi(demo=True)

## options
options = {
    "groupby": [
         {"function": "bar", "transform": "minute", "var": "ArrivalTime", "par": 30}
    ],
    "select": [
        "NumRuns",
        "TradeQuantityUSD",
        "ArrivalMidPerfBPS",
        "TWAPMidPerfBPS",
        "RiskTransferPricePerfBPS" ],
    "filter": [
        {"function": "within", "var": "Date", "pars": ["2018-01-01", "2018-12-31"]}
    ],
    "risk_price_benchmark": "TradefeedrModel",
    "notation": "performance"
}

# this is api end-point which returns parent order stats
endpoint = "v1/fx/algo/parent-order-stats"

## call the API
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response["result"])
select_index = data_frame.ArrivalTime != "TOTAL"
data_frame.loc[select_index, "ArrivalTime"] = data_frame.loc[select_index, "ArrivalTime"] if isinstance(data_frame.loc[select_index, "ArrivalTime"].iloc[0], str) else data_frame.loc[select_index, "ArrivalTime"].apply(lambda x: strftime("%H:%M:%S", gmtime(x["i"]*60)))

# data_frame = data_frame.set_index("ArrivalTime")
data_frame
```
```
#### Results

![api_algo_parent_order_stats_ex10.png](assets/images/api_algo/parent_order_stats/api_algo_parent_order_stats_ex10.png)

#### Figure

```python
```
# import plotly libary
import plotly.express as px

# Modify dataframe
data_frame = data_frame.set_index("ArrivalTime")
data_frame = data_frame.iloc[:-1,:]

# Plot figure
fig = px.line(data_frame.drop("TradeQuantityUSD", axis=1), x=data_frame.index,
              y=["ArrivalMidPerfBPS","TWAPMidPerfBPS","RiskTransferPricePerfBPS"],
              title="Intraday pattern of different performance metrics")
fig.show()
```
```
###  Algo performance in across different volatility regimes

Group modification function `hist` (stands for histogram buckets) splits the incoming variable range (`DailyVolatilityPct` in the below example) into a number of buckets of the same size. From `min` to `max` into several (10 in the below example) buckets.  Variables in the `select` operator are aggregated within those buckets. The mean values in each category are returned in the column with this variable name. Algo performance statistics in each bucket are calculated to study the dependence between this variable and algo performance. 

The example below shows how selected performance statistics vary across different volatility regimes. 

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
         {"function": "hist",  "var": "DailyVolatilityPct", "par": 10}
    ],
    "select": [
        "NumRuns",
        "TradeQuantityUSD",
        "ArrivalMidPerfBPS",
        "TWAPMidPerfBPS",
        "RiskTransferPricePerfBPS"
    ],
    "filter": [
        {"function": "within", "var": "Date", "pars": ["2018-01-01", "2018-12-31"]}
    ],
    "risk_price_benchmark": "TradefeedrModel",
    "notation": "performance"
}

# this is api end-point which returns parent order stats
endpoint = "v1/fx/algo/parent-order-stats"

## call the API
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response["result"])
# data_frame = data_frame.set_index("DailyVolatilityPct")
data_frame
```
```
#### Results

![api_algo_parent_order_stats_ex11.png](assets/images/api_algo/parent_order_stats/api_algo_parent_order_stats_ex11.png)

###  Algo performance in different geographic time-zone 

In this example we aggregate the data by grouping by `TimeZoneArrive` and `TimeZoneEnd`.
This allows you to evaluate the performance of the algo runs by the geographic time-zone.

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
        "TimeZoneArrive",
        "TimeZoneEnd"
    ],
    "select": [
        "NumRuns",
        "TradeQuantityUSD",
        "ArrivalMidPerfBPS",
        "TWAPMidPerfBPS",
        "RiskTransferPricePerfBPS"
    ],
    "filter": [
        {"function": "within", "var": "Date", "pars": ["2018-01-01", "2018-12-31"]}
    ],
    "risk_price_benchmark": "TradefeedrModel",
    "notation": "performance"
}

# this is api end-point which returns parent order stats
endpoint = "v1/fx/algo/parent-order-stats"

## call the API
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response["result"])
# data_frame = data_frame.set_index("TimeZoneArrive")
data_frame
```
```
#### Results

![api_algo_parent_order_stats_ex12.png](assets/images/api_algo/parent_order_stats/api_algo_parent_order_stats_ex12.png)

## Field Definitions
Refer to [Analytics Algo](../analytics/algo.md) page for details and formula.


### Possible Aggregation Columns (for `select` if `groupby` is present)

```csv
Name,Description
NumRuns,Number of Algo Runs
TradeQuantityUSD,USD Equivalent of TradeQuantity
OrderQuantityUSD,USD Equivalent of OrderQuantity
Duration,Order Duration in seconds.
AssumedRisk,Cumulative volatility of the market during ParentOrderID. Based on Tradefeedr intraday volatility model. Volatility is estimated for each minute and integrated over the duration of the algo. Expressed in basis points.
TradeIntensity,Trading intensity per ParentOrderID: average speed of execution in USD traded per minute. Equals to TradeQuantityUSD/ (Duration/60)
SpreadPaidBPSChildOrders,"Spread paid on child fills . TradeQuantityUSD-weighted average across of spread paid of all child fills and then across ParendOrderIDs if further aggregated (driven by ""groupby"").  For individual child order the spread paid is simply the difference between mid price and executed price expressed in basis points and adjusted for Side. Positive number mean buying above mid and selling below mid. Negative number is the opposite. Expresses in basis points. "
ArrivalMidPerfBPS,"Total algo performance to ArrivalPrice (arrival mid). Positive number means out-performance (buying below mid, selling below mid). Weighted average of ArrivalMidPerfTradeBPS and ArrivalMidPerfRemainBPS with weights being proportional to TradeQuantity and RemainQuantity.  Expressed in basis points. "
ArrivalMidPerfBPSStdDev,Standard Deviaition of ArrivalMidPerfBPS.  Expressed in basis points.
ArrivalMidPerfTradeBPS,Percentage Difference between ArrivalPrice (arrival mid) and AllInPrice. Adjusted for Side. Positive number means out-performance of mid price (buying below the ArrivalPrice and selling above). Expressed in basis points.
ArrivalMidPerfRemainBPS,Market move during algo execution adjusted by Side. When it is negative the market moved in the direction of trading making subsequent purchases more costly (e.g market moving up when algo was buying). This is used to adjust algo for un-executed amounts.   Expressed in basis points.
TWAPMidPerfBPS,Percentage difference between AllInPrice and TWAPPrice. Adjusted for Side. Positive number means out-performance of TWAPPrice (buying below the TWAPPrice and selling above TWAPPrice). Expressed in basis points
TWAPMidPerfBPSStdDev,TradeQuantityUSD-weighted Standard Deviaition of TWAPMidPerfBPS.  Expressed in basis points
RiskTransferCostBPS,"Risk Transfer Cost is the cost of alternative immediate execution (against risk transfer benchmark). The risk transfer benchmark is determined by selecting ""risk_transfer_benchmark"" in options. Aggregated across individual ParentOrderIDs as a weighted average with TradeQuantityUSD being the weights.  Expressed in basis points (to mid)"
RiskTransferPerfBPS,Performance of AllInPrice to Risk Transfer Price benchmark.  Positive numbers are out-performance  of Risk Transfer Benchmark (buying below Risk Transfer benchmark price and selling above) and negative number mean underperformance.  Aggregated as a weighted average across individual parent Orders with with TradeQuantityUSD being the weights.The type of risk transfer benchmark can be specified by selecting risk_transfer_benchmark in options. Expressed in basis points
RiskTransferPerfBPSStdDev,Standard Deviation of the RiskTransferPerfBPS benchmark. Aggregated as a weighted standard deviation with TradeQuantityUSD being the weights.  Expressed in basis points.
RiskTransferPerfIR,Information Ratio (RiskTransferPerfBPS divided by its standard deviation - RiskTransferPerfBPSStdDev). Unit free.
ArrivalMidPerfNetBPS,"Net total algo performance to ArrivalPrice (arrival mid).  Positive in out-performance (buying below mid, selling below mid). When aggregated it is weighted average of ArrivalMidPerfTradeNetBPS and ArrivalMidPerfRemainNetBPS with weights being proportional to TradeQuantity and RemainQuantity.  Expressed in basis points "
ArrivalMidPerfNetBPSStdDev,Standard Deviation of ArrivalMidPerfNetBPS.  Expressed in Basis Points
ArrivalMidPerfTradeNetBPS,Performance To Arrival Mid. Percentage Difference between ArrivalPrice and AllInNetPrice. Adjusted for Side. Positive number means out-performance of mid price (buying below the ArrivalPrice and selling above. Expressed in basis points.
ArrivalMidPerfRemainNetBPS,Market move during algo execution adjusted to the Side. When it is negative the market moved in the direction of trading making subsequent purchases more costly (e.g. market moving up when algo was buying). This is used to adjust algo for un-executed amounts.   
TWAPMidPerfNetBPS,Percentage difference between AllInNetPrice and TWAPPrice. Adjusted for Side. Positive number means outperformance of TWAPPrice (buying below the TWAPPrice and selling above TWAPPrice). Expressed in basis points
TWAPMidPerfNetBPSStdDev,Standard Deviation of TWAPMidPerfNetBPS.  Expressed in Basis Points
RiskTransferPricePerfNetBPS,Performance of AllInNetPrice (see parent-orders) to Risk Transfer Price benchmark.  Positive numbers are out-performance  of Risk Transfer Benchmark (buying below Risk Transfer benchmark price and selling above) and negative number mean underperformance.  Aggregated as a weighted average across individual parent Orders with with TradeQuantityUSD being the weights.The type of risk transfer benchmark can be specified by selecting risk_transfer_benchmark in options. Expressed in basis points
RiskTransferPricePerfNetBPSStdDev,Standard Deviation of the RiskTransferPricePerfNetBPS benchmark. Aggregated as a weighted standard deviation with TradeQuantityUSD being the weights.  Expressed in basis points.
RiskTransferPricePerfNetIR,Information Ratio (RiskTransferPerfNetBPS divided by its standard deviation - RiskTransferPerfNetBPSStdDev). Unit free.
ExecutionScore,"TradeQuantityUSD-Weighed-Average Scores of Individual Child Orders. Execution Scores  of individual child fills are calculated as rank-percentile of Price against the distribution of mid-price during algo execution.  It is the number between 0 and 100. For example, buy at the low of range would get a rank of 100 and buy at the high the price range would get a rank of 0 (reverse for sell order)."
ReversalScore,"TradeQuantityUSD-Weighed-Average Reversal Scores of Individual Child Orders. Reversal Scores of individual child fills are calculated as rank percentiles of Price against the distribution of mid-price post algo execution.  It is a number between 0 and 100. For example, buy at the low of range would get a rank of 100 and buy at the high the price range would get a rank of 0 (reverse for sell order)."
```

### Possible Modification Function for `filter` and `groupby` 

```csv
Name,Description
Date,Date of ArrivalTime. For example: 2020-12-31
ParentOrderID,Unique identifier per algo run
Symbol,Currency pair of ParentOrderID. For example:  EURUSD
TradeCurrency,Denomination currency for OrderQuantity
Side,"Buy (B) or Sell (S). Buy or sell applies to currency pair (Symbol) in FX market convention, not to TradeCurrency.  For example, if Symbol is provided as EURUSD,  buys always means buying EUR and selling USD"
LegSymbols,"All currency pairs which have been traded to execute this ParentOrderID. This is relevant for multi-leg execution. For example, where AUDNOK is traded through 3 legs:  AUDUSD, EURNOK and EURUSD  "
Trader,The name of  a trader associated with this ParentOrderID
Account,Name of the underlying client this ParentOrderID executed on behalf of
SubAccount,SubAccount associated with this ParentOrderID
AlgoName,"AlgoName such as  ""TWAP"", ""Shortfall"", ""Tiger"" (normally marketing name under which an algo is sold by AlgoVendor)"
LP,AlgoVendor: institution responsible for overall algo execution
TimeZoneArrive,"Trading time zone of the ArrivalTime: ""London"" (07:00-15:00 GMT), ""NewYork"" (15:00-22:00 GMT) and ""Asia"" (22:00-07:00 GMT)"
HourArrive,"Hour of the ArrivalTime, GMT, 0 to 23. ""0""  for ArrivalTime between 00:00 and 00:59:59, ""1"" for  ArrivalTime between 01:00 and 01:59:59 etc"
TimeZoneEnd,"Trading time zone of the LastTime: ""London"" (07:00-15:00 GMT), ""NewYork"" (15:00-22:00 GMT) and ""Asia"" (22:00-07:00 GMT)"
HourEnd,"Hour of the LastTime, GMT, 0 to 23. ""0""  for LastTime between 00:00 and 00:59:59, ""1"" for  LastTime between 01:00 and 01:59:59 etc"
G10EM,"G10 or EM currency pair. G10 currency is EUR,USD,JPY,GBP,AUD,NZD,CAD,NOK,SEK,CHF.  If at least one currency in currency pair is not G10 currency then currency pair is classified as EM, otherwise it is G10"
TradeSizeBucketUSDM,"Translation of TradeQuantityUSD into USD size bucket in human readable format like 0-50, 50-100 etc.  0-50 means algo TradeQuantityUSD is between 0 and $50mil etc "
OrderQuantity,"Total  quantity ordered. For example: 10,000,000. In units of TradeCurrency. For ParentOrderID with multiple order quantities (amends) only the last ordered quantity is reported. "
AvgChildOrderQuantityUSD,Average Size of Child Order in USD
OrderQuantityUSD,USD Equivalent of OrderQuantity
TradeQuantityUSD,USD Equivalent of TradeQuantity
TradeQuantity,TradeQuantity in TradeCurrency
RemainQuantity,Amount which is not executed (in TradeCurrency)
ArrivalTime,Time (GMT) when the execution desk starts to execute the order.
ArrivalPrice,The Tradefeedr mid-price of the Symbol at the time immediately preceding the ArrivalTime. This is used for ArrivalMidPerfBPS.
TWAPPrice,Time Weighted Average Price of Symbol during algo execution
LastTime,The time the algo execution is done. Unless specific instruction is provided by AlgoVendor it is the time of the last fill.
LastPrice,Last mid price for Symbol observed at LastTime. The RemainQuantity is marked to market at LastPrice and is used to calculate ArrivalMidPerfRemainNetBPS
NumChildEvents,"Total Number of Child Events in ParentOrderID. The events include child order execution (fills), rejects and order placement by AlgoVendor"
NumParentEvents,"Total Number of Parent Events in ParentOrderID. The events include Parent Order Events. There should be at least one per ParentOrderID describing initial algo orders. Parent events represent all user instructions delivered to AlgoVendor (LP) such as LimitPrice changes, Algo Urgency changes, Order Size Changes, Stop and Start etc."
CurrencyPositions,"Decomposition of all child order executions into positions by currency. For example {‘EUR’: -1000, “USD”: 1100}. Normally only useful for multi-leg algo where for example AUDNOK is executed through AUDUSD, EURNOK and EURUSD legs and the resulting position will contain two main target currencies in the cross (AUD and NOK in this case). "
Duration,Order Duration in seconds.
TradeIntensity,Trading intensity per ParentOrderID: average speed of execution in USD traded per minute. Equals to TradeQuantityUSD/ (Duration/60)
OrderIntensity,Trading intensity per ParentOrderID based on OrderQuantityUSD.  Average speed of execution in USD traded per minute. Equals to OrderQuantityUSD/ (Duration/60)
RiskTransferPrice,Risk Transfer Price at ArrivalTime and for OrderQuantity for this order as submitted by AlgoVendor
PrincipalMid,PrincipalMid at ArrivalTime for this order as submitted by AlgoVendor
DailyVolatilityPct,"Volatility forecast for the execution day. Expressed as annualised volatility of Symbol in percentage points. For example, 10.5% is reported as 10.5."
ArrivalVolatilityPct,Volatility as measured at the ArrivalTime. Based on intraday volatility model. Expressed as annualized volatility of Symbol in percentage points. For example 10.5% is reported as 10.5.
SpreadPaidPMChildOrders,TradeQuantityUSD-weighted average spread paid of child fills. For each child fill the spread paid is the difference between mid price and executed price expressed in $/m (100xbasis point) and adjusted for Side. Positive number means buying above the mid and selling below. Expressed in $/m.
AllInPrice,"Effective overall rate at which ParentOrderID was executed. For single leg executions it is TradeQuantityUSD-weighted-average Price over all child fills.
For multi-leg order each execution is split into individual currencies. Then effective currency balances of all executions are aggregated. Finally, effective rate is calculated as a ratio of the balance of target currencies. For example if target Symbol is AUDNOK and the AUD balance is 1m and NOK balance is 6m then the effective execution rate would be 6m/1m = 6.
"
AllInNetPrice,Net effective overall rate at which ParentOrderID was executed. It is AllInPrice adjusted for algo provider fees. It is calculated by Tradefeedr from NetPrices of child orders in the same way as AllInPrice. Should be above AllInPrice for Side=B and below AllInPrice for Side=S with the difference being execution fees
ExecutionScore,"TradeQuantityUSD-Weighed-Average Scores of Individual Child Orders. Execution Scores  of individual child fills are calculated as rank-percentile of Price against the distribution of mid-price during algo execution.  It is the number between 0 and 100. For example, buy at the low of range would get a rank of 100 and buy at the high the price range would get a rank of 0 (reverse for sell order)."
ReversalScore,"TradeQuantityUSD-Weighed-Average Reversal Scores of Individual Child Orders. Reversal Scores of individual child fills are calculated as rank percentiles of Price against the distribution of mid-price post algo execution.  It is a number between 0 and 100. For example, buy at the low of range would get a rank of 100 and buy at the high the price range would get a rank of 0 (reverse for sell order)."
RiskTransferCostReportedPM,"Risk transfer cost as reported by AlgoVendor. If AlgoVendor does not submit this information, None is returned.  Expressed in $/m (100 x basis point)"
RiskTransferCostStaticPM,Risk trader cost as submitted by Tradefeedr client. Can be missing/None if it was not provided by the Tradefeedr client. Expressed in $/m (100 x basis point)
RiskTransferCostVolBumpPM,RiskTransferCostStaticPM adjusted for volatility level to reflect current market trading conditions. Expressed in $/m (100 x basis point)
RiskTransferCostModelPM,"Tradefeedr estimated risk transfer cost, average level per symbol per trading day.  Expressed in $/m (100xbasis point). Mainly used to calibrate user provided RiskTransferCostStaticPM"
RiskTransferCostTradefeedrPM,Tradefeedr estimated risk transfer cost  for ParentOrderID.  Expressed in $/m (100xbasis point).
AssumedRisk,Cumulative volatility of the market during ParentOrderID. Based on Tradefeedr intraday volatility model. Volatility is estimated for each minute and integrated over the duration of the algo. Expressed in basis points.
ArrivalMidPerfTradeBPS,Percentage Difference between ArrivalPrice (arrival mid) and AllInPrice. Adjusted for Side. Positive number means out-performance of mid price (buying below the ArrivalPrice and selling above). Expressed in basis points.
ArrivalMidPerfRemainBPS,Market move during algo execution adjusted by Side. When it is negative the market moved in the direction of trading making subsequent purchases more costly (e.g. market moving up when algo was buying). This is used to adjust algo for un-executed amounts.   Expressed in basis points.
ArrivalMidPerfBPS,"Total algo performance to ArrivalPrice (arrival mid). Positive number means out-performance (buying below mid, selling below mid). Weighted average of ArrivalMidPerfTradeBPS and ArrivalMidPerfRemainBPS with weights being proportional to TradeQuantity and RemainQuantity.  Expressed in basis points. "
TWAPMidPerfBPS,Percentage difference between AllInPrice and TWAPPrice. Adjusted for Side. Positive number means out-performance of TWAPPrice (buying below the TWAPPrice and selling above TWAPPrice). Expressed in basis points
ArrivalMidPerfNetBPS,"Net total algo performance to ArrivalPrice (arrival mid).  Positive in out-performance (buying below mid, selling below mid). When aggregated it is weighted average of ArrivalMidPerfTradeNetBPS and ArrivalMidPerfRemainNetBPS with weights being proportional to TradeQuantity and RemainQuantity.  Expressed in basis points "
ArrivalMidPerfTradeNetBPS,Performance To Arrival Mid. Percentage Difference between ArrivalPrice and AllInNetPrice. Adjusted for Side. Positive number means out-performance of mid price (buying below the ArrivalPrice and selling above. Expressed in basis points.
ArrivalMidPerfRemainNetBPS,Market move during algo execution adjusted to the Side. When it is negative the market moved in the direction of trading making subsequent purchases more costly (e.g. market moving up when algo was buying). This is used to adjust algo for un-executed amounts.   
TWAPMidPerfNetBPS,Percentage difference between AllInNetPrice and TWAPPrice. Adjusted for Side. Positive number means outperformance of TWAPPrice (buying below the TWAPPrice and selling above TWAPPrice). Expressed in basis points
SlippageToArrivalMidTradePM,"SlippageToArrivalMidTradePM. Percentage difference between ArrivalPrice and AllInPrice. Adjusted for Side. Positive number means underperformance of mid price (buying above the ArrivalPrice and selling below. Expressed in $/m (100 x Basis Point or 10,000 percent)"
SlippageToArrivalMidRemainPM,SlippageToArrivalMidRemainPM. Market move during algo execution adjusted to the Side. This is used to adjust algo for un-executed amounts.   
SlippageToArrivalMidPM,"SlippageToArrivalMid (Positive in underperformance, negative is out-performance). Total slippage to arrival mid. Weighted average of SlippageToArrivalMidTradePM and SlippageToArrivalMidRemainPM with wights proportional to TradeQuantity and RemainQuantity.  Expressed in $/m (100 x Basis Point or 10,000 percent)"
SlippageToTWAPMidPM,"Percentage Difference between Algo Effective Execution Price (AllInPrice) and TWAPPrice. Adjusted for Side. Positive number means underperformance of TWAPPrice (buying above the TWAPPrice and selling below TWAPPrice). Expressed in $/m (100 x Basis Point or 10,000 percent)"
SlippageToArrivalMidNetPM,"SlippageToArrivalMid (Positive in underperformance, negative is out-performance). Total slippage to arrival mid. Weighted average of SlippageToArrivalMidTradePM and SlippageToArrivalMidRemainPM with weights being proportional to TradeQuantity and RemainQuantity.  Expressed in $/m (100 x Basis Point)"
SlippageToArrivalMidTradeNetPM,SlippageToArrivalMidTradePM. Percentage Difference between ArrivalPrice and AllInPrice. Adjusted for Side. Positive number means underperformance of mid price (buying above the ArrivalPrice and selling below. Expressed in $/m (100 x Basis Point)
SlippageToArrivalMidRemainNetPM,SlippageToArrivalMidRemainPM. Market move during algo execution adjusted to the Side. This is used to adjust algo for non-executed amounts.   
SlippageToTWAPMidNetPM,Percentage Difference between AllInNetPrice and TWAPPrice. Adjusted for Side. Positive number means net under-performance of TWAPPrice (buying above the TWAPPrice and selling below TWAPPrice). Expressed in $/m (100 x Basis Point)
SubmissionTime,Time (GMT) when the order arrives to the execution desk.
SubmissionPrice,The Tradefeedr mid-price of the Symbol at the time immediately preceding the SubmissionTime. This is used for SubmissionMidPerfBPS.
FirstFillTime,Time (GMT) when the the first order is executed.
FirstFillPrice,The Tradefeedr mid-price of the Symbol at the time immediately preceding the FirstFillTime. This is used for FirstFillMidPerfBPS.
SubmissionMidPerfBPS,"Total algo performance to SubmissionPrice. Positive number means out-performance (buying below mid, selling below mid). Weighted average of SubmissionMidPerfTradeBPS and SubmissionMidPerfRemainBPS with weights being proportional to TradeQuantity and RemainQuantity. Expressed in basis points."
SubmissionMidPerfTradeBPS,Percentage Difference between SubmissionPrice  and AllInPrice. Adjusted for Side. Positive number means out-performance of mid price (buying below the SubmissionPrice  and selling above). Expressed in basis points.
SubmissionMidPerfRemainBPS,Market move during algo execution adjusted by Side. When it is negative the market moved in the direction of trading making subsequent purchases more costly (e.g. market moving up when algo was buying). This is used to adjust algo for un-executed amounts. Expressed in basis points.
SubmissionMidPerfNetBPS,Net of fees version of SubmissionMidPerfBPS
SubmissionMidPerfTradeNetBPS,Net of fees version of SubmissionMidPerfTradeBPS
SubmissionMidPerfRemainNetBPS,Net of fees (client price) version of SubmissionMidPerfRemainBPS
FirstFillMidPerfBPS,"Total algo performance to FirstFillPrice. Positive number means out-performance (buying below mid, selling below mid). Weighted average of FirstFillMidPerfTradeBPS and FirstFillMidPerfRemainBPS with weights being proportional to TradeQuantity and RemainQuantity. Expressed in basis points."
FirstFillMidPerfTradeBPS,Percentage Difference between FirstFillPrice and AllInPrice. Adjusted for Side. Positive number means out-performance of mid price (buying below the SubmissionPriceÂ  and selling above). Expressed in basis points.
FirstFillMidPerfRemainBPS,Market move during algo execution adjusted by Side. When it is negative the market moved in the direction of trading making subsequent purchases more costly (e.g. market moving up when algo was buying). This is used to adjust algo for un-executed amounts.Expressed in basis points.
FirstFillMidPerfNetBPS,Net of fees version of FirstFillMidPerfBPS
FirstFillMidPerfTradeNetBPS,Net of fees version of FirstFillMidPerfTradeBPS
FirstFillMidPerfRemainNetBPS,Net of fees version of FirstFillMidPerfRemainBPS
```