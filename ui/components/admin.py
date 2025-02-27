import streamlit as st
from views.views import View
from .auth import Auth
import pandas as pd
from ..styles import Style
from time import sleep
from models.members import Permission
from datetime import datetime

class AdminUI:
    @staticmethod
    def render():
        AdminUI.admin_sidebar()
        AdminUI.render_page()

    @staticmethod
    def admin_sidebar():
        with st.sidebar:
            st.title("TriboPapo - ADMIN")
            st.session_state.admin_selected_page = st.selectbox(
                "Gerenciar", 
                [
                    "Usuários",
                    "Grupos",
                    "Mensagens",
                    "Membros"
                ],
                key="admin_page"
            )
            Auth.render_logout_button()

    @staticmethod
    def render_page():
        Style.padding__adjust_render()
        match st.session_state.admin_selected_page:
            case "Usuários":
                AdminUI.users_page()
            case "Grupos":
                AdminUI.groups_page()
            case "Mensagens":
                AdminUI.messages_page()
            case "Membros":
                AdminUI.members_page()
            case _:
                st.write("Select a page to get started.")

    @staticmethod
    def users_page():
        create, read, update, delete = st.tabs(["Create", "Read", "Update", "Delete"])

        with create:
            name = st.text_input("Name", key="create_name")
            email = st.text_input("Email", key="create_email")
            password = st.text_input("Password", type="password", key="create_password")
            if st.button("Create"):
                View.create_user(name, email, password)
                st.success("User created!")
                sleep(2)
                st.rerun()
        
        with read:
            search_id = st.number_input(
                "Search by ID",
                key="search_id",
                min_value=0,
                step=1,
                format="%d"
            )
            if st.button("Buscar"):
                user = View.get_user_by_id(int(search_id))
                with st.container(border=True):
                    if user:
                        st.success(f"""
                                   Username: {user.username}\n
                                   E-mail: {user.email}
                            """)
                    else:
                        st.warning("User not found.")

            users = View.list_users()
            users = [{"ID": user.id, "Name": user.username, "Email": user.email} for user in users]
            df = pd.DataFrame(users, columns=["ID", "Name", "Email"])
            st.dataframe(df, use_container_width=True, hide_index=True)

        with update:
            name = st.selectbox(
                "Escolher usuário",
                [user.username for user in View.list_users()],
                key="update_user_select" 
            )
            user_id = View.get_user_by_name(name)
            if user_id is None:
                st.error("User not found.")
            else:
                user_id = user_id.id
                name = st.text_input(
                                "Novo nome",
                                key="update_name",
                                value=View.get_user_by_id(user_id).username
                            )
                email = st.text_input(
                                "Novo e-mail",
                                key="update_email",
                                value=View.get_user_by_id(user_id).email
                            )
                password = st.text_input(
                                "Nova senha",
                                type="password",
                                key="update_password",
                                value=View.get_user_by_id(user_id).password
                            )
                if st.button("Update"):
                    View.update_user(user_id, name, email, password)
                    st.success("User updated!")
                    sleep(2)
                    st.rerun()

        with delete:
            name = st.selectbox(
                "Escolher usuário",
                [user.username for user in View.list_users()],
                key="delete_user_select"  
            )

            user_id = View.get_user_by_name(name)

            if user_id is None:
                st.error("Usuário não encontrado.")
            else:
                user_id = user_id.id

                if st.button("Delete"):
                    View.delete_user(user_id)
                    st.success("User deleted!")
                    sleep(2)
                    st.rerun()

    @staticmethod
    def groups_page():
        create, read, update, delete = st.tabs(["Create", "Read", "Update", "Delete"])

        with create:
            group_name = st.text_input("Group Name", key="create_group_name")
            description = st.text_input("Description", key="create_description")

            selected_usernames = st.multiselect(
                "Members",
                [user.username for user in View.list_users()],
                key="create_members"
            )

            if st.button("Create"):
                try:
                    View.create_group(group_name, description)
                    group = View.get_group_by_name(group_name)

                    if not group:
                        st.error("Erro ao criar o grupo. Tente novamente.")
                        return

                    group_id = group.id

                    if selected_usernames:
                        members = [View.get_user_by_name(username) for username in selected_usernames]
                        
                        for member in members:
                            View.add_member(group_id, member.id, Permission.read_messages | Permission.send_messages) 

                        st.success("Group created and members added successfully!")
                    else:
                        st.success("Group created successfully! No members added.")
                    
                    sleep(2)
                    st.rerun()

                except Exception as e:
                    st.error(f"Erro: {e}. Insira todos os campos corretamente.")


        with read:
            search_id = st.number_input(
                "Search by ID",
                key="search_group_id",
                min_value=0,
                step=1,
                format="%d"
            )
            if st.button("Buscar"):
                group = View.get_group_by_id(int(search_id))
                with st.container(border=True):
                    if group:
                        st.success(f"""
                                   Group Name: {group.group_name}\n
                                   Description: {group.description}
                            """)
                    else:
                        st.warning("Group not found.")

            groups = View.list_groups()
            groups_data = [{"ID": group.id, "Name": group.group_name, "Description": group.description} for group in groups]
            df = pd.DataFrame(groups_data, columns=["ID", "Name", "Description"])
            st.dataframe(df, use_container_width=True, hide_index=True)

        with update:
            group_name = st.selectbox(
                "Choose group",
                [group.group_name for group in View.list_groups()],
                key="update_group_select" 
            )
            if group_name:
                group_id = View.get_group_by_name(group_name).id
                description = st.text_input(
                                "New description",
                                key="update_description",
                                value=View.get_group_by_id(group_id).description
                            )
                members = st.multiselect(
                    "Gerenciar membros",
                    [user.username for user in View.list_users()],
                    key="update_members_group",
                    default=[View.get_user_by_id(member.user_id).username for member in View.get_members_by_group(group_id)]
                )
                if st.button("Update"):
                    View.update_group(group_id, group_name, description)

                    for member in View.get_members_by_group(group_id):
                        View.remove_member(group_id, member.user_id)

                    for member in members:
                        View.add_member(group_id, View.get_user_by_name(member).id, Permission.read_messages | Permission.send_messages)
                        
                    st.success("Group updated!")
                    sleep(2)
                    st.rerun()

        with delete:
            group_name = st.selectbox(
                "Choose group",
                [group.group_name for group in View.list_groups()],
                key="delete_group_select"  # Key única
            )
            if group_name:
                group_id = View.get_group_by_name(group_name).id
                if st.button("Delete"):
                    View.delete_group(group_id)
                    st.success("Group deleted!")
                    sleep(2)
                    st.rerun()  

    @staticmethod
    def messages_page():
        create, read, update, delete = st.tabs(["Create", "Read", "Update", "Delete"])

        with create:
            groups = View.list_groups()
            if not groups:
                st.warning("Nenhum grupo disponível.")
                return  

            group_name = st.selectbox(
                "Group",
                [group.group_name for group in groups],
                key="select_group_message"
            )

            selected_group = View.get_group_by_name(group_name)
            group_id = selected_group.id

            members = View.get_members_by_group(group_id)
                
            if not members:
                st.warning("Nenhum usuário disponível para este grupo.")
                return  

            user_name = st.selectbox(
                "User",
                [View.get_user_by_id(user.user_id).username for user in members],
                key="select_user_message"
            )

            selected_user = View.get_user_by_name(user_name)
            user_id = selected_user.id

            content = st.text_input("Content", key="create_content")

            if st.button("Create"):
                if not content.strip():
                    st.error("A mensagem não pode estar vazia.")
                else:
                    View.send_message(group_id, user_id, content)
                    st.success("Message sent!")
                    sleep(2)
                    st.rerun()

        with read:
            search_id = st.number_input(
                "Search by ID",
                key="search_message_id",
                min_value=0,
                step=1,
                format="%d"
            )
            if st.button("Buscar"):
                message = View.get_message_by_id(int(search_id))
                with st.container(border=True):
                    if message:
                        st.success(f"""
                                   Content: {message.content}\n
                                   Date: {message.timestamp}
                            """)
                    else:
                        st.warning("Message not found.")

            messages = View.list_messages()
            if messages:
                messages = [{"ID": message.id, "Content": message.content, "Sender": View.get_user_by_id(message.sender_id).username, "Group": View.get_group_by_id(message.group_id).group_name, "Date": message.timestamp} for message in messages]
            df = pd.DataFrame(messages, columns=["ID", "Content", "Sender", "Group", "Date"])
            st.dataframe(df, use_container_width=True, hide_index=True)

        with update:
            id = st.number_input(
                "ID",
                key="update_message_id",
                min_value=0,
                step=1,
                format="%d"
            )
            if View.get_message_by_id(id):
                with st.container(border=True):
                    st.write(f"Mensagem antiga: {View.get_message_by_id(id).content}")

                content = st.text_input(
                    "Nova mensagem",
                    key="update_content",
                    value=View.get_message_by_id(id).content
                )

                if st.button("Update"):
                    View.update_message(id, content)
                    st.success("Message updated!")
                    sleep(2)
                    st.rerun()

        with delete:
            id = st.number_input(
                "ID",
                key="delete_message_id",
                min_value=0,
                step=1,
                format="%d"
            )
            content = View.get_message_by_id(id)

            if content:
                with st.container(border=True):
                    st.write(f"Content: {content.content}")
            else:
                st.warning("Message not found.")

            if st.button("Delete"):
                View.delete_message(id)
                st.success("Message deleted!")
                sleep(2)
                st.rerun()

    @staticmethod
    def members_page():
        create, read, update, delete = st.tabs(["Create", "Read", "Update", "Delete"])

        with create:
            groups = View.list_groups()
            if not groups:
                st.warning("Nenhum grupo disponível.")
                return  

            group_name = st.selectbox(
                "Group",
                [group.group_name for group in groups],
                key="select_group_member"
            )

            new_member = st.selectbox(
                "User",
                [View.get_user_by_id(user.id).username for user in View.list_users()],
                key="select_user_member"
            )

            group_id = View.get_group_by_name(group_name).id
            new_member_id = View.get_user_by_name(new_member).id

            if st.button("Create"):
                View.add_member(group_id, new_member_id, Permission.read_messages | Permission.send_messages)
                st.success("Member added!")
                sleep(2)
                st.rerun()

        with read:
            search_id = st.number_input(
                "Search by ID",
                key="search_member_id",
                min_value=0,
                step=1,
                format="%d"
            )
            if st.button("Buscar"):
                member = View.get_member_by_id(int(search_id))
                with st.container(border=True):
                    if member:
                        group = View.get_group_by_id(member.group_id)
                        if group:
                            st.success(f"""
                                User: {View.get_user_by_id(member.user_id).username}\n
                                Group: {group.group_name}
                            """)
                        else:
                            st.warning("O grupo associado ao membro não foi encontrado.")
                    else:
                        st.warning("Membro não encontrado.")

            members = View.list_members()

            if members:
                member_data = []
                for member in members:
                    user = View.get_user_by_id(member.user_id)
                    group = View.get_group_by_id(member.group_id) if member.group_id else None

                    member_data.append({
                        "ID": member.id,
                        "User": user.username if user else "Usuário não encontrado",
                        "Group": group.group_name if group else "Grupo não encontrado",
                        "Permission": [perm.name for perm in Permission if perm in member.permissions]

                    })

                df = pd.DataFrame(member_data, columns=["ID", "User", "Group", "Permission"])
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.warning("Nenhum membro encontrado.")

        with update:
            group = st.selectbox(
                "Group",
                [group.group_name for group in View.list_groups()],
                key="select_group_member_update"
            )

            user = st.selectbox(
                "User",
                [View.get_user_by_id(user.id).username for user in View.list_users() if View.get_user_by_id(user.id).id in [member.user_id for member in View.list_members()]],
                key="select_user_member_update"
            )

            group_id = View.get_group_by_name(group).id
            user_id = View.get_user_by_name(user).id

            member = View.get_member_by_user_and_group(user_id, group_id)

            if member:
                with st.container(border=True):
                    st.write(f"""
                        User: {View.get_user_by_id(member.user_id).username}\n
                        Group: {View.get_group_by_id(member.group_id).group_name}\n
                        Permission: {member.permissions}
                    """)

                permissions = st.multiselect(
                    "Permission",
                    [perm.name for perm in Permission],
                    default=[perm.name for perm in member.permissions],
                    key="select_permission_member_update"
                )

                if st.button("Update"):
                    View.update_member(member.id, permissions)
                    st.success("Member updated!")
                    sleep(2)
                    st.rerun()
            else:
                st.warning("Member not found.")

        with delete:
            groups = View.list_groups()
    
            if not groups:
                st.warning("Nenhum grupo disponível.")
            else:
                group_name = st.selectbox(
                    "Group",
                    [group.group_name for group in groups],
                    key="select_group_member_delete"
                )

                selected_group = View.get_group_by_name(group_name)
                group_id = selected_group.id if selected_group else None

                members = View.get_members_by_group(group_id) if group_id else []

                if not members:
                    st.warning("Nenhum usuário disponível para este grupo.")
                else:
                    user_name = st.selectbox(
                        "User",
                        [View.get_user_by_id(member.user_id).username for member in members],
                        key="select_user_member_delete"
                    )

                    selected_user = View.get_user_by_name(user_name)
                    user_id = selected_user.id if selected_user else None

                    if st.button("Delete"):
                        member = View.get_member_by_user_and_group(user_id, group_id)
                        
                        if member:
                            View.delete_member(member.id)
                            st.success("Member deleted!")
                            sleep(2)
                            st.rerun()
                        else:
                            st.error("Membro não encontrado para este grupo.")



