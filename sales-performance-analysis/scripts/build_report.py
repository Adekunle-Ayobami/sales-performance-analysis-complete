"""Create figures and a factual findings report from the cleaned outputs."""
from pathlib import Path
import json
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'data/processed'
m=json.loads((P/'metrics.json').read_text())
monthly=pd.read_csv(P/'monthly.csv')
countries=pd.read_csv(P/'countries.csv')
products=pd.read_csv(P/'products.csv',dtype={'StockCode':str})
merch=products[products.StockCode.str.fullmatch(r'[0-9]{5}[A-Z]?')].copy()
merch.to_csv(P/'standard_code_products.csv',index=False)
segments=pd.read_csv(P/'customer_segments.csv')
complete=monthly[monthly.PeriodComplete.eq(1)]
peak=complete.loc[complete.GrossSales.idxmax()]
uk=countries[countries.Country.eq('United Kingdom')].iloc[0]
fig,axs=plt.subplots(2,2,figsize=(15,9),layout='constrained')
fig.suptitle('UK online retail: sales performance | Dec 2010–Dec 2011',fontsize=19,fontweight='bold',color='#24476B')
axs[0,0].plot(monthly.YearMonth,monthly.GrossSales/1e6,color='#24476B',marker='o');axs[0,0].set_title('Monthly gross sales (£ million)');axs[0,0].tick_params(axis='x',rotation=65);axs[0,0].set_ylim(bottom=0)
axs[0,0].annotate('Partial month: 1–9 Dec',xy=(12,monthly.GrossSales.iloc[-1]/1e6),xytext=(6,.15),arrowprops={'arrowstyle':'->','color':'#D08A37'})
cs=countries.head(6).iloc[::-1];axs[0,1].barh(cs.Country,cs.GrossSales/1e6,color='#24476B');axs[0,1].set_title('Top customer countries (£ million)')
ps=merch.head(5).iloc[::-1];axs[1,0].barh(ps.Description,ps.NetRevenue/1000,color='#517C61');axs[1,0].set_title('Standard product codes: net revenue (£ thousands)')
axs[1,1].bar(segments.CustomerType.str.replace(' within observed period',''),segments.Customers,color=['#75899B','#24476B']);axs[1,1].set_title('Known customer purchasing behaviour');axs[1,1].set_ylabel('Customers')
for ax in axs.flat:ax.spines[['top','right']].set_visible(False);ax.grid(axis='y',alpha=.15);ax.set_axisbelow(True)
fig.savefig(ROOT/'reports/analysis_dashboard.png',dpi=160)
plt.close(fig)
report=f'''# Sales performance findings

This is a historical portfolio case study using the full UCI Online Retail dataset. It is not current market research or a client engagement.

## Scope and definitions

The ledger covers {m['date_start']} to {m['date_end']}. All prices are GBP, including overseas customer transactions. Country describes the customer location. The data does not contain product cost, profit, acquisition channel, UK region or store location.

An order is a distinct positive-sale invoice, not a transaction line. Gross sales sums positive, non-cancellation lines. Credits sum the absolute value of negative line amounts. Net revenue sums signed line amounts. These are analytical invoice-value measures, not audited revenue or profit. Shipping and manual invoice items are included in headline values.

## Results

| Metric | Result |
|---|---:|
| Source transaction lines | {m['raw_rows']:,} |
| Clean ledger lines | {m['clean_rows']:,} |
| Gross sales | £{m['gross_sales']:,.2f} |
| Credit value | £{m['credit_value']:,.2f} |
| Net revenue | £{m['net_revenue']:,.2f} |
| Sale invoices | {m['orders']:,} |
| Average order value | £{m['average_order_value']:,.2f} |
| Known purchasing customers | {m['known_customers']:,} |
| Repeat customers | {m['repeat_customers']:,} |
| Repeat customer rate | {m['repeat_customer_rate']:.1%} |
| Sales without a customer ID | {m['unknown_customer_sales_share']:.1%} |

### Monthly sales

The strongest complete month was **{peak.YearMonth}**, with **£{peak.GrossSales:,.2f}** gross sales. December 2011 is partial and must not be presented as a full-month decline. One observed annual cycle is not enough to establish a stable seasonal pattern.

### Geography

The UK contributed **£{uk.GrossSales:,.2f}**, or **{uk.RevenueShare:.1%}** of gross sales. The next two countries were {countries.iloc[1].Country} (£{countries.iloc[1].GrossSales:,.2f}) and {countries.iloc[2].Country} (£{countries.iloc[2].GrossSales:,.2f}). This shows concentration in the UK customer base, rather than evidence that international expansion will be profitable.

### Products and invoice items

The highest net-value invoice code was **{products.iloc[0].StockCode}: {products.iloc[0].Description}**, which is postage rather than merchandise. A separate, explicitly defined standard-product-code filter (`^[0-9]{{5}}[A-Z]?$`) identifies **{merch.iloc[0].Description}** as the top item in that subset, with **£{merch.iloc[0].NetRevenue:,.2f}** net revenue. The filter is a practical proxy, not a supplied product taxonomy. Report both gross and net values because large credits can change rankings.

### Customers and credits

**{m['repeat_customers']:,} of {m['known_customers']:,}** known purchasing customers placed at least two invoices during the observation period. This {m['repeat_customer_rate']:.1%} measure is an observed repeat-purchase rate, not customer retention, churn or lifetime value. Missing IDs account for {m['unknown_customer_sales_share']:.1%} of gross sales, limiting customer-level conclusions. Credit value represents {m['credit_value_ratio']:.1%} of gross sales, but credits are not matched to original orders and can include adjustments.

## Five recommendations

1. **Prepare capacity before the observed autumn peak.** Review stock availability, supplier lead times and fulfilment staffing ahead of a comparable trading period. Validate the pattern with additional years. Track fulfilment delays and stockouts rather than promising a sales increase.
2. **Protect the core UK business and assess overseas opportunities separately.** Compare the Netherlands, EIRE and Germany using shipping costs, demand and margin information before allocating growth spending. Those costs are absent here.
3. **Use merchandise rankings for assortment decisions.** Separate postage/manual codes and compare product net revenue, quantities and credit exposure. Review availability of the strongest standard-code products; check margins before increasing stock.
4. **Investigate unusually large credits.** Check the original invoices and adjustment reasons, especially where gross and net rankings diverge. Establish a credit-reason log and track credit value as a share of sales.
5. **Improve identification and test repeat-purchase activity.** Increase valid customer-ID capture and run a small measured campaign for eligible customers. Compare repeat orders in a defined follow-up window; this dataset alone cannot prove campaign effectiveness.

## Limitations and next steps

Exact duplicate removal assumes repeated identical source lines are duplicates; some may be legitimate. Nonpositive-price and zero-quantity rows were excluded. Customer metrics cover known buyers only. No inflation adjustment is made. Customer country is the available geography. Product descriptions can vary for the same code; grouping uses StockCode, with modal descriptions in Python and an example description in SQL. Large wholesale invoices affect AOV. Raw-source dates are used without timezone conversion. Reconcile every desktop tool against metrics.json before describing those tools as used in your CV.

## Source and licence

Chen, D. (2015). Online Retail [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5BW33. Source page: https://archive.ics.uci.edu/dataset/352/online+retail. Dataset licence: CC BY 4.0. This project removes duplicates, filters invalid lines, normalises text and derives revenue fields. The source workbook is included unchanged.
'''
(ROOT/'reports/findings.md').write_text(report)
print('Report and analysis dashboard created.')
