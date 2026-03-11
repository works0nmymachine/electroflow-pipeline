import sys
import os

# Ensure the script runs from the data_generators directory or can find the modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from generate_customers import generate_customers_csv
from generate_products import generate_products_csv
from generate_coupons import generate_coupons_csv
from generate_orders import generate_orders_json
from generate_order_payments import generate_order_payments_csv
from utils.integrity_utils import get_valid_ids

def run_all_generators():
    print("🚀 Starting Data Generation Pipeline...\n")

    # Step 1: Generate Independent Base Data
    print("--- Step 1: Base Data ---")
    generate_customers_csv(num_records=1000)
    generate_products_csv(num_records=50)
    generate_coupons_csv()  # Does not accept num_records
    print("✅ Base Data Generated.\n")
    
    # Optional Validation step
    print("--- Integrity Check ---")
    cust_ids = get_valid_ids("data/raw/customers.csv", "customer_id", use_cache=False)
    prod_ids = get_valid_ids("data/raw/products.csv", "product_id", use_cache=False)
    print(f"Validated {len(cust_ids)} unique customers and {len(prod_ids)} unique products.")
    print("✅ Integrity Check Passed.\n")

    # Step 2: Generate Relational Data (Requires Base Data)
    print("--- Step 2: Orders (Requires Customers & Products) ---")
    generate_orders_json(num_records=5000)
    print("✅ Orders Generated.\n")

    # Step 3: Generate Dependent Relational Data (Requires Orders)
    print("--- Step 3: Order Payments (Requires Orders) ---")
    generate_order_payments_csv()
    print("✅ Payments Generated.\n")
    
    print("🎉 All data successfully generated in `data/raw/`!")

if __name__ == "__main__":
    run_all_generators()
