## tradefeedr library
from tradefeedr_public_content.v1.generic.tradefeedr_api import TradefeedrApi  

## need pandas to translate JSON results from API
import pandas as pd 

## create API object 
tf_api_object = TradefeedrApi(demo=False)

## options
options = {
    "filter": [
        {"function": "eq", "var": "CreatedFor", "par": ""},
        {"function": "in", "var": "LP", "pars": ["TRADEFEEDR","LP1masked"]},
        {"function": "within", "var": "Date", "par": ["2017-02-01", "2017-02-10"]}
    ]
}

# this is api end-point which returns bilateral market share
endpoint  =  "v1/fx/rfs/bilateral-market-share"

## call the API 
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response['result'])
data_frame