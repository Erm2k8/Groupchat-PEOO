from models.users import User
from models.groups import Group
from models.messages import Message
from models.members import Member, Permission
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
    def get_user_by_id(id):
        return UserDAO.get_by_id(id)
    
    @staticmethod
    def get_user_by_email(email):
        for user in UserDAO.read_all():
            if user.email == email:
                return user
        return None

    @staticmethod
    def get_user_by_name(name):
        for user in UserDAO.read_all():
            if user.username == name:
                return user
        return None

    @staticmethod
    def list_users():
        return UserDAO.read_all()

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
    def get_group_by_id(id: int) -> Group | None:
        return GroupDAO.get_by_id(id)

    @staticmethod
    def create_group(name, description, list_members=None):
        if list_members is None:
            list_members = []
        group = Group(0, name, [], description)
        GroupDAO.create(group)
        group.members = [m for m in View.read_all_members() if m.group_id == group.id]
        GroupDAO.update(group)

    @staticmethod
    def update_group(id, name, description):
        group = Group(id, name, View.get_members_by_group(id), description)
        GroupDAO.update(group)

    @staticmethod
    def delete_group(id):
        GroupDAO.delete(id)

    @staticmethod
    def read_all_members():
        return MemberDAO.read_all()

    @staticmethod
    def add_member(group_id, user_id, permissions=Permission.read_messages | Permission.send_messages):
        group = View.get_group_by_id(group_id)
        if not group:
            raise ValueError(f"Group with ID {group_id} not found.")
        
        member = Member(0, group_id=group_id, user_id=user_id, permissions=permissions)
        MemberDAO.create(member) 
        group.members.append(member) 
        GroupDAO.update(group)  

    @staticmethod
    def remove_member_from_group(group_id, user_id):
        """
        Remove um membro de um grupo.
        """
        member = View.get_member_by_user_and_group(user_id, group_id)
        if member:
            MemberDAO.delete(member.id)
        
        group = View.get_group_by_id(group_id)
        if group:
            group.members = [m for m in group.members if m.user_id != user_id]
            GroupDAO.update(group)

    @staticmethod
    def get_members_by_group(group_id):
        return [member for member in MemberDAO.read_all() if member.group_id == group_id]

    @staticmethod
    def get_member_by_id(id):
        return MemberDAO.get_by_id(id)

    @staticmethod
    def get_member_by_user_and_group(user_id, group_id):
        """
        Retorna o membro com base no user_id e group_id.
        """
        for member in MemberDAO.read_all():
            if member.user_id == user_id and member.group_id == group_id:
                return member
        return None

    @staticmethod
    def list_messages():
        return MessageDAO.read_all()

    @staticmethod
    def get_messages_by_group(group_id):
        return [message for message in MessageDAO.read_all() if message.group_id == group_id]

    @staticmethod
    def get_message_by_id(id):
        return MessageDAO.get_by_id(id)

    @staticmethod
    def send_message(group_id, user_id, content):
        message = Message(0, content, datetime.now(), user_id, group_id)
        MessageDAO.create(message)

    @staticmethod
    def delete_message(id):
        MessageDAO.delete(id)

    @staticmethod
    def leave_group(user_id, group_id):
        View.remove_member_from_group(group_id, user_id)

    @staticmethod
    def update_message(id, content):
        message = MessageDAO.get_by_id(id)
        message.content = content
        MessageDAO.update(message)
    
    @staticmethod
    def list_members():
        return MemberDAO.read_all()
    
    @staticmethod
    def update_member_permissions(member_id, permissions):
        """
        Atualiza as permissões de um membro.
        """
        member = MemberDAO.get_by_id(member_id)
        if member:
            member.permissions = permissions
            MemberDAO.update(member)

    @staticmethod
    def delete_member(id):
        member = MemberDAO.get_by_id(id)
        View.remove_member_from_group(member.group_id, member.user_id)
        MemberDAO.delete(id)
    
    @staticmethod
    def search_groups(search_string):
        if search_string == "":
            return GroupDAO.read_all()

        return [group for group in GroupDAO.read_all() if search_string.lower() in group.group_name.lower()]
    
    @staticmethod
    def add_members_to_group(group_name, members_ids, admin=False):
        group = View.get_group_by_name(group_name)
        if not group:
            raise ValueError(f"Group with name {group_name} not found.")
        
        if admin:
            for member_id in members_ids:
                View.add_member(group.id, member_id, Permission.ALL)
            return
        
        for member_id in members_ids:
            member = View.get_member_by_user_and_group(member_id, group.id)
            if not member:
                View.add_member(group.id, member_id, Permission.read_messages | Permission.send_messages)
            else:
                View.update_member(member.id, group.id, member_id, Permission.read_messages | Permission.send_messages)

    @staticmethod
    def is_user_group_admin(user_id, group_id):
        member = View.get_member_by_user_and_group(user_id, group_id)
        return member and member.permissions == Permission.ALL