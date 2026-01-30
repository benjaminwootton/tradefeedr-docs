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