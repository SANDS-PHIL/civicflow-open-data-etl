"""
Transform module for CivicFlow Open Data ETL.

Handles validating and cleaning the extracted data using Pydantic models.
"""
import logging
from typing import List, Dict, Any
import pandas as pd
from .models import BuildingConsent

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
        Each dictionary corresponds to a BuildingConsent model instance.
    """
    validated_records = []
    for idx, record in enumerate(raw_data):
        try:
            # Map the raw API record to the expected model fields.
            # For the mock API (jsonplaceholder), we map:
            #   id -> consent_id
            #   userId -> property_id
            #   title -> status
            #   body -> (we don't have a real date, so we use a placeholder)
            # In a real implementation, the mapping would depend on the API structure.
            mapped_record = {
                "consent_id": record.get("id"),
                "property_id": record.get("userId"),
                "status": record.get("title"),
                # Placeholder date: in a real scenario, this would be a date field from the API.
                "date_approved": "2023-01-01"
            }
            # Validate and parse the record using the Pydantic model
            consent = BuildingConsent(**mapped_record)
            # Convert the model back to a dictionary (with datetime objects)
            validated_records.append(consent.dict())
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