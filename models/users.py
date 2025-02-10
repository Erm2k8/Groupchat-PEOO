class User:
    def __init__(self, id: int, username: str, email: str, password: str) -> None:
        self.id = id
        self.username = username
        self.email = email
        self.password = password


    @property
    def id(self) -> int:
        return self.__id
    

    @id.setter
    def id(self, new_id: int) -> None:
        if new_id < 0:
            raise ValueError("ID deve ser um inteiro positivo.")
        self.__id = new_id
            

    @property
    def username(self) -> str:
        return self.__username


    @username.setter
    def username(self, new_username: str) -> None:
        if not (3 <= len(new_username) <= 20):
            raise ValueError("Nome de usuário deve ser uma string de 3 a 20 caracteres.")
        self.__username = new_username
        

    @property
    def email(self) -> str:
        return self.__email
    

    @email.setter
    def email(self, new_email: str) -> None:
        if "@" not in new_email:
            raise ValueError("E-mail inválido.")
        self.__email = new_email


    @property
    def password(self) -> str:
        return self.__password
    

    @password.setter
    def password(self, new_password: str) -> None:
        if new_password.replace(' ', '').isalpha():
            raise ValueError("Senha deve conter um número ou caractere especial.")
        self.__password = new_password


    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'password': self.password
        }
    

    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        return cls(
            id=data.get('id', 0),
            username=data.get('username', ''),
            email=data.get('email', ''),
            password=data.get('password', '')
        )

        if not username or not email or not password:
            raise ValueError("Dados insuficientes para criar o usuário.")


    def __str__(self):
        return f'User: ID = {self.id}, Nome de usuário = {self.username}, E-mail = {self.email}'


    def __repr__(self):
        return f"User(id={self.id}, username='{self.username}', email='{self.email}', password='{self.password}')"

        