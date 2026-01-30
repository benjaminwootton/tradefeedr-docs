## tradefeedr library
from tradefeedr_public_content.v1.generic.tradefeedr_api import TradefeedrApi  

## need pandas to translate JSON results from API
import pandas as pd 

## create API object 
tf_api_object = TradefeedrApi(demo=False)

## options
options =  {
    "groupby": [
        "LP",
        "Symbol"
    ],
    "select":[
        "LP",
        "NumberOfParticipations",
        "NumberOfWins",
        "ActualWinRatio",
        "ExpectedWinRatio",
        "VolumeParticipated",
        "VolumeWon",
        "ExpectedWinVolume",
        "ActualVolumeWinRatio",
        "ExpectedVolumeWinRatio",
        "AverageRFQPanelSize",
        "WinPerformanceScore",
        "VolumePerformanceScore",  
    ],
    "filter":[
        {"function":"within","var":"date","pars":["2014-01-01","2021-11-30"]},
        {"function":"like","var":"Symbol","pars":"USD*"}
    ],
}

# this is api end-point which returns RFQ outrights participation report
endpoint  =  "v1/fx/rfq-outrights/participation-report"

## call the API 
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response['result'])
data_frame