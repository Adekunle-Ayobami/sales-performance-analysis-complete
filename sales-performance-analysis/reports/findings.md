# Sales performance findings

This is a historical portfolio case study using the full UCI Online Retail dataset. It is not current market research or a client engagement.

## Scope and definitions

The ledger covers 2010-12-01 08:26:00 to 2011-12-09 12:50:00. All prices are GBP, including overseas customer transactions. Country describes the customer location. The data does not contain product cost, profit, acquisition channel, UK region or store location.

An order is a distinct positive-sale invoice, not a transaction line. Gross sales sums positive, non-cancellation lines. Credits sum the absolute value of negative line amounts. Net revenue sums signed line amounts. These are analytical invoice-value measures, not audited revenue or profit. Shipping and manual invoice items are included in headline values.

## Results

| Metric | Result |
|---|---:|
| Source transaction lines | 541,909 |
| Clean ledger lines | 534,129 |
| Gross sales | £10,642,110.80 |
| Credit value | £893,979.73 |
| Net revenue | £9,748,131.07 |
| Sale invoices | 19,960 |
| Average order value | £533.17 |
| Known purchasing customers | 4,338 |
| Repeat customers | 2,845 |
| Repeat customer rate | 65.6% |
| Sales without a customer ID | 16.5% |

### Monthly sales

The strongest complete month was **2011-11**, with **£1,503,866.78** gross sales. December 2011 is partial and must not be presented as a full-month decline. One observed annual cycle is not enough to establish a stable seasonal pattern.

### Geography

The UK contributed **£9,001,744.09**, or **84.6%** of gross sales. The next two countries were Netherlands (£285,446.34) and EIRE (£283,140.52). This shows concentration in the UK customer base, rather than evidence that international expansion will be profitable.

### Products and invoice items

The highest net-value invoice code was **DOT: DOTCOM POSTAGE**, which is postage rather than merchandise. A separate, explicitly defined standard-product-code filter (`^[0-9]{5}[A-Z]?$`) identifies **REGENCY CAKESTAND 3 TIER** as the top item in that subset, with **£164,459.49** net revenue. The filter is a practical proxy, not a supplied product taxonomy. Report both gross and net values because large credits can change rankings.

### Customers and credits

**2,845 of 4,338** known purchasing customers placed at least two invoices during the observation period. This 65.6% measure is an observed repeat-purchase rate, not customer retention, churn or lifetime value. Missing IDs account for 16.5% of gross sales, limiting customer-level conclusions. Credit value represents 8.4% of gross sales, but credits are not matched to original orders and can include adjustments.

## Five recommendations

1. **Prepare capacity before the observed autumn peak.** Review stock availability, supplier lead times and fulfilment staffing ahead of a comparable trading period. Validate the pattern with additional years. Track fulfilment delays and stockouts rather than promising a sales increase.
2. **Protect the core UK business and assess overseas opportunities separately.** Compare the Netherlands, EIRE and Germany using shipping costs, demand and margin information before allocating growth spending. Those costs are absent here.
3. **Use merchandise rankings for assortment decisions.** Separate postage/manual codes and compare product net revenue, quantities and credit exposure. Review availability of the strongest standard-code products; check margins before increasing stock.
4. **Investigate unusually large credits.** Check the original invoices and adjustment reasons, especially where gross and net rankings diverge. Establish a credit-reason log and track credit value as a share of sales.
5. **Improve identification and test repeat-purchase activity.** Increase valid customer-ID capture and run a small measured campaign for eligible customers. Compare repeat orders in a defined follow-up window; this dataset alone cannot prove campaign effectiveness.

## Limitations and next steps

Exact duplicate removal assumes repeated identical source lines are duplicates; some may be legitimate. Nonpositive-price and zero-quantity rows were excluded. Customer metrics cover known buyers only. No inflation adjustment is made. Customer country is the available geography. Product descriptions can vary for the same code; grouping uses StockCode, with modal descriptions in Python and an example description in SQL. Large wholesale invoices affect AOV. Raw-source dates are used without timezone conversion. Reconcile every desktop tool against metrics.json before describing those tools as used in your CV.

## Source and licence

Chen, D. (2015). Online Retail [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5BW33. Source page: https://archive.ics.uci.edu/dataset/352/online+retail. Dataset licence: CC BY 4.0. This project removes duplicates, filters invalid lines, normalises text and derives revenue fields. The source workbook is included unchanged.
