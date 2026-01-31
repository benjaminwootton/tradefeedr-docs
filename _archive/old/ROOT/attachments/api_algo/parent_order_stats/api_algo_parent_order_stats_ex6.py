## tradefeedr library
from tradefeedr_public_content.v1.generic.tradefeedr_api import TradefeedrApi  

## need pandas to translate JSON results from API
import pandas as pd 

## create API object 
tf_api_object = TradefeedrApi(demo=False)

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
data_frame = pd.DataFrame(response['result'])
data_frame