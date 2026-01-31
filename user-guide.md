# User Guide

## Tradefeedr Data Model

Tradefeedr design specific data model workflows. These workflows include:

- Algo execution
- Request for stream execution
- Request for quote execution

## FX Product Coverage

This section contains different workflow examples.

Namely:

- Algo: How to compare algo performance and select the best algos, algo cost curve & using risk transfer price.
  - See [Algo Analytics](../analytics/algo.md) for more details

- RFS: How to monitor flow performance, communicate back to your LP and why it is important
  - See [RFS Analytics](../analytics/rfs.md) for more details
  - See [RFS Bilateral Sharing Analytics](../analytics/bilateral-sharing.md) for more details

- RFQ: How to compare liquidity providers across different RFQ, RFQ panel size and performance, RFQ cost curves
  - See [RFQ Analytics](../analytics/rfq.md) for more details

## API User Guides

The API user guides provide you a detailed tutorial of how to run the API endpoints.
Each endpoint has a specific use case which is detailed the API guide.
They also provide you with example analytics and data visualization using Plotly in Python.
The code provided in the guides can be copied and run directly on the Tradefeedr platform, giving the you the same results displayed in the guides.

- [Algo API Guide](algo/README.md)
- [RFS API Guide](api-rfs/api-rfs.md)
- [RFS Bilateral API Guide](api-rfs-bilateral/api-rfs-bilateral.md)
- [RFQ API Guide](api-rfq/api-rfq.md)