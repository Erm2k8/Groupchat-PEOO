from typing import Any, Type
from models.users import User
from .model_dao import ModelDAO

class UserDAO(ModelDAO):
    objects: list[Any] = []
    path: str = "data/users.json"
    model: Type[Any] = User
