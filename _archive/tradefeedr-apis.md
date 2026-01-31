# Tradefeedr APIS

GET[/api/v1/trades/{trade\_type}/aggregations](https://51.137.147.43:8000/docs#/Trades/get_aggregations_api_v1_trades__trade_type__aggregations_get)Get Aggregations

Get trade aggregations (counts by symbol, status, side, currency, reason).

Args: request: FastAPI request object trade\_type: Type of trade (spot, fx, etc.) is\_enriched: Whether to use enriched or raw table status: Optional status filter (comma-separated for multiple) start\_date: Optional start date filter end\_date: Optional end date filter tenant\_key: Tenant key (injected) trade\_service: Trade service (injected)

Returns: ApiResponse with aggregation data

**Parameters**

Try it out

| Name                                                  | Description                                                                            |
| ----------------------------------------------------- | -------------------------------------------------------------------------------------- |
| trade\_type \*string(path)                            | <p><em>Available values</em> : spot, algo, forward, swap</p><p>spotalgoforwardswap</p> |
| is\_enrichedboolean(query)                            | <p>Use enriched table</p><p><em>Default value</em> : false</p><p>--truefalse</p>       |
| statusstring(query)                                   | Filter by status (can be comma-separated)                                              |
| start\_datestring(query)                              | Start date filter (YYYY-MM-DD)                                                         |
| end\_datestring(query)                                | End date filter (YYYY-MM-DD)                                                           |
| X-Tenant-IDstring \| (string \| null)(header)         |                                                                                        |
| current\_tenant\_idstring \| (string \| null)(cookie) |                                                                                        |

**Responses**

<table><thead><tr><th>Code</th><th>Description</th><th>Links</th></tr></thead><tbody><tr><td>200</td><td><p>Successful Response</p><p>Media typeapplication/jsonControls <code>Accept</code> header.</p><ul><li>Example Value</li><li>Schema</li></ul><pre class="language-json"><code class="lang-json">{
  "name": "Success Response",
  "summary": "Successful API response",
  "value": {
    "data": {
      "id": 1,
      "name": "Example"
    },
    "message": "Operation completed successfully",
    "meta": {
      "count": 1,
      "total": 1
    },
    "request_id": "req_abc123",
    "success": true
  }
}
</code></pre></td><td><em>No links</em></td></tr><tr><td>422</td><td><p>Validation Error</p><p>Media typeapplication/json</p><ul><li>Example Value</li><li>Schema</li></ul><pre class="language-json"><code class="lang-json">{
  "detail": [
    {
      "loc": [
        "string",
        0
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}
</code></pre></td><td></td></tr></tbody></table>
