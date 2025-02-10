from typing import List
from enum import IntFlag

# Definindo as permissões com IntFlag
class Permission(IntFlag):
    read_messages = 1        # 000001
    send_messages = 2        # 000010
    edit_message = 4         # 000100
    exclude_message = 8      # 001000       
    manage_members = 16      # 010000 
    delete_group = 32        # 100000
    ALL = (read_messages | send_messages | edit_message | exclude_message | 
           manage_members | delete_group)


class Member:
    def __init__(self, id: int, group_id: int, user_id: int, permissions: Permission) -> None:
        self.id = id
        self.group_id = group_id
        self.user_id = user_id
        self.permissions = permissions

    @property
    def id(self) -> int:
        return self.__id
    
    @id.setter
    def id(self, new_id: int) -> None:
        if new_id < 0:
            raise ValueError("ID deve ser um inteiro positivo.")
        self.__id = new_id

    @property
    def group_id(self) -> int:
        return self.__group_id

    @group_id.setter
    def group_id(self, new_group_id: int) -> None:
        if new_group_id < 0:
            raise ValueError("ID do grupo deve ser um inteiro positivo.")
        self.__group_id = new_group_id

    @property
    def user_id(self) -> int:
        return self.__user_id

    @user_id.setter
    def user_id(self, new_user_id: int) -> None:
        if new_user_id < 0:
            raise ValueError("ID do usuário deve ser um inteiro positivo.")
        self.__user_id = new_user_id

    @property
    def permissions(self) -> Permission:
        return self.__permissions

    @permissions.setter
    def permissions(self, new_permissions: Permission) -> None:
        if not isinstance(new_permissions, Permission):
            raise ValueError("Permissões devem ser do tipo Permission.")
        self.__permissions = new_permissions

    @property
    def can_read(self) -> bool:
        return Permission.read_messages in self.permissions

    @property
    def can_send(self) -> bool:
        return Permission.send_messages in self.permissions

    @property
    def can_edit(self) -> bool:
        return Permission.edit_message in self.permissions

    @property
    def can_exclude(self) -> bool:
        return Permission.exclude_message in self.permissions

    @property
    def can_manage_members(self) -> bool:
        return Permission.manage_members in self.permissions

    @property
    def can_delete_group(self) -> bool:
        return Permission.delete_group in self.permissions

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'group_id': self.group_id,
            'user_id': self.user_id,
            'permissions': self.permissions
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Member':
        return cls(
            id=data.get('id', 0),
            group_id=data.get('group_id', 0),
            user_id=data.get('user_id', 0),
            permissions=Permission(data.get('permissions', 0))  # Garantir que as permissões sejam passadas corretamente
        )

    def __str__(self) -> str:
        return (f"Member: ID = {self.id}, Group ID = {self.group_id}, User ID = {self.user_id}, "
                f"Permissões = {bin(self.permissions).count('1')}")

    def __repr__(self) -> str:
        return f"Member(id={self.id}, group_id={self.group_id}, user_id={self.user_id}, permissions={self.permissions})"
