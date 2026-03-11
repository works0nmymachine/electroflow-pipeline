import os
import pandas as pd
import random
from faker import Faker

# Reverted to default English Faker
fake = Faker()

def generate_products_csv(num_records=50):
    # Defining Belsimpel-like product catalogs
    smartphone_catalog = {
        "Apple":["iPhone 15", "iPhone 15 Pro", "iPhone 14", "iPhone 13", "iPhone SE"],
        "Samsung":["Galaxy S24", "Galaxy S24 Ultra", "Galaxy A54", "Galaxy A34", "Galaxy Z Flip5"],
        "Google":["Pixel 8", "Pixel 8 Pro", "Pixel 7a"],
        "Xiaomi":["Redmi Note 13", "13T Pro", "Poco X6"],
        "OnePlus":["12", "Nord 3", "Open"]
    }
    
    wearable_audio_catalog = {
        "Apple":["AirPods Pro 2", "Watch Series 9", "Watch Ultra 2"],
        "Samsung": ["Galaxy Buds2 Pro", "Galaxy Watch6"],
        "Sony":["WH-1000XM5", "WF-1000XM5"],
        "Google":["Pixel Buds Pro", "Pixel Watch 2"]
    }

    # Translated colors to English
    colors =["Black", "White", "Blue", "Green", "Red", "Silver", "Gold", "Titanium", "Pink"]
    storages =["64GB", "128GB", "256GB", "512GB", "1TB"]
    
    products =[]

    for _ in range(num_records):
        # 6-character numerical IDs
        product_id = f"{random.randint(100000, 999999)}"
        
        # Decide the product type with weighted probability
        product_type = random.choices(["Smartphone", "Audio/Wearable", "Accessory"], 
            weights=[0.6, 0.2, 0.2], 
            k=1
        )[0]
        
        # Generate properties based on Belsimpel's offerings
        if product_type == "Smartphone":
            brand = random.choice(list(smartphone_catalog.keys()))
            model = random.choice(smartphone_catalog[brand])
            color = random.choice(colors)
            storage = random.choice(storages)
            product_name = f"{brand} {model} {storage} {color}"
            category = "Smartphones"
            base_price = round(random.uniform(250.0, 1500.0), 2)
            
        elif product_type == "Audio/Wearable":
            brand = random.choice(list(wearable_audio_catalog.keys()))
            model = random.choice(wearable_audio_catalog[brand])
            color = random.choice(colors)
            product_name = f"{brand} {model} {color}"
            category = "Audio & Smartwatches"
            base_price = round(random.uniform(90.0, 450.0), 2)
            
        else: # Accessories
            brand = random.choice(["Spigen", "Otterbox", "Mobilize", "Apple", "Samsung", "PanzerGlass"])
            # Translated accessory types to English
            acc_type = random.choice(["Silicone Case", "Book Case", "Screen Protector", "Fast Charger", "USB-C Cable"])
            # Translated accessory colors to English
            color = random.choice(["Black", "Transparent", "Blue"]) if "Case" in acc_type else ""
            product_name = f"{brand} {acc_type} {color}".strip()
            category = "Accessories"
            base_price = round(random.uniform(10.0, 60.0), 2)

        products.append({
            "product_id": product_id,
            "product_name": product_name,
            "brand": brand,
            "category": category,
            "base_price": base_price,
            # Translated Belsimpel-style rapid delivery statuses into English
            "stock_status": random.choice(["Ordered today, delivered tomorrow", "In stock", "Temporarily out of stock"])
        })

    # Create DataFrame and handle duplicates
    df = pd.DataFrame(products).drop_duplicates(subset=['product_id'])

    # Save to CSV
    output_path = "data/raw/products.csv"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    
    print(f"Generated {len(df)} Belsimpel-like products to {output_path} with 6-digit IDs.")
    return df

if __name__ == "__main__":
    generate_products_csv()