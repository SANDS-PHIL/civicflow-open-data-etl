"""
Transform module for CivicFlow Open Data ETL.

Handles validating and cleaning the extracted data using Pydantic models.
"""
import logging
from typing import List, Dict, Any, Tuple
from decimal import Decimal, InvalidOperation
import pandas as pd
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


def aggregate_property_data(consents_df: pd.DataFrame, overlays_df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate property data by joining consents and overlays datasets.

    Performs a left join of consents data with overlays data on a common property identifier.
    Handles missing values gracefully and provides logging on join success rates.

    Args:
        consents_df: DataFrame containing property consent data
        overlays_df: DataFrame containing planning overlay data

    Returns:
        pd.DataFrame: Joined dataset with consents as primary and overlay data appended
    """
    logger.info("Starting property data aggregation")

    # Check if dataframes are empty
    if consents_df.empty:
        logger.warning("Consents DataFrame is empty. Returning empty DataFrame.")
        return pd.DataFrame()

    if overlays_df.empty:
        logger.warning("Overlays DataFrame is empty. Returning consents data with overlay columns.")
        # Add overlay columns with default values
        result_df = consents_df.copy()
        # Add common overlay columns with default values
        overlay_columns = ['symbol_colour', 'metadata_url', 'original_data_source',
                          'shape_area', 'shape_length']
        for col in overlay_columns:
            if col not in result_df.columns:
                result_df[col] = 'No Specific Overlay' if col in ['symbol_colour', 'metadata_url', 'original_data_source'] else 0
        return result_df

    # Determine common join key
    # Try common property identifiers in order of preference
    possible_keys = ['valuation_number', 'address', 'object_id', 'OBJECTID', 'property_id']
    join_key = None

    for key in possible_keys:
        if key in consents_df.columns and key in overlays_df.columns:
            join_key = key
            break

    # If no exact match, try case-insensitive matching
    if join_key is None:
        consents_cols_lower = {col.lower(): col for col in consents_df.columns}
        overlays_cols_lower = {col.lower(): col for col in overlays_df.columns}

        for key in possible_keys:
            if key.lower() in consents_cols_lower and key.lower() in overlays_cols_lower:
                join_key = consents_cols_lower[key.lower()]  # Use actual column name from consents
                # We'll need to use the actual column names from both dataframes
                break

    if join_key is None:
        logger.error("No common join key found between consents and overlays datasets.")
        logger.info(f"Consents columns: {list(consents_df.columns)}")
        logger.info(f"Overlays columns: {list(overlays_df.columns)}")
        # Return consents data with placeholder overlay columns
        result_df = consents_df.copy()
        overlay_columns = ['symbol_colour', 'metadata_url', 'original_data_source',
                          'shape_area', 'shape_length']
        for col in overlay_columns:
            if col not in result_df.columns:
                result_df[col] = 'No Specific Overlay' if col in ['symbol_colour', 'metadata_url', 'original_data_source'] else 0
        return result_df

    logger.info(f"Using '{join_key}' as the join key for property data aggregation")

    # Prepare overlays data for join - ensure we have the join key
    if join_key not in overlays_df.columns:
        # Try to find the column in overlays with case-insensitive match
        overlays_cols_lower = {col.lower(): col for col in overlays_df.columns}
        if join_key.lower() in overlays_cols_lower:
            actual_overlays_key = overlays_cols_lower[join_key.lower()]
        else:
            logger.error(f"Join key '{join_key}' not found in overlays dataset.")
            # Return consents data with placeholder overlay columns
            result_df = consents_df.copy()
            overlay_columns = ['symbol_colour', 'metadata_url', 'original_data_source',
                              'shape_area', 'shape_length']
            for col in overlay_columns:
                if col not in result_df.columns:
                    result_df[col] = 'No Specific Overlay' if col in ['symbol_colour', 'metadata_url', 'original_data_source'] else 0
            return result_df
    else:
        actual_overlays_key = join_key

    # Perform left join
    try:
        # Select relevant columns from overlays to avoid unnecessary data
        overlay_cols_to_keep = [actual_overlays_key, 'symbol_colour', 'metadata_url',
                               'original_data_source', 'shape_area', 'shape_length']
        # Filter to only columns that actually exist in overlays_df
        overlay_cols_to_keep = [col for col in overlay_cols_to_keep if col in overlays_df.columns]

        overlays_subset = overlays_df[overlay_cols_to_keep].copy()

        # Perform the left join
        result_df = consents_df.merge(
            overlays_subset,
            left_on=join_key,
            right_on=actual_overlays_key,
            how='left',
            suffixes=('', '_overlay')
        )

        # Count successful joins vs unmatched
        matched_count = result_df['symbol_colour'].notna().sum() if 'symbol_colour' in result_df.columns else 0
        total_count = len(result_df)
        unmatched_count = total_count - matched_count

        logger.info(f"Property data aggregation complete: {matched_count} records matched with overlays, {unmatched_count} records without overlay data")

        # Fill missing overlay data with appropriate default values
        if 'symbol_colour' in result_df.columns:
            result_df['symbol_colour'] = result_df['symbol_colour'].fillna('No Specific Overlay')
        if 'metadata_url' in result_df.columns:
            result_df['metadata_url'] = result_df['metadata_url'].fillna('No Specific Overlay')
        if 'original_data_source' in result_df.columns:
            result_df['original_data_source'] = result_df['original_data_source'].fillna('No Specific Overlay')
        if 'shape_area' in result_df.columns:
            result_df['shape_area'] = result_df['shape_area'].fillna(0)
        if 'shape_length' in result_df.columns:
            result_df['shape_length'] = result_df['shape_length'].fillna(0)

        # Remove the duplicate join key column from overlays if it exists
        if f'{join_key}_overlay' in result_df.columns:
            result_df = result_df.drop(columns=[f'{join_key}_overlay'])
        elif actual_overlays_key != join_key and actual_overlays_key in result_df.columns:
            # If we used different column names, drop the overlays version
            result_df = result_df.drop(columns=[actual_overlays_key])

        logger.info(f"Final aggregated dataset has {len(result_df)} records and {len(result_df.columns)} columns")
        return result_df

    except Exception as e:
        logger.error(f"Error during property data aggregation: {str(e)}")
        # Return consents data with placeholder overlay columns as fallback
        result_df = consents_df.copy()
        overlay_columns = ['symbol_colour', 'metadata_url', 'original_data_source',
                          'shape_area', 'shape_length']
        for col in overlay_columns:
            if col not in result_df.columns:
                result_df[col] = 'No Specific Overlay' if col in ['symbol_colour', 'metadata_url', 'original_data_source'] else 0
        return result_df