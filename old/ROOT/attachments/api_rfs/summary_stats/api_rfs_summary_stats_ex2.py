## tradefeedr library
from tradefeedr_public_content.v1.generic.tradefeedr_api import TradefeedrApi  

## need pandas to translate JSON results from API
import pandas as pd 

## create API object 
tf_api_object = TradefeedrApi(demo=False)

## options
options = {
      "groupby":[
          "Symbol",
      ],
      "filter":[
        {"function": "within", "var": "Date", "pars": ["2017-01-01", "2017-12-31"]},
        {"function": "not_in", "var": "Symbol", "pars": ["EURUSD","USDJPY","GBPUSD"]},
      ]
}

# this is api end-point which returns summary stats
endpoint  = "v1/fx/rfs/summary-stats"

## call the API 
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response['result'])
data_frame