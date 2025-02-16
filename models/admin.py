class Admin:
    username: str = 'admin'
    password: str = 'admin'

    @classmethod
    def __repr__(cls):
        return f"Admin(username='{cls.username}', password='{cls.password}')"

    @classmethod
    def authenticate_admin(cls, username: str, password: str) -> bool:
        return username == cls.username and password == cls.password
