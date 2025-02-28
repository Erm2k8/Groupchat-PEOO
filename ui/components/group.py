import streamlit as st
from views.views import View
import uuid

class Groups:
    @staticmethod
    def render_group(group_name: str):
        group = View.get_group_by_name(group_name)

        if group:
            key = str(uuid.uuid4())
            st.title(group.group_name)
            if st.button("Detalhes do grupo", key=key):
                Groups.group_info(group_name)
            # st.write(f"Descrição: {group.description}")
            
            Groups.render_messages(View.get_group_by_id(group.id))
            
            members = View.get_members_by_group(group.id)
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
    @st.dialog("Informações do grupo")
    def group_info(group_name: str):
        with st.container(border=True):
            st.write(f"Título: {group_name}")
        with st.container(border=True):
            st.write(f"Descrição: {View.get_group_by_name(group_name).description}")

        members = View.get_members_by_group(View.get_group_by_name(group_name).id)
        if members:
            with st.container(border=True):
                st.write("Membros:")
                for member in members:
                    st.markdown('- ' + View.get_user_by_id(member.user_id).username)
        else:
            st.write("Sem membros ainda.")

    @staticmethod
    @st.dialog("Criar grupo", width="large")
    def create_group():
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
            