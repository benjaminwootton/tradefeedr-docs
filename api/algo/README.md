# Algo API 

## APIs Summary 

The set of Tradefeedr Algo APIs allows you to perform any task from calculating top level algo performance summary table to investigating the quality of individual child fills. 

Refer to [Algo Analytics](../analytics/algo.md) page for field definitions.

The set of Algo API endpoints:

1. [Parent Order - v1/fx/algo/parent-orders](algo/parent-orders.md)
  - This endpoint can be used to create a algo trading blotter, it returns a table of algo execution information
2. [Parent Order Stats- v1/fx/algo/parent-order-stats](algo/parent-order-stats.md)
  - This endpoint provides parent level performance statistics
3. [PnL History- v1/fx/algo/pnl-history](algo/pnl-history.md)
  - This endpoint provides the dynamics of the tick-by-tick algo P&L. The P&L is split into AlgoVendor (Bank) P&L and algo user
4. [Event History- v1/fx/algo/event-history](algo/event-history.md)
  - This endpoint allows you to query all trading events for a given ParentOrderID
5. [Market Data- v1/fx/algo/market-data](algo/market-data.md)
  - This endpoint returns all relevant market data around an algo run - specified by ParentOrderID
6. [Markouts- v1/fx/algo/markouts](algo/markouts.md)
  - This endpoint is used to study the markout curves
7. [Execution Stats- v1/fx/algo/execution-stats](algo/execution-stats.md)
  - This endpoint is designed to study general algo execution patterns, anything from child fill quality and market impact of individual child fills to user specific events
8. [Risk Transfer Cost v1/fx/stats/risk-transfer-cost](api-algo/api-stats-risk-transfer-cost.md)
  - This is endpoint is used when you want to estimate the RFQ cost to execute full amount immediately

## API Default Aggregation 

For convenience and speed of use Tradefeedr API allows to specify column name **without** having to specify aggregation function in an API call.
In this case default aggregation function is selected automatically depending on the column name. 
This ensures sensible default behaviour. 
 
All results returned by API endpont are aggregated across individual algo runs and the logic is as follows:

- USD denominated variables like `TradeQuantityUSD` and `OrderQuantityUSD` and `TradeQuantityUSD` can be aggregated across regardless the group by operator. They can aggregated as `sum`.

- Variables that start with `Num` for example `NumRuns` are aggregated using the `count` function.

- Variables with `StdDev` in the end represent weighted standard deviation of their respective performance metric with the weights being `TradeQuantityUSD`.

- Risk-adjusted performance metrics (ending with `IR` for Information Ratio) are simply the ratio of relevant performance metric and its standard deviation.

- Weighted average for all performance metrics.

**Note:** Use only the field names defined for the `select` likewise for the `groupby` and `filter` options. Otherwise no output will be returned.