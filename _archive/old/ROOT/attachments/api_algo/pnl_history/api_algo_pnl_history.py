## tradefeedr library
from tradefeedr_public_content.v1.generic.tradefeedr_api import TradefeedrApi  

## need pandas to translate JSON results from API
import pandas as pd 

## create API object 
tf_api_object = TradefeedrApi(demo=False)

## options
options = {
      "filter": [
          {"function": "eq", "var": "ParentOrderID", "par": "20180921-A07"}
      ]
}

# this is api end-point which returns parent order stats one algo run per row  
endpoint = "v1/fx/algo/pnl-history"

## call the API 
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response['result'])

## translate Time to human readable time
data_frame.Time = pd.to_datetime(data_frame.Time, unit="ms")
data_frame