# Bronze Layer

The Bronze layer is the first step in the pipeline. It takes the raw files from the landing zone and loads them into Delta tables without any transformations.

## What It Does

- Reads CSV and JSON files from the Databricks Volume (`/Volumes/dev/electroflow_pipeline/landing_data/`)
- Converts them to Delta format
- Adds metadata columns for traceability:
  - `_ingestion_timestamp` — when the data was loaded
  - `_source_file_path` — which file it came from
  - `_ingestion_job_id` — unique ID for the run
- Saves everything as managed tables in Unity Catalog (`dev.electroflow_pipeline.bronze_*`)

## Why No Cleaning?

The Bronze layer is meant to be a raw copy. I don't want to lose any data at this stage — even if it has duplicates or messy formats. All the cleaning happens in Silver.

## Tables Created

| Table | Source File |
|:---|:---|
| `bronze_customers` | `customers.csv` |
| `bronze_products` | `products.csv` |
| `bronze_orders` | `orders.json` |
| `bronze_payments` | `order_payments.csv` |
| `bronze_coupons` | `coupons.csv` |
