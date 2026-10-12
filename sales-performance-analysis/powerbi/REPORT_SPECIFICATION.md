# Power BI report specification

Use the full `sales_clean.csv`, not the learning sample or monthly summary table, for the report fact table. Import it as `Sales`. Create the Date table from measures.dax, mark Date[Date] as the date column and relate Date[Date] (one) to Sales[InvoiceDay] (many), active with single-direction filtering. Leave all other relationships absent for this simple model.

Use a 16:9 page, white background and the included theme. Currency is GBP with two decimals for cards and suitable £K/£M display units for charts. Percentages use one decimal place. Keep the same period and customer definitions across pages.

## Page 1 — Sales overview

- Cards: Gross Sales, Credit Value, Net Revenue, Orders, Average Order Value.
- Line chart: Date[YearMonth] on X, Gross Sales and Net Revenue on Y. Use the column itself, not a date hierarchy. Sort ascending.
- Bar chart: Sales[Country] on Y, Gross Sales on X. Sort descending and set a Top N 10 visual filter by Gross Sales.
- Slicers: Date[Date] as Between, Sales[Country] as dropdown.
- Text box: 'Historical data: 1 Dec 2010–9 Dec 2011. December 2011 is partial. All values GBP.'
- Matrix for monthly validation: Date[YearMonth], Gross Sales, Credit Value, Net Revenue, Orders, Average Order Value, MoM Growth.

## Page 2 — Products and credits

- Bar chart: Sales[StockCode] by Net Revenue, Top N 10 by Net Revenue.
- Table: StockCode, Gross Sales, Credit Value, Net Revenue, Credit Value Ratio. Sort Net Revenue descending. Product labels can vary by invoice, so do not group by Description alone.
- To show standard-code merchandise separately, import `standard_code_products.csv` as an independent summary table. Use StockCode, Description and NetRevenue for a full-period, explicitly labelled chart. Do not relate it to Sales or imply that fact-table date slicers filter this snapshot.
- Label the summary chart 'Standard-code product subset — full observed period'.
- Text box: 'Postage/manual codes appear in invoice rankings. Credits are not matched to their original orders.'

## Page 3 — Customer behaviour and quality

- Cards: Known Customers, Repeat Customers, Repeat Customer Rate, Unknown Customer Sales Share.
- Import `customer_segments.csv` as an independent full-period snapshot for a two-category customer chart. Do not relate it to Sales. Label it 'Customer segments — full observed period'.
- Table: Sales[CustomerID], Orders, Gross Sales. Set visual filter CustomerID is not blank/empty and IsSale=1; sort Gross Sales descending.
- Cards: Ledger Lines, Revenue Bridge Difference. The latter should display £0.00.
- Text box: 'Repeat means at least two invoices in the selected context. Snapshot segment chart uses the full observed period. Missing customer IDs remain in overall sales.'

## Validation before saving

Clear all slicers and visual filters before comparing cards to metrics.json. The Date table extends to 31 December but contains no fact rows after 9 December. Set charts to avoid showing unsupported future dates as actual observations.

Check full-period card totals, known and repeat customers, November and partial December values. Filter UK and verify £9,001,744.094 gross sales. Verify the monthly matrix and clear filters again. Save `Sales_Performance.pbix`; capture all three pages as real Power BI screenshots and add them to reports/. Update README status only after this work is complete.
