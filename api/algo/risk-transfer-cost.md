# Risk Transfer Cost


##  Introduction 
The `v1/fx/stats/risk-transfer-cost` endpoint attempts to create an approximation of fair price of immediate execution. 
This endpoint is used when you want to estimate the "fair" spread they would pay if they were to execute full amount immediately.

There are different approaches to estimate the risk transfer costs. Those approaches rank from model driven to purely empirical (measure realized transaction costs and assume they those are best forecast for future). 

Tradefeedr is not a trading company, does not have a live market feeds and hence lacks the data to estimate this risk transfer reliably and consistency with the market. Therefore, Tradefeedr relies on the combined information provided by its member banks and distills this information into a factor model to project fair risk transfer cost for each market environment. 

## Model Specification 
For the model specification refer to the [Risk Transfer Benchmark](../analytics/risk-transfer-price.md) page for details.

## API Specification 

The API endpoint requires a JSON object representing query logic similar to SQL and containing the following fields:

- `select`  - which fields should be returned in the end result. For example `OrderQuantity`
- `filter`  - how the underlying data should be filtered

**Note**: filter takes only `Symbol`,`ArrivalTime` and `OrderQuantity`.

- `OrderQuantity` defaults to 1m USD.
- `ArrivalTime` defaults to the current timestamp.
-  If `Symbol` is not present in the filter no results are returned.

## Examples 
**Note**: For display purposes we have limited the number of rows to 5 and and columns to 10.

### For A Single Trade   

You can query a single trade using the `filter` option to select a single `Symbol`, `ArrivalTime` and `OrderQuantity`(in USD million).

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
    "select":[
        "Date",
        "Symbol",
        "ArrivalTime",
        "OrderQuantity",
        "VolatilityRollingPct",
        "VolatilityIntegratedPct",
        "VolatilityRollingEMAPct",
        "RiskTransferCostBPS"
    ],
    "filter":[
        {"var":"Symbol", "par":["EURUSD"]},
        {"var":"ArrivalTime", "par": ["2022.01.20D11:38:48.725717000"]},
        {"var":"OrderQuantity", "par": 100},
    ],
}

# this is api end-point which returns parent order stats one algo run per row
endpoint = "v1/fx/stats/risk-transfer-cost"

## call the API
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response["result"])

## translate ArrivalTime to human readable time
data_frame["ArrivalTime"] = pd.to_datetime(data_frame["ArrivalTime"], unit="ms" if str(data_frame["ArrivalTime"].dtype) == "int64" else None)
data_frame = data_frame.sort_values(by="ArrivalTime", ascending=False)
# data_frame = data_frame.set_index("Date")
data_frame
```
```
#### Results

![api_algo_risk_transfer_cost_ex1.png](assets/images/api_algo/risk_transfer_cost/api_algo_risk_transfer_cost_ex1.png)

### For A Selection Of Trades   

You can query a selection of trades using the `filter` option to select a list of `Symbol`, `ArrivalTime` and `OrderQuantity`(in USD million).

Then use the `select` option to select the columns displayed.

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
    "select":[
        "Date",
        "Symbol",
        "ArrivalTime",
        "OrderQuantity",
        "VolatilityRollingPct",
        #"VolatilityIntegratedPct",
        #"VolatilityRollingEMAPct",
        "RiskTransferCostBPS"
    ],
    "filter":[
        {"var":"Symbol", "pars":["USDZAR", "EURGBP", "EURUSD"]},
        {"var":"ArrivalTime", "pars": ["2022.01.20D11:38:48.725717000", "2022.01.19D07:52:08.725717000", "2022.01.18D04:05:28.725717000"]},
        {"var":"OrderQuantity", "pars": [100, 200, 300]},
    ],
}

# this is api end-point which returns parent order stats one algo run per row
endpoint = "v1/fx/stats/risk-transfer-cost"

## call the API
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response["result"])

## translate ArrivalTime to human readable time
data_frame["ArrivalTime"] = pd.to_datetime(data_frame["ArrivalTime"], unit="ms" if str(data_frame["ArrivalTime"].dtype) == "int64" else None)
data_frame = data_frame.sort_values(by="ArrivalTime", ascending=False)
# data_frame = data_frame.set_index("Date")
data_frame
```
```
#### Results

![api_algo_risk_transfer_cost_ex2.png](assets/images/api_algo/risk_transfer_cost/api_algo_risk_transfer_cost_ex2.png)

###  By `OrderQuantity`

The example below shows how risk transfer price depends on the order size. 

The dependences of the model are estimated based on empirical data and the coefficients are different for different currencies.  

**Note:** Each of the `filter` options fields must be of equal length in order for the query to run. 

```python
```
## tradefeedr library
from tradefeedr_public_content.v1.generic.tradefeedr_api import TradefeedrApi

## need pandas to translate JSON results from API
import pandas as pd

## create API object
tf_api_object = TradefeedrApi(demo=True)

## options
symbol = "EURUSD"
arrival_time = "2022.01.20D11:38:48.725717000"
quantities = [10, 50, 100, 250, 500, 1000] # this is in millions
n = len(quantities)

options = {
    "select":[
        "Date",
        "Symbol",
        "ArrivalTime",
        "OrderQuantity",
       # "VolatilityRollingPct",
       # "VolatilityIntegratedPct",
       # "VolatilityRollingEMAPct",
        "RiskTransferCostBPS"
    ],
    "filter":[
        {"var":"Symbol", "pars":n*[symbol]},
        {"var":"ArrivalTime", "pars":n*[arrival_time]},
        {"var":"OrderQuantity", "pars": quantities},
    ],
}
# this is api end-point which returns parent order stats one algo run per row
endpoint = "v1/fx/stats/risk-transfer-cost"

## call the API
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response["result"])

## translate ArrivalTime to human readable time
data_frame["ArrivalTime"] = pd.to_datetime(data_frame["ArrivalTime"], unit="ms" if str(data_frame["ArrivalTime"].dtype) == "int64" else None)
data_frame = data_frame.sort_values(by="ArrivalTime", ascending=False)
# data_frame = data_frame.set_index("Date")
data_frame
```
```
#### Results

![api_algo_risk_transfer_cost_ex3.png](assets/images/api_algo/risk_transfer_cost/api_algo_risk_transfer_cost_ex3.png)

#### Figure

```python
```
# import plotly libary
import plotly.express as px

# Plot figure
fig = px.line(data_frame, x="OrderQuantity", y="RiskTransferCostBPS",
              title="Risk Transfer Cost by OrderQuantity")
fig.show()
```
```
### By `ArrivalTime` 

Dynamics of Risk Transfer Costs over time is mainly determined by volatility of the underlying asset.
In the example below, if the measured volatiliity (estimates on a rolling basis for 20 days preceding the day/time of the trade) then EURUSD risk transfer price increases.   
 

```python
```
## tradefeedr library
from tradefeedr_public_content.v1.generic.tradefeedr_api import TradefeedrApi

## need pandas to translate JSON results from API
import pandas as pd

## create API object
tf_api_object = TradefeedrApi(demo=True)

## options
symbol = "EURUSD"
arrival_times = list(pd.date_range(start="01/01/2022", end="01/15/2022", freq="B"))
n = len(arrival_times)

options = {
    "select":[
        "Date",
        "Symbol",
        "ArrivalTime",
        "OrderQuantity",
       # "VolatilityRollingPct",
       # "VolatilityIntegratedPct",
       # "VolatilityRollingEMAPct",
        "RiskTransferCostBPS"
    ],
    "filter":[
        {"var":"Symbol", "pars":n*[symbol]},
        {"var":"ArrivalTime", "pars": [x.strftime("%Y.%m.%d") for x in arrival_times]},
        {"var":"OrderQuantity", "pars": n*[100]},
    ],
}
# this is api end-point which returns parent order stats one algo run per row
endpoint = "v1/fx/stats/risk-transfer-cost"

## call the API
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response["result"])

## translate ArrivalTime to human readable time
data_frame["ArrivalTime"] = pd.to_datetime(data_frame["ArrivalTime"], unit="ms" if str(data_frame["ArrivalTime"].dtype) == "int64" else None)
data_frame = data_frame.sort_values(by="ArrivalTime", ascending=False)
# data_frame = data_frame.set_index("Date")
data_frame
```
```
#### Results

![api_algo_risk_transfer_cost_ex4.png](assets/images/api_algo/risk_transfer_cost/api_algo_risk_transfer_cost_ex4.png)

#### Figure

```python
```
# import plotly libary
import plotly.express as px

# import plotly libary
import plotly.express as px

# Plot figure
fig = px.line(data_frame, x="ArrivalTime", y="RiskTransferCostBPS",
              title="Risk Transfer Cost by ArrivalTime")
fig.show()
```
```
## Field Definitions
Refer to [Risk Transfer Benchmark](../analytics/risk-transfer-price.md) page for details and formula.

```csv
Name,Description
Date,Date corresponding to ArrivalTime
Symbol,Currency pair. For example EURUSD
ArrivalTime,ArrivalTime is the time when trade request was sent. It is GMT time
OrderQuantity,Total  quantity ordered in millions USD
VolatilityRollingPct,Annualised (times sqrt(252)) 20 day rolling volatility of the return series of the specified Symbol and ArrivalTime
VolatilityIntegratedPct,Annualised (times sqrt(252)) square root of the 20 day moving average of the squared return series of the specified Symbol and ArrivalTime
VolatilityRollingEMAPct,Annualised (times sqrt(252)) square root of the 20 day exponential moving average of the squared return series of the specified Symbol and ArrivalTime
RiskTransferCostBPS,Risk Transfer Cost is the cost of alternative immediate execution (against risk transfer benchmark). Aggregated across individual ParentOrderIDs as a weighted average with TradeQuantityUSD being the weights.  Expressed in basis points (to mid)
```