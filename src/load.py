"""
Load module for CivicFlow Open Data ETL.

Handles saving the transformed data to a local file (CSV or Parquet).
"""
import os
import logging
from typing import List, Dict, Any, Optional
import pandas as pd

# Configure logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def load_data(
    data: List[Dict[str, Any]],
    output_format: str = None,
    output_path: str = None
) -> None:
    """
    Save the transformed data to a local file.

    Args:
        data: List of dictionaries containing the validated records.
        output_format: Either 'csv' or 'parquet'. If not provided, reads from
            OUTPUT_FORMAT environment variable (defaults to 'csv').
        output_path: The file path to write to. If not provided, reads from
            OUTPUT_PATH environment variable (defaults to 'output/data.csv' or
            'output/data.parquet' based on format).

    Raises:
        ValueError: If an unsupported output_format is provided.
        OSError: If there is an issue writing the file.
    """
    if not data:
        logger.warning("No data to load")
        return

    # Determine output format
    if output_format is None:
        output_format = os.getenv("OUTPUT_FORMAT", "csv").lower()
    if output_format not in ("csv", "parquet"):
        logger.error(f"Unsupported output format: {output_format}")
        raise ValueError("output_format must be either 'csv' or 'parquet'")

    # Determine output path
    if output_path is None:
        default_filename = f"data.{output_format}"
        output_path = os.getenv("OUTPUT_PATH", os.path.join("output", default_filename))

    # Ensure the output directory exists
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
        logger.info(f"Created output directory: {output_dir}")

    # Convert to DataFrame
    df = pd.DataFrame(data)
    logger.info(f"Saving {len(df)} records to {output_path} in {output_format} format")

    try:
        if output_format == "csv":
            df.to_csv(output_path, index=False)
        elif output_format == "parquet":
            df.to_parquet(output_path, index=False)
        logger.info(f"Successfully saved data to {output_path}")
    except Exception as e:
        logger.error(f"Failed to save data to {output_path}: {e}")
        raise

def save_to_csv(data: List[Dict[str, Any]], output_path: str) -> None:
    """
    Save the transformed data to a CSV file.

    This is a convenience function for CSV-only saving.

    Args:
        data: List of dictionaries containing the validated records.
        output_path: The file path to write the CSV file.
    """
    load_data(data, output_format="csv", output_path=output_path)