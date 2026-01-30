## tradefeedr library
from tradefeedr_public_content.v1.generic.tradefeedr_api import TradefeedrApi  

## need pandas to translate JSON results from API
import pandas as pd 

## create API object 
tf_api_object = TradefeedrApi(demo=False)

## options
options =  {
    "filter":[
        {"function":"within","var":"date","pars":["2014-01-01","2021-11-30"]}, 
        {"function":"in","var":"LP","pars":["LP_1"]}
    ]
}

# this is api end-point which returns RFQ outrights opportunity report
endpoint  =  "v1/fx/rfq-outrights/opportunity-report"

## call the API 
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response['result'])

## translate TradeTime to human readable time
data_frame["TradeTime"] = pd.to_datetime(data_frame["TradeTime"], unit="ms")
data_frame