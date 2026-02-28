# Part 1 — Excel Workbook Structure (Offline-First)

## Workbook and sheet layout

Create one workbook: `Smart_Business_Data_System_MVP.xlsx` with these sheets:

1. `Sales_Data`
2. `Purchase_Data`
3. `Inventory`
4. `Expenses`
5. `Traders`
6. `Monthly_Overview`
7. `Lists` (helper sheet for dropdown values)

> Naming convention: all headers are database-ready (`snake_case`, no spaces).

---

## 1) Sheet: Sales_Data

### Columns

- `transaction_id`
- `date`
- `market` (Singa / Sabon_Gari)
- `trader_id`
- `product_name`
- `category` (FMCG / Agro)
- `quantity_sold`
- `unit_price`
- `total_sales` (auto)
- `payment_method` (Cash / Transfer / POS)

### Excel table

Convert to table and name it: `tbl_sales`.

### Formula

In `total_sales` column of `tbl_sales`:

```excel
=[@quantity_sold]*[@unit_price]
```

### Data validation

- `market`: list = `Singa,Sabon_Gari`
- `category`: list = `FMCG,Agro`
- `payment_method`: list = `Cash,Transfer,POS`
- `trader_id`: reference dynamic trader list from `tbl_traders[trader_id]`

---

## 2) Sheet: Purchase_Data

### Columns

- `purchase_id`
- `date`
- `trader_id`
- `supplier_name`
- `supplier_phone`
- `product_name`
- `quantity_bought`
- `unit_cost`
- `total_purchase_cost` (auto)

### Excel table

Name: `tbl_purchases`.

### Formula

In `total_purchase_cost`:

```excel
=[@quantity_bought]*[@unit_cost]
```

### Data validation

- `trader_id`: from `tbl_traders[trader_id]`
- `supplier_phone`: enforce text format to preserve leading zeros.

---

## 3) Sheet: Inventory

### Columns

- `product_name`
- `category`
- `opening_stock`
- `quantity_purchased`
- `quantity_sold`
- `current_stock` (auto)
- `reorder_level`
- `stock_status` (auto: OK / Restock_Needed)

### Excel table

Name: `tbl_inventory`.

### Formulas

In `current_stock`:

```excel
=[@opening_stock]+[@quantity_purchased]-[@quantity_sold]
```

In `stock_status`:

```excel
=IF([@current_stock]<=[@reorder_level],"Restock_Needed","OK")
```

### Data validation

- `category`: list = `FMCG,Agro`

### Conditional formatting (recommended)

- Highlight `stock_status = Restock_Needed` in red fill.
- Add icon set on `current_stock` vs `reorder_level`.

---

## 4) Sheet: Expenses

### Columns

- `expense_id`
- `date`
- `trader_id`
- `expense_category` (Transport, Rent, Staff, Misc)
- `amount`
- `notes`

### Excel table

Name: `tbl_expenses`.

### Data validation

- `expense_category`: list = `Transport,Rent,Staff,Misc`
- `trader_id`: from `tbl_traders[trader_id]`

---

## 5) Sheet: Traders

### Columns

- `trader_id`
- `trader_name`
- `market`
- `phone`
- `business_type`

### Excel table

Name: `tbl_traders`.

### Data validation

- `market`: `Singa,Sabon_Gari`
- `business_type`: `FMCG,Agro,Mixed`

---

## 6) Sheet: Monthly_Overview (simple summary)

Create month selector in `B1` (`YYYY-MM` format), then add KPI cards:

- Monthly Revenue
- Monthly Purchase Cost
- Monthly Expenses
- Gross Profit
- Active Traders

### Example formulas (Excel 365)

Assume `B1` contains start date of month, and `EOMONTH(B1,0)` is month end.

Monthly Revenue:

```excel
=SUMIFS(tbl_sales[total_sales],tbl_sales[date],">="&$B$1,tbl_sales[date],"<="&EOMONTH($B$1,0))
```

Monthly Purchase Cost:

```excel
=SUMIFS(tbl_purchases[total_purchase_cost],tbl_purchases[date],">="&$B$1,tbl_purchases[date],"<="&EOMONTH($B$1,0))
```

Monthly Expenses:

```excel
=SUMIFS(tbl_expenses[amount],tbl_expenses[date],">="&$B$1,tbl_expenses[date],"<="&EOMONTH($B$1,0))
```

Gross Profit:

```excel
=[Monthly Revenue]-[Monthly Purchase Cost]-[Monthly Expenses]
```

Active Traders:

```excel
=COUNTA(UNIQUE(FILTER(tbl_sales[trader_id],(tbl_sales[date]>=B1)*(tbl_sales[date]<=EOMONTH(B1,0)))))
```

---

## 7) Sheet: Lists (helper)

Keep lookup lists used by data validation:

- Markets
- Categories
- Payment Methods
- Expense Categories
- Business Types

Use named ranges for easy maintenance and future expansion.

---

## Scalability and migration readiness

- Add `*_id` keys everywhere to simplify migration to PostgreSQL.
- Keep one transaction per row (no merged cells, no subtotals in tables).
- Restrict free-text entries where possible with dropdowns.
- Archive old months by appending rows, not creating new sheets.
- This structure supports growth up to at least **5,000 traders** when loaded to Power BI using incremental refresh later.
