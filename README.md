# ElectroFlow Pipeline

My first data engineering project. I built a full end-to-end pipeline using the **Medallion Architecture** on **Databricks**, going from raw mock data all the way to a Star Schema ready for **Power BI**.

## Project Structure

```
├── data_generators/       # Python scripts that generate realistic mock data
├── 01_bronze/             # Raw ingestion — CSV/JSON into Delta tables
├── 02_silver/             # Cleaning — deduplication, type casting, normalization
├── 03_gold/               # Business layer — Star Schema (dims + facts)
├── data/raw/              # Local output folder for generated data (not synced to Databricks)
└── docs/                  # Specifications and documentation
```

## How It Works

1. **Generate** mock data locally with `data_generators/run_all.py`
2. **Upload** the CSV/JSON files to a Databricks Volume (`/Volumes/dev/electroflow_pipeline/landing_data/`)
3. **Run** the notebooks in order: Bronze → Silver → Gold
4. **Connect** Power BI to the Gold tables in Unity Catalog

## Tech Stack

- **Databricks** (Unity Catalog, Delta Lake, PySpark)
- **Python** (Pandas, Faker) for data generation
- **Power BI** for dashboards (coming soon)

## Quick Start

```bash
# Set up a virtual environment
python3 -m venv .venv
source .venv/bin/activate
pip install pandas faker openpyxl numpy

# Generate all mock data in one go
python data_generators/run_all.py
```

This creates `customers.csv`, `products.csv`, `orders.json`, `order_payments.csv`, and `coupons.csv` inside `data/raw/`.
