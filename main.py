import os
from dotenv import load_dotenv
from src.extract import extract_facility_data  # Function name stays the same
from src.transform import transform_and_validate, aggregate_property_data, transform_to_dataframe
from src.load import save_to_csv, load_data
import logging
import pandas as pd

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    load_dotenv()

    # WCC District Plan GIS Overlays (Primary dataset)
    API_URL = os.getenv("API_URL", "https://data-wcc.opendata.arcgis.com/api/download/v1/items/2ba14e04e38442ffb7e39fe622ffacae_19/csv?layers=19")
    FALLBACK_CSV = os.getenv("FALLBACK_CSV", "data/wcc_district_plan_overlays.csv")
    OUTPUT_PATH = os.getenv("OUTPUT_PATH", "output/cleaned_district_plan_overlays.csv")

    # Optional consents dataset for aggregation
    CONSENTS_CSV_PATH = os.getenv("CONSENTS_CSV_PATH")

    logger.info("Starting CivicFlow Property Data Pipeline")
    logger.info("This pipeline processes property data for LIM report integration")

    # 1. Extract primary dataset (overlays)
    logger.info("Step 1: Extracting planning overlay data")
    raw_overlay_data = extract_facility_data(API_URL, FALLBACK_CSV)

    # 2. Transform & Validate primary dataset
    logger.info("Step 2: Transforming and validating planning overlay data")
    clean_overlay_data, overlay_stats = transform_and_validate(raw_overlay_data)

    # Convert to DataFrame for potential aggregation
    overlay_df = transform_to_dataframe(clean_overlay_data)

    # Check if we should perform aggregation with consents data
    if CONSENTS_CSV_PATH and os.path.exists(CONSENTS_CSV_PATH):
        logger.info(f"Step 3: Loading consents data from {CONSENTS_CSV_PATH}")
        try:
            consents_df = pd.read_csv(CONSENTS_CSV_PATH)
            logger.info(f"Loaded {len(consents_df)} consent records")

            # Perform aggregation
            logger.info("Step 4: Aggregating property data (consents + overlays)")
            aggregated_df = aggregate_property_data(consents_df, overlay_df)

            # Save aggregated data
            logger.info("Step 5: Saving aggregated property data")
            save_to_csv(aggregated_df.to_dict('records'), OUTPUT_PATH)

            logger.info(f"Aggregation complete. {len(aggregated_df)} total property records saved.")
            logger.info(f"Overlay stats: {overlay_stats['valid']} valid, {overlay_stats['invalid']} invalid records")

        except Exception as e:
            logger.error(f"Error processing consents data: {e}")
            logger.warning("Falling back to overlay-only output due to consents processing error")
            # Save overlay-only data as fallback
            save_to_csv(clean_overlay_data, OUTPUT_PATH)
            logger.info(f"Overlay-only pipeline complete. {overlay_stats['valid']} valid records saved.")
    else:
        if CONSENTS_CSV_PATH:
            logger.warning(f"CONSENTS_CSV_PATH is set but file not found: {CONSENTS_CSV_PATH}")
        else:
            logger.info("CONSENTS_CSV_PATH not set - running in overlay-only mode (Phase 1)")

        logger.warning("Skipping consents aggregation - running Phase 1 overlay-only pipeline")
        # Save overlay-only data (original behavior)
        logger.info("Step 3: Saving planning overlay data")
        save_to_csv(clean_overlay_data, OUTPUT_PATH)

        logger.info(f"Overlay-only pipeline complete. {overlay_stats['valid']} valid planning overlays saved.")
        logger.info(f"{overlay_stats['invalid']} records rejected due to data quality issues.")
        logger.info("Clean overlay data ready for LIM report generation.")

if __name__ == "__main__":
    main()