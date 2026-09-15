"""
Transform module for CivicFlow Open Data ETL.

Handles validating and cleaning the extracted data using Pydantic models.
"""
import logging
from typing import List, Dict, Any
import pandas as pd
from .models import PublicFacility

# Configure logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def transform_data(raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Transform raw data into validated and cleaned records.

    Args:
        raw_data: List of dictionaries as extracted from the API.

    Returns:
        List of dictionaries that have been validated and cleaned.
        Each dictionary corresponds to a PublicFacility model instance.
    """
    validated_records = []
    for idx, record in enumerate(raw_data):
        try:
            # Map the raw API record to the expected model fields.
            # For the mock API (jsonplaceholder), we map:
            #   id -> facility_id (as string)
            #   title -> name
            #   We don't have real data for suburb, status, latitude, longitude, last_inspected, has_accessible_parking,
            #   so we use placeholders or defaults that satisfy validation.
            # In a real implementation, the mapping would depend on the actual API structure.
            mapped_record = {
                "facility_id": str(record.get("id")),
                "name": record.get("title", "Unnamed Facility"),
                "suburb": "Wellington Central",  # placeholder
                "status": "Open",  # placeholder that matches pattern
                "latitude": -41.29,  # placeholder within NZ range
                "longitude": 174.78,  # placeholder within NZ range
                "last_inspected": None,  # placeholder
                "has_accessible_parking": None  # placeholder
            }
            # Validate and parse the record using the Pydantic model
            facility = PublicFacility(**mapped_record)
            # Convert the model back to a dictionary (with datetime objects if any)
            validated_records.append(facility.model_dump())
        except Exception as e:
            # Log the error but continue processing other records
            logger.warning(
                f"Record {idx} failed validation: {e}. Record data: {record}"
            )
            continue

    logger.info(
        f"Transformed {len(validated_records)} valid records out of {len(raw_data)}"
    )
    return validated_records

def transform_to_dataframe(raw_data: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Transform raw data into a pandas DataFrame of validated records.

    This is a convenience function that returns a DataFrame.

    Args:
        raw_data: List of dictionaries as extracted from the API.

    Returns:
        pandas.DataFrame: DataFrame containing validated and cleaned records.
    """
    validated_records = transform_data(raw_data)
    if not validated_records:
        logger.warning("No valid records to convert to DataFrame")
        return pd.DataFrame()
    return pd.DataFrame(validated_records)