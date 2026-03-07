import os
import pandas as pd
import random
from datetime import datetime, timedelta

def generate_coupons_csv():
    campaigns = [
        {"name": "Black Friday 2025", "prefix": "BF25", "months_ago": 4},
        {"name": "Cyber Monday 2025", "prefix": "CM25", "months_ago": 3},
        {"name": "Winter Sale", "prefix": "WINT", "months_ago": 2},
        {"name": "Summer Splash", "prefix": "SUMR", "months_ago": 8},
        {"name": "New User Welcome", "prefix": "HI10", "months_ago": 12},
    ]
    
    coupons = []
    base_date = datetime.now()

    for camp in campaigns:
        # Each campaign has multiple coupon variants
        num_variants = random.randint(3, 8)
        start_dt = base_date - timedelta(days=camp["months_ago"] * 30)
        end_dt = start_dt + timedelta(days=random.randint(7, 30))
        
        for i in range(num_variants):
            discount = random.choice([0.05, 0.10, 0.15, 0.20, 0.25])
            coupons.append({
                "coupon_code": f"{camp['prefix']}-{random.randint(100, 999)}",
                "discount_percentage": discount,
                "campaign_name": camp["name"],
                "valid_from": start_dt.strftime("%Y-%m-%d"),
                "valid_to": end_dt.strftime("%Y-%m-%d")
            })
            
    df = pd.DataFrame(coupons)
    output_path = "00_landing/raw/coupons.csv"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Generated {len(df)} coupons to {output_path}.")
    return df

if __name__ == "__main__":
    generate_coupons_csv()
