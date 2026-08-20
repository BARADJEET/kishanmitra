from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from datetime import datetime
from ..database import Base

class AdminAuditLog(Base):
    __tablename__ = "admin_audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    admin_id = Column(Integer, nullable=False, index=True)
    admin_email = Column(String(255), nullable=False)
    entity_type = Column(String(100), nullable=False, index=True)  # Policy, Product, Disease, YardSheet, User
    entity_id = Column(Integer, nullable=True)
    action = Column(String(50), nullable=False)  # CREATE, UPDATE, DELETE
    old_values_json = Column(Text, nullable=True)
    new_values_json = Column(Text, nullable=True)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
