import streamlit as st
from views.views import View

class Groups:
    @staticmethod
    def render_group(group_name: str):
        group = View.get_group_by_name(group_name)

        if group:
            st.title(group.group_name)
            if st.button("Group Info", key=f"group_info_{group_name}"):
                Groups.group_info(group_name)
            st.write(f"Descrição: {group.description}")
            
            Groups.render_messages(View.get_group_by_id(group.id))
            
            members = View.get_members_by_group(group.id)
        else:
            st.error("Group not found.")

    @staticmethod
    def render_messages(group):
        messages = View.get_messages_by_group(group.id)
        if messages:
            with st.container(height=550, border=False):
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
                    