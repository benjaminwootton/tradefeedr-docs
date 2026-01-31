## tradefeedr library
from tradefeedr_public_content.v1.generic.tradefeedr_api import TradefeedrApi  

## need pandas to translate JSON results from API
import pandas as pd 

## create API object 
tf_api_object = TradefeedrApi(demo=False)

## options
options = {
    
    'select': ['ParentOrderID', 'ArrivalTime', 'Symbol', 'Side', 'AllInPrice', 'TWAPMidPerfBPS'],
    'filter': [
        {'function':'within', 'var':'Date', 'par': ['2017-01-01', '2022-01-01']}
    ]
}

# this is api end-point which returns parent order stats one algo run per row  
endpoint  = "v1/fx/algo/parent-orders"

## call the API 
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response['result'])

## translate ArrivalTime to human readable time
data_frame['ArrivalTime'] = pd.to_datetime(data_frame['ArrivalTime'], unit='ms')
data_frame