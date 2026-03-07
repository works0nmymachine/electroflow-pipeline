# ElectroFlow Pipeline: Data Generation Specifications

This document outlines the requirements and logic for the mock data generation layer of the ElectroFlow project.

## 1. Customer Generation (`generate_customers.py`)

The customer dataset serves as the source of truth for all user-related analysis.

### Required Rules
- **Reference Data**: Located in [**`electroflow-pipeline/data_generators/ultils_data/`**](electroflow-pipeline/data_generators/ultils_data/). Must use `landcode currency language phone.xlsx` for geographical accuracy and `country_gdp_data.xlsx` for probability weighting.
- **GDP-Weighted Selection**: 
    - Selection probability is calculated as: `(Normalized_Nominal_GDP * 0.7) + (Normalized_GDP_Per_Capita * 0.3)`.
    - Data is scraped from Wikipedia (IMF, World Bank, and UN sources) and averaged.
- **Geographic Consistency**: 
    - `Country`, `CountryCode`, `City`, `State_Province`, and `Postal_Code` are generated using localized Faker providers to ensure realistic geographical data.
    - `Phone numbers` must be prefixed with the correct international dial code from the reference file.
- **Gender & Name Logic**: 
    - Names must be gender-consistent (e.g., male names for male gender).
    - Email addresses must be derived from the name (e.g., `first.last@domain.com`).
- **Data Messiness (for training)**:
    - 10% chance of missing phone numbers.
    - Mixed date formats (`YYYY-MM-DD` vs `MM/DD/YYYY`) to practice cleaning.
    - 5% intentional duplicate records for deduplication practice.

---

## 2. Order Generation (`generate_orders.py`)

The order dataset represents transactional activity.

### Required Rules
- **Referential Integrity**: 
    - **Crucial**: Every `customer_id` in the orders file MUST exist in the `customers.csv` file. 
    - If no customers exist yet, the script must fail or trigger the customer generator.
- **Data Structure**:
    - Format: Nested JSON.
    - Hierarchy: One order contains a list of 1-4 items.
- **Item Logic**:
    - Each item includes `product_id`, `quantity`, and `unit_price`.

---

## 3. Integrity Layer (`integrity_utils.py`)

To prevent "orphan" records (e.g., an order for a customer that doesn't exist), we use a helper utility.

### Integrity Rules
- **Cross-Reference Checking**: Before generating a child record (like an Order), the script must check the parent file (Customers or Products).
- **ID Matching**: Only IDs that actually exist in the parent CSV/JSON are allowed to be used in the child files.
- **Fail-Fast**: Scripts will stop and report an error if a required parent file is missing.

## 4. Directory Structure
All generated raw data is stored in:
`electroflow-pipeline/00_landing/raw/`

## 5. How to Run the Pipeline
1. Run [**`electroflow-pipeline/data_generators/generate_customers.py`**](electroflow-pipeline/data_generators/generate_customers.py) and [**`electroflow-pipeline/data_generators/generate_products.py`**](electroflow-pipeline/data_generators/generate_products.py) first.
2. Run [**`electroflow-pipeline/data_generators/generate_orders.py`**](electroflow-pipeline/data_generators/generate_orders.py) last (as it depends on the first two).
