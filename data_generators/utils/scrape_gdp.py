import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import os
import io

def clean_val(val):
    if pd.isna(val) or val == '—' or val == '':
        return np.nan
    # Remove commas, quotes, footnotes [123], and non-numeric chars
    clean = str(val).split('(')[0].split('[')[0].replace(',', '').replace('"', '').strip()
    try:
        return float(clean)
    except:
        return np.nan

def scrape_wikipedia_gdp():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    print("Scraping GDP (Nominal)...")
    url_gdp = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)"
    resp = requests.get(url_gdp, headers=headers)
    soup = BeautifulSoup(resp.text, 'html.parser')
    
    table = soup.find('table', {'class': 'wikitable'})
    if not table:
        print("Error: No wikitables found on GDP page")
        return None
    
    df_gdp = pd.read_html(io.StringIO(str(table)))[0]
    
    # Flatten multi-index if it exists
    if isinstance(df_gdp.columns, pd.MultiIndex):
        df_gdp.columns = [' '.join([str(i) for i in col]).strip() for col in df_gdp.columns.values]
    
    col_mapping = {}
    for col in df_gdp.columns:
        low = str(col).lower()
        if 'country' in low or 'territory' in low:
            col_mapping[col] = 'Country'
        elif 'imf' in low:
            col_mapping[col] = 'GDP_IMF'
        elif 'world bank' in low:
            col_mapping[col] = 'GDP_WB'
        elif 'united nations' in low:
            col_mapping[col] = 'GDP_UN'
            
    df_gdp = df_gdp[list(col_mapping.keys())].rename(columns=col_mapping)
    df_gdp['Country'] = df_gdp['Country'].str.replace(r'\[.*\]', '', regex=True).str.strip()
    
    for col in ['GDP_IMF', 'GDP_WB', 'GDP_UN']:
        if col in df_gdp.columns:
            df_gdp[col] = df_gdp[col].apply(clean_val)
            
    df_gdp['GDP_Avg'] = df_gdp[['GDP_IMF', 'GDP_WB', 'GDP_UN']].mean(axis=1)
    
    print("Scraping GDP Per Capita...")
    url_capita = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)_per_capita"
    resp = requests.get(url_capita, headers=headers)
    soup = BeautifulSoup(resp.text, 'html.parser')
    
    table_cap = soup.find('table', {'class': 'wikitable'})
    if not table_cap:
        print("Error: No wikitables found on per capita page")
        return None
        
    df_cap = pd.read_html(io.StringIO(str(table_cap)))[0]
    
    if isinstance(df_cap.columns, pd.MultiIndex):
        df_cap.columns = [' '.join([str(i) for i in col]).strip() for col in df_cap.columns.values]
        
    cap_mapping = {}
    for col in df_cap.columns:
        low = str(col).lower()
        if 'country' in low or 'territory' in low:
            cap_mapping[col] = 'Country'
        elif 'imf' in low:
            cap_mapping[col] = 'Capita_IMF'
        elif 'world bank' in low:
            cap_mapping[col] = 'Capita_WB'
        elif 'united nations' in low:
            cap_mapping[col] = 'Capita_UN'

    df_cap = df_cap[list(cap_mapping.keys())].rename(columns=cap_mapping)
    df_cap['Country'] = df_cap['Country'].str.replace(r'\[.*\]', '', regex=True).str.strip()
    
    for col in ['Capita_IMF', 'Capita_WB', 'Capita_UN']:
        if col in df_cap.columns:
            df_cap[col] = df_cap[col].apply(clean_val)
            
    df_cap['Capita_Avg'] = df_cap[['Capita_IMF', 'Capita_WB', 'Capita_UN']].mean(axis=1)
    
    # Merge
    final_df = pd.merge(df_gdp, df_cap, on='Country', how='inner')
    
    # Filter out world/regions
    exclude = ['World', 'European Union', 'Africa', 'Asia', 'Europe', 'North America', 'South America', 'Oceania']
    final_df = final_df[~final_df['Country'].isin(exclude)]

    # --- Add Country Code (Requested by User) ---
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.abspath(os.path.join(script_dir, "..", "ultils_data"))
    ref_path = f"{output_dir}/landcode currency language phone.xlsx"
    if os.path.exists(ref_path):
        try:
            ref_df = pd.read_excel(ref_path)
            ref_subset = ref_df[['Country', 'CountryCode']].drop_duplicates()
            final_df = pd.merge(final_df, ref_subset, on='Country', how='left')
        except Exception as e:
            print(f"Warning: Could not merge with country codes: {e}")

    # --- Pre-calculate Rankings and Weights (Requested by User) ---
    # User's request: 70% weight for Nominal GDP, 30% for GDP per Capita
    final_df['norm_gdp'] = final_df['GDP_Avg'] / final_df['GDP_Avg'].sum()
    final_df['norm_capita'] = final_df['Capita_Avg'] / final_df['Capita_Avg'].sum()
    final_df['selection_weight'] = (final_df['norm_gdp'] * 0.7) + (final_df['norm_capita'] * 0.3)
    
    # Scale it for easier readability/ranking
    final_df['gdp_rank'] = final_df['GDP_Avg'].rank(ascending=False).astype(int)
    final_df['capita_rank'] = final_df['Capita_Avg'].rank(ascending=False).astype(int)
    final_df['overall_rank'] = final_df['selection_weight'].rank(ascending=False).astype(int)
    
    os.makedirs(output_dir, exist_ok=True)
    output_path = f"{output_dir}/country_gdp_data.xlsx"
    final_df.to_excel(output_path, index=False)
    print(f"Data saved to {output_path} with rankings, weights, and country codes.")
    return final_df

if __name__ == "__main__":
    scrape_wikipedia_gdp()
