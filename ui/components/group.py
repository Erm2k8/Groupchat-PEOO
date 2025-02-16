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
                st.write("Messages:")
                for message in messages:
                    st.write(f"{message.user_id}: {message.content}")
            else:
                st.write("No messages yet.")
            
            user_id = st.session_state.get("user_id", None)
            if user_id:
                message_content = st.text_area("Write your message")
                if st.button("Send Message"):
                    if message_content:
                        View.send_message(group.id, user_id, message_content)
                        st.success("Message sent successfully!")
                    else:
                        st.error("Please enter a message.")
            
            members = View.get_members_by_group(group.id)
            if members:
                st.write("Group Members:")
                for member in members:
                    st.write(f"User {member.user_id} with permission {member.permissions}")
            else:
                st.write("No members found.")
        else:
            st.error("Group not found.")
