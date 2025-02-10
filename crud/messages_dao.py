from typing import Any, Type
from models.messages import Message
from .model_dao import ModelDAO

class MessageDAO(ModelDAO):
    objects: list[Any] = []
    path: str = "data/messages.json"
    model: Type[Any] = Message

