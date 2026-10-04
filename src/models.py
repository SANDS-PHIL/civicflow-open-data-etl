# src/models.py
from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional
from decimal import Decimal

class DistrictPlanOverlay(BaseModel):
    """
    Pydantic model for WCC District Plan GIS Overlays.
    Enforces data governance on complex planning/geospatial data.
    """
    # Ignore extra columns from the CSV that we don't care about
    model_config = ConfigDict(extra='ignore')

    # Use exact lowercase names to match the CSV dictionary keys
    object_id: int = Field(..., gt=0, description="Unique GIS feature ID")

    symbol_colour: Optional[str] = Field(None, description="Map visualization colour code")
    metadata_url: Optional[str] = Field(None, max_length=500, description="Link to planning documentation")
    original_data_source: Optional[str] = Field(None, max_length=500, description="Source system reference")

    # Geospatial validation
    shape_area: Decimal = Field(..., gt=0, description="Polygon area in square metres")
    shape_length: Decimal = Field(..., gt=0, description="Polygon perimeter in metres")

    @field_validator('shape_area')
    @classmethod
    def validate_area_reasonable(cls, v: Decimal) -> Decimal:
        """Ensure area is within reasonable bounds for Wellington city features (e.g., < 10 km²)"""
        if v > 10000000:
            raise ValueError('Area exceeds reasonable bounds for a single planning overlay')
        return v