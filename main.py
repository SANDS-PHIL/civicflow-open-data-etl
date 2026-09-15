"""
Main ETL orchestrator for CivicFlow Open Data ETL.

This script runs the complete Extract, Transform, Load pipeline for public data.
"""
import logging
import sys
import os
from src.extract import extract_facility_data
from src.transform import transform_data
from src.load import load_data

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def main() -> None:
    """
    Run the ETL pipeline.
    """
    logger.info("Starting CivicFlow Open Data ETL pipeline")
    try:
        # Get configuration from environment
        api_url = os.getenv("API_URL")
        fallback_csv_path = os.getenv("FALLBACK_CSV_PATH", "data/fallback_facilities.csv")

        if not api_url:
            logger.error("API_URL environment variable is not set")
            sys.exit(1)

        # Extract
        raw_data = extract_facility_data(api_url, fallback_csv_path)
        # Transform
        cleaned_data = transform_data(raw_data)
        # Load
        load_data(cleaned_data)
        logger.info("ETL pipeline completed successfully")
    except Exception as e:
        logger.error(f"ETL pipeline failed: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()