# RFS (Request for Stream) API 

## APIs Summary 

The set of Tradefeedr RFS  APIs allows you to perform any task from calculating top level trading performance summary table to investigating the quality of individual child fills. 

Refer to [RFS Analytics](../analytics/rfs.md) page for field definitions.

The set of RFS API endpoints:

1. [Summary Stats - v1/fx/rfs/summary-stats](api-rfs/api-rfs-summary-stats.md)
  - This endpoint produces an execution summary report containing flow quality metrics such as trading volume, spread paid, rejection costs and market impact (flow toxicity)
2. [Execution Stats - v1/fx/rfs/execution-stats](api-rfs/api-rfs-execution-stats.md)
  - This endpoint is designed to study general execution quality of the trades and their associated market impact
3. [Execution History - v1/fx/rfs/execution-history](api-rfs/api-rfs-execution-history.md)
  - This endpoint is used to study all trades on a given date
4. [Markouts - v1/fx/rfs/markouts](api-rfs/api-rfs-markouts.md)
  - This endpoint is used to study the markout curves

## API Default Aggregation 

For convenience and speed of use Tradefeedr API allows to specify column name **without** having to specify aggregation function in an API call. In this case default aggregation function is selected automatically depending on the column name. This ensures sensible default behaviour. The logic is as follows:

- USD denominated variables like `TradeQuantityUSD` can be aggregated across regardless the group by operator. They can aggregated as `sum`.

- Dimension-less variable like `*PM` (per-million measures). They are aggregated as weighted average using `TradeQuantityUSD` as weights

- Symbolic variables (like `LP`  or `Symbol`) do not have sensible default aggregation. For example, it is not clear how to aggregate strings like "EURUSD" and "USDJPY".  Therefore, by default if you select `ExecVenue` in `groupby` and `Symbol` as column then `None` is returned.  However, if the `groupby` variables include globally unique values like `TradeID` then default aggregation is this value.

- Price information does not have sensible default aggregation  (summing or averaging EURUSD and USDJPY prices generally does not make sense) so `Price` and `Mid0` column returns `None`. This is unless `groupby` contains `TradeID` or `Symbol` and `Side` together.

- Other variables such as `LatencyMillis` does not have a default aggregation. You have to specify the aggregation logic.