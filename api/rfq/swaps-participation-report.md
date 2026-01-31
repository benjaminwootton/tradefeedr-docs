# Swaps Participation Report- `v1/fx/rfq-swaps/participation-report`

## Introduction
The `v1/fx/rfq-swaps/participation-report` endpoint returns a table summarises the swaps RFQ participation rate by `LP`. 

This endpoint is used to study the hit ratios of the requested swaps RFQs, you can rank each `LP` against various performance ratios. 
Such as `ActualWinRatio`, `ActualVolumeWinRatio`, `WinPerformanceScore` etc. 

You have the ability to see the total requested RFQs (`NumberOfParticipations`),`NumberOfWins` also see how competitive the RFQ stack is. 
This done by looking at the `AverageRFQPanelSize` larger this number more `LP` s competing to price the swap RFQ. 

From this number the expected win rate is derived `ExpectedWinRatio`, higher the `AverageRFQPanelSize` smaller the `ExpectedWinRatio`, inversely proportional. 

## API Specification

The API endpoint requires a JSON object representing query logic similar to SQL and containing the following fields:

- `groupby` - which fields the results will be aggregated by
- `select`  - which fields should be returned in the end result. For example `NumberOfWins`
- `filter`  - how the underlying data should be filtered

**Note:**  The endpoint requires a `LP` `filter` to return a result.

## Example 
Please refer to [v1/fx/rfq-outrights/participation-report](api-rfq/api-rfq-outrights-participation-report.md) to see examples

## Field Definitions

Refer to [Analytics RFQ](../analytics/rfq.md) page for details and formula.

[%header,format=csv, cols=["60%", "40%"]]

```csv
Name,Description
LP,Executing LP - counterparty to the trade.
NumberOfParticipations,Number of RFQ requests participated in
NumberOfWins,Number of RFQ requests won
ExpectedWins,NumberOfParticipations * ExpectedWinRatio
ActualWinRatio,(NumberOfWins%NumberOfParticipations)*100
ExpectedWinRatio,(ExpectedWins %NumberOfParticipations)*100
VolumeParticipated,Volume of the RFQ requests participated in
VolumeWon,Volume  of RFQ requests won
ExpectedWinVolume,ExpectedWinRatio * TradeQuantityUSD
ActualVolumeWinRatio,(VolumeWon%VolumeParticipated)*100
ExpectedVolumeWinRatio,(ExpectedWinVolume % VolumeParticipated)*100
AverageRFQPanelSize,The average size of the pannel of LPs
WinPerformanceScore,ActualWinRatio - ExpectedWinRatio
VolumePerformanceScore,ActualVolumeWinRatio - ExpectedVolumeWinRatio
```