from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PolicyCreate(BaseModel):
    title: str
    scheme_name: str
    description: str
    eligibility_criteria: str
    applicable_state: Optional[str] = "All India"
    applicable_crops: Optional[str] = "All Crops"
    benefits: str
    valid_until: Optional[str] = "Ongoing"
    official_portal_url: Optional[str] = None
    attachment_url: Optional[str] = None
    category: Optional[str] = "Subsidy"

class PolicyUpdate(BaseModel):
    title: Optional[str] = None
    scheme_name: Optional[str] = None
    description: Optional[str] = None
    eligibility_criteria: Optional[str] = None
    applicable_state: Optional[str] = None
    applicable_crops: Optional[str] = None
    benefits: Optional[str] = None
    valid_until: Optional[str] = None
    official_portal_url: Optional[str] = None
    attachment_url: Optional[str] = None
    category: Optional[str] = None

class PolicyResponse(PolicyCreate):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
