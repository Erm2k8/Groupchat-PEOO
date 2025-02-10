class Notification:
    def __init__(self, id: int, sender_id: int, mentioned_id: int, message_id: int) -> None:
        self.id = id
        self.sender_id = sender_id
        self.mentioned_id = mentioned_id
        self.message_id = message_id

    @property
    def id(self) -> int:
        return self.__id

    @id.setter
    def id(self, new_id: int) -> None:
        if new_id < 0:
            raise ValueError("ID deve ser um inteiro positivo.")
        self.__id = new_id

    @property
    def sender_id(self) -> int:
        return self.__sender_id

    @sender_id.setter
    def sender_id(self, new_sender_id: int) -> None:
        if new_sender_id < 0:
            raise ValueError("ID do remetente deve ser um inteiro positivo.")
        self.__sender_id = new_sender_id

    @property
    def mentioned_id(self) -> int:
        return self.__mentioned_id

    @mentioned_id.setter
    def mentioned_id(self, new_mentioned_id: int) -> None:
        if new_mentioned_id < 0:
            raise ValueError("ID do mencionado deve ser um inteiro positivo.")
        self.__mentioned_id = new_mentioned_id

    @property
    def message_id(self) -> int:
        return self.__message_id

    @message_id.setter
    def message_id(self, new_message_id: int) -> None:
        if new_message_id < 0:
            raise ValueError("ID da mensagem deve ser um inteiro positivo.")
        self.__message_id = new_message_id

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'sender_id': self.sender_id,
            'mentioned_id': self.mentioned_id,
            'message_id': self.message_id
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Notification':
        return cls(
            id=data.get('id', 0),
            sender_id=data.get('sender_id', 0),
            mentioned_id=data.get('mentioned_id', 0),
            message_id=data.get('message_id', 0)
        )

    def __str__(self) -> str:
        return (f"Notification: ID = {self.id}, Sender ID = {self.sender_id}, "
                f"Mentioned ID = {self.mentioned_id}, Message ID = {self.message_id}")

    def __repr__(self) -> str:
        return (f"Notification(id={self.id}, sender_id={self.sender_id}, "
                f"mentioned_id={self.mentioned_id}, message_id={self.message_id})")
