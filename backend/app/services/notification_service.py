from sqlalchemy.orm import Session
from ..models.notification import Notification

def create_user_notification(
    db: Session,
    user_id: int,
    title: str,
    message: str,
    notif_type: str = "weather",
    action_url: str = None
) -> Notification:
    notif = Notification(
        user_id=user_id,
        title=title,
        message=message,
        type=notif_type,
        action_url=action_url,
        is_read=False
    )
    db.add(notif)
    db.commit()
    db.refresh(notif)
    return notif
