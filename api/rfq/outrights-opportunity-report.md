# Outrights Opportunity Report

## Introduction
The `v1/fx/rfq-outrights/opportunity-report` endpoint  generates an opportunity report which displays the `OutCome` of the outrights RFQ if it was `WON` or `Lost`.
From this piece of information you can review pricing to see why the `LP` `LOST` or `WON` the RFQ. 

You can compare the price they were quoted for the outrights RFQ the `AllInRate` against the `PriceShown` (price that won the RFQ). 
To see how far the price was off the winning quote (`MissedByPIPS` column). They can also review the volume of the `LOST` trades that where traded away with another `LP`.

## API Specification

The API endpoint requires a JSON object representing query logic similar to SQL and containing the following fields:

- `select`  - which fields should be returned in the end result. For example  `AllInRate`.
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
        {"function":"within","var":"date","pars":["2014-01-01","2021-11-30"]},
        {"function":"in","var":"LP","pars":["LP_1"]}
    ]
}

# this is api end-point which returns RFQ outrights opportunity report
endpoint =  "v1/fx/rfq-outrights/opportunity-report"

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

![api_rfq_outrights_opportunity_report_ex1.png](assets/images/api_rfq/outrights/opportunity_report/api_rfq_outrights_opportunity_report_ex1.png)

#### Figure

```python
```
# import plotly libary
import plotly.express as px

# Modify dataframe
data_frame = data_frame[data_frame.Symbol=="AUDUSD"]

# Plot figure
fig= px.scatter(data_frame, x="TradeTime", y=["PriceShown"], color="OutCome",
                title="Scatter plot of AUDUSD PriceShown by OutCome")
fig.show()
```
```
### Selecting All `LP` s for a Date Range

In this example we generate a opportunity report selecting all the `LP` s using a wildcard search.

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
        "OutCome",
       # "Symbol",
        "TradeCcy",
        "Side",
        "TradeTime",
        "ProductType",
        "PriceShown",
        "MissedByPIPS"
    ],
    "filter":[
        {"function":"within","var":"date","pars":["2014-01-01","2021-11-30"]},
        {"function":"like","var":"LP","par": "LP*"},
        {"function":"like","var":"Symbol","par": "USD*"},
    ],
}

# this is api end-point which returns RFQ outrights opportunity report
endpoint =  "v1/fx/rfq-outrights/opportunity-report"

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

![api_rfq_outrights_opportunity_report_ex2.png](assets/images/api_rfq/outrights/opportunity_report/api_rfq_outrights_opportunity_report_ex2.png)

### Select Losing RFQs only

Below we have filtered the `OutCome` column to select only the cases where the RFQ was `LOST`. 
You can review these cases to see how far off the price was from the winning quote.

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
        "OutCome",
        #"Symbol",
        "TradeCcy",
        "Side",
        "TradeTime",
        "ProductType",
        "PriceShown",
        "MissedByPIPS"
    ],
    "filter":[
        {"function":"within","var":"date","pars":["2014-01-01","2021-11-30"]},
        {"function":"like","var":"LP","par": "LP*"},
        {"function":"eq","var":"OutCome","par":"LOST"},
    ],
}

# this is api end-point which returns RFQ outrights opportunity report
endpoint =  "v1/fx/rfq-outrights/opportunity-report"

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

![api_rfq_outrights_opportunity_report_ex3.png](assets/images/api_rfq/outrights/opportunity_report/api_rfq_outrights_opportunity_report_ex3.png)

#### Figure

```python
```
# import plotly libary
import plotly.express as px

# Modify dataframe
data_frame = data_frame[data_frame.TradeCcy=="AUD"].head(50)

# Plot figure
fig = px.scatter(data_frame, x="TradeTime" , y="MissedByPIPS", title="Selecting Losing RFQs only (TradeCcy:AUD)")
fig.show()
```
```
## Field Definitions

[%header,format=csv, cols=["60%", "40%"]]

```csv
Name,Description
LP,Executing LP - counterparty to the trade.
OutCome,If the trade was WON or LOST.
Symbol,Currency pair. For example EURUSD.
Side,"Trade side. ""B” for buy and ""S” for sell."
TradeQuantity,Traded quantity expressed in TradeCurrency
TradeCcy,"Denomination Currency for TradeQuantity and OrderQuantity. For example
    EUR."
TradeTime,TradeTime - Time (GMT) when the trade was filled
AllInRate,Price quoted for the trade
PriceShown,Price the trade traded at
ProductType,Type of product traded. For example SPOT
MissedByPIPS,The difference between the AllInRate and the PriceShown expressed in pips
MissedByUSDPM,The difference between the AllInRate and the PriceShown expressed in USD per Mil
```