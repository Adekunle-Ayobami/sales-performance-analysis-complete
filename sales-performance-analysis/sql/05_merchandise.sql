USE retail_portfolio;
-- Practical standard-code subset, not an official merchandise classification.
SELECT StockCode,MAX(Description) AS example_description,
 SUM(SaleRevenue) AS gross_sales,SUM(CreditValue) AS credits,SUM(LineRevenue) AS net_revenue
FROM sales WHERE StockCode REGEXP '^[0-9]{5}[A-Z]?$'
GROUP BY StockCode ORDER BY net_revenue DESC LIMIT 20;
