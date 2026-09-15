import os
import logging
import requests
import pandas as pd
import io
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

def extract_facility_data(api_url: str, fallback_csv_path: str) -> List[Dict[str, Any]]:
    """
    Extracts public facility data. Handles both JSON and CSV API responses,
    with a graceful fallback to a local CSV if the API fails.
    """
    logger.info(f"Attempting to fetch live data from: {api_url}")

    try:
        response = requests.get(api_url, timeout=10.0)
        response.raise_for_status()

        # Check if the response is CSV or JSON based on headers or URL
        if 'text/csv' in response.headers.get('Content-Type', '') or api_url.endswith('.csv'):
            # Parse CSV directly from the API response
            df = pd.read_csv(io.StringIO(response.text))
            logger.info(f"Successfully fetched and parsed {len(df)} live CSV records from API.")
            return df.to_dict(orient="records")
        else:
            # Fallback to JSON parsing
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