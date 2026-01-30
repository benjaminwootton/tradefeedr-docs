## tradefeedr library
from tradefeedr_public_content.v1.generic.tradefeedr_api import TradefeedrApi

## need pandas to translate JSON results from API
import pandas as pd

## create API object
tf_api_object = TradefeedrApi(demo=True)

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
        "AverageRFQPanelSize",
        "WinPerformanceScore",
    ],
    "filter":[
        {"function":"lt","var":"WinPerformanceScore","par": 0},
    ],
}

# this is api end-point which returns RFQ outrights participation report
endpoint =  "v1/fx/rfq-outrights/participation-report"

## call the API
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response["result"])
# data_frame = data_frame.set_index("LP")
data_frame