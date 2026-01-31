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