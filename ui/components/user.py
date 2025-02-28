import streamlit as st
from views.views import View

class UserUI:
    @st.dialog("Editar Perfil", width="large")
    @staticmethod
    def edit_profile():
        user_id = st.session_state.get("user_id")
        if not user_id:
            st.error("Usuário não autenticado.")
            return

        user = View.get_user_by_id(user_id)

        st.title("Editar Perfil")

        new_username = st.text_input("Nome de usuário", value=user.username)
        new_email = st.text_input("E-mail", value=user.email)

        st.divider()
        st.subheader("Alterar Senha (Opcional)")
        current_password = st.text_input("Senha Atual", type="password")
        new_password = st.text_input("Nova Senha", type="password")
        confirm_password = st.text_input("Confirme a Nova Senha", type="password")

        if st.button("Salvar Alterações", type="primary"):
            if new_username != user.username and View.get_user_by_name(new_username):
                st.error("Nome de usuário já está em uso.")
                return

            if new_email != user.email and View.get_user_by_email(new_email):
                st.error("E-mail já está cadastrado.")
                return

            if new_password:
                if new_password != confirm_password:
                    st.error("As senhas não coincidem.")
                    return
                
                if not View.verify_password(user_id, current_password):
                    st.error("Senha atual incorreta.")
                    return

                View.update_user(user_id, new_username, new_email, new_password)
            else:
                View.update_user(user_id, new_username, new_email)

            st.success("Perfil atualizado com sucesso!")
            st.rerun()

