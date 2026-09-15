import os
import logging
import requests
import pandas as pd
from typing import List, Dict, Any

# Configure logging
logger = logging.getLogger(__name__)

def extract_facility_data(api_url: str, fallback_csv_path: str) -> List[Dict[str, Any]]:
    """
    Extracts public facility data from a government open data API.
    Includes an enterprise-grade fallback to a local CSV if the API is unreachable.
    """
    logger.info(f"Attempting to fetch live data from: {api_url}")

    try:
        # Attempt live API fetch (timeout after 5 seconds to prevent hanging)
        response = requests.get(api_url, timeout=5.0)
        response.raise_for_status() # Raise exception for 4xx/5xx HTTP errors

        # Assuming the API returns JSON (common for Socrata/CKAN portals)
        # If it returns CSV, we would use pd.read_csv(io.StringIO(response.text))
        data = response.json()
        logger.info(f"Successfully fetched {len(data)} live records from API.")
        return data

    except (requests.exceptions.RequestException, ValueError) as e:
        # Graceful degradation: API failed, fall back to local cache
        logger.warning(f"Live API extraction failed ({e}). Falling back to local cache: {fallback_csv_path}")

        if not os.path.exists(fallback_csv_path):
            logger.error(f"Fallback file {fallback_csv_path} not found. Aborting extraction.")
            raise FileNotFoundError(f"Neither API nor fallback CSV is available.")

        # Read local CSV and convert to list of dictionaries to match JSON structure
        df = pd.read_csv(fallback_csv_path)
        logger.info(f"Successfully loaded {len(df)} records from local fallback cache.")
        return df.to_dict(orient="records")