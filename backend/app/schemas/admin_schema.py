from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class AdminAuditLogResponse(BaseModel):
    id: int
    admin_id: int
    admin_email: str
    entity_type: str
    entity_id: Optional[int] = None
    action: str
    old_values_json: Optional[str] = None
    new_values_json: Optional[str] = None
    description: str
    created_at: datetime

    class Config:
        from_attributes = True

class DashboardAnalyticsResponse(BaseModel):
    total_farmers: int
    total_farms: int
    total_acreage: float
    total_yard_sheets: int
    total_ml_predictions: int
    total_policies: int
    total_products: int
    crops_distribution: Dict[str, int]
    top_detected_diseases: List[Dict[str, Any]]
    top_recommended_crops: List[Dict[str, Any]]
    recent_farmer_activity: List[Dict[str, Any]]
    recent_predictions: List[Dict[str, Any]]
    active_alerts: List[Dict[str, Any]]
