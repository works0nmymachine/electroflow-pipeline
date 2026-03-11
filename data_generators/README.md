# Data Generators

Python scripts that create realistic mock data for the pipeline. Everything outputs to `data/raw/`.

## Scripts

| Script | Output | Notes |
|:---|:---|:---|
| `generate_customers.py` | `customers.csv` | GDP-weighted country selection, localized names and addresses |
| `generate_products.py` | `products.csv` | Belsimpel-style product catalog (phones, accessories, audio) |
| `generate_orders.py` | `orders.json` | Nested JSON with funnel timestamps and order items |
| `generate_order_payments.py` | `order_payments.csv` | 1 payment per order, only Klarna supports installments |
| `generate_coupons.py` | `coupons.csv` | Campaign-based discount codes |
| **`run_all.py`** | **All of the above** | **Runs everything in the correct order with integrity checks** |

## Utilities

- `utils/integrity_utils.py` — Makes sure every order references a real customer and product ID
- `utils/scrape_gdp.py` — Scrapes GDP data from Wikipedia for the country weighting logic

## How to Run

```bash
python data_generators/run_all.py
```

This runs the generators in dependency order (customers & products first, then orders, then payments) and validates referential integrity along the way.
