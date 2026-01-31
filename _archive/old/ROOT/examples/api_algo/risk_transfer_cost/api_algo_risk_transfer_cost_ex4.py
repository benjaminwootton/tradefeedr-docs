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