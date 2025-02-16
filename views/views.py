from models.users import User
from models.groups import Group
from models.messages import Message
from models.members import Member
from crud.users_dao import UserDAO
from crud.groups_dao import GroupDAO
from crud.messages_dao import MessageDAO
from crud.members_dao import MemberDAO

from datetime import datetime

class View:
    @staticmethod
    def authenticate_user(email, password):
        for user in UserDAO.read_all():
            if user.email == email and user.password == password:
                return {"id": user.id, "name": user.username}
        return None

    @staticmethod
    def create_user(name, email, password):
        user = User(0, name, email, password)
        UserDAO.create(user)

    @staticmethod
    def update_user(id, name, email, password):
        user = User(id, name, email, password)
        UserDAO.update(user)

    @staticmethod
    def delete_user(id):
        UserDAO.delete(id)

    @staticmethod
    def list_groups():
        return GroupDAO.read_all()

    @staticmethod
    def get_group_by_name(name: str) -> Group | None:
        for group in GroupDAO.read_all():
            if group.group_name == name:  
                return group
        return None

    @staticmethod
    def create_group(name, description):
        group = Group(0, name, [], description)
        GroupDAO.create(group)

    @staticmethod
    def update_group(id, name, description):
        group = Group(id, name, description)
        GroupDAO.update(group)

    @staticmethod
    def delete_group(id):
        GroupDAO.delete(id)

    @staticmethod
    def add_member(group_id, user_id, permissions):
        member = Member(0, group_id, user_id, permissions)
        MemberDAO.create(member)

    @staticmethod
    def remove_member(group_id, user_id):
        for member in MemberDAO.read_all():
            if member.group_id == group_id and member.user_id == user_id:
                MemberDAO.delete(member.id)
                break

    @staticmethod
    def get_members_by_group(group_id):
        return [member for member in MemberDAO.read_all() if member.group_id == group_id]

    @staticmethod
    def get_messages_by_group(group_id):
        return [message for message in MessageDAO.read_all() if message.group_id == group_id]

    @staticmethod
    def send_message(group_id, user_id, content):
        message = Message(0, content, datetime.now(), user_id, group_id)
        MessageDAO.create(message)

    @staticmethod
    def leave_group(user_id, group_id):
        View.remove_member(group_id, user_id)
