USE retail_portfolio;
-- Replace the path. Import only once into an empty table.
-- Alternative: Workbench Table Data Import Wizard; map all 16 fields to the existing table.
-- LOCAL must be enabled in the local client and server. Never enable it on untrusted servers.
LOAD DATA LOCAL INFILE 'C:/Users/YOUR_NAME/Documents/sales-performance-analysis/data/processed/sales_clean.csv'
INTO TABLE sales CHARACTER SET utf8mb4
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' ESCAPED BY '"'
LINES TERMINATED BY '\n' IGNORE 1 LINES
(LineID,InvoiceNo,StockCode,Description,Quantity,InvoiceDate,UnitPrice,CustomerID,Country,
 LineRevenue,IsSale,SaleRevenue,CreditValue,InvoiceDay,YearMonth,PeriodComplete);
SELECT COUNT(*) AS imported_rows FROM sales;
SHOW WARNINGS;
