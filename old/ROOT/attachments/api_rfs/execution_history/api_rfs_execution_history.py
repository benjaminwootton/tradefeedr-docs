## tradefeedr library
from tradefeedr_public_content.v1.generic.tradefeedr_api import TradefeedrApi  

## need pandas to translate JSON results from API
import pandas as pd 

## create API object 
tf_api_object = TradefeedrApi(demo=False)

## options
options =  {
    "select":['TradeTime',
              'OrderStatus',
              "TradeQuantityUSD", 
              'Symbol',
              'Side',
              'Price',
              'SpreadPnL',
              'DecayNeg10s',
              'DecayPMNeg10s',
              'Mid0',
              'Decay30s',
              'DecayPM30s'
             ],
    "filter":[
        {"function":"eq","var":"Date","par":"2017-02-02"},
    ]
}

# this is api end-point which returns execution history 
endpoint  =  "v1/fx/rfs/execution-history"

## call the API 
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response['result'])

## translate TradeTime to human readable time
data_frame["TradeTime"] = pd.to_datetime(data_frame["TradeTime"], unit="ms")
data_frame