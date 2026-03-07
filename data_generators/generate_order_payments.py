import os
import json
import random
import pandas as pd

def generate_order_payments_csv():
    order_file = "00_landing/raw/orders.json"
    
    if not os.path.exists(order_file):
        print(f"Error: {order_file} not found. Generate orders first.")
        return

    with open(order_file, "r") as f:
        orders = json.load(f)

    payments = []
    payment_types = ["credit_card", "voucher", "boleto", "debit_card"]
    
    print(f"Generating payments for {len(orders)} orders...")
    
    for order in orders:
        order_id = order["order_id"]
        total_value = order["total_order_value"]
        
        # Determine if order has multiple payments (10% chance)
        num_payments = 1
        if random.random() < 0.1 and total_value > 20.0:
            num_payments = random.randint(2, 3)
            
        remaining_value = total_value
        
        for i in range(1, num_payments + 1):
            if i == num_payments:
                # Final payment takes the rest
                p_value = round(remaining_value, 2)
            else:
                # Split a portion for the first payment
                p_value = round(random.uniform(5.0, remaining_value * 0.5), 2)
                remaining_value -= p_value

            p_type = random.choice(payment_types)
            # Installments (mostly 1, but up to 12 for credit cards)
            installments = 1
            if p_type == "credit_card":
                installments = random.choice([1, 1, 3, 6, 12])
            
            payments.append({
                "order_id": order_id,
                "payment_sequential": i,
                "payment_type": p_type,
                "payment_installments": installments,
                "payment_value": p_value
            })

    df = pd.DataFrame(payments)
    output_path = "00_landing/raw/order_payments.csv"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Generated {len(df)} payment records to {output_path}.")
    return df

if __name__ == "__main__":
    generate_order_payments_csv()
