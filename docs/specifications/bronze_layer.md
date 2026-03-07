# 🥉 ElectroFlow: Bronze Layer Documentation

The **Bronze Layer** is the first stop for data in our Medallion Architecture. Its primary job is to ingest raw data from the **Landing Zone** while preserving history and providing a stable foundation for downstream cleaning.

## 🎯 Primary Goals
- **Zero-Loss Ingestion**: We load data exactly as it was received. No cleaning or filtering happens here.
- **Modernization**: Convert raw CSV and JSON files into the **Delta Lake** format.
- **Metadata Enrichment**: Add lineage information (ingestion timestamp, source file name).
- **History Tracking**: Maintain an immutable history of all data loads.

---

## 🏗️ Implementation Guidelines

### 1. File Format Normalization
While the landing zone contains mixed formats (CSV, JSON), the Bronze layer consolidates everything into **Delta**. This provides:
- **ACID Transactions**: No partial or corrupted writes.
- **Time Travel**: Allows us to query data as it looked at a specific point in time.
- **Schema Evolution**: Handles unexpected changes in source file structures.

### 2. Standard Metadata Columns
Every Bronze table MUST include the following technical metadata:
- `_ingestion_timestamp`: UTC time of the data load.
- `_source_file_path`: Path to the original file in Landing.
- `_ingestion_job_id`: Unique identifier for the run.

---

## 🛠️ Typical Loading Logic (Landing ➡️ Bronze)
1. **Discover**: Identify new files in [**`00_landing/raw/`**](electroflow-pipeline/00_landing/raw/).
2. **Schema Influx**: Read the files with `inferSchema=true` or use a curated schema.
3. **Metadata**: Use `withColumn()` to inject the required audit fields.
4. **Append**: Save the result to [**`01_bronze/delta/`**](electroflow-pipeline/01_bronze/delta/) using `.mode("append")`.

## 📜 Next Steps
After data is captured in Bronze, it moves to the **Silver Layer** where we perform deduplication, enforce schemas, and resolve data quality issues found in the mock generation process (like missing phone numbers).

---
*For more details on the final data structure, see the [Gold Layer Guide](electroflow-pipeline/docs/specifications/gold_layer.md) (coming soon).*
