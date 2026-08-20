from sqlalchemy import Column, Integer, String, DateTime, Text, Date
from datetime import datetime
from ..database import Base

class GovernmentPolicy(Base):
    __tablename__ = "government_policies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    scheme_name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    eligibility_criteria = Column(Text, nullable=False)
    applicable_state = Column(String(100), default="All India", index=True)
    applicable_crops = Column(String(500), default="All Crops")
    benefits = Column(Text, nullable=False)
    valid_until = Column(String(100), default="Ongoing")
    official_portal_url = Column(String(500), nullable=True)
    attachment_url = Column(String(500), nullable=True)
    category = Column(String(100), default="Subsidy")  # Subsidy, Insurance, Financial Aid, Equipment, Soil Health, Organic
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
