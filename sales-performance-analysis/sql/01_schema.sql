-- MySQL 8+. Create only this project's database and table.
CREATE DATABASE IF NOT EXISTS retail_portfolio CHARACTER SET utf8mb4;
USE retail_portfolio;
CREATE TABLE IF NOT EXISTS sales (
 LineID INT PRIMARY KEY, InvoiceNo VARCHAR(20), StockCode VARCHAR(30),
 Description VARCHAR(255), Quantity INT, InvoiceDate DATETIME,
 UnitPrice DECIMAL(18,4), CustomerID VARCHAR(20), Country VARCHAR(80),
 LineRevenue DECIMAL(18,4), IsSale TINYINT, SaleRevenue DECIMAL(18,4),
 CreditValue DECIMAL(18,4), InvoiceDay DATE, YearMonth CHAR(7), PeriodComplete TINYINT
);
-- No credentials or local machine paths are stored in this script.
