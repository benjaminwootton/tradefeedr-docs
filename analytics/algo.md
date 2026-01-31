# Algo Analytics

## Introduction

Algo is defined as a combination of one or several Parent instructions and child orders.

Parent instructions are conveyed from algo user to algo provider and include initial instruction (e.g. buy 100m EURUSD using Algo1 with Limit Price 1.20) and subsequent instructions
(e.g. amend LimitPrice, amend OrderQuantity, amend Algo Urgency etc). Child orders are executed by algo provider as part of execution.

The absolute minimum for meaningful analysis is to have Parent instruction and child fills. Depending on the algo provider other child events such as order placements and rejects can be analysed as well.

### Figure

Typical algo life cycle is depicted below:

![Algo Life Cycle](assets/images/algo_life_cycle.svg)

## Parent Order Stats

Parent level performance statistics attaches one number to each algo run.
In the below metric descriptions **PM** stands for _Per Million_ and **BPS** stands for _Basis Point_.
Tradefeedr variables are sufficed with either `PM` or `BBP` to highlight their unit of measure.

_Performance_ vs _Slippage_ is simply a terminology preference.

For _Slippage_, positive is bad and negative is good; For _Performance_ it is vice versa.

Tradefeedr API support both notations as some organizations have strict preferences.

### SlippageToArrivalMidTrade

`SlippageToArrivalMidTrade` is a percentage difference between `ArrivalPrice` and Algo `AllInExecutionPrice`.

The formal definition as per below:

[latexmath]

`AllInExecutionPrice` is simply the size-weighted execution prices of child orders.
For example if Tradefeedr market mid was `1.20` at the order arrival time and `AllInExecutionPrice` is `1.205`, then the Slippage will be:

[latexmath]

The performance metric, `SlippageToArrivalMidTrade`, terminology is "slippage" rather than "performance".
Thus, the positive number resulting from the example above means an **underperformance** with respect to mid-price, i.e. buying above the `ArrivalPrice` and selling below it.

===	SlippageToArrivalMidRemain

If the order is not fully filled but is stopped for some reason, the remaining part has to be executed at
market price prevailing at the time the order was stopped. To adjust the performance metric for
unexecuted quantity, `SlippageToArrivalMidRemain` is applied. It is the difference between the mid prices prevailing at the beginning and at the end of algo execution:

[latexmath]

For example, if the `LastMidPrice` is `1.21` and `ArrivalMidPrice` is `1.20`. Assuming a buy order, the `SlippageToArrivalMidRemain` is calculated as:

[latexmath]

### SlippageToArrivalMid

For algo executions which are fully filled it is simply equal to `SlippageToArrivalMidTrade` as the `RemainQuantity` is zero.

The formal definition is per below:

[latexmath]

For example, if we combine the above two examples for `SlippageToArrivalMidRemain` and `SlippageToArrivalMidTrade` and set the `RemainQuantity` to `OrderQuantity` ratio to be 10% we have:

[latexmath]

This metric is also commonly referred to as **Implementation Shortfall** and one of the oldest metrics for algo execution.

### ArrivalMidPerfTrade

`ArrivalMidPerfTradeBPS` is a basis point difference between `ArrivalPrice` and Algo `AllInExecutionPrice`. The formal definition as per below:

[latexmath]

`AllInExecutionPrice` is the size-weighted execution prices of child orders.
For example, if Tradefeedr market mid was `1.20` at the order arrival time and `AllInExecutionPrice` is `1.205`, then the Performance will be:

[latexmath]

The metric `AllInExecutionPrice` terminology is "performance". Thus, the negative number resulting from the example above means an underperformance with respect to mid-price (e.g. buying above the `ArrivalPrice` and selling below it).

It is clear that there is a negative relationship with the `SlippageToArrivalMidTrade` metric, with a conversion between "BPS" and "PM":

[latexmath]

The reason to report both metrics is that in some scenario "performance" is used and sometimes "slippage" is more appropriate.

###  ArrivalMidPerfRemain

If the order is not fully filled but is stopped for some reason, the remaining part has to be executed at market price prevailing at the time the order was stopped. To adjust the performance metric for the non-executed quantity `ArrivalMidPerfRemain` is applied.

It is the difference between the mid prices prevailing in the beginning and end of algo execution respectively:

[latexmath]

For example, if you have been buying and the market has been going up, the `LastMidPrice` will be above the `ArrivalMidPrice` and naturally the performance will be negative.

It only matters if there is a non-executed amount left after the algo is completed - e.g. user cancelled before the ordered amount was filled.

An example of the above equation. If the `LastMidPrice` is `1.21` and `ArrivalMidPrice` is `1.20` and it is a buy, order the `ArrivalMidPerfRemain` is:

[latexmath]

There is an negative relationship with the `SlippageToArrivalMidRemain` metric, with a conversion between "BPS" and "PM":

[latexmath]

### ArrivalMidPerf

`ArrivalMidPerf` is aggregated performance, a weighted average of `ArrivalMidPerfTrade` and `ArrivalMidPerfRemain`.
For algo executions which are fully filled the metrics is equal to `ArrivalMidPerfTrade`.

The formal definition is per below:

[latexmath]

For example, if we combine the above two examples for `ArrivalMidPerfRemain` and `ArrivalMidPerfTrade` and set the `RemainQuantity` to `OrderQuantity` ratio to be `10%` we have:

[latexmath]

This metric is the **negative** of the commonly used **Implementation Shortfall** which is of the oldest metrics for algo execution.

[latexmath]

### Execution Score

Each algo child fill is ranked from 0 to 100 against the full tick history during algo execution (mid prices only).
Therefore, the `ExecutionScore` of each child fill is simply a Rank Percentile of the execution price against the tick history of mid prices during algo execution period.

For instance, buying at the very low of price range would get a rank of 100 and buying at the very high of the price range would get a rank of 0.
It is reverse for sell order. A rank of, e.g. 60, means than 60% of tick prices during the run are worse (higher for buy order, lower for sell order) than the current execution price.

The individual Execution Score are aggregated to obtain Parent Level Execution Score the whole algo.
The Execution Score is simply Trade-Size-Weighted-Average of the Scores of Individual Child Orders.

### Reversal Score

Each child fills has a `ReversalScore` which is calculated in the same way as the Execution Score but using mid prices distribution after the execution (we typically take half algo duration for reversal period). The logic is to see whether there was an opportunity to deal at better price _post_ algo execution.

#### Figures

The figures below illustrate the different scenarios for Execution And Reversal Scores.

![Algo Life Cycle](assets/images/algo_ex_reversal_score.png)

### SlippageToTWAPMid(PM)

`SlippageToTWAPMid` is the difference between Algo Execution Price and TWAP Price.

Positive number means that the algo is underperforming with respect to a TWAP (e.g. buying at the price above TWAP price or selling below it). This metric is in "slippage" terminology.

The formal definition is per below:

[latexmath]

### SlippageToRiskTransferPrice(PM)

This is the difference between Algo Execution Price and Risk Transfer Benchmark. Risk Transfer price is the benchmark which approximate the costs of executing the same algo order immediately (hence Risk Transfer).

Positive number mean the algo is underperforming Risk Transfer price (e.g. buying above the Risk Transfer Benchmark or selling below it). This metric is in "slippage" terminology.

The formal definition is per below:

[latexmath]

### RiskTransferPricePerfBPS

This is the difference between Algo Execution Price and Risk Transfer Benchmark. Risk Transfer price is the benchmark which approximate the costs of executing the same algo order immediately (hence Risk Transfer).

Positive number mean the algo is outperforming Risk Transfer price (e.g. buying below the Risk Transfer Benchmark and selling above it). This metric is in "performance" terminology.

The formal definition is per below:

[latexmath]

### RiskTransferPrice – Saving USD

Algo trading performance can be evaluated against the alternative of executing immediately. Immediate execution benchmark is the Risk Transfer Price.
USD saving is simply the out-performance over the multiplied by Trading Volume.

It is defined as:

[latexmath]

This number can be negative if algo underperforms against the benchmark. It can also be expressed in thousands of USD if appropriate.

### Assumed Risk

`Assumed risk` is the volatility risk taken by the algo. Tradefeedr constructs minute by minute volatility model for each currency pair and each day.
This volatility is used to estimate the risk of algo.

The formal definition of assumed risk is as per below:

[latexmath]

### SpreadPaidChildOrders

This is `TradeQuantityUSD`-weighted average of Spread Paid of all algo child fills.
The Spread Paid per each child is defined below in Child Order Metrics sections. Note that this is a unit-less measure which does not depend on the algo size. It is expressed in **$/m**.

To calculate the total spread paid per algo in USD, this number should be multiplied by `TradeQuantityUSD`.

###  SpreadPaidChildOrders BPS

This is the TradeQuantityUSD-weighted average of Spread Paid of all algo child fills.

The Spread Paid per each child is defined below in Child Order Metrics sections. Note this is a unit-less measure which does not depend on the algo size. It can be expressed in **$/m** or in **BPS**.

To calculate the total spread paid per algo in USD, this number should be multiplied by `TradeQuantityUSD`.

## Child Order Metrics

Child order metrics apply to each individual child event. The most commonly used child event is child fill but most of the analysis can be applied to rejects and order submission.

### Spread Paid (PM)

`Spread Paid` on each child execution is simply the difference between price paid and the mid-price prevailing the time of the execution.

The formal definition is as per below:

[latexmath]

The number can also be expressed in BPS:

[latexmath]

To illustrate the equations above, if the market mid is 1.20 and we buy at 1.2001 using the formula above we calculate spread paid to be equal to:

[latexmath]

[latexmath]

Note that this is unit-less measure (USD per million USD traded). To calculate total USD value of spread
paid we need to multiply it by `TradeQuantityUSD` (also available via Tradefeedr API) and adjusted by either
latexmath:[10^6](for $/m) or latexmath:[10^4] (for BPS measure).

### Markouts curve (Market Impact of Child Fills)

Markout is the change in mid-price before or after the trade execution. It can be defined as direct markout which only approximates market impact of child event.

The formal definition is below:

[latexmath]

The latexmath:[mid_{0}] is the mid-price at the time of the event (typically trade) and latexmath:[mid_{t}]is the mid-price at some time t.
Note at time `t=0` markout is exactly zero as there has been no change in the mid-price.
Markout can also be calculated from the initial spread paid (as opposed to from zero); it then represents the P&L of the counterparty to the trade.

The formal definition is as per below:

[latexmath]

### Execution and Reversal Scores

Described in the Parent Order Stats section of this document and this is also available for each child order.