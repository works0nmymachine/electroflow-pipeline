import os
import json
import random
import pandas as pd
from datetime import timedelta
from faker import Faker
from utils.integrity_utils import select_valid_id

fake = Faker()

def generate_orders_json(num_records=5000):
    customer_file = "data/raw/customers.csv"
    product_file = "data/raw/products.csv"
    
    if not os.path.exists(customer_file) or not os.path.exists(product_file):
        print("Dependency Error: Ensure customers.csv and products.csv exist.")
        return

    # Load products to lookup prices for financial totals is NO LONGER needed here
    # We leave the price lookup logic to Gold Layer and Payment generator

    orders = []
    statuses = ["delivered", "shipped", "canceled", "processing", "unavailable"]
    status_weights = [0.85, 0.08, 0.03, 0.03, 0.01]

    for _ in range(num_records):
        customer_id = select_valid_id(customer_file, "customer_id")
        status = random.choices(statuses, weights=status_weights)[0]
        
        # --- Timestamps (Funnel Analysis) ---
        purchase_dt = fake.date_time_between(start_date='-1y', end_date='now')
        
        # Promise date is usually purchase + 3-7 days
        estimated_dt = purchase_dt + timedelta(days=random.randint(3, 7))
        
        # approved_at (usually within 24h)
        approved_at = purchase_dt + timedelta(minutes=random.randint(5, 1440)) if status != "canceled" else None
        
        # carrier_date (1-3 days after approval)
        carrier_dt = None
        if status in ["delivered", "shipped"] and approved_at:
            carrier_dt = approved_at + timedelta(days=random.randint(1, 3))
            
        # customer_date (2-5 days after carrier)
        customer_dt = None
        if status == "delivered" and carrier_dt:
            customer_dt = carrier_dt + timedelta(days=random.randint(2, 5))

        # --- Items ---
        order_items = []
        num_items = random.randint(1, 4)
        
        for _ in range(num_items):
            p_id = str(select_valid_id(product_file, "product_id"))
            qty = random.randint(1, 3)
            
            order_items.append({
                "product_id": p_id,
                "quantity": qty
            })

        shipping_cost = round(random.uniform(5.0, 25.0), 2)
        tax_pct = random.choice([0.05, 0.07, 0.10, 0.21]) # Sample tax brackets

        order = {
            "order_id": str(random.randint(100000, 999999)),
            "customer_id": str(customer_id),
            "order_status": status,
            # Timestamps
            "order_purchase_timestamp": purchase_dt.isoformat(),
            "order_approved_at": approved_at.isoformat() if approved_at else None,
            "order_delivered_carrier_date": carrier_dt.isoformat() if carrier_dt else None,
            "order_delivered_customer_date": customer_dt.isoformat() if customer_dt else None,
            "order_estimated_delivery_date": estimated_dt.isoformat(),
            # Logistics
            "shipping_zip_code": fake.postcode(),
            "shipping_city": fake.city(),
            # Financials (only native facts)
            "payment_currency": "USD", # simplify for now
            "shipping_cost": shipping_cost,
            "tax_percentage": tax_pct,
            "items": order_items
        }
        
        orders.append(order)
    
    output_path = "data/raw/orders.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(orders, f, indent=4)
        
    print(f"Generated {len(orders)} advanced orders to {output_path} with Funnel Timestamps.")
    return orders

if __name__ == "__main__":
    generate_orders_json()
