import streamlit as st
from views.views import View
from models.members import Permission

class Groups:
    @staticmethod
    def render_group(group_name: str):
        group = View.get_group_by_name(group_name)

        if group:
            st.title(group.group_name)

            is_user_admin = View.is_user_group_admin(st.session_state.user_id, group.id)
            Groups.render_messages(View.get_group_by_id(group.id))
        else:
            st.error("Group not found.")

    @st.fragment(run_every="1s")
    @staticmethod
    def render_messages(group):
        messages = View.get_messages_by_group(group.id)
        if messages:
            with st.container(height=450, border=False):
                for i, message in enumerate(messages):
                    avatar = "❤" if st.session_state.user_id == message.sender_id else "👤"
                    with st.chat_message('message', avatar=avatar):
                        st.write(f"{View.get_user_by_id(message.sender_id).username} ({message.sender_id})")
                        st.write(f"<b>{message.content}</b>", unsafe_allow_html=True)
        else:
            st.write("No messages yet.")
        
        user_id = st.session_state.get("user_id", None)
        if user_id:
            message_content = st.chat_input("Write your message")
            if message_content:
                View.send_message(group.id, user_id, message_content)
                st.rerun()

    @staticmethod
    def group_info(group_name: str, user_is_admin=False):
        group = View.get_group_by_name(group_name)
        
        with st.container(border=True):
            st.write(f"Título: {group_name}")
        with st.container(border=True):
            st.write(f"Descrição: {group.description}")

        members = View.get_members_by_group(group.id)
        if members:
            with st.container(border=True):
                st.write("Membros:")
                for member in members:
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.markdown('- ' + View.get_user_by_id(member.user_id).username)
                    with col2:
                        if user_is_admin and member.user_id != st.session_state.user_id:
                            with st.popover(""):
                                if st.button(f"Remover {View.get_user_by_id(member.user_id).username} do grupo", key=f"remove_{member.user_id}"):
                                    View.remove_member_from_group(group.id, member.user_id)
                                    st.rerun()
                                
                                is_member_admin = member.permissions == Permission.ALL
                                
                                if is_member_admin:
                                    if st.button(f"Remover admin {View.get_user_by_id(member.user_id).username}", key=f"remove_admin_{member.user_id}"):
                                        View.update_member_permissions(member.id, Permission.read_messages | Permission.send_messages)
                                        st.rerun()
                                
                                st.write("Permissões:")
                                can_read = st.checkbox(
                                    "Ler mensagens",
                                    value=bool(member.permissions & Permission.read_messages),
                                    key=f"read_{member.user_id}"
                                )
                                can_send = st.checkbox(
                                    "Enviar mensagens",
                                    value=bool(member.permissions & Permission.send_messages),
                                    key=f"send_{member.user_id}"
                                )
                                can_admin = st.checkbox(
                                    "Administrar",
                                    value=is_member_admin,
                                    key=f"admin_{member.user_id}"
                                )

                                if st.button(f"Salvar permissões para {View.get_user_by_id(member.user_id).username}", key=f"save_permissions_{member.user_id}"):
                                    new_permissions = Permission(0)
                                    if can_read:
                                        new_permissions |= Permission.read_messages
                                    if can_send:
                                        new_permissions |= Permission.send_messages
                                    if can_admin:
                                        new_permissions = Permission.ALL
                                    View.update_member_permissions(member.id, new_permissions)
                                    st.rerun()
        else:
            st.write("Sem membros ainda.")

    @staticmethod
    def create_group():
        with st.expander("Criar grupo"):
            group_name = st.text_input("Nome do grupo")
            description = st.text_input("Descrição do grupo")
            members = st.multiselect(
                "Membros",
                [user.username for user in View.list_users() if user.id != st.session_state.user_id],
            )

            if st.button("Criar"):
                if not group_name:
                    st.error("O nome do grupo é obrigatório.")
                    return

                if group_name in [group.group_name for group in View.list_groups()]:
                    st.error("Já existe um grupo com esse nome.")
                    return

                if not members:
                    st.error("Selecione pelo menos um membro.")
                    return

                members_ids = [View.get_user_by_name(member).id for member in members]
                if not description:
                    description = ""

                try:
                    View.create_group(group_name, description)
                    View.add_members_to_group(group_name, members_ids)
                    View.add_members_to_group(group_name, [st.session_state.user_id], admin=True)
                    st.success("Grupo criado com sucesso!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao criar o grupo: {e}")