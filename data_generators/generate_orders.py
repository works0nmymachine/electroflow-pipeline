import os
import json
import random
import pandas as pd
from datetime import timedelta
from faker import Faker
from utils.integrity_utils import select_valid_id

fake = Faker()

def generate_orders_json(num_records=5000):
    customer_file = "00_landing/raw/customers.csv"
    product_file = "00_landing/raw/products.csv"
    
    if not os.path.exists(customer_file) or not os.path.exists(product_file):
        print("Dependency Error: Ensure customers.csv and products.csv exist.")
        return

    # Load products to lookup prices for financial totals
    products_df = pd.read_csv(product_file)
    product_prices = dict(zip(products_df['product_id'].astype(str), products_df['base_price']))

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

        # --- Items & Financials ---
        order_items = []
        subtotal = 0
        num_items = random.randint(1, 4)
        
        for _ in range(num_items):
            p_id = str(select_valid_id(product_file, "product_id"))
            price = product_prices.get(p_id, 0.0)
            qty = random.randint(1, 3)
            item_total = round(price * qty, 2)
            subtotal += item_total
            
            order_items.append({
                "product_id": p_id,
                "quantity": qty,
                "unit_price": price,
                "item_total": item_total
            })

        shipping_cost = round(random.uniform(5.0, 25.0), 2)
        tax_pct = random.choice([0.05, 0.07, 0.10, 0.21]) # Sample tax brackets
        tax_amount = round((subtotal + shipping_cost) * tax_pct, 2)
        total_value = round(subtotal + shipping_cost + tax_amount, 2)

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
            # Financials
            "payment_currency": "USD", # simplify for now
            "subtotal": round(subtotal, 2),
            "shipping_cost": shipping_cost,
            "tax_percentage": tax_pct,
            "tax_amount": tax_amount,
            "total_order_value": total_value,
            "items": order_items
        }
        
        orders.append(order)
    
    output_path = "00_landing/raw/orders.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(orders, f, indent=4)
        
    print(f"Generated {len(orders)} advanced orders to {output_path} with Funnel Timestamps.")
    return orders

if __name__ == "__main__":
    generate_orders_json()
