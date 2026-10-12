USE retail_portfolio;
SELECT COUNT(*) AS clean_rows,COUNT(DISTINCT LineID) AS unique_line_ids,
 SUM(SaleRevenue) AS gross_sales,SUM(CreditValue) AS credit_value,SUM(LineRevenue) AS net_revenue,
 SUM(SaleRevenue)-SUM(CreditValue)-SUM(LineRevenue) AS revenue_bridge_difference,
 SUM(CASE WHEN Quantity=0 OR UnitPrice<=0 THEN 1 ELSE 0 END) AS invalid_lines,
 SUM(CASE WHEN IsSale=1 AND (Quantity<=0 OR InvoiceNo LIKE 'C%') THEN 1 ELSE 0 END) AS sale_classification_errors
FROM sales;
-- Compare with data/processed/metrics.json. All error/difference fields must be zero.
