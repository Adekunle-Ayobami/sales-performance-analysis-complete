# Start-to-finish walkthrough

This guide assumes Windows, matching your desktop setup. VS Code is where you organise files, read the analysis and run optional scripts. Excel opens the workbook, MySQL executes SQL, and Power BI Desktop builds the report. VS Code does not replace those applications.

## 1. Understand the question before opening the tools

Imagine a retail manager asking: 'Which months, products, countries and customers drive sales, and what should we review next?' Your job is to define reliable measures, check the data, analyse the evidence and explain decisions. You are not just making attractive charts.

Read README.md, docs/DATA_DICTIONARY.md and reports/findings.md first. Learn why invoice lines are not orders, why negative quantities remain in the ledger, why unidentified customers are retained in sales, and why December 2011 is partial. Write your own two-sentence business objective in the README.

**Finish this step when:** you can explain gross sales, credits, net revenue, orders and repeat customers without reading the definitions.

## 2. Extract and open the project

1. Download the ZIP and right-click it in File Explorer. Choose Extract All.
2. Put the extracted project in a stable folder such as `C:\Users\YOUR_NAME\Documents\sales-performance-analysis`. Avoid leaving it inside the ZIP.
3. Open VS Code. Choose File > Open Folder and select the folder containing README.md, data, sql and powerbi. The correct folder is the project root; do not open its parent by mistake.
4. Click README.md in the Explorer. Use the preview button, or Ctrl+Shift+V, to read the formatted document.
5. Open Terminal > New Terminal. The terminal path should end in the project folder.

The original public dataset is already included. You do not need a Kaggle account or another download. It contains 541,909 source rows, so importing it may take a few minutes.

**Finish this step when:** all project folders are visible in VS Code and you can open reports/findings.md.

## 3. Install the applications you need

- VS Code: https://code.visualstudio.com/
- Git for Windows: https://git-scm.com/downloads/win
- MySQL Community Server: https://dev.mysql.com/downloads/mysql/
- MySQL Workbench: https://dev.mysql.com/downloads/workbench/
- Power BI Desktop: https://www.microsoft.com/en-us/download/details.aspx?id=58494 or the Microsoft Store.
- Excel desktop with Power Query: use your existing Microsoft Office installation.
- Optional Python: https://www.python.org/downloads/windows/ . Select the installer option to add Python to PATH if available.

MySQL Workbench is the client application. You also need a running MySQL server. During local setup, choose a password you can remember and keep it outside the project files. Use MySQL 8 or later because the analysis uses common table expressions and window functions.

Open Excel, Power BI and Workbench once to check they start. In the VS Code terminal run `git --version`. If Git is not recognised, restart VS Code after installation. Python is optional because all cleaned data and results are included.

**Finish this step when:** the applications open, Git reports a version, and Workbench connects to your local server.

## 4. Explore the completed Excel workbook

Open excel/Sales_Performance_Analysis.xlsx in Excel. Start with Summary, then Monthly, Countries, Invoice items, Customer segments and Quality. The Learning sample contains 5,000 selected lines to practise row-level formulas. **The sample is not the source of the full-data headline figures.** All business summaries use full-dataset aggregates.

Check these numbers in Summary:

| Measure | Expected result |
|---|---:|
| Gross sales | £10,642,110.80 |
| Credit value | £893,979.73 |
| Net revenue | £9,748,131.07 |
| Orders | 19,960 |
| Known customers | 4,338 |
| Repeat customer rate | 65.6% |

Click formula cells and read the formula bar. Monthly net revenue is gross sales minus credits; AOV is sales divided by orders; growth compares consecutive complete months. Quality contains independent reconciliation differences that should be £0.00.

Practise on a copy of the Learning sample: change one positive quantity and watch line revenue and sale revenue update. Change it back. Do not describe sample totals as full-dataset totals.

The delivered workbook is a summary snapshot. Changing the external CSV does not automatically refresh it. To update it after rebuilding, replace the **input** values in Monthly (month, sales, credits, orders, completion flag), Countries (country, sales, credits) and Customer segments (type, customers, orders, sales), retaining formula columns. For new months/countries, extend formulas, tables and chart ranges. Keep Summary's order/customer inputs consistent with metrics.json. A separate Power Query workbook is preferable for a recurring production report.

**Finish this step when:** you can trace at least three headline results back to their source summaries and explain both reconciliation checks.

## 5. Reproduce the cleaning in Excel Power Query

This step is important if you want to say you used Excel/Power Query for cleaning rather than only opened a supplied workbook.

1. Create a new Excel workbook. Save it as excel/Power_Query_Practice.xlsx.
2. Choose Data > Get Data > From Other Sources > Blank Query. In Power Query Editor, use Home > Manage Parameters > New Parameter.
3. Name the parameter **ProjectFolder**, set Type to Text, and enter your actual extracted project path, without a trailing slash.
4. Create another blank query. Name it **SalesClean**. Open Advanced Editor, replace its contents with excel/Clean_raw_retail.pq, and select Done.
5. Review the Applied Steps. Understand what each removes or adds. Enable column quality/distribution/profiling if useful; when checking completeness, set profiling to the entire dataset rather than only the first 1,000 rows.
6. Choose Close & Load To. For the full dataset, use Only Create Connection and Add this data to the Data Model, where your Excel edition supports it. You may instead load the 534,129 rows to a worksheet; they fit within Excel's row limit but can make the workbook large and slower.
7. Verify the query has 534,129 rows. Sum SaleRevenue, CreditValue and LineRevenue using PivotTables/Data Model or worksheet sums. Match the expected totals.

The M query uses the same documented rules, but it has not been executed in your Excel version here. If a total differs, inspect duplicates, numeric types, missing IDs and filters before claiming agreement. Table.Distinct does not promise which duplicate instance or row order survives, so LineID can differ without changing sums.

Build a PivotTable with YearMonth in Rows and SaleRevenue in Values. Use Sum, not Count. Build another with Country in Rows and SaleRevenue in Values. Sort descending. Distinct invoice counts require the Data Model's Distinct Count option; an ordinary Count of InvoiceNo counts lines and is wrong for orders. Save two screenshots showing your own cleaning steps and PivotTables.

**Finish this step when:** your cleaning and totals match, and you can explain each Applied Step.

## 6. Load and analyse the data in MySQL

1. Open Workbench and connect to your local MySQL server.
2. Use File > Open SQL Script to open sql/01_schema.sql. Execute it with the lightning button. Refresh the Schemas panel and expand retail_portfolio > Tables > sales.
3. Import data/processed/sales_clean.csv into the existing sales table. Use the Table Data Import Wizard from the table/schema context menu. CSV headers correspond to the 16 columns in 01_schema.sql. Ensure IDs are text, money has four decimals, dates are date/datetime and the first row is treated as headers. Full import can take time; do not start a second import while the first runs.
4. Alternatively, edit the file path in sql/02_load.sql and use LOAD DATA LOCAL INFILE when both the client and your trusted local server allow it. The default path is a placeholder. If LOCAL is disabled, use the wizard instead of changing unrelated global settings.
5. Run `SELECT COUNT(*) FROM retail_portfolio.sales;`. Expected result: **534129**. Check import warnings. An incomplete import must be fixed before analysis. If restarting an import, use a fresh project table or deliberately clear only that project table after checking its identity; do not delete unrelated databases.
6. Open sql/03_analysis.sql. Execute one query at a time by selecting that query's text and running it. Read the result before moving to the next.
7. Run sql/04_validation.sql. Compare results to data/processed/metrics.json. Unique line IDs should equal row count, invalid/classification-error counts should be zero and the revenue bridge difference should be zero.
8. Run sql/05_merchandise.sql. Notice why the result differs from the unfiltered invoice-item ranking.
9. Export selected result grids as CSV or save screenshots of the monthly, country and product outputs. Put your evidence in reports/. Do not replace the reference CSVs with results from a partial import.

Learn these SQL concepts from the supplied queries: SUM aggregates amounts; GROUP BY creates meaningful summaries; DISTINCT prevents counting invoice lines as orders; CASE defines conditional metrics; NULLIF prevents division by zero; WITH organises steps; LAG finds the previous month's value; a window SUM calculates total-country share without collapsing rows.

**Finish this step when:** every validation result matches, and you can explain at least the monthly, country and customer queries.

## 7. Build the Power BI model

Power BI Desktop runs locally on Windows. There is no native PBIX in the supplied package, so this is the required desktop completion step.

1. Open Power BI Desktop and create a blank report.
2. Choose Get Data > Text/CSV and select data/processed/sales_clean.csv. Choose Transform Data, not immediate Load, so you can inspect types.
3. Rename the query **Sales**. Set InvoiceNo, StockCode, Description, CustomerID, Country and YearMonth to Text. Set Quantity, LineID, IsSale and PeriodComplete to Whole Number. Set InvoiceDate to Date/Time and InvoiceDay to Date. Set price/revenue fields to Decimal Number; do not round the underlying values to two decimals.
4. Alternatively, create the ProjectFolder text parameter in Power Query and paste powerbi/Sales_from_clean_csv.pq into a blank query named Sales. This supplies the types and blank-ID handling. Use either import route, not both.
5. Choose Close & Apply. Create the Date calculated table by copying only its definition from measures.dax into Modeling > New Table.
6. Select the Date table and use Mark as date table, choosing Date[Date]. In Model view, create an active one-to-many relationship from Date[Date] to Sales[InvoiceDay], with single-direction filtering from Date to Sales. InvoiceDay is date-only; joining to InvoiceDate timestamps would fail to match most rows.
7. Create every measure separately with Modeling > New Measure. Copy one expression at a time from measures.dax. Create the Date table before the previous-month measures.
8. Format money measures as GBP, counts as whole numbers and rates as percentages with one decimal. Use formatting for display; do not change the underlying source values.
9. Import the report theme from powerbi/theme.json through View > Themes > Browse for themes.

A direct MySQL connection is optional. The CSV route is simpler and sufficient to demonstrate SQL analysis plus Power BI reporting. Microsoft documents that its MySQL connector requires Oracle's MySQL Connector/NET. Use the documented connector only if you choose the direct database route.

**Finish this step when:** the Sales and Date tables are related correctly and a Gross Sales card matches £10,642,110.80 with no filters.

## 8. Build, validate and save the Power BI report

Follow powerbi/REPORT_SPECIFICATION.md for the three pages: Sales overview, Products and credits, Customer behaviour and quality. It specifies fields, measures, filters, sorting, labels and full-period snapshot charts.

For each visual, select the chart type and drag the specified field/measure into its axis/value slots. For Top N charts, open the visual's Filters pane, choose Top N, enter 10, drag the revenue measure into By value and apply the filter. For a monthly chart use Date[YearMonth] itself, sorted ascending. A month name alone would mix years or sort alphabetically.

Add a date range slicer and country dropdown. Select UK and confirm the chart/card changes. Clear the filter and reconcile headline cards to metrics.json. Known Customers should be 4,338 and Repeat Customers 2,845 for the full period. Customer repeat status changes under date/product filters; label that context clearly. Snapshot customer/product charts are explicitly full-period and are not connected to these slicers.

Save the report as powerbi/Sales_Performance.pbix. Save screenshots of all three actual Power BI pages into reports/, for example powerbi_overview.png. Add one of those screenshots near the top of README.md and explain the model/measures in your own words. The supplied analysis_dashboard.png is a reference-analysis figure, not Power BI evidence.

**Finish this step when:** the PBIX opens, refreshes successfully from your folder, filters work and all unfiltered reconciliation measures match. A shareable screenshot is enough for recruiters to view the dashboard; they do not need Power BI installed to see it.

## 9. Optional: run the reproducible Python reference

In the VS Code terminal, from the project root:

```powershell
py -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe scripts\build_analysis.py
.venv\Scripts\python.exe scripts\build_report.py
```

Using the virtual environment's Python directly avoids PowerShell activation-policy problems. The first script reads the original workbook, rebuilds outputs and performs independent SQLite arithmetic checks. The second creates the report and figures. These scripts are supporting automation, not substitutes for learning Excel, SQL and Power BI. They do not regenerate the delivered Excel workbook or a PBIX.

**Finish this step when:** both commands succeed and reports/validation.md is present. If you skip this step, you can still finish the intended Excel/MySQL/Power BI project.

## 10. Publish to your GitHub account using VS Code

Create a GitHub account at https://github.com if you do not have one. Sign in through VS Code when prompted. Publication is done from your computer; no repository has been created for you by this package.

### Option A: VS Code buttons

1. Open the project root in VS Code. Choose Source Control in the left sidebar.
2. Select Initialize Repository. Review changes; .gitignore excludes .venv and temporary/intermediate files.
3. If Git asks for identity, set your name and GitHub-associated email using the commands below. A GitHub-provided no-reply email is also valid.
4. Stage the intended project files with the + button. Enter a commit message such as 'Add retail sales analysis, workbook and SQL'. Select Commit.
5. Select Publish Branch/Publish to GitHub. Authorise VS Code's GitHub sign-in. Name the repository sales-performance-analysis and choose Public if you want recruiters to view it without requesting access.
6. Open the resulting repository in your browser and verify README, charts, SQL and workbook are present. Add your completed PBIX and screenshots before describing the report as completed.

### Option B: terminal commands

Create a new **empty** repository on GitHub named sales-performance-analysis. Do not initialise it with a README, .gitignore or licence because those files are already local. Copy the repository's HTTPS URL from GitHub.

```powershell
git config --global user.name "YOUR NAME"
git config --global user.email "YOUR GITHUB EMAIL"
git init
git add .
git commit -m "Add retail sales analysis, workbook and SQL"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/sales-performance-analysis.git
git push -u origin main
```

Replace placeholders. Run each line separately. Git may open a browser authentication window; complete that sign-in. Do not paste passwords or access tokens into project files. If origin already exists, inspect it with `git remote -v` rather than adding another origin. If the remote was accidentally initialised with files, resolve that history normally instead of force-pushing.

Use Git rather than browser uploads for the full clean CSV: it exceeds the browser's single-file upload limit, while individual supplied data files are below GitHub's 100 MiB Git-file limit. Before adding a PBIX, check its size. For a report above that limit, use Git LFS or keep screenshots, measures and report instructions in the repository and provide the large report through an appropriate download location.

Add a repository description: 'Retail sales analysis using Excel, SQL/MySQL and Power BI, covering revenue trends, country performance and customer behaviour.' Add relevant topics such as sql, power-bi, excel and data-analysis. Pin the repository on your GitHub profile. Replace the desktop-completion status in README only after finishing those steps.

**Finish this step when:** the public link opens in a signed-out browser, README images load and the expected files are visible.

## 11. Make it your work and update your CV

Read docs/CV_AND_INTERVIEW.md. Add your completed project under Portfolio Projects, with its direct GitHub URL. Do not list it under Latrims employment or imply that a retailer hired you.

Before using the completed-project wording, personally run the desktop stages, explain the definitions, write at least one extra query and add one meaningful visual or question. For example, compare AOV and credit exposure between the UK and the Netherlands. Record the result and its limitations. You do not need to disguise assistance: the useful evidence is that you can understand, reproduce and adapt the work.

## Final checklist

- [ ] I can explain the business question and source.
- [ ] My Excel/Power Query cleaning and totals reconcile.
- [ ] My MySQL import contains 534,129 rows and validation passes.
- [ ] My Power BI model, measures and filters work.
- [ ] I saved a native PBIX and actual report screenshots.
- [ ] My recommendations distinguish evidence from proposed actions.
- [ ] My GitHub README accurately describes completed work.
- [ ] My CV links to the repository and makes no unsupported impact claims.

## Official references

- UCI dataset and licence: https://archive.ics.uci.edu/dataset/352/online+retail
- MySQL Workbench import: https://dev.mysql.com/doc/workbench/en/wb-admin-export-import-table.html
- Power BI data import: https://learn.microsoft.com/en-us/power-bi/connect-data/desktop-quickstart-connect-to-data
- Date tables: https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-date-tables
- MySQL Power Query connector: https://learn.microsoft.com/en-us/power-query/connectors/mysql-database
- GitHub existing-project publication: https://docs.github.com/en/migrations/importing-source-code/using-the-command-line-to-import-source-code/adding-locally-hosted-code-to-github
