from typing import List

class Group:
    def __init__(self, id: int, group_name: str, members: List['Member'], description: str) -> None:
        self.id = id
        self.group_name = group_name
        self.members = members
        self.description = description


    @property
    def id(self) -> int:
        return self.__id
    

    @id.setter
    def id(self, new_id: int) -> None:
        if new_id < 0:
            raise ValueError("ID deve ser um inteiro positivo.")
        self.__id = new_id
            

    @property
    def group_name(self) -> str:
        return self.__group_name


    @group_name.setter
    def group_name(self, new_group_name: str) -> None:
        if not (3 <= len(new_group_name) <= 50):
            raise ValueError("Nome do grupo deve ser uma string de 3 a 50 caracteres.")
        self.__group_name = new_group_name
        

    @property
    def members(self) -> List['Member']:
        return self.__members
    

    @members.setter
    def members(self, new_members: List['Member']) -> None:
        if not isinstance(new_members, list):
            raise ValueError("Membros devem ser uma lista.")
        self.__members = new_members


    @property
    def description(self) -> str:
        return self.__description
    

    @description.setter
    def description(self, new_description: str) -> None:
        if len(new_description) > 255:
            raise ValueError("Descrição não pode ser maior que 255 caracteres.")
        self.__description = new_description


    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'group_name': self.group_name,
            'members': self.members,
            'description': self.description
        }
    

    @classmethod
    def from_dict(cls, data: dict) -> 'Group':
        return cls(
            id=data.get('id', 0),
            group_name=data.get('group_name', ''),
            members=data.get('members', []),
            description=data.get('description', '')
        )


    def __str__(self):
        return f'Group: ID = {self.id}, Nome do grupo = {self.group_name}, Membros = {len(self.members)}'


    def __repr__(self):
        return f"Group(id={self.id}, group_name='{self.group_name}', members={self.members}, description='{self.description}')"
