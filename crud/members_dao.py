from typing import Any, Type
from models.members import Member
from .model_dao import ModelDAO

class MemberDAO(ModelDAO):
    objects: list[Any] = []
    path: str = "data/members.json"
    model: Type[Any] = Member
