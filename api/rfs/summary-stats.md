# Summary Stats

## Introduction

The `v1/fx/rfs/summary_stats` endpoint is designed to provide you the ability to summarise the trading performance looking in particular at the spreads and rejects. For example, you can rank the fill quality of their `LP` s using the summary stats within specific time frame or for certain currency pairs.   

Allows the API user to generate an execution summary report.  The summary report includes standard flow quality metrics such as trading volume, spread paid, rejection costs, market impact (flow toxicity) across user defined categories. The query returns a table with the metrics (fields) `groupby` the user defined columns. 

## API Specification
The API endpoint requires a JSON object representing query logic similar to SQL and containing the following fields:

- `groupby` - which fields the results will be aggregated by
- `select`  - which fields should be returned in the end result.
- `filter`  - how the underlying data should be filtered
- `time_offset` - is the decay time offset to use for the performance, e.g. 250ms, 30s, 10m etc

**Note**: That `time_offset` defaults to `DecayPM500ms`

## API Field Descriptions 

### NumberOfFills

The total number of trades that filled.

###  NumberOfRejects

The total number of trades that were rejected.

###  FillVolume

Total volume of the trades that were filled.

[latexmath]

  
###  RejectVolume

Total volume of the trades that were rejected. 

[latexmath]

###  AvgTradeSizeUSD

The average size in USD of a trade. It is the volume weighted average of the `TradeQuantityUSD`.

The formal definition is as per below.
 
[latexmath]

  
###  SpreadPaid

Spread Paid (expressed $/m) - relative difference between price paid and mid price. Positive number means buying above the mid and selling below the mid.

It is formulated as the volume weighted average of the `SpreadPnLPM` and `TradeQuantityUSD`.

The formal definition is as per below.

  
[latexmath]

###  RejectCost

Cost of rejected trade (in $/m).  Relative move in mid-price from the time rejection message was received (time t) to time t + X miliseconds. 
X milliseconds can be selected by the used. Side adjusted. Positive number means price goes up after buy and down after sell.  

It is the volume weighted average of the markouts of the trades which were rejected.

More formually it is the volume weighted average of the decay (selected by the `time_offset` parameter) and the `RejectVolume`. 

The formal definition is as per below.

[latexmath]

Where latexmath:[N_{rej}] is the total number of the rejected trades and  each j is a trade which was rejected.

###  ToxicityOfFills

Cost of filled trades (in $/m). It is the relative move in mid price from the time trade was done (time t) to time t + X milliseconds. X millisecond can be selected by the used. Side adjusted.

It is the weighted volume average of the markouts of the trades which were filled.
        
More formually it is the volume weighted average of the decay (selected by the `time_offset` parameter) and the `TradeQuantityUSD` were the `OrderStatus` was F. 

The formal definition is as per below.

[latexmath]

Where latexmath:[N_{fill}] is the total number of the filled trades and  each i is a trade which was fill.

###  RejectToFill

Ratio of the RejectedVolume to the FillVolume.

[latexmath]

###  EffectiveSpread

It is the total of the `SpreadPaid` and the `RejectedCost` multiplied by the `RejectRatio`. (All defined above).

[latexmath]

###  VolumeShare

It is the `FillVolume` that a row in the table (the query produces) as a percentage contribution to the total FillVolume of the table.

For example, if we `groupby` `LP` the `VolumeShare` metric of LP1 is the `FillVolume` it contributes to the total FillVolume of all the `LP` s as a percentage.

###  RejectCostUSD

Total cost in USD of the rejected trades. This is the product of the `RejectVolume` and the `RejectCost` (as defined above).

The formal definition is as per below.
[latexmath]

## Examples 

**Note**: For display purposes we have limited the number of rows to 5 and and columns to 10.

### Default aggregation

Refer to [RFS API](api-rfs/api-rfs.md) page for page for details on aggregation logic.

We do not pass any parameters into the `groupby` or `filter` options.

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
      "groupby":[
      ],
      "filter":[
      ]
}

# this is api end-point which returns summary stats
endpoint = "v1/fx/rfs/summary-stats"

## call the API
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response["result"])
# data_frame = data_frame.set_index("NumbeOfFills")
data_frame
```
```
#### Results

![api_rfs_summary_stats_ex1.png](assets/images/api_rfs/summary_stats/api_rfs_summary_stats_ex1.png)

### Only `Symbol` in `groupby`

In this example we group the results by `Symbol` and apply a filter on the `Date` range and `Symbol`s to be excluded.

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
      "groupby":[
          "Symbol",
      ],
      "filter":[
        {"function": "within", "var": "Date", "pars": ["2017-01-01", "2017-12-31"]},
        {"function": "not_in", "var": "Symbol", "pars": ["EURUSD","USDJPY","GBPUSD"]},
      ]
}

# this is api end-point which returns summary stats
endpoint = "v1/fx/rfs/summary-stats"

## call the API
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response["result"])
# data_frame = data_frame.set_index("Symbol")
data_frame
```
```
#### Results

![api_rfs_summary_stats_ex2.png](assets/images/api_rfs/summary_stats/api_rfs_summary_stats_ex2.png)

#### Figure

```python
```
# import plotly libary
import plotly.express as px

# Modify dataframe
data_frame =data_frame.sort_values(by="ToxicityOfFills", ascending=False)

# Plot figure
fig = px.bar(data_frame, x="Symbol", y="ToxicityOfFills",
             title="ToxicityOfFills by Symbol",
             barmode="group")
fig.show()
```
```
### Rejected Volume and Spread analysis

In this example we conduct a venue analysis where we group the results by `LP`, `ExecVenue`, `Symbol`. 
You can assess the fills/rejects and spreads across LPs, different platforms and ECNs. Also, how their volume distribution differs across them.

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
        "LP",          # this is the actual LP for the child order -  can be same as AlgoVendor
        "ExecVenue",   # venue where trading takes place -  can be "CboeFX", "EuronextFX"
        "Symbol",

    ],

    "filter": [
        {"function": "within", "var": "Date", "pars": ["2017-01-01", "2017-12-31"]},
        {"function": "in", "var": "Symbol", "pars": ["EURUSD", "USDJPY"]},

    ]
}

# this is api end-point which returns summary stats
endpoint = "v1/fx/rfs/summary-stats"

## call the API
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response["result"])
# data_frame = data_frame.set_index("LP")
data_frame
```
```
#### Results

![api_rfs_summary_stats_ex3.png](assets/images/api_rfs/summary_stats/api_rfs_summary_stats_ex3.png)

#### Figures

```python
```
# import plotly libary
import plotly.express as px

# Plot figure 1
fig = px.bar(data_frame.groupby("LP").sum(), y="RejectVolume",
             title="Rejected Volume Bar Chart")

fig.update_layout(xaxis={"categoryorder":"total descending"})
fig.show()

# Plot figure 2
fig = px.bar(data_frame, x="LP", y="SpreadPaid",
             color="Symbol",
             title="Spread analysis Bar Chart",
             barmode="group")
fig.show()
```
```
### LP review (masking)

In this example we use the `eqx` function on LP1 and EURUSD.
This enables you to provide a summary report to LP1 highlighting their own statistics and how it aligns with all the other LPs the RFS user has.

It anonymises the data hiding the details of the names of the other `LP`s you have. 
Applying, `eqx` on EURUSD outputs a row for EURUSD and aggregates all the other pairs together in a separate row, labelled as Other.

This can also be used by the LP to do internal analysis of one their account versus everything else.

**Note:** For more details on `eqx` refer to the [Execution Stats](api-rfs/api-rfs-execution-stats.md) page. 

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
        {"function": "eqx", "var": "LP", "par": "LP1"},
        {"function": "eqx", "var": "Symbol", "par": "EURUSD"},
        "ExecVenue",
    ],

    "filter": [
        {"function": "within", "var": "Date", "pars": ["2014-01-01", "2021-11-30"]},
    ]
}

# this is api end-point which returns summary stats
endpoint = "v1/fx/rfs/summary-stats"

## call the API
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
## translate API result into pandas dataframe
data_frame = pd.DataFrame(response["result"])
# data_frame = data_frame.set_index("LP")
data_frame
```
```
#### Results

![api_rfs_summary_stats_ex4.png](assets/images/api_rfs/summary_stats/api_rfs_summary_stats_ex4.png)

### LP review (masking with decay offset)

In this example we show how to apply the `time_offset` and `select` filters to customise the example above.

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
        {"function": "eqx", "var": "LP", "par": "LP1"},
        {"function": "eqx", "var": "Symbol", "par": "EURUSD"},
        "ExecVenue",
    ],

    "select":["NumberOfFills","NumberOfRejects","FillVolume","RejectVolume","SpreadPaid","RejectCost","ToxicityOfFills"],

    "filter": [
        {"function": "within", "var": "Date", "pars": ["2014-01-01", "2021-11-30"]},
    ],
    "time_offset": "1m"
}

# this is api end-point which returns summary stats
endpoint = "v1/fx/rfs/summary-stats"

## call the API
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response["result"])
# data_frame = data_frame.set_index("LP")
data_frame
```
```
#### Results

![api_rfs_summary_stats_ex5.png](assets/images/api_rfs/summary_stats/api_rfs_summary_stats_ex5.png)

## Field Definitions

Refer to [Analytics RFS](../analytics/rfs.md) page for details and formula.

```csv
Name,Description
NumberOfFills,The total number of trades that filled
NumberOfRejects,The total number of trades that where rejected
FillVolume,Total volume of the trades that where filled
RejectVolume,Total volume of the trades that where rejected
AvgTradeSizeUSD,The average size in USD of a trade
SpreadPaid,Spread Paid (expressed $/m) - relative difference between price paid and mid price. Positve number means buying above the mid and selling below the mid.
RejectCost,"	
 Cost of rejected trade (in $/m).  Relative move in mid price from the time rejection message was received (time t) to time t + X miliseconds X millisecond can be selected by the used. Side adjusted. Positive number means price goes up after buy and down after sell.     "
ToxicityOfFills,"	
 Relative move in mid price from the time trade was done (time t) to time t + X miliseconds.  X millisecond can be selected by the used. Side adjusted"
RejectToFill,Ratio of the RejectedVolume to the FillVolume
EffectiveSpread,SpreadPaid +  RejectRatio*RejectCosts (in $/m)
VolumeShare,Is the share of total fill volume
RejectCostUSD,"Is RejectVolume times RejectCost. It is expressed in USD rather than millions of USD of rejections

"
```