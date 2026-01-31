## tradefeedr library
from tradefeedr_public_content.v1.generic.tradefeedr_api import TradefeedrApi  

## need pandas to translate JSON results from API
import pandas as pd 

## create API object 
tf_api_object = TradefeedrApi(demo=False)

## options
options = {
    # "select" clause omitted
    "filter": [
        {"function": "within", "var": "Date", "pars": ["2014-01-01", "2025-12-31"]}
    ],
}

# this is api end-point which returns parent order stats one algo run per row  
endpoint = "v1/fx/algo/parent-orders"

## call the API 
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response['result'])
data_frame
