# Parent Orders 

## Introduction

The `v1/fx/algo/parent-orders` endpoint can be used to build algo trading blotter. For example, you can query the most recent trades and their associated performance metrics. 
API  endpoint can also be used to compare the distributions of algo trading performance across different algo providers, business units, currencies etc (algo wheel).

It returns a table of algo execution information, one algo run per table row. Each row contains a number of fields controlled by the `select` parameter. 
The fields are either (1) descriptive such as `ParentOrderID`, `Symbol`, `LP`  or (2) calculated such as `ArrivalMidPerfBPS`.  

## API Specification 
The API endpoint requires a JSON query representing query logic in SQL-like fashion and containing the following fields:

- `select`  - which variables should be returned in the end result. For example `ArrivalMidPerfBPS`. The full list of possible values can be found at the end of this notebook
- `filter`  - how the underlying data should be filtered

## Examples

**Note**: For display purposes we have limited the number of rows to 5 and and columns to 10.

### Algo Blotter 

Typical application of this  API end point is algo trading blotter. 
A list of most recent algo executions can be queried from underlying dataset and presented as the table.

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

### Filtering by performance metric

This example selects a number of algo runs done in specific currency pair (EURUSD) and applies a filter to a performance metric (for example `ArrivalMidPerfBPS`). 

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
performance_metric = ["ArrivalMidPerfBPS", "ArrivalMidPerfNetBPS", "TWAPMidPerfBPS", "TWAPMidPerfBPS"][0]
options = {
    "select": [
        "Date",
        "ParentOrderID",
        "ArrivalTime",
        "NumChildEvents",
        "NumParentEvents",
        "Side",
        "Symbol",
        "Duration",
        "TradeQuantityUSD",
        "AlgoName",
        "LP",
        "ArrivalPrice",
        "AllInPrice",
        "ArrivalMidPerfBPS",
        "ArrivalMidPerfNetBPS",
        "TWAPMidPerfBPS",
        "TWAPMidPerfNetBPS"
        ],
    "filter": [
        {"function": "within", "var": "Date", "pars": ["2014-01-01", "2025-12-31"]},
        {"function": "eq", "var": "Symbol", "par": "EURUSD"},
        {"function": "lt", "var": performance_metric, "par": 100}
    ],
}

# this is api end-point which returns parent order stats one algo run per row
endpoint = "v1/fx/algo/parent-orders"

## call the API
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response["result"])
# data_frame = data_frame.set_index("Date")

## translate ArrivalTime to human readable time
data_frame["ArrivalTime"] = pd.to_datetime(data_frame["ArrivalTime"], unit="ms" if str(data_frame["ArrivalTime"].dtype) == "int64" else None)
data_frame = data_frame.sort_values(by="ArrivalTime", ascending=False)
data_frame
```
```
#### Results

**Note**: In the table below the result set has been truncated and it is not displaying the performance metrics.

![api_algo_parent_orders_ex2.png](assets/images/api_algo/parent_orders/api_algo_parent_orders_ex2.png)

### Performance Metric Distribution

In this example, we filter the algo runs to find algos with a negative ArrivalMidPerfBPS.
From this dataset we can construct a histogram showcasing the distribution of the Algo runs with a negative  `ArrivalMidPerfBPS`.

[source, python]
```
```
## tradefeed library
from tradefeedr_public_content.v1.generic.tradefeedr_api import TradefeedrApi

## need pandas to translate JSON results from API
import pandas as pd

## create API object
tf_api_object = TradefeedrApi(demo=True)

## options
options = {
    "select": [
        "Date",
        "ParentOrderID",
        "LP",
        "Side",
        "Symbol",
        "Duration",
        "TradeQuantityUSD",
        "AlgoName",
        "ArrivalMidPerfBPS",
        ],
    "filter": [
        {"function": "within", "var": "Date", "pars": ["2014-01-01", "2025-12-31"]},
        {"function": "eq", "var": "Symbol", "par": "EURUSD"},
        {"function": "within", "var": "ArrivalMidPerfBPS", "par": [-20,0]}
    ],
}

# this is api end-point which returns parent order stats one algo run per row
endpoint = "v1/fx/algo/parent-orders"

## call the API
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response["result"])
#data_frame = data_frame.set_index("Date")

## translate ArrivalTime to human readable time
data_frame.head()
```
```
#### Results

![api_algo_parent_orders_ex6.png](assets/images/api_algo/parent_orders/api_algo_parent_orders_ex6.png)

#### Figure

The figure below plots the distibution of the ArrivalMidPerfBPS metric queried in the example above. 

[source, python]
```
```
# import plotly libary
import plotly.express as px

# Plot figure 1
fig =  px.histogram(data_frame, x="ArrivalMidPerfBPS", title="Histogram of ArrivalMidPerfBPS")
fig.show()
```
```
### Descriptive statistics for algo performance 

API user gets access to all individual parent order executions. 
These can be used to generate descriptive statistics per AlgoVendor (`LP`), `Symbol` or any other descriptive variable.   

Below we apply the pandas groupby and describe function to produce statstics on the `ArrivalMidPerfNetBPS` metric by `LP`.

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
performance_metric = ["ArrivalMidPerfBPS", "ArrivalMidPerfNetBPS", "TWAPMidPerfBPS",  "AssumedRisk", "ExecutionScore"][1]
options = {
    "select": [
        "LP",
        performance_metric,
        ],
    "filter": [
        {"function": "within", "var": "Date", "pars": ["2014-01-01", "2025-12-31"]},
        {"function": "lt", "var": performance_metric, "par": 100},
    ],
}

# this is api end-point which returns parent order stats one algo run per row
endpoint = "v1/fx/algo/parent-orders"

## call the API
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response["result"])

## display results
if data_frame.shape[0] > 0:
    display(data_frame.groupby(["LP"]).describe())
```
```
#### Results

![api_algo_parent_orders_ex3.png](assets/images/api_algo/parent_orders/api_algo_parent_orders_ex3.png)

### Selecting all with  a filter

Omitting `select` option results in API returning all columns. You can then select any metrics required for further analysis from the returned table.  

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
    # "select" clause omitted
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
#data_frame = data_frame.set_index("LP")
data_frame
```
```
#### Results

![api_algo_parent_orders_ex4.png](assets/images/api_algo/parent_orders/api_algo_parent_orders_ex4.png)

### Selecting all the data

Omitting both `select` and `filter` returns the entire algo parent order stats table. 

**Warning**: Returned result can be very large.

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
}

# this is api end-point which returns parent order stats one algo run per row
endpoint = "v1/fx/algo/parent-orders"

## call the API
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response["result"])
# data_frame = data_frame.set_index("ParentOrderID")
data_frame
```
```
#### Results

![api_algo_parent_orders_ex5.png](assets/images/api_algo/parent_orders/api_algo_parent_orders_ex5.png)

## Field Definitions
Refer to [Analytics Algo](../analytics/algo.md) page for details and formula.

[%header,format=csv, cols=["60%", "40%"]]

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