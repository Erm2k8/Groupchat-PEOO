from crud.users_dao import UserDAO
from models.users import User

def test_create():
    UserDAO.create(User(0, "user1", "email1@example.com", "password1"))
    UserDAO.create(User(0, "user2", "email2@example.com", "password2"))
    UserDAO.create(User(0, "user3", "email3@example.com", "password3"))
    print("Usuários criados com sucesso.")

def test_read_all():
    users = UserDAO.read_all()
    print("Lista de usuários:")
    for user in users:
        print(user)

def test_get_by_id():
    user = UserDAO.get_by_id(4)
    print("Usuário encontrado:", user if user else "Nenhum usuário com esse ID.")

def test_update():
    user = UserDAO.get_by_id(1)
    if user:
        user.username = "updated_user1"
        UserDAO.update(user)
        print("Usuário atualizado:", user)
    else:
        print("Usuário não encontrado para atualização.")

def test_delete():
    UserDAO.delete(2)
    print("Usuário com ID 2 deletado.")

if __name__ == "__main__":
    # test_create()
    # test_read_all()
    # test_get_by_id()
    # test_update()
    # test_read_all()
    test_delete()
    test_read_all()
