# API

## Tradefeedr API Structure

Conceptually, each API call has two components:

- `API end-point` which can be thought of as function doing specific job. Consider for example API endpoint `v1/fx/algo/parent-orders`.

- JSON string containing a set of parameters for the API end-point function. The exact structure of the query string depends on the end point but the following parameters are typically present
  - `groupby` –  variables by which the results would have to be grouped by. For example: `{'groupby':['Symbol']}` implies that results have to be grouped by symbol.
  -  `var`    -  which variables should be returned in the end points.  For example
  -  `filter` - how to filter the results.

All API end-points return a JSON dictionary which can translated into a Python Pandas DataFrame.

### Example API Usage

Example API usage is presented below:

[source, python]

```
```
## tradefeedr library
from tradefeedr_public_content.v1.generic.tradefeedr_api import TradefeedrApi

## need pandas to translate JSON results from API
import pandas as pd

## create API object
tf_api_object = TradefeedrApi(demo=True)

## options
options = {
    "select": [
        "ParentOrderID",
        "ArrivalTime",
        "Side",
        "Symbol",
        "TradeQuantityUSD",
        "AlgoName",
        "LP",
        "ArrivalPrice",
        "AllInPrice",
        "ArrivalMidPerfBPS",
        "TWAPMidPerfBPS",
        "SpreadPaidPMChildOrders",
        #"DailyVolatilityPct",
        #"RiskTransferCostReportedPM",
        #"RiskTransferCostTradefeedrPM",
        "ExecutionScore",
        "ReversalScore",
       ],
    "filter": [
        {"function": "within", "var": "Date", "pars": ["2014-01-01", "2025-12-31"]}
    ],
}

# this is api end-point which returns parent order stats one algo run per row
endpoint = "v1/fx/algo/parent-orders"

## call the API
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response["result"])
# data_frame = data_frame.set_index("ParentOrderID")

## translate ArrivalTime to human readable time
data_frame["ArrivalTime"] = pd.to_datetime(data_frame["ArrivalTime"], unit="ms" if str(data_frame["ArrivalTime"].dtype) == "int64" else None)
data_frame = data_frame.sort_values(by="ArrivalTime", ascending=False)
data_frame
```
```
#### Results

![api_algo_parent_orders_ex1.png](assets/images/api_algo/parent_orders/api_algo_parent_orders_ex1.png)