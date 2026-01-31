# RFQ API  

## APIs Summary 

The set of Tradefeedr RFQ APIs allow you to query all RFQ history provided by its liquidity providers or platforms. 
The API is split into `outrights` and `swaps`.

Refer to [RFQ Analytics](../analytics/rfs.md) page for field definitions.

The set of RFQ API endpoints:

1. [Outrights Execution History - v1/fx/rfq-outrights/execution-history](api-rfq/api-rfq-outrights-execution-history.md)
  - This endpoint is used query all trading events for outrights RFQ. It should be used when you require a detailed analysis and understanding of the execution
2. [Swaps Execution History - v1/fx/rfq-swaps/execution-history](api-rfq/api-rfq-swaps-execution-history.md)
  - This endpoint is used query all trading events for swaps RFQ. It should be used when you require a detailed analysis and understanding of the execution
3. [Outrights Execution Stats - v1/fx/rfq-outrights/execution-stats](api-rfq/api-rfq-outrights-execution-stats.md)
  - This endpoint is designed to study general execution quality of the outrights RFQ trades
4. [Swaps Execution Stats - v1/fx/rfq-swaps/execution-stats](api-rfq/api-rfq-swaps-execution-stats.md)
  - This endpoint is designed to study general execution quality of the swaps RFQ trades
5. [Outrights Opportunity Report - v1/fx/rfq-outrights/opportunity-report](api-rfq/api-rfq-outrights-opportunity-report.md)
  - This endpoint generates an opportunity report which displays the `OutCome` of the outrights RFQ if it was `WON` or `Lost`
6. [Swaps Opportunity Report - v1/fx/rfq-swaps/opportunity-report](api-rfq/api-rfq-swaps-opportunity-report.md)
  - This endpoint generates an opportunity report which displays the `OutCome` of the swaps RFQ if it was `WON` or `Lost`
7. [Outrights Participation Report - v1/fx/rfq-outrights/participation-report](api-rfq/api-rfq-outrights-participation-report.md)
  - This endpoint returns a table which summarises the outrights RFQ participation rate by `LP`
8. [Swaps Participation Report - v1/fx/rfq-swaps/participation-report](api-rfq/api-rfq-swaps-participation-report.md)
  - This endpoint returns a table which summarises the swaps RFQ participation rate by `LP`