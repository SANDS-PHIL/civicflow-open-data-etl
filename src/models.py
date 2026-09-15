# src/models.py
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

class PublicFacility(BaseModel):
    """
    Pydantic model for Wellington City Council Public Facilities (e.g., Toilets, Halls).
    Enforces strict data governance on messy open data.
    """
    # Allow extra fields from the raw API without crashing, but ignore them
    model_config = ConfigDict(extra='ignore')

    facility_id: str = Field(..., description="Unique identifier for the asset")
    name: str = Field(..., min_length=1, max_length=150, description="Facility name")
    suburb: str = Field(..., description="Wellington suburb location")
    status: str = Field(..., pattern="^(Open|Closed|Under Maintenance)$", description="Operational status")

    # Geospatial data - required for mapping, validated for NZ coordinates
    latitude: float = Field(..., ge=-45.0, le=-35.0, description="Latitude in WGS84")
    longitude: float = Field(..., ge=170.0, le=180.0, description="Longitude in WGS84")

    # Optional metadata - often missing in open data, so we make it Optional
    last_inspected: Optional[datetime] = Field(None, description="Date of last council inspection")
    has_accessible_parking: Optional[bool] = Field(None, description="Accessibility compliance flag")