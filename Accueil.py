import streamlit as st
from auth import verifier_connexion, afficher_sidebar_deconnexion

# --- Style personnalisé AVANT vérification connexion ---
primary_color = "#D28E8E"
background_color = "#528D4E"
secondary_background_color = "#F0F2F6"
text_color = "#31333F"
font_family = "sans-serif"

st.markdown(
    f"""
    <style>
    body {{
        background-color: {background_color};
        font-family: {font_family};
        color: {text_color};
    }}
    .stApp {{ background-color: {background_color}; color: {text_color}; }}
    .stSidebar {{ background-color: {secondary_background_color}; color: {text_color}; }}
    .stButton>button {{
        background-color: {primary_color}; color: white; border: none;
    }}
    h1, h2, h3, h4, h5, h6 {{ color: {primary_color}; font-family: {font_family}; }}
    </style>
    """,
    unsafe_allow_html=True
)

# --- Blocage si non connecté ---
verifier_connexion()

# --- Sidebar déconnexion ---
afficher_sidebar_deconnexion()

# --- Contenu principal après connexion ---
st.title("📊 Bienvenue sur l'application PME Cameroun")

st.markdown("""
<h4 style='text-align:center;'>🏛️ Institut National de la Statistique (INS) - Cameroun</h4>
<hr>
<p style='text-align:center;'><strong>Titre :</strong><br><em>Dispositif pour le suivi des PME au Cameroun</em></p>
<p style='text-align:center;'>Auteur : <strong>TIAO Eliasse</strong></p>
<p style='text-align:center;'>Date : <strong>2025</strong></p>
<p style='text-align:center;'><strong>Stage :</strong> Du 19 Mars au 19 Juillet</p>
<p style='text-align:center;'><strong>Mise en place par :</strong><br><strong>TIAO Eliasse</strong>, Élève Ingénieur Statisticien Economiste 3ème année</p>
<div style='display:flex; justify-content:space-between;'>
  <div style='width:48%; font-size:16px;'>
    <strong>Encadreur professionnel :</strong><br>
    M. KONLACK LONLACK Giscard<br>
    Chargé d’études assistant à l’INS
  </div>
  <div style='width:48%; font-size:16px; text-align:right;'>
    <strong>Encadreur académique :</strong><br>
    M. CHASSEM TCHATCHUN Nacisse Palissy<br>
    Enseignant associé à l’ISSEA
  </div>
</div>
""", unsafe_allow_html=True)
