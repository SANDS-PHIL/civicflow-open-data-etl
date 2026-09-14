"""
Extract module for CivicFlow Open Data ETL.

Handles fetching data from the public API endpoint.
"""
import os
import logging
from typing import Any, Dict, List
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def extract_data() -> List[Dict[str, Any]]:
    """
    Fetch JSON data from the configured public API endpoint.

    Returns:
        List[Dict[str, Any]]: List of records retrieved from the API.

    Raises:
        requests.RequestException: If there is an error in the HTTP request.
        ValueError: If the response is not valid JSON or if the API_URL is not set.
    """
    api_url = os.getenv("API_URL")
    if not api_url:
        logger.error("API_URL environment variable is not set")
        raise ValueError("API_URL environment variable is not set")

    logger.info(f"Fetching data from {api_url}")
    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        data = response.json()
        if not isinstance(data, list):
            logger.error("Expected a JSON list but got %s", type(data))
            raise ValueError("Expected a JSON list from the API")
        logger.info(f"Successfully fetched {len(data)} records")
        return data
    except requests.RequestException as e:
        logger.error(f"Failed to fetch data from {api_url}: {e}")
        raise
    except ValueError as e:
        logger.error(f"Invalid response from {api_url}: {e}")
        raise