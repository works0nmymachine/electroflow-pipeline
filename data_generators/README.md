# 🛠️ Data Generation Toolkit

This folder contains Python scripts and reference data used to generate a realistic, high-quality mock dataset for the ElectroFlow pipeline.

## 🚀 Core Generation Scripts

| File | Purpose | Key Feature |
| :--- | :--- | :--- |
| [**`generate_customers.py`**](electroflow-pipeline/data_generators/generate_customers.py) | Creates the `customers.csv` master file. | Uses **GDP-weighted country selection** (70% Nominal GDP, 30% GDP Per Capita) and localized `Faker` profiles for realistic names, cities, and postcodes. |
| [**`generate_products.py`**](electroflow-pipeline/data_generators/generate_products.py) | Creates the `products.csv` reference file. | Generates random catalog items across categories like Electronics, Tools, and Home Appliances. |
| [**`generate_orders.py`**](electroflow-pipeline/data_generators/generate_orders.py) | Creates the `orders.json` transactional file. | Enforces **Referential Integrity**: Every order is linked to a valid `customer_id` and contains valid `product_id`s. |
| [**`generate_order_payments.py`**](electroflow-pipeline/data_generators/generate_order_payments.py) | Creates `order_payments.csv`. | Splits order totals into 1 or more payment methods (credit card, voucher, etc.). |
| [**`generate_coupons.py`**](electroflow-pipeline/data_generators/generate_coupons.py) | Creates `coupons.csv`. | Generates marketing campaign codes (e.g., Black Friday) with discount percentages and validity dates. |

---

## 🔧 Utilities & Reference Data

### [**`utils/`**](electroflow-pipeline/data_generators/utils/)
- **`scrape_gdp.py`**: A powerful web-scraping script that fetches the latest economic data from Wikipedia (IMF, WB, UN sources) to refine our generation weights.
- **`integrity_utils.py`**: A helper module that ensures children records (like Orders) are correctly linked to existing parent records (like Customers/Products).

### [**`ultils_data/`**](electroflow-pipeline/data_generators/ultils_data/)
- **`landcode currency language phone.xlsx`**: The master source for geographical mapping.
- **`country_gdp_data.xlsx`**: The output of the scraper, containing GDP rankings, weights, and country codes.

---

## 🏗️ How to run
1. Start by updating the economic statistics (optional):
   `python data_generators/utils/scrape_gdp.py`
2. Generate base entities:
   `python data_generators/generate_customers.py`
   `python data_generators/generate_products.py`
3. Generate transactions (depends on the above):
   `python data_generators/generate_orders.py`
4. Generate secondary transaction data:
   `python data_generators/generate_order_payments.py`
   `python data_generators/generate_coupons.py`
