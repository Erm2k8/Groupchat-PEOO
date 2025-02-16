import streamlit as st
from views.views import View

class Groups:
    @staticmethod
    def render_group(group_name: str):
        group = View.get_group_by_name(group_name)
        
        if group:
            st.title(group.group_name)
            st.write(f"Description: {group.description}")
            
            messages = View.get_messages_by_group(group.id)
            if messages:
                with st.container(height=400, border=False):
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
                    # st.success("Message sent successfully!")
                    st.rerun()
            
            members = View.get_members_by_group(group.id)
            if members:
                st.write("Group Members:")
                for member in members:
                    st.write(f"User {member.user_id} with permission {member.permissions}")
            else:
                st.write("No members found.")
        else:
            st.error("Group not found.")

    @staticmethod
    def render_messages():
        ...