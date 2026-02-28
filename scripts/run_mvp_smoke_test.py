#!/usr/bin/env python3
"""Offline smoke test for Smart Business Data System MVP CSV templates.

This verifies template integrity and computes a mini KPI snapshot from sample data.
"""

from __future__ import annotations

import csv
from collections import defaultdict
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "excel_templates"

REQUIRED_COLUMNS: Dict[str, List[str]] = {
    "sales_data.csv": [
        "transaction_id",
        "date",
        "market",
        "trader_id",
        "product_name",
        "category",
        "quantity_sold",
        "unit_price",
        "total_sales",
        "payment_method",
    ],
    "purchase_data.csv": [
        "purchase_id",
        "date",
        "trader_id",
        "supplier_name",
        "supplier_phone",
        "product_name",
        "quantity_bought",
        "unit_cost",
        "total_purchase_cost",
    ],
    "inventory.csv": [
        "product_name",
        "category",
        "opening_stock",
        "quantity_purchased",
        "quantity_sold",
        "current_stock",
        "reorder_level",
        "stock_status",
    ],
    "expenses.csv": [
        "expense_id",
        "date",
        "trader_id",
        "expense_category",
        "amount",
        "notes",
    ],
    "traders.csv": [
        "trader_id",
        "trader_name",
        "market",
        "phone",
        "business_type",
    ],
}

MARKETS = {"Singa", "Sabon_Gari"}
CATEGORIES = {"FMCG", "Agro"}
PAYMENT_METHODS = {"Cash", "Transfer", "POS"}


@dataclass
class SmokeResult:
    total_revenue: Decimal
    total_purchase_cost: Decimal
    total_expenses: Decimal
    gross_profit: Decimal
    active_traders: int
    revenue_by_market: Dict[str, Decimal]
    products_at_risk: int


def read_csv(name: str) -> List[dict]:
    path = TEMPLATES / name
    if not path.exists():
        raise FileNotFoundError(f"Missing required template: {path}")
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def d(value: str) -> Decimal:
    return Decimal(value.strip())


def assert_columns() -> None:
    for file_name, expected in REQUIRED_COLUMNS.items():
        rows = read_csv(file_name)
        headers = list(rows[0].keys()) if rows else expected
        if headers != expected:
            raise AssertionError(
                f"{file_name} column mismatch.\nExpected: {expected}\nActual:   {headers}"
            )


def assert_sales_rules(sales_rows: List[dict]) -> None:
    for row in sales_rows:
        if row["market"] not in MARKETS:
            raise AssertionError(f"Invalid market in sales_data.csv: {row['market']}")
        if row["category"] not in CATEGORIES:
            raise AssertionError(f"Invalid category in sales_data.csv: {row['category']}")
        if row["payment_method"] not in PAYMENT_METHODS:
            raise AssertionError(
                f"Invalid payment_method in sales_data.csv: {row['payment_method']}"
            )

        expected_total = d(row["quantity_sold"]) * d(row["unit_price"])
        actual_total = d(row["total_sales"])
        if expected_total != actual_total:
            raise AssertionError(
                f"total_sales mismatch for {row['transaction_id']}: "
                f"expected {expected_total}, got {actual_total}"
            )


def assert_purchase_rules(purchase_rows: List[dict]) -> None:
    for row in purchase_rows:
        expected_total = d(row["quantity_bought"]) * d(row["unit_cost"])
        actual_total = d(row["total_purchase_cost"])
        if expected_total != actual_total:
            raise AssertionError(
                f"total_purchase_cost mismatch for {row['purchase_id']}: "
                f"expected {expected_total}, got {actual_total}"
            )


def assert_inventory_rules(inventory_rows: List[dict]) -> int:
    at_risk = 0
    for row in inventory_rows:
        expected_stock = (
            d(row["opening_stock"]) + d(row["quantity_purchased"]) - d(row["quantity_sold"])
        )
        actual_stock = d(row["current_stock"])
        if expected_stock != actual_stock:
            raise AssertionError(
                f"current_stock mismatch for {row['product_name']}: "
                f"expected {expected_stock}, got {actual_stock}"
            )

        expected_status = "Restock_Needed" if actual_stock <= d(row["reorder_level"]) else "OK"
        if row["stock_status"] != expected_status:
            raise AssertionError(
                f"stock_status mismatch for {row['product_name']}: "
                f"expected {expected_status}, got {row['stock_status']}"
            )
        if expected_status == "Restock_Needed":
            at_risk += 1
    return at_risk


def run_smoke_test() -> SmokeResult:
    assert_columns()

    sales = read_csv("sales_data.csv")
    purchases = read_csv("purchase_data.csv")
    inventory = read_csv("inventory.csv")
    expenses = read_csv("expenses.csv")

    assert_sales_rules(sales)
    assert_purchase_rules(purchases)
    products_at_risk = assert_inventory_rules(inventory)

    total_revenue = sum((d(r["total_sales"]) for r in sales), Decimal("0"))
    total_purchase_cost = sum((d(r["total_purchase_cost"]) for r in purchases), Decimal("0"))
    total_expenses = sum((d(r["amount"]) for r in expenses), Decimal("0"))
    gross_profit = total_revenue - total_purchase_cost - total_expenses
    active_traders = len({r["trader_id"] for r in sales})

    revenue_by_market: Dict[str, Decimal] = defaultdict(lambda: Decimal("0"))
    for row in sales:
        revenue_by_market[row["market"]] += d(row["total_sales"])

    return SmokeResult(
        total_revenue=total_revenue,
        total_purchase_cost=total_purchase_cost,
        total_expenses=total_expenses,
        gross_profit=gross_profit,
        active_traders=active_traders,
        revenue_by_market=dict(revenue_by_market),
        products_at_risk=products_at_risk,
    )


def main() -> None:
    result = run_smoke_test()
    print("[PASS] Template schema and calculation checks passed.")
    print("KPI Snapshot (sample rows):")
    print(f"- Total Revenue: {result.total_revenue}")
    print(f"- Total Purchase Cost: {result.total_purchase_cost}")
    print(f"- Total Expenses: {result.total_expenses}")
    print(f"- Gross Profit: {result.gross_profit}")
    print(f"- Active Traders: {result.active_traders}")
    print(f"- Products At Risk: {result.products_at_risk}")
    print("- Revenue by Market:")
    for market, amount in sorted(result.revenue_by_market.items()):
        print(f"  - {market}: {amount}")


if __name__ == "__main__":
    main()
