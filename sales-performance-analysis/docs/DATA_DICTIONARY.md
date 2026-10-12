# Data dictionary and analysis rules

## Grain

One row is one invoice line. An invoice normally contains several products. Counting rows as orders would overstate the order count. LineID is a project-generated unique row key after cleaning, not a source transaction identifier.

| Field | Type | Meaning |
|---|---|---|
| LineID | Integer | Generated ledger row identifier |
| InvoiceNo | Text | Invoice identifier; C prefix indicates cancellation |
| StockCode | Text | Invoice item identifier; includes merchandise and service codes |
| Description | Text | Source item description; missing values become UNKNOWN DESCRIPTION |
| Quantity | Integer | Signed number of units |
| InvoiceDate | Date/time | Source invoice timestamp |
| UnitPrice | Decimal | Price per unit in GBP; some source prices have more than two decimals |
| CustomerID | Text | Public source customer identifier; empty string means unidentified |
| Country | Text | Customer country, not UK region or retailer location |
| LineRevenue | Decimal | Quantity × UnitPrice, rounded to four decimals |
| IsSale | Integer | 1 for positive quantity and invoice not starting C; otherwise 0 |
| SaleRevenue | Decimal | LineRevenue for IsSale=1, otherwise zero |
| CreditValue | Decimal | Absolute value of negative LineRevenue, otherwise zero |
| InvoiceDay | Date | Date-only invoice key for the Power BI relationship |
| YearMonth | Text | YYYY-MM chronological month key |
| PeriodComplete | Integer | 0 for December 2011, 1 for other observed months |

## Cleaning decisions

1. Remove exact duplicates across the original eight columns, before text normalisation. This is an assumption; identical lines can sometimes be legitimate.
2. Strip text spaces and uppercase invoice/item codes. Replace missing descriptions without deleting associated valid revenue.
3. Keep CustomerID as text, preserving missing IDs as blank. Never invent customer IDs or assign all unidentified people to one customer.
4. Exclude zero quantities, nonpositive prices, missing dates and empty invoice/item keys. Negative quantities remain when prices are positive.
5. Preserve credits/negative values for net revenue. Do not delete all cancellations and then call the result net revenue.
6. Calculate source amounts to four decimals, displaying headline money to two decimals. Retaining source precision keeps cross-tool totals aligned.
7. Flag December 2011 as incomplete. Do not extrapolate it or present its month-on-month fall as a complete-month business decline.

## KPI definitions

- **Gross sales:** sum of SaleRevenue across the selected ledger.
- **Credits:** sum of CreditValue. It can contain corrections as well as customer cancellations.
- **Net revenue:** sum of signed LineRevenue. In this dataset, gross sales minus credits reconciles to net revenue because there are no positive-quantity C-prefixed eligible rows.
- **Orders:** distinct InvoiceNo where IsSale=1.
- **Average order value:** gross sales divided by sale orders. This includes unidentified buyers and invoice service amounts.
- **Known customers:** distinct nonblank CustomerID with at least one sale invoice.
- **Repeat customer:** known customer with at least two distinct sale invoices in the observation period. The Power BI measure responds to the selected date/country/product context; label it accordingly.
- **Repeat customer rate:** repeat customers divided by known purchasing customers for the same context.
- **Credit value ratio:** credit value divided by gross sales. Not an order-return rate because credits are not matched to original invoices.
- **Customer-ID missing sales share:** sales with a missing ID divided by all gross sales.
- **Country share:** country gross sales divided by total gross sales in the same scope.
- **MoM growth:** current complete-month gross sales divided by previous-month gross sales, minus one. First observed month has no comparison; December 2011 is suppressed.

Customer-segment counts use all observed dates. Power BI slicers can change a customer's classification. Do not compare a filtered dashboard count with an unfiltered full-period CSV.
