# Smart Business Data System – Trade Intelligence for Kano Markets (MVP)

This repository contains a practical MVP blueprint for FMCG and Agro traders in **Singa Market** and **Sabon Gari Market** using:

- **Microsoft Excel** for offline data capture.
- **Power BI** for analytics and dashboards.

## Deliverables in this repo

1. Excel-ready templates (`excel_templates/*.csv`) with database-ready column names.
2. Workbook build instructions with formulas, data validation, and Monthly Overview.
3. Power BI star schema design and relationship map.
4. DAX measures for executive, sales, inventory, supplier, and profitability analysis.
5. Implementation and rollout instructions tailored for Northern Nigerian market operations.

## Quick start

1. Open Excel and create a workbook named `Smart_Business_Data_System_MVP.xlsx`.
2. Import each CSV in `excel_templates/` into separate sheets.
3. Convert each range to **Excel Table** (`Ctrl+T`) using table names provided in `docs/excel_workbook_design.md`.
4. Apply formulas/data validation from the design guide.
5. Connect Power BI Desktop to the workbook and implement model + measures from `docs/powerbi_model_and_dax.md`.

## Files

- `docs/excel_workbook_design.md`
- `docs/powerbi_model_and_dax.md`
- `docs/implementation_guide.md`
- `excel_templates/sales_data.csv`
- `excel_templates/purchase_data.csv`
- `excel_templates/inventory.csv`
- `excel_templates/expenses.csv`
- `excel_templates/traders.csv`

## Offline smoke test (run it locally)

To validate template schemas and sample KPI math end-to-end:

```bash
python scripts/run_mvp_smoke_test.py
```

This checks:
- Required column names for all template files.
- Auto-calculation fields (`total_sales`, `total_purchase_cost`, `current_stock`, `stock_status`) against expected logic.
- Domain values for market/category/payment method.
- A sample KPI snapshot (revenue, costs, profit, active traders, stock risk, revenue by market).
