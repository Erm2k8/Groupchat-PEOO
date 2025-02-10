from typing import Any, Type
from models.notifications import Notification
from .model_dao import ModelDAO

class NotificationDAO(ModelDAO):
    objects: list[Any] = []
    path: str = "data/notifications.json"
    model: Type[Any] = Notification
