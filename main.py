import os
from dotenv import load_dotenv
from src.extract import extract_facility_data  # Function name stays the same
from src.transform import transform_and_validate
from src.load import save_to_csv
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    load_dotenv()

    # WCC District Plan GIS Overlays
    API_URL = os.getenv("API_URL", "https://data-wcc.opendata.arcgis.com/api/download/v1/items/2ba14e04e38442ffb7e39fe622ffacae_19/csv?layers=19")
    FALLBACK_CSV = os.getenv("FALLBACK_CSV", "data/wcc_district_plan_overlays.csv")
    OUTPUT_PATH = os.getenv("OUTPUT_PATH", "output/cleaned_district_plan_overlays.csv")

    logger.info("Starting CivicFlow WCC District Plan Data Pipeline")
    logger.info("This pipeline validates geospatial planning overlays for LIM report integration")

    # 1. Extract
    raw_data = extract_facility_data(API_URL, FALLBACK_CSV)

    # 2. Transform & Validate
    clean_data, stats = transform_and_validate(raw_data)

    # 3. Load
    save_to_csv(clean_data, OUTPUT_PATH)

    logger.info(f"Pipeline complete. {stats['valid']} valid planning overlays saved.")
    logger.info(f"{stats['invalid']} records rejected due to data quality issues.")
    logger.info("Clean data ready for LIM report generation and planning consent workflows.")

if __name__ == "__main__":
    main()