import os
import pandas as pd
import random
from faker import Faker

fake = Faker()

def generate_products_csv(num_records=50):
    categories = ["Electronics", "Home Appliances", "Kitchenware", "Personal Care", "Tools"]
    products = []
    
    for _ in range(num_records):
        # User requested 6-character numerical IDs
        product_id = f"{random.randint(100000, 999999)}"
        
        products.append({
            "product_id": product_id,
            "product_name": fake.catch_phrase(),
            "category": random.choice(categories),
            "base_price": round(random.uniform(5.0, 1000.0), 2),
            "supplier": fake.company()
        })
    
    df = pd.DataFrame(products).drop_duplicates(subset=['product_id'])
    
    output_path = "00_landing/raw/products.csv"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Generated {len(df)} products to {output_path} with 6-digit IDs.")
    return df

if __name__ == "__main__":
    generate_products_csv()
