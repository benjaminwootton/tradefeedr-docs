import pandas as pd 
tf_api_object = TradefeedrApi(demo=False)
options =  {
    "filter":[
    ]
}

# this is api end-point which returns RFQ swaps opportunity report
endpoint  =  "v1/fx/rfq-swaps/participation-report"

## call the API 
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response['result'])

## translate TradeTime to human readable time
data_frame["TradeTime"] = pd.to_datetime(data_frame["TradeTime"], unit="ms")
data_frame