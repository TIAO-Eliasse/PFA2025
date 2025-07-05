import streamlit as st






# --- Définition des couleurs et police ---
primary_color = "#D28E8E"
background_color = "#528D4E"
secondary_background_color = "#F0F2F6"
text_color = "#31333F"
font_family = "sans-serif" # Correspond à "Sans empattement"


# --- Injection de CSS personnalisé ---
st.markdown(
    f"""
    <style>
    /* Général (corps de la page) */
    body {{
        color: {text_color};
        background-color: {background_color};
        font-family: {font_family};
    }}

    /* Styles pour le conteneur principal de Streamlit */
    .stApp {{
        background-color: {background_color};
        color: {text_color};
        font-family: {font_family};
    }}

    /* Barre latérale et éléments similaires (secondary_background_color) */
    .stSidebar {{
        background-color: {secondary_background_color};
        color: {text_color}; /* Le texte dans la sidebar devrait être lisible */
    }}

    .st-emotion-cache-16txt3u {{ /* Cible le fond des conteneurs par exemple */
        background-color: {secondary_background_color};
    }}

    .st-emotion-cache-zq5wmm {{ /* Cible le fond des conteneurs par exemple */
        background-color: {secondary_background_color};
    }}

    /* Boutons (primary_color) */
    .stButton>button {{
        background-color: {primary_color};
        color: white; /* Texte blanc sur bouton primaire pour un bon contraste */
        border: none;
    }}

    /* Curseurs (sliders) - la couleur principale est souvent utilisée ici */
    .stSlider>div>div>div>div {{ /* La barre du curseur */
        background-color: {primary_color};
    }}
    .stSlider>div>div>div>div>div[data-testid="stSliderHandle"] {{ /* Le "pouce" du curseur */
        background-color: {primary_color};
    }}

    /* Entrées de texte, zones de texte (peut aussi utiliser primaryColor ou textColor) */
    .stTextInput>div>div>input {{
        color: {text_color};
        background-color: {secondary_background_color};
        border-color: {primary_color}; /* Bordure pour les inputs */
    }}
    .stTextArea>div>div>textarea {{
        color: {text_color};
        background-color: {secondary_background_color};
        border-color: {primary_color};
    }}

    /* Titres (H1, H2, etc.) */
    h1, h2, h3, h4, h5, h6 {{
        color: {primary_color}; /* Utiliser la couleur primaire pour les titres peut être sympa */
        font-family: {font_family};
    }}

    /* Texte général */
    p, li, div, span {{
        color: {text_color};
        font-family: {font_family};
    }}

    /* Liens */
    a {{
        color: {primary_color};
    }}

    /* Expander / Checkbox / Radio / Selectbox */
    .st-emotion-cache-1f1c24p, /* Checkbox label */
    .st-emotion-cache-1cpxd0t, /* Radio label */
    .st-emotion-cache-1oe5f0g, /* Selectbox label */
    .st-emotion-cache-1c09d5y, /* Expander header */
    .st-emotion-cache-1y4y1h6 {{ /* Expander header content */
        color: {text_color};
    }}

    .st-emotion-cache-v0n0as, /* Background of selectbox options */
    .st-emotion-cache-j9f0gy,
    .st-emotion-cache-1c9s62z {{ /* Hover background of selectbox options */
        background-color: {secondary_background_color} !important;
        color: {text_color} !important;
    }}

    /* La couleur de survol pour les options sélectionnées */
    .st-emotion-cache-1c9s62z:hover {{
        background-color: {primary_color} !important;
        color: white !important;
    }}

    /* Éléments st.container avec bordure */
    .stContainer {{
        background-color: {secondary_background_color};
        border: 1px solid {primary_color}; /* Ajoute une bordure pour distinguer */
    }}
    </style>
    """,
    unsafe_allow_html=True
)




if "acces_autorise" not in st.session_state:
    st.session_state["acces_autorise"] = False

if not st.session_state["acces_autorise"]:
    st.title("🔒 Connexion requise")

    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Code d'accès", type="password")

    if st.button("Se connecter"):
        if username == "PME_SUIVI" and password == "2025":
            st.session_state["acces_autorise"] = True
            st.rerun()

        else:
            st.error("❌ Identifiants incorrects.")
else:
    st.title("📊 Bienvenue sur l'application PME Cameroun")


    
    

    st.markdown("""
        <style>
            .centered {
                text-align: center;
                margin: 6px 0;
                color: #003366;
                font-weight: 600;
            }
            .title-section {
                font-size: 20px;
            }
            .row-container {
                display: flex;
                justify-content: space-between;
                margin-top: 20px;
                padding-top: 10px;
                border-top: 1px solid #ccc;
            }
            .row-item {
                width: 48%;
                font-size: 16px;
                line-height: 1.4;
            }
        </style>

        <h4 class="centered">🏛️ Institut National de la Statistique (INS) - Cameroun</h4>
        

        <hr style="margin:8px 0 18px 0;">

        <p class="centered" style="margin-top:12px;"><strong>Titre :</strong><br>
        <em>Dispositif pour le suivi des PME au Cameroun</em></p>
        <p class="centered">Auteur : <strong>TIAO Eliasse</strong></p>
        <p class="centered">Date : <strong>2025</strong></p>

        <p class="centered" style="margin-top:14px;"><strong>Stage :</strong> Du 19 Mars au 19 Juillet</p>

        <p class="centered" style="margin-top:18px;"><strong>Mise en place par :</strong><br>
        <strong>TIAO Eliasse</strong>, Élève Ingénieur Statisticien Economiste 3ème année</p>

        <div class="row-container">
            <div class="row-item">
                <strong>Encadreur professionnel :</strong><br>
                M. KONLACK LONLACK Giscard<br>
                Chargé d’études assistant à l’INS
            </div>
            <div class="row-item" style="text-align:right;">
                <strong>Encadreur académique :</strong><br>
                M. CHASSEM TCHATCHUN Nacisse Palissy<br>
                Enseignant associé à l’ISSEA
            </div>
        </div>
    """, unsafe_allow_html=True)


    st.markdown("""
        <style>
        /* Arrière-plan général */
        .stApp {
            background-color: #FFFFFF;
            color: #333333;
        }

        /* Titre principal */
        .main-title {
            background-color: #003366;
            color: white;
            padding: 18px;
            border-radius: 10px;
            text-align: center;
            font-size: 28px;
            margin-bottom: 25px;
        }

        /* Cartes et boîtes secondaires */
        .card, .stMarkdown, .stDataFrame, .stTable {
            background-color: #E6F0FA;
            padding: 20px;
            border-radius: 10px;
            border: 1px solid #B0C4DE;
            margin-bottom: 20px;
            color: #333333;
        }

        /* Titres et sous-titres */
        h1, h2, h3, h4, h5, h6 {
            color: #003366;
        }

        /* Boutons */
        .stButton button {
            background-color: #003366;
            color: white;
            border-radius: 8px;
            padding: 12px 20px;
            font-size: 16px;
            border: none;
        }
        .stButton button:hover {
            background-color: #005599;
            color: #f0f0f0;
        }

        /* Inputs */
        input, select, textarea {
            background-color: #FFFFFF;
            border: 2px solid #B0C4DE;
            border-radius: 8px;
            padding: 10px;
            font-size: 15px;
            color: #333333;
        }
        input:focus, select:focus, textarea:focus {
            border: 2px solid #003366;
            background-color: #F8FBFF;
            outline: none;
        }

        /* Slider */
        .stSlider > div {
            background: #E6F0FA;
            padding: 8px;
            border-radius: 10px;
            border: 1px solid #B0C4DE;
        }

        /* Radio et checkbox */
        .stRadio, .stCheckbox {
            background-color: #E6F0FA;
            padding: 10px;
            border-radius: 8px;
            border: 1px solid #B0C4DE;
        }

        /* Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
        }
        ::-webkit-scrollbar-thumb {
            background: #003366;
            border-radius: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #E6F0FA;
        }

        /* Separator line */
        hr {
            border: 1px solid #003366;
        }

        /* Plotly Charts */
        .modebar {
            display: none !important;
        }

        </style>
    """, unsafe_allow_html=True)

    
    # --- Définition des couleurs et police ---
    primary_color = "#D28E8E"
    background_color = "#528D4E"
    secondary_background_color = "#F0F2F6"
    text_color = "#31333F"
    font_family = "sans-serif" # Correspond à "Sans empattement"


    # --- Injection de CSS personnalisé ---
    st.markdown(
        f"""
        <style>
        /* Général (corps de la page) */
        body {{
            color: {text_color};
            background-color: {background_color};
            font-family: {font_family};
        }}

        /* Styles pour le conteneur principal de Streamlit */
        .stApp {{
            background-color: {background_color};
            color: {text_color};
            font-family: {font_family};
        }}

        /* Barre latérale et éléments similaires (secondary_background_color) */
        .stSidebar {{
            background-color: {secondary_background_color};
            color: {text_color}; /* Le texte dans la sidebar devrait être lisible */
        }}

        .st-emotion-cache-16txt3u {{ /* Cible le fond des conteneurs par exemple */
            background-color: {secondary_background_color};
        }}

        .st-emotion-cache-zq5wmm {{ /* Cible le fond des conteneurs par exemple */
            background-color: {secondary_background_color};
        }}

        /* Boutons (primary_color) */
        .stButton>button {{
            background-color: {primary_color};
            color: white; /* Texte blanc sur bouton primaire pour un bon contraste */
            border: none;
        }}

        /* Curseurs (sliders) - la couleur principale est souvent utilisée ici */
        .stSlider>div>div>div>div {{ /* La barre du curseur */
            background-color: {primary_color};
        }}
        .stSlider>div>div>div>div>div[data-testid="stSliderHandle"] {{ /* Le "pouce" du curseur */
            background-color: {primary_color};
        }}

        /* Entrées de texte, zones de texte (peut aussi utiliser primaryColor ou textColor) */
        .stTextInput>div>div>input {{
            color: {text_color};
            background-color: {secondary_background_color};
            border-color: {primary_color}; /* Bordure pour les inputs */
        }}
        .stTextArea>div>div>textarea {{
            color: {text_color};
            background-color: {secondary_background_color};
            border-color: {primary_color};
        }}

        /* Titres (H1, H2, etc.) */
        h1, h2, h3, h4, h5, h6 {{
            color: {primary_color}; /* Utiliser la couleur primaire pour les titres peut être sympa */
            font-family: {font_family};
        }}

        /* Texte général */
        p, li, div, span {{
            color: {text_color};
            font-family: {font_family};
        }}

        /* Liens */
        a {{
            color: {primary_color};
        }}

        /* Expander / Checkbox / Radio / Selectbox */
        .st-emotion-cache-1f1c24p, /* Checkbox label */
        .st-emotion-cache-1cpxd0t, /* Radio label */
        .st-emotion-cache-1oe5f0g, /* Selectbox label */
        .st-emotion-cache-1c09d5y, /* Expander header */
        .st-emotion-cache-1y4y1h6 {{ /* Expander header content */
            color: {text_color};
        }}

        .st-emotion-cache-v0n0as, /* Background of selectbox options */
        .st-emotion-cache-j9f0gy,
        .st-emotion-cache-1c9s62z {{ /* Hover background of selectbox options */
            background-color: {secondary_background_color} !important;
            color: {text_color} !important;
        }}

        /* La couleur de survol pour les options sélectionnées */
        .st-emotion-cache-1c9s62z:hover {{
            background-color: {primary_color} !important;
            color: white !important;
        }}

        /* Éléments st.container avec bordure */
        .stContainer {{
            background-color: {secondary_background_color};
            border: 1px solid {primary_color}; /* Ajoute une bordure pour distinguer */
        }}
        </style>
        """,
        unsafe_allow_html=True
    )