"""
Main ETL orchestrator for CivicFlow Open Data ETL.

This script runs the complete Extract, Transform, Load pipeline for public data.
"""
import logging
import sys
from src.extract import extract_data
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
        # Extract
        raw_data = extract_data()
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