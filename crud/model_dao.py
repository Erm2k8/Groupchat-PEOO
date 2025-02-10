from typing import Any, Type
import json

class ModelDAO:
    objects: list[Any] = []
    path: str = ""
    model: Type[Any] = None

    @classmethod
    def open(cls) -> None:
        try:
            with open(cls.path, "r") as data:
                cls.objects = [cls.model.from_dict(o) for o in json.load(data)]
        except (FileNotFoundError, json.JSONDecodeError):
            cls.objects = []

    @classmethod
    def save(cls) -> None:
        try:
            with open(cls.path, "w") as file:
                json.dump(cls.objects, file, default=lambda obj: obj.to_dict(), indent=4)
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    @classmethod
    def create(cls, obj: Any) -> None:
        cls.open()
        cls.objects.append(obj)
        cls.save()

    @classmethod
    def read_all(cls) -> list:
        cls.open()
        return cls.objects

    @classmethod
    def get_by_id(cls, id: int) -> Any | None:
        cls.open()
        for obj in cls.objects:
            if obj.id == id:
                return obj
        return None

    @classmethod
    def update(cls, obj: Any) -> None:
        cls.open()
        to_update = cls.get_by_id(obj.id)
        if to_update is not None:
            cls.objects.remove(to_update)
            cls.objects.append(obj)
            cls.save()

    @classmethod
    def delete(cls, id: int) -> None:
        cls.open()
        to_delete = cls.get_by_id(id)
        if to_delete is not None:
            cls.objects.remove(to_delete)
            cls.save()