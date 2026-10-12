// Use in Excel Power Query to reproduce the cleaning from the original UCI workbook.
// Create a text parameter named ProjectFolder pointing to your extracted project folder.
let
 Source = Excel.Workbook(File.Contents(ProjectFolder & "\data\raw\Online Retail.xlsx"),null,true),
 Sheet = Table.SelectRows(Source,each [Kind]="Sheet"){0}[Data],
 Headers = Table.PromoteHeaders(Sheet,[PromoteAllScalars=true]),
 Unique = Table.Distinct(Headers),
 Typed = Table.TransformColumnTypes(Unique,{{"InvoiceNo",type text},{"StockCode",type text},{"Description",type text},{"Quantity",Int64.Type},{"InvoiceDate",type datetime},{"UnitPrice",type number},{"CustomerID",type text},{"Country",type text}}),
 TextClean = Table.TransformColumns(Typed,{{"InvoiceNo",each Text.Upper(Text.Trim(_)),type text},{"StockCode",each Text.Upper(Text.Trim(_)),type text},{"Description",each if _=null then "UNKNOWN DESCRIPTION" else Text.Trim(_),type text},{"Country",each if _=null then "Unknown" else Text.Trim(_),type text},{"CustomerID",each if _=null then "" else Text.BeforeDelimiter(_ & ".","."),type text}}),
 Eligible = Table.SelectRows(TextClean,each [Quantity]<>0 and [UnitPrice]>0 and [InvoiceDate]<>null and [InvoiceNo]<>"" and [StockCode]<>""),
 Indexed = Table.AddIndexColumn(Eligible,"LineID",1,1,Int64.Type),
 Revenue = Table.AddColumn(Indexed,"LineRevenue",each Number.Round([Quantity]*[UnitPrice],4),type number),
 SaleFlag = Table.AddColumn(Revenue,"IsSale",each if [Quantity]>0 and not Text.StartsWith([InvoiceNo],"C") then 1 else 0,Int64.Type),
 Sales = Table.AddColumn(SaleFlag,"SaleRevenue",each if [IsSale]=1 then [LineRevenue] else 0,type number),
 Credits = Table.AddColumn(Sales,"CreditValue",each if [LineRevenue]<0 then -[LineRevenue] else 0,type number),
 Day = Table.AddColumn(Credits,"InvoiceDay",each Date.From([InvoiceDate]),type date),
 Month = Table.AddColumn(Day,"YearMonth",each Date.ToText([InvoiceDay],"yyyy-MM"),type text),
 Complete = Table.AddColumn(Month,"PeriodComplete",each if [YearMonth]="2011-12" then 0 else 1,Int64.Type)
in Complete
