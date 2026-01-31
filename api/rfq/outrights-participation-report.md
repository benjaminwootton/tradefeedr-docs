# Outrights Participation Report

## Introduction
This endpoint returns a table summarises the outrights RFQ participation rate by `LP`. 

The `v1/fx/rfq-outrights/participation-report` endpoint is used to study the hit ratios of the requested outrights RFQs, you can rank each `LP` against various performance ratios. 
Such as `ActualWinRatio`, `ActualVolumeWinRatio`, `WinPerformanceScore` etc. 

You have the ability to see the total requested RFQs (`NumberOfParticipations`),`NumberOfWins` also see how competitive the RFQ stack is. 
This done by looking at the `AverageRFQPanelSize` larger this number more `LP`s competing to price the outright RFQ. 

From this number the expected win rate is derived `ExpectedWinRatio`, higher the `AverageRFQPanelSize` smaller the `ExpectedWinRatio`, inversely proportional. 

## API Specification

The API endpoint requires a JSON object representing query logic similar to SQL and containing the following fields:

- `groupby` - which fields the results will be aggregated by
- `select`  - which fields should be returned in the end result. For example `NumberOfWins`
- `filter`  - how the underlying data should be filtered

**Note:**  The endpoint requires a `LP` `filter` to return a result.

## Example 
**Note**: For display purposes we have limited the number of rows to 5 and and columns to 10.

### Default Results

In the below example the results show the default columns selected when no select option is passed.

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
    "filter":[
    ]
}

# this is api end-point which returns RFQ outrights participation report
endpoint =  "v1/fx/rfq-outrights/participation-report"

## call the API
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response["result"])
# data_frame = data_frame.set_index("LP")
data_frame
```
```
#### Results

![api_rfq_outrights_participation_report_ex1.png](assets/images/api_rfq/outrights/participation_report/api_rfq_outrights_participation_report_ex1.png)

#### Figure

```python
```
# import plotly libary
import plotly.express as px

# Plot figure
fig = px.bar(data_frame, x="LP", y=["NumberOfWins", "ExpectedWins"],
             barmode="group", title="Number of Outright RFQs Won by LP")
fig.show()
```
```
### Hit Ratios  by `LP`

Below we have used the `select` parameter to create a report to show the win rates of the RFQ requests by `LP`.

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
    "select":[
        "LP",
        "NumberOfParticipations",
        "NumberOfWins",
        "ExpectedWins",
        "ActualWinRatio",
        "ExpectedWinRatio",
        "AverageRFQPanelSize",
        "WinPerformanceScore",
    ],
    "filter":[
        {"function":"within","var":"date","pars":["2014-01-01","2021-11-30"]},
    ],
}

# this is api end-point which returns RFQ outrights participation report
endpoint =  "v1/fx/rfq-outrights/participation-report"

## call the API
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response["result"])
# data_frame = data_frame.set_index("LP")
data_frame
```
```
#### Results

![api_rfq_outrights_participation_report_ex2.png](assets/images/api_rfq/outrights/participation_report/api_rfq_outrights_participation_report_ex2.png)

#### Figure

```python
```
# import plotly libary
import plotly.express as px

# Plot figure
fig = px.bar(data_frame, x="LP", y="WinPerformanceScore",
             barmode="group", title="WinPerformanceScore by LP")
fig.show()
```
```
### Volume metrics by `LP`

Below we have used the `select` parameter to create a report to show the volume won of the RFQ requests by `LP`.

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
    "select":[
        "LP",
        "VolumeParticipated",
        "VolumeWon",
        "ExpectedWinVolume",
        "ActualVolumeWinRatio",
        "ExpectedVolumeWinRatio",
        "AverageRFQPanelSize",
        "VolumePerformanceScore",
    ],
    "filter":[
        {"function":"within","var":"date","pars":["2014-01-01","2021-11-30"]},
    ],
}

# this is api end-point which returns RFQ outrights participation report
endpoint =  "v1/fx/rfq-outrights/participation-report"

## call the API
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response["result"])
# data_frame = data_frame.set_index("LP")
data_frame
```
```
#### Results

![api_rfq_outrights_participation_report_ex3.png](assets/images/api_rfq/outrights/participation_report/api_rfq_outrights_participation_report_ex3.png)

#### Figure

```python
```
# import plotly libary
import plotly.express as px

# Plot figure
fig = px.bar(data_frame, x="LP", y="VolumePerformanceScore",
              title="VolumePerformanceScore by LP")
fig.show()
```
```
###  Comparing WinRatios

Below we have used the `select` parameter to create a report to compare the `ActualWinRatio` vs `ActualVolumeWinRatio`.

A high `ActualWinRatio` vs a low `ActualVolumeWinRatio` indicates that the `LP` is competitive with smaller ticket RFQs but not larger volume RFQ requests.

A high `ActualVolumeWinRatio` vs a low `ActualWinRatio` indicates that the `LP` is winning larger volume trades but not as competitive on the small volume tickets.

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
    "select":[
        "LP",
        "NumberOfParticipations",
        "NumberOfWins",
        "VolumeParticipated",
        "VolumeWon",
        "ActualWinRatio",
        "ActualVolumeWinRatio",
    ],
    "filter":[
        {"function":"within","var":"date","pars":["2014-01-01","2021-11-30"]},
    ],
}

# this is api end-point which returns RFQ outrights participation report
endpoint =  "v1/fx/rfq-outrights/participation-report"

## call the API
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response["result"])
# data_frame = data_frame.set_index("LP")
data_frame
```
```
#### Results

![api_rfq_outrights_participation_report_ex4.png](assets/images/api_rfq/outrights/participation_report/api_rfq_outrights_participation_report_ex4.png)

#### Figure

```python
```
# import plotly libary
import plotly.express as px

# Plot figure
fig = px.bar(data_frame, x="LP", y=["ActualWinRatio", "ActualVolumeWinRatio"],
             barmode="group", title="Comparing WinRatios")
fig.show()
```
```
### Groupby `LP` and `Symbol` 

In the below example we `groupby` `LP` and `Symbol`. 

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
    "groupby": [
        "LP",
        "Symbol"
    ],
    "select":[
        "LP",
        "NumberOfParticipations",
        "NumberOfWins",
        "ActualWinRatio",
        "ExpectedWinRatio",
        "VolumeParticipated",
        "VolumeWon",
        "ExpectedWinVolume",
        "ActualVolumeWinRatio",
        "ExpectedVolumeWinRatio",
        "AverageRFQPanelSize",
        "WinPerformanceScore",
        "VolumePerformanceScore",
    ],
    "filter":[
        {"function":"within","var":"date","pars":["2014-01-01","2021-11-30"]},
        {"function":"like","var":"Symbol","pars":"USD*"}
    ],
}

# this is api end-point which returns RFQ outrights participation report
endpoint =  "v1/fx/rfq-outrights/participation-report"

## call the API
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response["result"])
# data_frame = data_frame.set_index("LP")
data_frame
```
```
#### Results

![api_rfq_outrights_participation_report_ex5.png](assets/images/api_rfq/outrights/participation_report/api_rfq_outrights_participation_report_ex5.png)

### Filtering for lower than expected win rate

Below we have filtered the `WinPerformanceScore` to highlight the cases where an `LP` is winning RFQs less than the expected rate. (`ActualWinRatio`< `ExpectedWinRatio`).
The `ExpectedWinRatio` is 1/`AverageRFQPanelSize`.

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
    "groupby": [
        "LP",
        "Symbol"
    ],
    "select":[
        "LP",
        "NumberOfParticipations",
        "NumberOfWins",
        "ActualWinRatio",
        "ExpectedWinRatio",
        "AverageRFQPanelSize",
        "WinPerformanceScore",
    ],
    "filter":[
        {"function":"lt","var":"WinPerformanceScore","par": 0},
    ],
}

# this is api end-point which returns RFQ outrights participation report
endpoint =  "v1/fx/rfq-outrights/participation-report"

## call the API
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response["result"])
# data_frame = data_frame.set_index("LP")
data_frame
```
```
#### Results

![api_rfq_outrights_participation_report_ex6.png](assets/images/api_rfq/outrights/participation_report/api_rfq_outrights_participation_report_ex6.png)

###   Filtering for the Time of Day

In the below example we show you how to filter `TradeTime`.

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
    "groupby": [
        "LP",
        "Symbol"
    ],
    "select":[
        "LP",
        "NumberOfParticipations",
        "NumberOfWins",
        "ActualWinRatio",
        "ExpectedWinRatio",
        "VolumeParticipated",
        "VolumeWon",
        "ExpectedWinVolume",
        "ActualVolumeWinRatio",
        "ExpectedVolumeWinRatio",
        "AverageRFQPanelSize",
        "WinPerformanceScore",
        "VolumePerformanceScore",
    ],
    "filter":[
        {"function":"within","var":"date","pars":["2014-01-01","2021-11-30"]},
        {"function": "within", "var": "TradeTime", "transform": "time", "pars": ["12:00:00", "14:00:00"]},
        {"function":"like","var":"Symbol","pars":"USD*"}
    ],
}

# this is api end-point which returns RFQ outrights participation report
endpoint =  "v1/fx/rfq-outrights/participation-report"

## call the API
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response["result"])
# data_frame = data_frame.set_index("LP")
data_frame
```
```
#### Results

![api_rfq_outrights_participation_report_ex7.png](assets/images/api_rfq/outrights/participation_report/api_rfq_outrights_participation_report_ex7.png)

### Filtering for Larger Trades

In the below example we filter the `TradeQuantityUSD` for trades larger than $100M.
You then can see which `LP` s  are more competitive at larger RFQ trades. 

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
    "select":[
        "LP",
        "NumberOfParticipations",
        "NumberOfWins",
        "ActualWinRatio",
        "ExpectedWinRatio",
        "VolumeParticipated",
        "VolumeWon",
        "ExpectedWinVolume",
        "ActualVolumeWinRatio",
        "ExpectedVolumeWinRatio",
        "AverageRFQPanelSize",
        "WinPerformanceScore",
        "VolumePerformanceScore",
    ],
    "filter":[
        {"function":"within","var":"date","pars":["2014-01-01","2021-11-30"]},
        {"function":"gt","var":"TradeQuantityUSD","par":1e8}
    ],
}

# this is api end-point which returns RFQ outrights participation report
endpoint =  "v1/fx/rfq-outrights/participation-report"

## call the API
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response["result"])
# data_frame = data_frame.set_index("LP")
data_frame
```
```
#### Results

![api_rfq_outrights_participation_report_ex8.png](assets/images/api_rfq/outrights/participation_report/api_rfq_outrights_participation_report_ex8.png)

###  Filtering for Smaller Trades

In the below example we filter the `TradeQuantityUSD` for trades less than $20M.
You then can see which `LP` s are more competitive at smaller RFQ trades. 

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
    "select":[
        "LP",
        "NumberOfParticipations",
        "NumberOfWins",
        "ActualWinRatio",
        "ExpectedWinRatio",
        "VolumeParticipated",
        "VolumeWon",
        "ExpectedWinVolume",
        "ActualVolumeWinRatio",
        "ExpectedVolumeWinRatio",
        "AverageRFQPanelSize",
        "WinPerformanceScore",
        "VolumePerformanceScore",
    ],
    "filter":[
        {"function":"within","var":"date","pars":["2014-01-01","2021-11-30"]},
        {"function":"lt","var":"TradeQuantityUSD","par":2e7}
    ],
}

# this is api end-point which returns RFQ outrights participation report
endpoint =  "v1/fx/rfq-outrights/participation-report"

## call the API
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response["result"])
# data_frame = data_frame.set_index("LP")
data_frame
```
```
#### Results

![api_rfq_outrights_participation_report_ex9.png](assets/images/api_rfq/outrights/participation_report/api_rfq_outrights_participation_report_ex9.png)

## Field Definitions

Refer to [Analytics RFQ](../analytics/rfq.md) page for details and formula.

[%header,format=csv, cols=["60%", "40%"]]

```csv
Name,Description
LP,Executing LP - counterparty to the trade.
NumberOfParticipations,Number of RFQ requests participated in
NumberOfWins,Number of RFQ requests won
ExpectedWins,NumberOfParticipations * ExpectedWinRatio
ActualWinRatio,(NumberOfWins%NumberOfParticipations)*100
ExpectedWinRatio,(ExpectedWins %NumberOfParticipations)*100
VolumeParticipated,Volume of the RFQ requests participated in
VolumeWon,Volume  of RFQ requests won
ExpectedWinVolume,ExpectedWinRatio * TradeQuantityUSD
ActualVolumeWinRatio,(VolumeWon%VolumeParticipated)*100
ExpectedVolumeWinRatio,(ExpectedWinVolume % VolumeParticipated)*100
AverageRFQPanelSize,The average size of the pannel of LPs
WinPerformanceScore,ActualWinRatio - ExpectedWinRatio
VolumePerformanceScore,ActualVolumeWinRatio - ExpectedVolumeWinRatio
```