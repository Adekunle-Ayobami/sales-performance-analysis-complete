// Create a text parameter named ProjectFolder, e.g. C:\Users\Ayo\Documents\sales-performance-analysis
// Query name must be Sales. Blank query > Advanced Editor > paste this entire query.
let
 Source = Csv.Document(File.Contents(ProjectFolder & "\data\processed\sales_clean.csv"),[Delimiter=",",Columns=16,Encoding=65001,QuoteStyle=QuoteStyle.Csv]),
 Headers = Table.PromoteHeaders(Source,[PromoteAllScalars=true]),
 Typed = Table.TransformColumnTypes(Headers,{{"LineID",Int64.Type},{"InvoiceNo",type text},{"StockCode",type text},{"Description",type text},{"Quantity",Int64.Type},{"InvoiceDate",type datetime},{"UnitPrice",type number},{"CustomerID",type text},{"Country",type text},{"LineRevenue",type number},{"IsSale",Int64.Type},{"SaleRevenue",type number},{"CreditValue",type number},{"InvoiceDay",type date},{"YearMonth",type text},{"PeriodComplete",Int64.Type}},"en-GB"),
 CustomerBlanks = Table.ReplaceValue(Typed,null,"",Replacer.ReplaceValue,{"CustomerID"})
in CustomerBlanks
