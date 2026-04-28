import streamlit as st

def verifier_connexion():
    if "acces_autorise" not in st.session_state:
        st.session_state["acces_autorise"] = False

    if not st.session_state["acces_autorise"]:
        # --- Masquer la sidebar, le header et le footer ---
        st.markdown("""
            <style>
                [data-testid="stSidebar"], header, footer {
                    visibility: hidden;
                }
            </style>
        """, unsafe_allow_html=True)

        st.title("🔒 Connexion requise")

        username = st.text_input("Nom d'utilisateur")
        password = st.text_input("Code d'accès", type="password")

        if st.button("Se connecter"):
            if username == "PME_SUIVI" and password == "2025":
                st.session_state["acces_autorise"] = True
                st.success("Connexion réussie ✅")
                st.stop()  # Stoppe ici et affiche le message
            else:
                st.error("❌ Identifiants incorrects.")
        st.stop()


def afficher_sidebar_deconnexion():
    with st.sidebar:
        st.success("✅ Connecté")
        if st.button("🚪 Se déconnecter"):
            st.session_state["acces_autorise"] = False
            st.success("Vous avez été déconnecté.")
            st.stop()
