## tradefeedr library
from tradefeedr_public_content.v1.generic.tradefeedr_api import TradefeedrApi

## need pandas to translate JSON results from API
import pandas as pd

## create API object
tf_api_object = TradefeedrApi(demo=True)

## options
options = {
      "filter": [
          {"function": "eq", "var": "ParentOrderID", "par": "lim_20180904-A00"}
      ]
}

# this is api end-point which returns parent order stats one algo run per row
endpoint = "v1/fx/algo/pnl-history"

## call the API
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response["result"])

## translate Time to human readable time
df["Time"] = pd.to_datetime(df["Time"], unit="ms" if str(df["Time"].dtype) == "int64" else None)
#data_frame = data_frame.set_index("Time")
data_frame