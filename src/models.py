"""
Pydantic models for CivicFlow Open Data ETL.

Defines the schema for validated Building Consent records.
"""
from datetime import datetime
from pydantic import BaseModel, Field, validator


class BuildingConsent(BaseModel):
    """
    Schema for a validated Building Consent record.
    """
    consent_id: int = Field(..., gt=0, description="Unique identifier for the building consent")
    property_id: int = Field(..., gt=0, description="Identifier for the property")
    status: str = Field(..., max_length=50, description="Current status of the consent")
    date_approved: datetime = Field(..., description="Date when the consent was approved")

    @validator('date_approved', pre=True)
    def parse_date_approved(cls, value):
        """
        Parse date_approved from various string formats.
        If value is already a datetime, return it.
        """
        if isinstance(value, datetime):
            return value
        # Try common date formats
        for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%Y/%m/%d"):
            try:
                return datetime.strptime(value, fmt)
            except ValueError:
                continue
        raise ValueError(f"Unable to parse date: {value}")


# Example of how to use the model (for documentation)
if __name__ == "__main__":
    # This is just for testing the model directly
    example_data = {
        "consent_id": 1,
        "property_id": 101,
        "status": "Approved",
        "date_approved": "2023-01-15"
    }
    consent = BuildingConsent(**example_data)
    print(consent)