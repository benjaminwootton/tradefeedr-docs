## tradefeedr library
from tradefeedr_public_content.v1.generic.tradefeedr_api import TradefeedrApi

## need pandas to translate JSON results from API
import pandas as pd

## create API object
tf_api_object = TradefeedrApi(demo=True)

## options
options = {
      "groupby":[
          {"transform": "date_london", "var": "TradeTime", "name":"LondonDate"},
          {"transform": "date_new_york", "var": "TradeTime", "name":"NewYorkDate"}, ## this is just calendar in NY time 
          {"transform": "date_trading", "var": "TradeTime", "name":"TradeDate"},    ## this is 5pm to 5pm NY time, value date
          
          ##  This aggregates by minute, par controls how many minutes, par=30 mean every 30 minutes
          ##  for example from 09:00 to 09:30
          #  {"function": "bar", "transform": "minute_london", "var": "TradeTime", "par": 30}
          
          ##  This aggregates by seconds in london time, 
          #   or controls how many second, par=30 mean every 30 seconds
          ##  for example from 09:00:00 to 09:00:30
          #   {"function": "bar", "transform": "second_london", "var": "TradeTime", "par": 1}
          
        ],
    "select": [
        "TradeQuantityUSD",
        {"function": "count", "var": "Symbol", "name": "NumEvents"}
    ], 
    "filter":[
        {"function": "within", "var": "Date", "pars": ["2017-01-01", "2017-04-28"]},
    ],
}

# this is api end-point which returns execution stats
endpoint = "v1/fx/rfs/execution-stats"

## call the API
response = tf_api_object.query_api(endpoint, options)

## translate API result into pandas dataframe
data_frame = pd.DataFrame(response["result"])
# data_frame = data_frame.set_index("DecayPM1m")
data_frame