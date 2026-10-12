"""Rebuild the documented analysis from UCI's original workbook. Python 3.10+."""
from pathlib import Path
import json, hashlib, sqlite3
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'data/raw/Online Retail.xlsx'
OUT = ROOT / 'data/processed'
OUT.mkdir(parents=True, exist_ok=True)
df = pd.read_excel(RAW, engine='openpyxl')  # read only; Excel authoring is separate
raw_count = len(df)
duplicates = int(df.duplicated().sum())
df = df.drop_duplicates().copy()
df['InvoiceNo'] = df.InvoiceNo.astype(str).str.strip().str.upper()
df['StockCode'] = df.StockCode.astype(str).str.strip().str.upper()
df['Description'] = df.Description.fillna('UNKNOWN DESCRIPTION').astype(str).str.strip()
df['Country'] = df.Country.fillna('Unknown').astype(str).str.strip()
df['CustomerID'] = df.CustomerID.apply(lambda x: '' if pd.isna(x) else str(int(x)))
df['InvoiceDate'] = pd.to_datetime(df.InvoiceDate)
bad = (df.Quantity.eq(0) | df.UnitPrice.le(0) | df.InvoiceDate.isna()
       | df.InvoiceNo.eq('') | df.StockCode.eq(''))
excluded = df[bad].copy()
df = df[~bad].copy()
df['LineID'] = range(1, len(df)+1)
# Four-decimal ledger amounts preserve source prices such as 0.001.
df['LineRevenue'] = (df.Quantity * df.UnitPrice).round(4)
df['IsSale'] = ((df.Quantity > 0) & ~df.InvoiceNo.str.startswith('C')).astype(int)
df['SaleRevenue'] = np.where(df.IsSale.eq(1), df.LineRevenue, 0)
df['CreditValue'] = np.where(df.LineRevenue.lt(0), -df.LineRevenue, 0)
df['InvoiceDay'] = df.InvoiceDate.dt.strftime('%Y-%m-%d')
df['YearMonth'] = df.InvoiceDate.dt.strftime('%Y-%m')
df['PeriodComplete'] = (df.YearMonth != '2011-12').astype(int)
cols=['LineID','InvoiceNo','StockCode','Description','Quantity','InvoiceDate','UnitPrice','CustomerID','Country','LineRevenue','IsSale','SaleRevenue','CreditValue','InvoiceDay','YearMonth','PeriodComplete']
df[cols].to_csv(OUT/'sales_clean.csv',index=False,date_format='%Y-%m-%d %H:%M:%S',float_format='%.4f')
excluded.to_csv(OUT/'excluded_rows.csv',index=False)
sales=df[df.IsSale.eq(1)].copy()
monthly=df.groupby('YearMonth').agg(GrossSales=('SaleRevenue','sum'),CreditValue=('CreditValue','sum'),NetRevenue=('LineRevenue','sum'),Lines=('LineID','count')).reset_index()
orders=sales.groupby('YearMonth').InvoiceNo.nunique()
monthly['Orders']=monthly.YearMonth.map(orders).fillna(0).astype(int)
monthly['AOV']=monthly.GrossSales/monthly.Orders
monthly['PeriodComplete']=(monthly.YearMonth!='2011-12').astype(int)
monthly['MoMGrowth']=monthly.GrossSales.pct_change()
monthly.loc[monthly.PeriodComplete.eq(0),'MoMGrowth']=np.nan
countries=df.groupby('Country').agg(GrossSales=('SaleRevenue','sum'),CreditValue=('CreditValue','sum'),NetRevenue=('LineRevenue','sum')).reset_index().sort_values('GrossSales',ascending=False)
countries['RevenueShare']=countries.GrossSales/countries.GrossSales.sum()
products=df.groupby('StockCode').agg(GrossSales=('SaleRevenue','sum'),CreditValue=('CreditValue','sum'),NetRevenue=('LineRevenue','sum')).reset_index()
names=df.groupby('StockCode').Description.agg(lambda x:x.mode().iloc[0])
products['Description']=products.StockCode.map(names)
products=products.sort_values('NetRevenue',ascending=False)
known=sales[sales.CustomerID.ne('')]
customers=known.groupby('CustomerID').agg(Orders=('InvoiceNo','nunique'),GrossSpend=('SaleRevenue','sum'),FirstPurchase=('InvoiceDate','min'),LastPurchase=('InvoiceDate','max')).reset_index()
customers['CustomerType']=np.where(customers.Orders.ge(2),'Repeat within observed period','One order within observed period')
customers=customers.sort_values('GrossSpend',ascending=False)
segments=customers.groupby('CustomerType').agg(Customers=('CustomerID','count'),Orders=('Orders','sum'),GrossSales=('GrossSpend','sum')).reset_index()
daily=df.groupby('InvoiceDay').agg(GrossSales=('SaleRevenue','sum'),CreditValue=('CreditValue','sum'),NetRevenue=('LineRevenue','sum')).reset_index()
for name,frame in [('monthly',monthly),('countries',countries),('products',products),('customers',customers),('customer_segments',segments),('daily',daily)]:
    frame.to_csv(OUT/f'{name}.csv',index=False,float_format='%.4f')
metrics=dict(raw_rows=raw_count,duplicate_rows_removed=duplicates,excluded_rows=len(excluded),clean_rows=len(df),sales_rows=len(sales),gross_sales=round(float(df.SaleRevenue.sum()),4),credit_value=round(float(df.CreditValue.sum()),4),net_revenue=round(float(df.LineRevenue.sum()),4),orders=int(sales.InvoiceNo.nunique()),known_customers=int(known.CustomerID.nunique()),repeat_customers=int(customers.Orders.ge(2).sum()),missing_customer_lines=int(df.CustomerID.eq('').sum()),unknown_customer_sales=round(float(sales.loc[sales.CustomerID.eq(''),'SaleRevenue'].sum()),4),countries=int(df.Country.nunique()),date_start=str(df.InvoiceDate.min()),date_end=str(df.InvoiceDate.max()),positive_cancellation_lines=int(((df.Quantity>0)&df.InvoiceNo.str.startswith('C')).sum()),source_sha256=hashlib.sha256(RAW.read_bytes()).hexdigest())
metrics['average_order_value']=metrics['gross_sales']/metrics['orders']
metrics['repeat_customer_rate']=metrics['repeat_customers']/metrics['known_customers']
metrics['credit_value_ratio']=metrics['credit_value']/metrics['gross_sales']
metrics['unknown_customer_sales_share']=metrics['unknown_customer_sales']/metrics['gross_sales']
# Independent SQL aggregation in SQLite validates the arithmetic, not MySQL runtime compatibility.
con=sqlite3.connect(':memory:')
df[cols].to_sql('sales',con,index=False)
sql=con.execute('SELECT COUNT(*),SUM(SaleRevenue),SUM(CreditValue),SUM(LineRevenue),COUNT(DISTINCT CASE WHEN IsSale=1 THEN InvoiceNo END) FROM sales').fetchone()
assert sql[0]==metrics['clean_rows'] and sql[4]==metrics['orders']
assert all(abs(sql[i+1]-metrics[k])<0.01 for i,k in enumerate(['gross_sales','credit_value','net_revenue']))
assert abs(monthly.GrossSales.sum()-metrics['gross_sales'])<.01
assert abs(countries.NetRevenue.sum()-metrics['net_revenue'])<.01
assert abs(products.NetRevenue.sum()-metrics['net_revenue'])<.01
assert abs(metrics['gross_sales']-metrics['credit_value']-metrics['net_revenue'])<.01
assert segments.Customers.sum()==metrics['known_customers']
assert not df.LineID.duplicated().any()
(OUT/'metrics.json').write_text(json.dumps(metrics,indent=2))
sample=df[cols].sample(n=min(5000,len(df)),random_state=42).sort_values('LineID')
sample.to_csv(OUT/'learning_sample_5000.csv',index=False,date_format='%Y-%m-%d %H:%M:%S',float_format='%.4f')
# Workbook inputs use full-data aggregates and a clearly labelled sample for row-level formulas.
payload={'metrics':metrics,'monthly':monthly.fillna('').to_dict('records'),'countries':countries.to_dict('records'),'products':products.head(20).to_dict('records'),'segments':segments.to_dict('records'),'sample':json.loads(sample.to_json(orient='records',date_format='iso'))}
(OUT/'workbook_inputs.json').write_text(json.dumps(payload,default=str))
(ROOT/'reports/validation.md').write_text(f'''# Validation\n\nSource SHA-256: `{metrics['source_sha256']}`\n\n- Raw rows: {raw_count:,}\n- Exact duplicates removed before text normalisation: {duplicates:,}\n- Nonzero-quantity, positive-price and required-field filter exclusions: {len(excluded):,}\n- Ledger rows: {len(df):,}\n- Independent SQLite row, sales, credit, net and order checks: passed (money tolerance £0.01).\n- Monthly, country and product reconciliation: passed.\n- Customer segment count and unique LineID checks: passed.\n- MySQL scripts, Power Query and DAX require execution in their target desktop applications; their runtime execution is not claimed here.\n\nDuplicate removal is an explicit analytical assumption: identical lines could be legitimate repeated entries. No claim of audited accounts is made.\n''')
print(json.dumps(metrics,indent=2))
