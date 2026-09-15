import pytest
from pydantic import ValidationError
from src.models import DistrictPlanOverlay

def test_valid_record():
    """Test that a valid record passes validation."""
    valid_data = {
        "object_id": 1,
        "symbol_colour": "#FF0000",
        "metadata_url": "https://example.com/metadata",
        "original_data_source": "WCC GIS",
        "shape_area": 1500.5,
        "shape_length": 200.3
    }
    # Should not raise
    overlay = DistrictPlanOverlay(**valid_data)
    assert overlay.object_id == 1
    assert overlay.shape_area == 1500.5

def test_invalid_geospatial_rejected():
    """Test that invalid geospatial data is rejected."""
    # Area too large (greater than 10 km^2)
    invalid_data = {
        "object_id": 2,
        "symbol_colour": "#00FF00",
        "metadata_url": None,
        "original_data_source": None,
        "shape_area": 15000000,  # 15 km^2 > 10 km^2
        "shape_length": 500.0
    }
    with pytest.raises(ValidationError):
        DistrictPlanOverlay(**invalid_data)