from datetime import datetime

class Message:
    def __init__(self, id: int, content: str, timestamp: datetime, sender_id: int, group_id: int) -> None:
        self.id = id
        self.content = content
        self.timestamp = timestamp
        self.sender_id = sender_id
        self.group_id = group_id

    @property
    def id(self) -> int:
        return self.__id

    @id.setter
    def id(self, new_id: int) -> None:
        if new_id < 0:
            raise ValueError("ID deve ser um inteiro positivo.")
        self.__id = new_id

    @property
    def content(self) -> str:
        return self.__content

    @content.setter
    def content(self, new_content: str) -> None:
        if not new_content:
            raise ValueError("Conteúdo não pode ser vazio.")
        self.__content = new_content

    @property
    def timestamp(self) -> datetime:
        return self.__timestamp

    @timestamp.setter
    def timestamp(self, new_timestamp: datetime) -> None:
        if not isinstance(new_timestamp, datetime):
            raise ValueError("Timestamp deve ser uma instância de datetime.")
        self.__timestamp = new_timestamp

    @property
    def sender_id(self) -> int:
        return self.__sender_id

    @sender_id.setter
    def sender_id(self, new_sender_id: int) -> None:
        if new_sender_id < 0:
            raise ValueError("ID do remetente deve ser um inteiro positivo.")
        self.__sender_id = new_sender_id

    @property
    def group_id(self) -> int:
        return self.__group_id

    @group_id.setter
    def group_id(self, new_group_id: int) -> None:
        if new_group_id < 0:
            raise ValueError("ID do grupo deve ser um inteiro positivo.")
        self.__group_id = new_group_id

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'content': self.content,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'sender_id': self.sender_id,
            'group_id': self.group_id
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Message':
        timestamp = datetime.strptime(data.get('timestamp', ''), '%Y-%m-%d %H:%M:%S')
        return cls(
            id=data.get('id', 0),
            content=data.get('content', ''),
            timestamp=timestamp,
            sender_id=data.get('sender_id', 0),
            group_id=data.get('group_id', 0)
        )

    def __str__(self) -> str:
        content_preview = self.content[:50] + '...' if len(self.content) > 50 else self.content
        return (f"Message: ID = {self.id}, Content = '{content_preview}', "
                f"Timestamp = {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}, "
                f"Sender ID = {self.sender_id}, Group ID = {self.group_id}")

    def __repr__(self) -> str:
        return (f"Message(id={self.id}, content='{self.content}', "
                f"timestamp='{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}', "
                f"sender_id={self.sender_id}, group_id={self.group_id})")
