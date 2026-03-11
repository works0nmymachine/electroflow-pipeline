import os
import json
import random
import pandas as pd

def generate_order_payments_csv():
    order_file = "data/raw/orders.json"
    
    if not os.path.exists(order_file):
        print(f"Error: {order_file} not found. Generate orders first.")
        return

    with open(order_file, "r") as f:
        orders = json.load(f)

    payments = []
    payment_types = [    "iDEAL", 
    "Mastercard", 
    "Visa", 
    "PayPal", 
    "Apple Pay", 
    "Google Pay", 
    "Klarna", 
    "Bank Transfer"]
    
    print(f"Generating payments for {len(orders)} orders...")
    
    for order in orders:
        order_id = order["order_id"]
        total_value = order["total_order_value"]
        
        # 1 Payment method per order
        p_type = random.choice(payment_types)
        
        # Installments: Only Klarna supports installments > 1
        installments = 1
        if p_type == "Klarna":
            installments = random.choice([1, 3, 6, 12])
            
        payments.append({
            "payment_id": str(random.randint(10000000, 99999999)),
            "order_id": order_id,
            "payment_sequential": 1,
            "payment_type": p_type,
            "payment_installments": installments,
            "payment_value": total_value
        })

    df = pd.DataFrame(payments)
    output_path = "data/raw/order_payments.csv"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Generated {len(df)} payment records to {output_path}.")
    return df

if __name__ == "__main__":
    generate_order_payments_csv()
