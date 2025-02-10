from typing import Any, Type
from models.groups import Group
from .model_dao import ModelDAO

class GroupDAO(ModelDAO):
    objects: list[Any] = []
    path: str = "data/groups.json"
    model: Type[Any] = Group
