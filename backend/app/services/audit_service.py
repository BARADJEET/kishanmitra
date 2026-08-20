import json
from sqlalchemy.orm import Session
from ..models.audit import AdminAuditLog
from ..models.user import User

def log_admin_action(
    db: Session,
    admin: User,
    entity_type: str,
    entity_id: int,
    action: str,
    description: str,
    old_values: dict = None,
    new_values: dict = None
) -> AdminAuditLog:
    log_entry = AdminAuditLog(
        admin_id=admin.id,
        admin_email=admin.email,
        entity_type=entity_type,
        entity_id=entity_id,
        action=action,
        description=description,
        old_values_json=json.dumps(old_values, default=str) if old_values else None,
        new_values_json=json.dumps(new_values, default=str) if new_values else None
    )
    db.add(log_entry)
    db.commit()
    db.refresh(log_entry)
    return log_entry
