"""
Transform module for CivicFlow Open Data ETL.

Handles validating and cleaning the extracted data using Pydantic models.
"""
import logging
from typing import List, Dict, Any, Tuple
from decimal import Decimal, InvalidOperation
from .models import DistrictPlanOverlay

# Configure logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def transform_and_validate(raw_data: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], Dict[str, int]]:
    """
    Transform raw data into validated and cleaned records, returning validation stats.

    Args:
        raw_data: List of dictionaries as extracted from the API.

    Returns:
        Tuple of (list of validated dictionaries, stats dict).
        Each dictionary in the list corresponds to a DistrictPlanOverlay model instance.
        Stats dict contains 'valid' and 'invalid' counts.
    """
    validated_records = []
    invalid_count = 0
    for idx, record in enumerate(raw_data):
        try:
            # Map the raw API record to the expected model fields.
            # For the District Plan GIS Overlays API, we expect fields:
            #   OBJECTID -> object_id (int)
            #   SymbolColour -> symbol_colour (str, optional)
            #   MetadataURL -> metadata_url (str, optional)
            #   OriginalData -> original_data_source (str, optional)
            #   ShapeSTArea -> shape_area (Decimal, required)
            #   ShapeSTLength -> shape_length (Decimal, required)
            # Missing or invalid required fields will cause the record to be skipped.

            # Extract and convert fields
            object_id_raw = record.get("OBJECTID")
            symbol_colour = record.get("SymbolColour")
            metadata_url = record.get("MetadataURL")
            original_data_source = record.get("OriginalData")
            shape_area_raw = record.get("ShapeSTArea")
            shape_length_raw = record.get("ShapeSTLength")

            # Validate and convert required fields
            if object_id_raw is None:
                raise ValueError("Missing required field: OBJECTID")
            try:
                object_id = int(object_id_raw)
                if object_id <= 0:
                    raise ValueError("OBJECTID must be positive")
            except (ValueError, TypeError):
                raise ValueError(f"Invalid OBJECTID: {object_id_raw}")

            if shape_area_raw is None:
                raise ValueError("Missing required field: ShapeSTArea")
            try:
                shape_area = Decimal(str(shape_area_raw))
                if shape_area <= 0:
                    raise ValueError("ShapeSTArea must be positive")
            except (InvalidOperation, ValueError):
                raise ValueError(f"Invalid ShapeSTArea: {shape_area_raw}")

            if shape_length_raw is None:
                raise ValueError("Missing required field: ShapeSTLength")
            try:
                shape_length = Decimal(str(shape_length_raw))
                if shape_length <= 0:
                    raise ValueError("ShapeSTLength must be positive")
            except (InvalidOperation, ValueError):
                raise ValueError(f"Invalid ShapeSTLength: {shape_length_raw}")

            # Optional fields: keep as-is if present, otherwise None
            # They are already strings or None from the record.get()

            mapped_record = {
                "object_id": object_id,
                "symbol_colour": symbol_colour,
                "metadata_url": metadata_url,
                "original_data_source": original_data_source,
                "shape_area": shape_area,
                "shape_length": shape_length,
            }

            # Validate and parse the record using the Pydantic model
            facility = DistrictPlanOverlay(**mapped_record)
            # Convert the model back to a dictionary
            validated_records.append(facility.model_dump())
        except Exception as e:
            # Log the error but continue processing other records
            logger.warning(
                f"Record {idx} failed validation: {e}. Record data: {record}"
            )
            invalid_count += 1
            continue

    valid_count = len(validated_records)
    logger.info(
        f"Transformed {valid_count} valid records out of {valid_count + invalid_count}"
    )
    stats = {"valid": valid_count, "invalid": invalid_count}
    return validated_records, stats

def transform_to_dataframe(raw_data: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Transform raw data into a pandas DataFrame of validated records.

    This is a convenience function that returns a DataFrame.

    Args:
        raw_data: List of dictionaries as extracted from the API.

    Returns:
        pandas.DataFrame: DataFrame containing validated and cleaned records.
    """
    validated_records, _ = transform_and_validate(raw_data)
    if not validated_records:
        logger.warning("No valid records to convert to DataFrame")
        return pd.DataFrame()
    return pd.DataFrame(validated_records)