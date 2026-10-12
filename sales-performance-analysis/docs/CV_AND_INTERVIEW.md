# Using the project on your CV and in interviews

## What this adds to your existing experience

Your MSc Management gives business context. Your Latrims development/data work gives technical experience and examples of understanding stakeholder needs. This project supplies visible, inspectable evidence of Excel, SQL and Power BI skills. It also shows that you can define a business question, check data quality and explain a recommendation.

Keep it under Portfolio Projects, separate from paid employment. Link directly to the project repository, not only your GitHub home page. Once finished, place it before employment in a Data Analyst CV if it provides your clearest analytical evidence. In a BA CV, emphasise business questions, KPI definitions, data-quality decisions and recommendations, while retaining your genuine stakeholder/requirements experience from work.

## Current status wording

Sales Performance Analysis — Excel, SQL/MySQL and Power BI | In progress

Reviewing a public retail dataset covering monthly sales, product revenue, customer-country performance and purchasing behaviour. Completing and validating the Excel, MySQL and Power BI workflow, with documented cleaning rules and business recommendations.

Use this while the local desktop execution/report is incomplete. The supplied scripts or figures do not prove that you personally built a Power BI dashboard.

## Completed wording — only after the desktop checklist is complete

Sales Performance Analysis — Excel, SQL/MySQL and Power BI | Personal portfolio project
GitHub: [paste your actual repository URL]

- Cleaned and analysed a public retail dataset containing 541,909 transaction lines, documenting duplicate, cancellation and missing-customer-ID treatment.
- Used SQL/MySQL to examine monthly sales, product revenue, customer-country performance and repeat purchasing behaviour.
- Built a Power BI report showing gross sales, net revenue, order value and customer measures, and checked its totals against the Excel and SQL results.
- Produced five recommendations covering stock planning, market concentration, product performance, credits and customer identification.

These statements describe outputs, not employment or measured commercial improvements. Do not claim that the recommendations increased revenue or reduced costs; no implementation experiment was conducted.

## Short version if CV space is limited

Sales Performance Analysis — Excel, SQL/MySQL and Power BI
Analysed 541,909 public retail transaction lines, built a sales dashboard and produced five business recommendations. Documented data-quality decisions and reconciled revenue measures across tools. GitHub: [actual link]

Use the short version after completing and understanding the workflow, including the native dashboard.

## Tailor the emphasis to the vacancy

| Target role | Lead with | Evidence to point to |
|---|---|---|
| Data Analyst | Cleaning, SQL, measures, dashboard and validation | Power Query steps, SQL queries, PBIX, metrics and screenshots |
| Business Analyst | Business problem, KPI definitions, interpretation and recommendations | Business questions, data dictionary, findings and decision assumptions |
| Technical Analyst | Data structure, reproducibility, troubleshooting and cross-tool consistency | MySQL schema, import validation, Power BI relationships and scripts |

This is an analysis case study, not evidence of interviews with real retailer stakeholders. Your genuine stakeholder experience belongs in your employment section. Do not add fabricated stakeholder workshops to this project.

## A natural interview introduction

'I used a public dataset from a UK online retailer to understand monthly sales, product performance and customer purchasing behaviour. The main challenge was defining reliable revenue and customer measures because the data included credits, duplicate lines and missing customer IDs. I checked the results across tools, built a dashboard and used the findings to propose five practical actions.'

Use that after performing the workflow. Explain any assistance openly if asked, then demonstrate your understanding by walking through a query or changing a measure.

## Questions you should be able to answer

1. **Why did you choose this dataset?** It contains invoice-level detail, products, country and customer IDs, allowing a connected business analysis. It is public and has a clear reuse licence. It is historical, so conclusions describe that period.
2. **Why are 534,129 rows left?** From 541,909 source lines, 5,268 exact duplicates were removed and 2,512 invalid lines excluded. Duplicate removal is an explicit assumption.
3. **What is an order?** A distinct invoice with at least one positive non-cancellation line. An invoice line is not an order.
4. **How did you treat credits?** Kept negative amounts in net revenue, showed their absolute value separately and avoided presenting them as a matched return rate.
5. **Why not drop missing customer IDs?** Their valid sales contribute to revenue. They cannot support distinct-customer counts, so those measures use known IDs only.
6. **What was the strongest month?** November 2011 among complete observed months. December 2011 is partial, so it cannot be compared as a full month.
7. **What was the top product?** The top invoice item was postage. In the explicitly defined standard-product-code subset, REGENCY CAKESTAND 3 TIER led net revenue. This distinction prevents misleading stock advice.
8. **What does repeat customer rate mean?** At least two sale invoices in the observed/selected period among identified purchasing customers. It is not churn or lifetime retention.
9. **How did you validate the dashboard?** Compare row counts and unfiltered KPI totals with the reference output, reconcile revenue by month/country/product, and test slicer behaviour.
10. **What would you ask the retailer for next?** Product costs/margins, reliable product categories, inventory and fulfilment records, credit reasons, acquisition channels and a longer history.

## Suggested personal extension

Write your own query comparing average order value and credit-value ratio for the UK, Netherlands, EIRE and Germany. Create a small Power BI comparison page, state the period and add a paragraph explaining why revenue alone cannot establish profitability. This is a concrete way to show you can adapt the project rather than only reproduce supplied steps.
