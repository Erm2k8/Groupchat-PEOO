class Admin:
    username: str = 'admin'
    password: str = 'admin'

    @classmethod
    def __repr__(cls):
        return f"Admin(username='{cls.username}', password='{cls.password}')"
