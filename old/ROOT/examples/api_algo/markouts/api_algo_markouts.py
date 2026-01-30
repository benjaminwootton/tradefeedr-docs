## tradefeedr library
from tradefeedr_public_content.v1.generic.tradefeedr_api import TradefeedrApi

## need pandas to translate JSON results from API
import pandas as pd

## create API object
tf_api_object = TradefeedrApi(demo=True)

## options
options = {
    "groupby": ["ParentOrderID"],
    "filter": [
        {"function": "like", "var": "ParentChild", "par": "Child"},
        {"function": "like", "var": "ParentOrderID", "par": "20180921-A00"},
    ],
}

# this is api end-point which returns markouts
endpoint = "v1/fx/algo/markouts"

## call the API
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response["result"])
# data_frame = data_frame.set_index("ParentOrderID")
data_frame