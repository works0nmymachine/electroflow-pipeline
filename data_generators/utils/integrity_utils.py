import os
import pandas as pd
import random
import json

_id_cache = {}

def get_valid_ids(file_path, id_column, use_cache=True):
    """
    Reads a file (CSV or JSON) and returns a list of unique values from the specified column.
    Uses a simple cache to avoid repeated file reads.
    """
    cache_key = f"{file_path}:{id_column}"
    if use_cache and cache_key in _id_cache:
        return _id_cache[cache_key]

    if not os.path.exists(file_path):
        return []
    
    ids = []
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
        ids = df[id_column].unique().tolist()
    elif file_path.endswith('.json'):
        with open(file_path, 'r') as f:
            data = json.load(f)
            ids = list(set(d.get(id_column) for d in data if d.get(id_column)))
    
    if use_cache:
        _id_cache[cache_key] = ids
    return ids

def select_valid_id(file_path, id_column, fallback_generator=None, use_cache=True):
    """
    Selects a random ID from an existing file. 
    """
    valid_ids = get_valid_ids(file_path, id_column, use_cache=use_cache)
    if valid_ids:
        return random.choice(valid_ids)
    
    if fallback_generator:
        return fallback_generator()
    
    raise ValueError(f"Required source file {file_path} is empty or missing, and no fallback provided.")
