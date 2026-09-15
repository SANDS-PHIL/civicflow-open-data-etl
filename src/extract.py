import os
import logging
import requests
import pandas as pd
import io
from typing import List, Dict, Any

# Configure logger
logger = logging.getLogger(__name__)

def extract_facility_data(api_url: str, fallback_csv_path: str) -> List[Dict[str, Any]]:
    """
    Extracts public facility data from a government open data API.
    Attempts to parse JSON, then CSV from the API response.
    Includes an enterprise-grade fallback to a local CSV if the API is unreachable or returns unparseable data.
    """
    logger.info(f"Attempting to fetch live data from: {api_url}")

    try:
        # Attempt live API fetch (timeout after 5 seconds to prevent hanging)
        response = requests.get(api_url, timeout=5.0)
        response.raise_for_status() # Raise exception for 4xx/5xx HTTP errors

        # Try to parse as JSON first (common for many APIs)
        try:
            data = response.json()
            logger.info(f"Successfully fetched {len(data)} live records from API (JSON).")
            return data
        except ValueError as json_err:
            # If JSON parsing fails, try to parse as CSV
            logger.warning(f"JSON parsing failed ({json_err}). Attempting to parse response as CSV.")
            try:
                # Use pandas to read CSV from the response text
                df = pd.read_csv(io.StringIO(response.text))
                logger.info(f"Successfully parsed {len(df)} records from API (CSV).")
                return df.to_dict(orient="records")
            except Exception as csv_err:
                logger.warning(f"CSV parsing also failed ({csv_err}). Falling back to local cache.")
                # Fall through to fallback logic below

    except requests.exceptions.RequestException as e:
        # Network or HTTP error
        logger.warning(f"Live API request failed ({e}). Falling back to local cache: {fallback_csv_path}")

    # If we reach here, either the request failed, or JSON/CSV parsing failed.
    # Fall back to local CSV
    logger.warning(f"Falling back to local cache: {fallback_csv_path}")

    if not os.path.exists(fallback_csv_path):
        logger.error(f"Fallback file {fallback_csv_path} not found. Aborting extraction.")
        raise FileNotFoundError(f"Neither API nor fallback CSV is available.")

    # Read local CSV and convert to list of dictionaries to match JSON structure
    df = pd.read_csv(fallback_csv_path)
    logger.info(f"Successfully loaded {len(df)} records from local fallback cache.")
    return df.to_dict(orient="records")