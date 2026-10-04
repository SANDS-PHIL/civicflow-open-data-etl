# src/extract.py (Update the extract_facility_data function)
import os
import logging
import requests
import pandas as pd
import io
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

def extract_facility_data(api_url: str, fallback_csv_path: str) -> List[Dict[str, Any]]:
    logger.info(f"Attempting to fetch live data from: {api_url}")

    # CRITICAL FIX: Spoof a standard browser to bypass ArcGIS bot blocking
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'Accept': 'text/csv,application/json'
    }

    try:
        response = requests.get(api_url, headers=headers, timeout=10.0)
        response.raise_for_status()

        if 'text/csv' in response.headers.get('Content-Type', '') or api_url.endswith('.csv'):
            df = pd.read_csv(io.StringIO(response.text))
            logger.info(f"Successfully fetched and parsed {len(df)} live CSV records from API.")
            return df.to_dict(orient="records")
        else:
            data = response.json()
            logger.info(f"Successfully fetched {len(data)} live JSON records from API.")
            return data

    except (requests.exceptions.RequestException, ValueError) as e:
        logger.warning(f"Live API extraction failed ({e}). Falling back to local cache: {fallback_csv_path}")

        if not os.path.exists(fallback_csv_path):
            logger.error(f"Fallback file {fallback_csv_path} not found. Aborting extraction.")
            raise FileNotFoundError(f"Neither API nor fallback CSV is available.")

        df = pd.read_csv(fallback_csv_path)
        logger.info(f"Successfully loaded {len(df)} records from local fallback cache.")
        return df.to_dict(orient="records")