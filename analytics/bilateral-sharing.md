# RFS Bilateral Sharing

## Process Description

Tradefeedr takes the transactions data from client databases, removes all the sensitive information and `aggregates` it. Before sharing this aggregated and cleaned information with LPs specified by the client.

## Aggregation Buckets

- `Date` - for example 2021-01-02
- `TradeTime` - 15 min time bucket, for example: 00:00 to 00:15
- `Symbol` - Currency Pair, e.g. `EURUSD`
- `OrderStatus` - typically only consider `F` for fill and `R` for reject
- `LP` - LP name. The LP who has access to aggregated, shared data sees its real name like `GoldmanSachs` or `JPM`.  They see all other LPs as `masked_LP_name_XXX`
- `LPstream` - name of the LP stream trade belong to. `LPstream` can take any values which reflect the liquidity provision contract between a client and an LP. The values have to make sense for the LP and the values can be shared by the client. (Not proprietary information which a client would like to keep secret from the LP). Conventional values would be  `LastLook`, `NoLastLook`, `FullAmount`, `Sweepable` etc. There is not precise structure, any nomenclature which is helpful for both LP and client is allowed.
- `LiqPool` - a liquidity pool LP belongs to.
The difference between `LPstream` and `LiqPool` is that `LPstream` is a property of bilateral liquidity provision between LP and client. While the `LiqPool` is normally a set of LPs defined by a client to provide liquidity in competition.
These values are often related  as a client start with understanding the type of liquidity they want (`LastLook`, `Sweepable` etc) and then creates a set of LPs (`LiqPool`) which provide liquidity according to those rules (`LPstream`).
`LiqPool` can take any values that reflect the set of LPs which are in competition for this trade (in case of RFS workflow). The values have to make sense for the LP and have to be something which a client is happy to share (not proprietary information which a client would like to keep secret from LP).
  - Generally values would be  `LastLook`, `NoLastLook`, `FullAmount`, `Sweepable`, `NoHFTPool`, `BanksOnly`, `InternalizersOnly` with same meaning as in `LPstream` and can also be reflective of the pool in total . There is not precise structure, any nomenclature  which is helpful for both LP and client is allowed.
- `SkewStatus` - this can be describing whether the trade belongs to `Skew-Safe` or to a `Not-Skew-Safe` stream. This information is given to a client by an LP as the LP decides whether to show skew on the stream or not. As with `LPstream` and `LiqPool` the values mentioned it can be anything which helps the dialogue between client and LP. We expected clients to be guided by their own understand and importantly by their LP in terms of what sort of information is important to communicate.

Aggregated database is created from individual clients trades according to the rules provided by a client and shared with LP of client choice. Therefore, recipient LP has access to `aggregated` client data with all descriptive information (such as trader name) `removed`.

## Client Choice & Configuration

Client choice involves the following:

- Client needs to define a `LP Map` which maps client internal LP names on Tradefeedr standard LP names.
For example, client internal LP names can be `GS` and `GS_PBNAME` and  `GS_streamname` --  all of those should be mapped to `goldmansachs` (Tradefeedr name) to define
that those trades are to be aggregated to be shared with `goldmansachs`.

- Client needs to define a `Flow Map` which maps client internal names onto standard Tradefeedr flow splitting variables such as `LPstream`,
`LiqPool` and `SkewSafe`. Client internal flow definitions can depend on other columns such as `LP`, `Account`, `Trader`, `LPstream` and `LiqPool`.
 For instance, it may be the case in client's internal nomenclature that `Account` variable determined  `LPstream` to be shared with LPs, e.g.  `Account1`
 and `Account2` may correspond to `LPstream` = `Sweepable` and `Account3` may correspond to `Full Price`. In this case `Account` will be part of the `Flow Map` configuration.

Schematically client `Flow Map` can look like this.

### Figure

![RFS Bilateral](assets/images/rfs_bilateral_analytics_flow_map.png)

An example of a `Flow Map`:

- The client knows that `LP1` and `LP2` belong to the same `LPstream` ( stream "1") while LP3 belongs to stream "2".
- The exact denomination of those stream is completely up to the client but it is important that the LP understands what they are being referred to as.

It is up to client as to which LP receives the information but the `Flow Map` is unique. The client cannot tell different information to different LPs, as it is likely to cause confusion.

### Results

LP	Account	Trader	bilateral_LPstream	bilateral_LiqPool	bilateral_SkewSafe
LP1	Account	Trader	1	1	Safe
LP2	Account	Trader	1	1	Safe
LP3	Account	Trader	2	2	NotSafe