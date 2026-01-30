---
description: >-
  An overview of the functionality of the Tradefeedr API itself. For details on
  individual endpoints, refer to the specific quickstart guides (e.g. Algo / RFS
  / RFQ / Pre-Trade).
icon: hand-wave
metaLinks: {}
---

# Tradefeedr API Quickstart

The Tradefeedr API is a REST interface that receives a JSON payload and returns a JSON response.

Endpoints have a nested structure, taking the form `${api-version}/${asset-class}/${category}/${function}`. For example `v1/fx/algo/parent-orders` can be broken down as:

* `v1` - API version 1
* `fx` - Foreign Exchange (FX)
* `algo` - Algorithmic Execution
* `parent-orders` - Parent Orders (the specific function/resource being accessed)

The JSON Payload is a dictionary where the keys (e.g. `select`, `groupby`, `filter`) are arguments to the API function being run.

The JSON Response is a dictionary, the `result` key is a list of fields & rows of data which can be trivially parsed into a table (e.g. Pandas DataFrame).

### JSON Payload

#### Simple parameters

The `select`, `groupby` and `domain` options use simple string parameters - the names of the fields themselves, e.g. `"Date"`.

#### Advanced parameters

In addition to simple strings, the API supports more complex values taking a dictionary with keys:

* `name` - (re)name the field
* `var` - var(iable), the column being selected
* `func` - the func(tion) you wish to apply
* `par` - par(ameters) to pass to the function

For example, to filter for all trades within the period 2025-01-01 and 2025-02-28 you can use the following `filter` clause:

```json
{
    "filter": [
        {
            "var": "Date",
            "func": "within",
            "par": [
                "2025-01-01",
                "2025-02-28",
            ]
        }
    ]
}
```

#### Select

The fields you wish to select from the API, e.g. to select `Date`, `ParentOrderID` and `TradeQuantityUSD` fields:

```json
{
    "select": [
        "Date",
        "ParentOrderID",
        "TradeQuantityUSD",
    ]
}
```

#### Filter

The clauses you wish to apply

#### Groupby

When querying the API, you may wish to aggregate the results by a particular field, e.g. "select sum TradeQuantityUSD by Trader". The API allows for this behaviour using the `groupby` parameter.

```json
{
    "select": [
        {
            "var": "TradeQuantityUSD",
            "func": "sum",
        }
    ],
    "groupby": [
        "Trader",
    ]
}
```

#### Domain

The `domain` parameter is used to return the range of distinct values for a given field, e.g. if you want to get the list of Traders, Symbols and LPs for a given date range you can use the `domain` functionality.

**NOTE:** For numeric values (e.g. `TradeQuantityUSD`) the API returns the min and max values.

```json
{
    "domain": [
        "Trader",
        "Symbol",
        "LP",
    ],
    "filter": [
        {
            "var": "Date",
            "func": "within",
            "par": [
                "2025-01-01",
                "2025-02-28",
            ]
        }
    ]
}
```

#### Advanced

**Available Functions**

| function           | description                                             |
| ------------------ | ------------------------------------------------------- |
| min                | calculate the minimum value of the column               |
| max                | calculate the maximum value of the column               |
| avg                | calculate the mean value of the column                  |
| sum                | calculate the total value of the column                 |
| dev                | calculate the standard deviation of the column          |
| count              | count the length of the column                          |
| first              | take the first value of the column                      |
| last               | take the last value of the column                       |
| percentile         |                                                         |
| plus               |                                                         |
| minus              |                                                         |
| multiply           |                                                         |
| divide             |                                                         |
| wavg               | calculate the weighted average of the column            |
| wdev               | calculate the weighted standard deviation of the column |
| wdev\_reagg        |                                                         |
| gt\_percentile     |                                                         |
| gte\_percentile    |                                                         |
| lt\_percentile     |                                                         |
| lte\_percentile    |                                                         |
| within\_percentile |                                                         |
| eq                 | column value is equal to parameter                      |
| not\_eq            | column value is not equal to parameter                  |
| eqx                |                                                         |
| in                 | value is in parameter list                              |
| not\_in            | value is not in parameter list                          |
| like               | value is (wildcard) like parameter string               |
| bar                |                                                         |
| bucket             |                                                         |
| diff\_nanos        |                                                         |
| diff\_millis       |                                                         |
| hist\_label        |                                                         |
| hist\_range        |                                                         |
| hist\_mid          |                                                         |
| hist\_index        |                                                         |
| hist               |                                                         |
| is\_number         | value is numerical                                      |
| not\_number        | value is not numerical                                  |

**Transforms**

Fields can also be "transformed" as part of the API query

| transform         | description                        |
| ----------------- | ---------------------------------- |
| month             | truncate date to month             |
| date              | converte/truncate datetime to date |
| minute            | convert to number of minutes       |
| second            | convert to number of seconds       |
| time              | convert to time                    |
| abs               | take absolute value                |
| plus              | add parameter to value             |
| minute            | subtract parameter from value      |
| multiply          | multiply value by parameter        |
| divide            | divide value by parameter          |
| x1e6              | multiply by 1e6                    |
| y1e6              | divide by 1e6                      |
| wavg              | weighted average                   |
| wdev              | weighted standard deviation        |
| wdev\_reagg       |                                    |
| diff\_nanos       |                                    |
| diff\_millis      |                                    |
| date\_london      | convert to London timezone         |
| minute\_london    | convert to London timezone         |
| second\_london    | convert to London timezone         |
| date\_new\_york   | convert to NY timezone             |
| minute\_new\_york | convert to NY timezone             |
| second\_new\_york | convert to NY timezone             |
| date\_trading     |                                    |
| minute\_trading   |                                    |
| second\_trading   |                                    |
| rank\_percentile  |                                    |
| stack\_spread     | calculate spread stack (RFQ/RFS)   |

### JSON Response

The JSON response is a dictionary containing some metadata along with the result itself.

An example response is shown below:

```json
{
    "result": {},
    "status": 200,
    "message": "OK",
    "time_request": "2025-04-04T12:34:56:789000000",
    "time_response": "2025-04-04T12:34:57:789000000"
    "meta": {},
    "error": None,
}
```

The "result" key contains the response data. In real API responses this will be a dictionary containing rows of table data that can be converted into a Pandas DataFrame using the `pandas.DataFrame` constructor.

### Calling the API

#### Within the platform

The platform has some helper code to make it easy to query the API. Example code is shown below:

```python
from tradefeedr_public_content.v1.generic.tradefeedr_api import TradefeedrApi
import pandas as pd

tradefeedr_api = TradefeedrApi(demo=True)

endpoint  = "v1/fx/algo/parent-orders"
options = {
    "domain": ["Symbol", "LP"], 
    "filter": [
        {"function": "within", "var": "Date", "pars": ["2025-01-01", "2025-12-31"]},
    ],
}

response = tradefeedr_api.query_api(endpoint, options)
df = pd.DataFrame(response["result"])
df
```

#### Outside of the platform

This is an example of using the Python requests library to query the API from outside of the platform, note that you will need to provide the API\_TOKEN yourself.

```python
import requests
import pandas as pd

token = "__API_TOKEN__"

endpoint = "v1/fx/algo/parent-orders"
options = {
    "domain": ["Symbol", "LP"], 
    "filter": [
        {"function": "within", "var": "Date", "pars": ["2025-01-01", "2025-12-31"]},
    ]
}

headers = dict(authentication=f"Bearer {token}")

resp = requests.post(
    f"https://api.tradefeedr.com/client/{endpoint}",
    json=dict(options=options),
    headers=headers,
)

if resp.status_code == 200:
    result = resp.json()
    df = pd.DataFrame(result["result"])
else:
    print(result.content)
```
