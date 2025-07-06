# auth.py
import streamlit as st

def verifier_connexion():
    if "acces_autorise" not in st.session_state:
        st.session_state["acces_autorise"] = False

    if not st.session_state["acces_autorise"]:
        # Appliquer les styles (masquer sidebar + header + footer)
        st.markdown("""
            <style>
                [data-testid="stSidebar"], header, footer {
                    visibility: hidden;
                }
            </style>
        """, unsafe_allow_html=True)

        st.title("🔒 Connexion requise")
        username = st.text_input("Nom d'utilisateur")
        password = st.text_input("Code d'accès", type="password", key="login")

        if st.button("Se connecter"):
            if username == "PME_SUIVI" and password == "2025":
                st.session_state["acces_autorise"] = True
                st.experimental_rerun()  # Utilisation compatible avec les anciennes versions
            else:
                st.error("❌ Identifiants incorrects.")
        st.stop()


def afficher_sidebar_deconnexion():
    with st.sidebar:
        st.success("✅ Connecté")
        if st.button("🚪 Se déconnecter"):
            st.session_state["acces_autorise"] = False
            st.experimental_rerun()
