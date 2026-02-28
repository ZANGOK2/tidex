# Part 4 — Technical Implementation Instructions

## 1) Excel setup (offline workflow)

1. Open Excel on trader laptop/desktop (no internet required).
2. Import each CSV from `excel_templates/` as a dedicated sheet.
3. Convert each dataset to structured table (`Ctrl+T`).
4. Apply formulas and validation rules from `docs/excel_workbook_design.md`.
5. Protect formula columns (`total_sales`, `total_purchase_cost`, `current_stock`, `stock_status`) to reduce accidental edits.
6. Save workbook locally and backup daily to USB/external drive.

### Suggested file naming

- Daily working file: `kano_trade_ops_YYYYMM.xlsx`
- Monthly archive: `kano_trade_archive_YYYYMM.xlsx`

## 2) Power BI connection

1. Open Power BI Desktop.
2. Get Data → Excel → select workbook.
3. Load `tbl_sales`, `tbl_purchases`, `tbl_expenses`, `tbl_inventory`, `tbl_traders`.
4. In Power Query:
   - Set data types explicitly (date, whole number, decimal, text).
   - Trim and clean text (`market`, `category`, `supplier_name`, `product_name`).
   - Build dimension tables by de-duplicating keys.
5. Build star schema relationships exactly as documented in `docs/powerbi_model_and_dax.md`.
6. Add DAX measures and dashboard pages.

## 3) Data quality controls for local market reality

- Enforce dropdowns to limit spelling differences (e.g., `Sabon_Gari` vs `Sabongari`).
- Use mandatory IDs (`transaction_id`, `purchase_id`, `expense_id`, `trader_id`) to avoid duplicate counting.
- For phone numbers, store as text for Nigerian formats (`080...`, `+234...`).
- Add weekly reconciliation process:
  - Sales totals vs cashbook
  - Purchases vs supplier invoices
  - Stock balance vs physical count

## 4) PostgreSQL migration readiness

This MVP is migration-ready because:

- Column names already use `snake_case`.
- Facts and dimensions are logically separated.
- Each row represents atomic business events.
- IDs are included for joins and future ETL.

### Suggested future PostgreSQL tables

- `fact_sales`
- `fact_purchases`
- `fact_expenses`
- `dim_date`
- `dim_product`
- `dim_trader`
- `dim_market`
- `dim_supplier`

## 5) Rollout plan for Kano markets

### Phase 1 (Week 1)

- Pilot with 10 traders each in Singa and Sabon Gari.
- Train one market supervisor per market.
- Validate ease of daily entry and data quality.

### Phase 2 (Weeks 2–4)

- Expand to 100+ traders.
- Weekly dashboard reviews with trader groups.
- Refine product naming and supplier master data.

### Phase 3 (Month 2+)

- Expand toward full target (up to 5,000 traders).
- Centralize files in controlled sync folder when connectivity permits.
- Introduce automated ETL to PostgreSQL and published Power BI Service reports.

## 6) Practical KPI usage for traders

- **Revenue by market**: compare Singa vs Sabon Gari demand patterns.
- **Top products**: identify fast movers in FMCG and Agro lines.
- **Stock risk alerts**: prevent lost sales due to stock-outs.
- **Supplier dependency**: reduce risk from over-reliance on one supplier.
- **Net margin tracking**: improve pricing and cost control decisions.
