## tradefeedr library
from tradefeedr_public_content.v1.generic.tradefeedr_api import TradefeedrApi  

## need pandas to translate JSON results from API
import pandas as pd 

## create API object 
tf_api_object = TradefeedrApi(demo=False)

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
data_frame = pd.DataFrame(response['result'])

## translate ArrivalTime to human readable time
data_frame["ArrivalTime"] = pd.to_datetime(data_frame["ArrivalTime"], unit="ms")
data_frame = data_frame.sort_values(by=ArrivalTime", ascending=False)
data_frame