'''
- [ ] GET /notifications — list user's notifications
- [ ] PATCH /notifications/{id} — mark as read
'''
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select

from auth.utils import get_current_user
from connector import get_session
from models.user import User
from models.notification import Notification, NotificationTypeEnum
from schemas.notification import NotificationRead, NotificationUpdate


router = APIRouter(
    prefix='/notifications',
    tags=['notifications']
)


@router.get('/')
def get_all_notifications(
    current_user: User = Depends(get_current_user),
    session=Depends(get_session)
) -> List[NotificationRead]:

    notifications_list = session.exec(select(Notification).where(Notification.user_id == current_user.id)).all()

    return notifications_list


@router.patch('/{id}')
def read_notification(
    id: int,
    current_user: User = Depends(get_current_user),
    session=Depends(get_session)
):

    notification_db = session.exec(select(Notification)
                                   .where(Notification.user_id == current_user.id)
                                   .where(Notification.id == id)).first()

    if not notification_db:
        raise HTTPException(status_code=404, detail='Notification is not found')

    notification_db.is_read = True

    session.add(notification_db)
    session.commit()
    session.refresh(notification_db)

    return {'message': f'Notifiaction with message "{notification_db.message}" is now read'}
