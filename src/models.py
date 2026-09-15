# src/models.py
from pydantic import BaseModel, Field, ConfigDict, validator
from typing import Optional
from decimal import Decimal

class DistrictPlanOverlay(BaseModel):
    """
    Pydantic model for WCC District Plan GIS Overlays.
    Enforces data governance on complex planning/geospatial data.
    """
    model_config = ConfigDict(extra='ignore', populate_by_name=True)

    # Core identifier
    object_id: int = Field(..., alias="OBJECTID", gt=0, description="Unique GIS feature ID")

    # Planning metadata
    symbol_colour: Optional[str] = Field(None, alias="SymbolColour", description="Map visualization colour code")
    metadata_url: Optional[str] = Field(None, alias="MetadataURL", max_length=500, description="Link to planning documentation")
    original_data_source: Optional[str] = Field(None, alias="OriginalData", max_length=500, description="Source system reference")

    # Geospatial validation - ShapeSTArea and ShapeSTLength are GIS geometry properties
    shape_area: Decimal = Field(..., alias="ShapeSTArea", gt=0, description="Polygon area in square metres")
    shape_length: Decimal = Field(..., alias="ShapeSTLength", gt=0, description="Polygon perimeter in metres")

    @validator('shape_area')
    def validate_area_reasonable(cls, v):
        """Ensure area is within reasonable bounds for Wellington city features"""
        if v > 10000000:  # 10 km² - larger than most Wellington suburbs
            raise ValueError('Area exceeds reasonable bounds for a single planning overlay')
        return v