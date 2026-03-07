import os
import random
import pandas as pd
import numpy as np
from faker import Faker

# We keep a cache of localized fakers
faker_cache = {
    'default': Faker()
}

def get_localized_faker(country_code):
    """Attempt to find a localized Faker for the given country code."""
    code = str(country_code).upper() if pd.notna(country_code) else 'DEFAULT'
    
    mappings = {
        'US': 'en_US', 'GB': 'en_GB', 'NL': 'nl_NL', 'DE': 'de_DE', 
        'FR': 'fr_FR', 'IT': 'it_IT', 'ES': 'es_ES', 'CA': 'en_CA', 
        'AU': 'en_AU', 'IN': 'en_IN', 'CN': 'zh_CN', 'JP': 'ja_JP',
        'BR': 'pt_BR', 'MX': 'es_MX', 'RU': 'ru_RU', 'PL': 'pl_PL',
        'TR': 'tr_TR', 'ID': 'id_ID', 'BE': 'nl_BE', 'CH': 'de_CH',
        'AT': 'de_AT', 'SE': 'sv_SE', 'NO': 'no_NO', 'DK': 'da_DK',
        'FI': 'fi_FI', 'PT': 'pt_PT', 'GR': 'el_GR', 'HU': 'hu_HU',
        'CZ': 'cs_CZ', 'RO': 'ro_RO', 'UA': 'uk_UA', 'ZA': 'en_ZA',
        'KR': 'ko_KR', 'TW': 'zh_TW'
    }
    
    locale = mappings.get(code)
    if not locale:
        return faker_cache['default']
        
    if locale not in faker_cache:
        try:
            faker_cache[locale] = Faker(locale)
        except:
            return faker_cache['default']
            
    return faker_cache[locale]

def generate_customers_csv(num_records=1000, 
                           reference_path='/home/user1/Documents/Projects/Data projects/electroflow/electroflow-pipeline/data_generators/ultils_data/landcode currency language phone.xlsx',
                           gdp_path='/home/user1/Documents/Projects/Data projects/electroflow/electroflow-pipeline/data_generators/ultils_data/country_gdp_data.xlsx',
                           geo_mapping_path='/home/user1/Documents/Projects/Data projects/electroflow/electroflow-pipeline/data_generators/ultils_data/geo_mapping.xlsx'):
    
    try:
        ref_df = pd.read_excel(reference_path)
        gdp_df = pd.read_excel(gdp_path)
        geo_df = pd.read_excel(geo_mapping_path)
    except Exception as e:
        print(f"Error reading references: {e}")
        return

    # Process geo_mapping into a usable dictionary
    # geo_mapping structure: CountryCode, City, State, ZipCodes (comma separated)
    GEO_DATA = {}
    for _, row in geo_df.iterrows():
        code = str(row['CountryCode']).upper()
        if code not in GEO_DATA:
            GEO_DATA[code] = []
        
        zips = str(row['ZipCodes']).split(',')
        GEO_DATA[code].append((row['City'], row['State'], zips))

    combined = pd.merge(gdp_df, ref_df, on='Country', suffixes=('', '_ref'))
    combined['selection_weight'] = combined['selection_weight'] / combined['selection_weight'].sum()
    
    print(f"Generating {num_records} customers with logically consistent Geography (from Excel mapping)...")

    customers = []
    domains = ["example.net", "info.com", "mailbox.org", "webmail.io"]
    countries_to_pick = combined['Country'].values
    weights = combined['selection_weight'].values
    chosen_indices = np.random.choice(len(combined), size=num_records, p=weights)
    
    for idx in chosen_indices:
        ref_row = combined.iloc[idx]
        country = ref_row['Country']
        country_code = ref_row['CountryCode']
        phone_prefix = str(ref_row['Phone nr']).strip()
        loc_fake = get_localized_faker(country_code)
        
        # 1. Names & Gender
        gender = random.choice(['male', 'female'])
        if gender == 'male':
            first_name = loc_fake.first_name_male()
            last_name = loc_fake.last_name()
        else:
            first_name = loc_fake.first_name_female()
            last_name = loc_fake.last_name()
        full_name = f"{first_name} {last_name}"
        email = f"{first_name.lower()}.{last_name.lower()}@{random.choice(domains)}"
        
        # 2. Logically Consistent Geography (Loading from external Excel)
        if country_code in GEO_DATA:
            city, state, zips = random.choice(GEO_DATA[country_code])
            postcode = random.choice(zips)
        else:
            city = loc_fake.city()
            postcode = loc_fake.postcode()
            state = "N/A"
            if hasattr(loc_fake, 'province'):
                state = loc_fake.province()
            elif hasattr(loc_fake, 'region'):
                state = loc_fake.region()

        # 3. Rest of fields
        phone_body = "".join([str(random.randint(0, 9)) for _ in range(8)])
        phone_number = f"{phone_prefix} {phone_body}" if random.random() > 0.1 else None
        date_format = "%Y-%m-%d" if random.random() > 0.5 else "%m/%d/%Y"
        join_date = loc_fake.date_between(start_date='-5y', end_date='today').strftime(date_format)
        
        customers.append({
            "customer_id": str(random.randint(100000, 999999)),
            "full_name": full_name,
            "gender": gender,
            "email": email,
            "city": city,
            "state_province": state,
            "postal_code": postcode,
            "country": country,
            "country_code": country_code,
            "phone_number": phone_number,
            "join_date": join_date
        })
    
    df = pd.DataFrame(customers)
    df = pd.concat([df, df.sample(frac=0.05)]) # Add duplicates
    
    output_path = "00_landing/raw/customers.csv"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Generated {len(df)} customers with synced City/Zip from mapping to {output_path}.")
    return df

if __name__ == "__main__":
    generate_customers_csv()
