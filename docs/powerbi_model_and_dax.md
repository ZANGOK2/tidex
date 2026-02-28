# Part 2 & 3 — Power BI Model Design and Dashboard Blueprint

## Star schema (described)

### Fact tables

1. `Fact_Sales` (from `tbl_sales`)
   - Keys: `date_key`, `trader_id`, `market_id`, `product_id`
   - Measures: `quantity_sold`, `unit_price`, `total_sales`

2. `Fact_Purchases` (from `tbl_purchases`)
   - Keys: `date_key`, `trader_id`, `supplier_id`, `product_id`
   - Measures: `quantity_bought`, `unit_cost`, `total_purchase_cost`

3. `Fact_Expenses` (from `tbl_expenses`)
   - Keys: `date_key`, `trader_id`
   - Attributes: `expense_category`
   - Measure: `amount`

### Dimension tables

1. `Dim_Date`
   - `date_key`, `date`, `year`, `quarter`, `month_no`, `month_name`, `week_no`, `day_name`

2. `Dim_Product`
   - `product_id`, `product_name`, `category`

3. `Dim_Trader`
   - `trader_id`, `trader_name`, `market_id`, `phone`, `business_type`

4. `Dim_Market`
   - `market_id`, `market_name` (`Singa`, `Sabon_Gari`)

5. `Dim_Supplier`
   - `supplier_id`, `supplier_name`, `supplier_phone`

### Relationships

- `Dim_Date[date_key]` 1-* to each fact table (`Fact_Sales`, `Fact_Purchases`, `Fact_Expenses`)
- `Dim_Trader[trader_id]` 1-* to each fact table
- `Dim_Market[market_id]` 1-* to `Fact_Sales` (and optional to `Dim_Trader`)
- `Dim_Product[product_id]` 1-* to `Fact_Sales` and `Fact_Purchases`
- `Dim_Supplier[supplier_id]` 1-* to `Fact_Purchases`

Use **single direction filter** from dimensions to facts to avoid ambiguity.

---

## Part 3 — Dashboard pages

## Page 1: Executive Overview

Visuals:

- Card: `Total Revenue (Monthly)`
- Card: `Total Expenses`
- Card: `Gross Profit`
- Card: `Active Traders`
- Clustered column chart: `Revenue by Market`
- Slicer: month, market, category

## Page 2: Sales Analytics

Visuals:

- Line chart: `Daily Sales Trend`
- Line chart: `Weekly Sales Trend`
- Bar chart: `Top 10 Products by Revenue`
- Donut/stacked bar: `Category Performance (FMCG vs Agro)`

## Page 3: Inventory Intelligence

Visuals:

- Table/matrix: `Current Stock Levels`
- KPI: `% Products Near Reorder`
- Alert table: products where `current_stock <= reorder_level`

## Page 4: Supplier Analysis

Visuals:

- Bar chart: `Purchase Volume by Supplier`
- Card: `Supplier Dependency %` (largest supplier share)
- Line chart: `Average Purchase Cost Trend`

## Page 5: Profitability Analysis

Visuals:

- Combo chart: `Revenue vs Cost`
- Card: `Net Margin %`
- Stacked bar: `Cost Breakdown by Category/Expense`

---

## Part 3 — DAX measures (key metrics)

```DAX
Total Revenue = SUM(Fact_Sales[total_sales])
```

```DAX
Total Purchase Cost = SUM(Fact_Purchases[total_purchase_cost])
```

```DAX
Total Expenses = SUM(Fact_Expenses[amount])
```

```DAX
Gross Profit = [Total Revenue] - [Total Purchase Cost] - [Total Expenses]
```

```DAX
Net Margin % = DIVIDE([Gross Profit], [Total Revenue], 0)
```

```DAX
Active Traders = DISTINCTCOUNT(Fact_Sales[trader_id])
```

```DAX
Revenue MTD = TOTALMTD([Total Revenue], Dim_Date[date])
```

```DAX
Revenue by Market = [Total Revenue]
```
(Use `Dim_Market[market_name]` on axis.)

```DAX
Daily Sales Trend = [Total Revenue]
```
(Use `Dim_Date[date]` on axis.)

```DAX
Weekly Sales Trend =
CALCULATE(
    [Total Revenue],
    ALLEXCEPT(Dim_Date, Dim_Date[year], Dim_Date[week_no])
)
```

```DAX
Top Product Rank =
RANKX(
    ALL(Dim_Product[product_name]),
    [Total Revenue],
    , DESC,
    Dense
)
```

```DAX
Products At Risk =
COUNTROWS(
    FILTER(
        Inventory,
        Inventory[current_stock] <= Inventory[reorder_level]
    )
)
```

```DAX
Products At Risk % =
DIVIDE(
    [Products At Risk],
    COUNTROWS(Inventory),
    0
)
```

```DAX
Purchase Volume = SUM(Fact_Purchases[quantity_bought])
```

```DAX
Supplier Dependency % =
VAR TopSupplierVolume =
    MAXX(
        VALUES(Dim_Supplier[supplier_name]),
        [Purchase Volume]
    )
RETURN
DIVIDE(TopSupplierVolume, [Purchase Volume], 0)
```

```DAX
Avg Purchase Cost = AVERAGE(Fact_Purchases[unit_cost])
```

```DAX
Revenue vs Cost Gap = [Total Revenue] - ([Total Purchase Cost] + [Total Expenses])
```

---

## Model notes for 5,000 traders

- Keep dimensions clean and de-duplicated in Power Query.
- Add surrogate keys (`market_id`, `product_id`, `supplier_id`) in Power Query if absent.
- Disable Auto Date/Time in Power BI and use one central `Dim_Date` table.
- Plan incremental refresh once data volume crosses ~1M fact rows.
