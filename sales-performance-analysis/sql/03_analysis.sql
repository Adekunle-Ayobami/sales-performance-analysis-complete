USE retail_portfolio;
-- 1. Headline metrics. Sales mean positive non-cancellation invoice lines.
SELECT COUNT(*) AS ledger_lines, SUM(SaleRevenue) AS gross_sales_gbp,
 SUM(CreditValue) AS credit_value_gbp, SUM(LineRevenue) AS net_revenue_gbp,
 COUNT(DISTINCT CASE WHEN IsSale=1 THEN InvoiceNo END) AS orders,
 SUM(SaleRevenue)/NULLIF(COUNT(DISTINCT CASE WHEN IsSale=1 THEN InvoiceNo END),0) AS aov_gbp,
 COUNT(DISTINCT CASE WHEN IsSale=1 AND CustomerID<>'' THEN CustomerID END) AS known_customers
FROM sales;
-- 2. Monthly trend; never compare a partial month as if complete.
WITH monthly AS (
 SELECT YearMonth, MIN(PeriodComplete) AS complete_month, SUM(SaleRevenue) AS gross_sales,
 SUM(CreditValue) AS credits, SUM(LineRevenue) AS net_revenue,
 COUNT(DISTINCT CASE WHEN IsSale=1 THEN InvoiceNo END) AS orders
 FROM sales GROUP BY YearMonth
), trend AS (
 SELECT *,LAG(gross_sales) OVER(ORDER BY YearMonth) AS previous_sales FROM monthly
)
SELECT *,gross_sales/NULLIF(orders,0) AS aov,
 CASE WHEN complete_month=1 THEN gross_sales/NULLIF(previous_sales,0)-1 END AS mom_growth
FROM trend ORDER BY YearMonth;
-- 3. Countries: this is customer geography, not store geography.
SELECT Country,SUM(SaleRevenue) AS gross_sales,SUM(CreditValue) AS credits,
 SUM(LineRevenue) AS net_revenue,
 SUM(SaleRevenue)/SUM(SUM(SaleRevenue)) OVER() AS gross_sales_share
FROM sales GROUP BY Country ORDER BY gross_sales DESC;
-- 4. Rank products using net revenue to expose the effect of credits.
SELECT StockCode,MAX(Description) AS example_description,
 SUM(SaleRevenue) AS gross_sales,SUM(CreditValue) AS credits,SUM(LineRevenue) AS net_revenue
FROM sales GROUP BY StockCode ORDER BY net_revenue DESC LIMIT 20;
-- MAX description is an example label; Python uses the modal description.
-- 5. Observed purchasing behaviour for customers with an ID.
WITH customer_orders AS (
 SELECT CustomerID,COUNT(DISTINCT InvoiceNo) AS orders,SUM(SaleRevenue) AS gross_spend
 FROM sales WHERE IsSale=1 AND CustomerID<>'' GROUP BY CustomerID
)
SELECT CASE WHEN orders>=2 THEN 'Repeat within observed period' ELSE 'One order within observed period' END AS customer_type,
 COUNT(*) AS customers,SUM(orders) AS customer_orders,SUM(gross_spend) AS gross_sales
FROM customer_orders GROUP BY customer_type;
-- 6. Missing IDs: exclude from customer metrics, retain in sales totals.
SELECT SUM(CASE WHEN CustomerID='' THEN 1 ELSE 0 END) AS unidentified_ledger_lines,
 SUM(CASE WHEN CustomerID='' THEN SaleRevenue ELSE 0 END) AS unidentified_sales,
 SUM(CASE WHEN CustomerID='' THEN SaleRevenue ELSE 0 END)/NULLIF(SUM(SaleRevenue),0) AS unidentified_sales_share
FROM sales;
-- 7. Credit exposure; this is a value ratio, not an order-return rate.
SELECT Country,SUM(CreditValue)/NULLIF(SUM(SaleRevenue),0) AS credit_value_ratio
FROM sales GROUP BY Country HAVING SUM(SaleRevenue)>0 ORDER BY credit_value_ratio DESC;
-- 8. Highest-value observed customers (gross spend, before credits).
SELECT CustomerID,COUNT(DISTINCT InvoiceNo) AS orders,SUM(SaleRevenue) AS gross_spend
FROM sales WHERE IsSale=1 AND CustomerID<>'' GROUP BY CustomerID ORDER BY gross_spend DESC LIMIT 20;
