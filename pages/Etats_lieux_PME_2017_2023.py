import pandas as pd
import json
import plotly.graph_objects as go
import streamlit as st
import folium
import plotly.express as px
from streamlit_folium import st_folium
import streamlit as st
import plotly.express as px

import streamlit as st
#st.header("Suivi des PME - Carte Plotly avec labels fixes")



import streamlit as st

# Bloquer l'accès si l'utilisateur n'est pas connecté
if "acces_autorise" not in st.session_state or not st.session_state["acces_autorise"]:
    st.error("🔒 Accès refusé. Veuillez d'abord vous connecter depuis la page d'accueil.")
    st.stop()



st.set_page_config(page_title="Suivi des PME", layout="wide")



st.markdown(
        """
        <h2 style='text-align: center; color: black; font-size: 30px;'>
            Eats des lieux des PME sur la période 2016-2023
        </h2>
        """,
        unsafe_allow_html=True
    )
## Fonctionn globale 


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


st.markdown("""
    <style>
    .stTabs [data-baseweb="tab-list"] {
        justify-content: space-around;
    }
    </style>
    """, unsafe_allow_html=True)



# 📦 Fonction de chargement et préparation de la base
@st.cache_data
def charger_base(path):
    base = pd.read_excel(path)
    base['Age_entreprise_reel'] = base.groupby('Type d\'entreprise')['Age_entreprise_reel'].transform(
        lambda x: x.fillna(x.median())
    )
    return base

# 📂 Chargement une seule fois via le cache
base_path = "data//base_finalPME_Annee_demaragetraité_en_attentant_confirmation13_modelisation.xlsx"
base = charger_base(base_path)

base['Région'] = base['Région'].str.upper().replace('SUD OUEST', 'SUD-OUEST')

    # Renommer 'AUTRES FORMES JURIDIQUE' en 'AUTRES'
base["Forme juridique"] = base["Forme juridique"].replace("Autres formes juridiques", "AUTRES")

# Configuration
#st.set_page_config(page_title="Tableau de bord PME Cameroun", layout="wide")

# Titre général
#st.title("📊 Tableau de bord PME Cameroun")
import json
import streamlit as st

# 📦 Fonction de chargement et mise en cache du GeoJSON
@st.cache_data
def charger_geojson(path):
    with open(path, encoding="utf-8") as f:
        geo = json.load(f)
    # Harmoniser les noms
    for feature in geo['features']:
        feature['properties']['NAME_1'] = feature['properties']['NAME_1'].upper()
    return geo

# 📂 Charger une seule fois
geojson_path ="data//cameroon_regions.geojson"
geo = charger_geojson(geojson_path)


# Création des onglets
tabs = st.tabs(["Répartitions des PME", "Analyse mortalité globale", "Analyse par région"])

# Onglet Statistiques descriptives
with tabs[0]:
    import streamlit as st
    import pandas as pd

    # Préparation des données
    type_counts = base["Secteur d'activités"].value_counts(normalize=True).reset_index()
    type_counts.columns = ["Secteur d'activités", 'Pourcentage']
    type_counts['Pourcentage'] *= 100
    type_counts['Pourcentage'] = type_counts['Pourcentage'].round(1)
    col=st.columns(3)
    with col[1]:
        st.write("Répartition des PME par secteur d'activités")
    # Créer les colonnes (3 colonnes côte à côte)
    col1, col2, col3= st.columns(3)

    # Afficher chaque modalité dans un carré
    with col1:
        
        st.markdown(
            f"""
            <div style='background-color:#dfe7fd; padding:20px; border-radius:12px; text-align:center;'>
                <h4>{type_counts.iloc[0,0]}</h4>
                <p style='font-size:32px; font-weight:bold;'>{type_counts.iloc[0,1]}%</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div style='background-color:#cfe2f3; padding:20px; border-radius:12px; text-align:center;'>
                <h4>{type_counts.iloc[1,0]}</h4>
                <p style='font-size:32px; font-weight:bold;'>{type_counts.iloc[1,1]}%</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div style='background-color:#b6d7a8; padding:20px; border-radius:12px; text-align:center;'>
                <h4>{type_counts.iloc[2,0]}</h4>
                <p style='font-size:32px; font-weight:bold;'>{type_counts.iloc[2,1]}%</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    
    import streamlit as st
    import pandas as pd
    import plotly.graph_objects as go

    # 📌 Récupération des secteurs disponibles
    secteurs_disponibles = sorted(base['Secteur d\'activités'].dropna().unique())

    # 📌 Division en deux colonnes (25% / 75%)
    col1, col2 = st.columns([1, 3])

    # 📋 Colonne de gauche : Cases à cocher une par une
    with col1:
        st.markdown("### 🔍 Choix du secteur")
        secteurs_selectionnes = []
        for secteur in secteurs_disponibles:
            if st.checkbox(secteur, value=True, key=secteur):
                secteurs_selectionnes.append(secteur)

    # 📌 Filtrage de la base selon les secteurs choisis
    base_filtrée = base[base["Secteur d'activités"].isin(secteurs_selectionnes)]

    # 📊 Effectifs et pourcentages par région
    counts = base_filtrée['Région'].value_counts().reset_index()
    counts.columns = ['Région', 'Nombre']
    total_pme = len(base_filtrée[base_filtrée["Type d'entreprise"].isin(['PE', 'TPE', 'ME'])])
    counts['Pourcentage'] = (counts['Nombre'] / total_pme) * 100

    # 📌 Calcul des centroïdes
    region_coords = []
    for feature in geo['features']:
        region_name = feature['properties']['NAME_1']
        coords = feature['geometry']['coordinates'][0]
        if isinstance(coords[0][0], list):  # MultiPolygon
            coords = coords[0]
        lon = [c[0] for c in coords]
        lat = [c[1] for c in coords]
        lon_center = sum(lon) / len(lon)
        lat_center = sum(lat) / len(lat)
        region_coords.append({'Région': region_name, 'lon': lon_center, 'lat': lat_center})

    coords_df = pd.DataFrame(region_coords)
    final_df = coords_df.merge(counts, on='Région', how='left').fillna(0)
    final_df['label'] = final_df['Région'] + "<br>" + final_df['Pourcentage'].round(1).astype(str) + " %"

    # 🗺️ Colonne de droite : Affichage de la carte
    with col2:
        fig = go.Figure()

        fig.add_trace(go.Choropleth(
            geojson=geo,
            locations=counts['Région'],
            z=counts['Pourcentage'],
            featureidkey="properties.NAME_1",
            colorscale="Blues",
            reversescale=False,
            colorbar_title="Taux (%)",
            marker_line_color="white",
            zmin=0,
            zmax=counts['Pourcentage'].max(),
            hovertemplate="<b>%{location}</b><br>Taux de cessation : %{z:.1f} %<extra></extra>"
        ))

        fig.add_trace(go.Scattergeo(
            lon=final_df['lon'],
            lat=final_df['lat'],
            text=final_df['label'],
            mode='text',
            textfont=dict(size=13, color="#000000"),
            showlegend=False
        ))

        fig.update_geos(
            fitbounds="locations",
            visible=False,
            showcountries=False,
            showsubunits=False,
            lonaxis_range=[8, 16.5],
            lataxis_range=[1.5, 13.5]
        )

        fig.update_layout(
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            height=500
        )

        st.plotly_chart(fig, use_container_width=True)
   

    # Liste des régions
    regions_disponibles = sorted(base['Région'].dropna().unique())

    # Initialisation session_state
    if "regions_cochées" not in st.session_state:
        st.session_state["regions_cochées"] = {region: True for region in regions_disponibles}

    def toggle_regions():
        tous_cochés = all(st.session_state["regions_cochées"].values())
        for region in regions_disponibles:
            st.session_state["regions_cochées"][region] = not tous_cochés

    # Injecter du CSS global pour limiter la hauteur + scroll dans la colonne de régions
    st.markdown(
        """
        <style>
        /* Sélecteur spécifique pour la colonne des régions */
        .css-1adrfps.e1fqkh3o3 {
            max-height: 500px;
            overflow-y: auto;
            border: none !important;
            padding: 0 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Colonnes principales
    col_régions, col1, col2 = st.columns([1, 2, 2])

    # Colonne régions
    with col_régions:
        st.markdown("##### Filtrer par région")
        st.button("Tout cocher / décocher", on_click=toggle_regions)

        n = len(regions_disponibles)
        for i in range(0, n, 2):
            cols = st.columns(2)
            for j in range(2):
                idx = i + j
                if idx < n:
                    region = regions_disponibles[idx]
                    checked = cols[j].checkbox(
                        region,
                        value=st.session_state["regions_cochées"][region],
                        key="region_" + region
                    )
                    st.session_state["regions_cochées"][region] = checked

    regions_selectionnees = [r for r in regions_disponibles if st.session_state["regions_cochées"][r]]

    # Filtrer la base
    base_filtrée = base[base['Région'].isin(regions_selectionnees)]

    # Graphique Forme juridique
    with col1:
        forme_counts = base_filtrée['Forme juridique'].value_counts(normalize=True).reset_index()
        forme_counts.columns = ['Forme juridique', 'Pourcentage']
        forme_counts['Pourcentage'] *= 100

        fig_forme = px.bar(
            forme_counts,
            x='Forme juridique',
            y='Pourcentage',
            color_discrete_sequence=['#003366'],
            text=forme_counts['Pourcentage'].apply(lambda x: f"{x:.1f}%")
        )
        fig_forme.update_traces(textposition='outside')
        fig_forme.update_layout(
            title="Répartition (%) par Forme juridique",
            yaxis_title="Pourcentage (%)",
            xaxis_title="",
            margin=dict(t=10, b=10)
        )
        st.plotly_chart(fig_forme, use_container_width=True)

    # Graphique Type d'entreprise
    with col2:
        type_counts = base_filtrée["Type d'entreprise"].value_counts(normalize=True).reset_index()
        type_counts.columns = ["Type d'entreprise", 'Pourcentage']
        type_counts['Pourcentage'] *= 100

        fig_type = px.pie(
            type_counts,
            names="Type d'entreprise",
            values='Pourcentage',
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig_type.update_traces(textposition='inside', textinfo='percent+label')
        fig_type.update_layout(
            title="Répartition (%) par Type d'entreprise",
            margin=dict(t=40, b=30)
        )
        st.plotly_chart(fig_type, use_container_width=True)




        #st.write("Met ici tes graphiques et indicateurs descriptifs généraux.")

# Onglet Analyse mortalité globale
with tabs[1]:
    st.header("  Analyse de la mortalité globale")
    
    # Exemple : Calculs
    nb_total = len(base)
    nb_cessation = base[base["Etat_entreprise"] == "Cessation activités"].shape[0]
    taux_mortalite = (nb_cessation / nb_total) * 100


    # Indicateurs sous forme de cards (réduction de taille)
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
            <div style="background-color:#E6F0FF;padding:15px;border-radius:12px;text-align:center;box-shadow: 0px 1px 5px rgba(0,0,0,0.1)">
                <h5 style="color:#004080;margin-bottom:8px;">Nombre total de PME</h5>
                <h2 style="color:#007BFF;margin:0;">{nb_total:,}</h2>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div style="background-color:#FFF0F0;padding:15px;border-radius:12px;text-align:center;box-shadow: 0px 1px 5px rgba(0,0,0,0.1)">
                <h5 style="color:#800000;margin-bottom:8px;">PME en cessation</h5>
                <h2 style="color:#FF4B4B;margin:0;">{nb_cessation:,}</h2>
            </div>
            """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
            <div style="background-color:#FFF7E6;padding:15px;border-radius:12px;text-align:center;box-shadow: 0px 1px 5px rgba(0,0,0,0.1)">
                <h5 style="color:#804000;margin-bottom:8px;">Taux de mortalité</h5>
                <h2 style="color:#FF8800;margin:0;">{taux_mortalite:.2f} %</h2>
            </div>
            """, unsafe_allow_html=True)


    # Calcul du taux de mortalité par Région
    total_region = base.groupby('Région').size().reset_index(name='Total_PME')
    cessation_region = base[base['Etat_entreprise'] == 'Cessation activités'].groupby('Région').size().reset_index(name='Cessation_PME')
    region_stats = pd.merge(total_region, cessation_region, on='Région', how='left').fillna(0)
    region_stats['Taux_mortalite'] = (region_stats['Cessation_PME'] / region_stats['Total_PME']) * 100
    region_stats = region_stats.sort_values('Taux_mortalite', ascending=False)

    # Calcul du taux de mortalité par Type d’entreprise
    total_type = base.groupby("Type d'entreprise").size().reset_index(name='Total_PME')
    cessation_type = base[base['Etat_entreprise'] == 'Cessation activités'].groupby("Type d'entreprise").size().reset_index(name='Cessation_PME')
    type_stats = pd.merge(total_type, cessation_type, on="Type d'entreprise", how='left').fillna(0)
    type_stats['Taux_mortalite'] = (type_stats['Cessation_PME'] / type_stats['Total_PME']) * 100
    type_stats = type_stats.sort_values('Taux_mortalite', ascending=False)

    # 📊 Affichage côte à côte dans Streamlit
    col1, col2 = st.columns(2)

    with col1:
        fig_region = px.bar(
            region_stats,
            x='Région',
            y='Taux_mortalite',
            color='Taux_mortalite',  # colore selon valeur du taux
            color_continuous_scale='Reds',
            text=region_stats['Taux_mortalite'].apply(lambda x: f"{x:.1f}%"),
            labels={'Taux_mortalite': 'Taux de mortalité (%)'}
        )

        fig_region.update_traces(textposition='inside')
        fig_region.update_coloraxes(showscale=False)  # retire colorbar
        fig_region.update_layout(
            title="Taux de mortalité par Région",
            showlegend=False,
            yaxis_title="Taux de mortalité (%)",
            margin=dict(l=20, r=20, t=50, b=50),
            height=350
        )

        st.plotly_chart(fig_region, use_container_width=True)

    with col2:
        fig_type = px.bar(
            type_stats,
            x="Type d'entreprise",
            y='Taux_mortalite',
            color='Taux_mortalite',
            color_continuous_scale='Reds',
            text=type_stats['Taux_mortalite'].apply(lambda x: f"{x:.1f}%"),
            labels={'Taux_mortalite': 'Taux de mortalité (%)'}
        )

        fig_type.update_traces(textposition='inside')
        fig_type.update_coloraxes(showscale=False)
        fig_type.update_layout(
            title="Taux de mortalité par Type d'entreprise",
            showlegend=False,
            yaxis_title="Taux de mortalité (%)",
            margin=dict(l=20, r=20, t=50, b=50),
            height=350
        )

        st.plotly_chart(fig_type, use_container_width=True)



    import streamlit as st
    import plotly.express as px
    import plotly.graph_objects as go

    # Calcul taux mortalité par Secteur d’activités
    secteur_stats = base.groupby('Secteur d\'activités').agg(
        Total_PME=('Etat_entreprise', 'count'),
        Cessation_PME=('Etat_entreprise', lambda x: (x == 'Cessation activités').sum())
    ).reset_index()
    secteur_stats['Taux_mortalite'] = (secteur_stats['Cessation_PME'] / secteur_stats['Total_PME']) * 100
    secteur_stats = secteur_stats.sort_values('Taux_mortalite', ascending=False)

    # Calcul taux mortalité par Forme juridique
    forme_stats = base.groupby('Forme juridique').agg(
        Total_PME=('Etat_entreprise', 'count'),
        Cessation_PME=('Etat_entreprise', lambda x: (x == 'Cessation activités').sum())
    ).reset_index()
    forme_stats['Taux_mortalite'] = (forme_stats['Cessation_PME'] / forme_stats['Total_PME']) * 100
    forme_stats = forme_stats.sort_values('Taux_mortalite', ascending=False)

    # Calcul par Tenue d'une comptabilité écrite
    compta_stats = base.groupby("Tenue d'une comptabilité écrite").agg(
        Total_PME=('Etat_entreprise', 'count'),
        Cessation_PME=('Etat_entreprise', lambda x: (x == 'Cessation activités').sum())
    ).reset_index()
    compta_stats['Taux_mortalite'] = (compta_stats['Cessation_PME'] / compta_stats['Total_PME']) * 100

    # Création colonnes Streamlit
    col1, col2, col3 = st.columns(3)

    with col1:
        fig_secteur = px.bar(
            secteur_stats,
            x='Secteur d\'activités',
            y='Taux_mortalite',
            color='Taux_mortalite',
            color_continuous_scale='Reds',
            text=secteur_stats['Taux_mortalite'].apply(lambda x: f"{x:.1f}%"),
        )
        fig_secteur.update_traces(textposition='inside')
        fig_secteur.update_coloraxes(showscale=False)
        fig_secteur.update_layout(
            title_text="Taux de mortalité par Secteur d'activités",
            yaxis_title="Taux de mortalité (%)",
            xaxis_title="Secteur d'activités",
            showlegend=False,
            margin=dict(l=20, r=20, t=50, b=50),
            height=350,
        )
        st.plotly_chart(fig_secteur, use_container_width=True)

    with col2:
        fig_forme = px.bar(
            forme_stats,
            x='Forme juridique',
            y='Taux_mortalite',
            color='Taux_mortalite',
            color_continuous_scale='Reds',
            text=forme_stats['Taux_mortalite'].apply(lambda x: f"{x:.1f}%"),
        )
        fig_forme.update_traces(textposition='inside')
        fig_forme.update_coloraxes(showscale=False)
        fig_forme.update_layout(
            title_text="Taux de mortalité par Forme juridique",
            yaxis_title="Taux de mortalité (%)",
            xaxis_title="Forme juridique",
            showlegend=False,
            margin=dict(l=20, r=20, t=50, b=50),
            height=350,
        )
        st.plotly_chart(fig_forme, use_container_width=True)

    with col3:
        fig_compta = px.bar(
            compta_stats,
            x="Tenue d'une comptabilité écrite",
            y='Taux_mortalite',
            color='Taux_mortalite',
            color_continuous_scale='Reds',
            text=compta_stats['Taux_mortalite'].apply(lambda x: f"{x:.1f}%"),
        )
        fig_compta.update_traces(textposition='inside')
        fig_compta.update_coloraxes(showscale=False)
        fig_compta.update_layout(
            title_text="Comptabilité écrite",
            yaxis_title="Taux de mortalité (%)",
            xaxis_title="Tenue d'une comptabilité écrite",
            showlegend=False,
            margin=dict(l=20, r=20, t=50, b=50),
            height=350,
        )
        st.plotly_chart(fig_compta, use_container_width=True)


    ### Analyse selon les caractéristiques du promoteur




    import streamlit as st
    import pandas as pd
    import plotly.express as px

    # Exemple : ta base 'base' avec les colonnes suivantes (à adapter) :
    # 'Part Fonds propres', 'part Prêt bancaire/Prêt EMF', 'part Subvention/Don/Autre', 'Etat_entreprise'

    # Définition des couleurs Institut National de la Statistique Cameroun
    color_map = {'En activité': '#003366', 'Cessation activités': '#D62728'}

    # Fonction corrigée pour calculer les pourcentages en fonction du seuil
    def calcul_pourcentage_seuil(data, var, seuil):
        if seuil == 0 or seuil == 100:
            return None, None  # Pas de découpage possible

        cat_var = f'Cat_{var}'
        data[cat_var] = pd.cut(
            data[var],
            bins=[0, seuil, 100],
            labels=[f'0-{seuil} %', f'{seuil}-100 %'],
            include_lowest=True
        )
        df_counts = data.groupby([cat_var, 'Etat_entreprise']).size().reset_index(name='count')
        total_par_cat = df_counts.groupby(cat_var)['count'].transform('sum')
        df_counts['percentage'] = round((df_counts['count'] / total_par_cat) * 100, 2)
        return df_counts, cat_var

    # Titre
    st.title("Taux de mortalité selon les sources de financement")

    # Slider unique pour le seuil
    seuil = st.slider(
        "Choisissez le seuil (%) pour catégoriser les parts de financement :",
        min_value=0,
        max_value=100,
        value=50,
        step=5
    )

    # Message d'alerte si seuil = 0 ou 100
    if seuil == 0 or seuil == 100:
        st.warning("⚠️ Veuillez choisir un seuil strictement compris entre 0 et 100 pour afficher les graphiques.")
    else:
        col1, col2, col3 = st.columns(3)

        # Fonds propres
        with col1:
            df_fp, var_fp = calcul_pourcentage_seuil(base, 'Part Fonds propres', seuil)
            fig_fp = px.bar(
                df_fp,
                x=var_fp,
                y='percentage',
                color='Etat_entreprise',
                barmode='group',
                text='percentage',
                color_discrete_map=color_map,
                title="Fonds propres"
            )
            fig_fp.update_traces(texttemplate='%{text:.1f}%', textposition='inside')
            fig_fp.update_layout(
                yaxis_title="Pourcentage (%)",
                xaxis_title="",
                margin=dict(t=40, b=30),
                legend_title_text=""
            )
            st.plotly_chart(fig_fp, use_container_width=True)

        # Prêt bancaire / EMF
        with col2:
            df_pb, var_pb = calcul_pourcentage_seuil(base, 'part Prêt bancaire/Prêt EMF', seuil)
            fig_pb = px.bar(
                df_pb,
                x=var_pb,
                y='percentage',
                color='Etat_entreprise',
                barmode='group',
                text='percentage',
                color_discrete_map=color_map,
                title="Prêt bancaire / EMF"
            )
            fig_pb.update_traces(texttemplate='%{text:.1f}%', textposition='inside')
            fig_pb.update_layout(
                yaxis_title="Pourcentage (%)",
                xaxis_title="",
                margin=dict(t=40, b=30),
                legend_title_text=""
            )
            st.plotly_chart(fig_pb, use_container_width=True)

        # Subvention / Don
        with col3:
            df_sd, var_sd = calcul_pourcentage_seuil(base, 'part Subvention/Don/Autre', seuil)
            fig_sd = px.bar(
                df_sd,
                x=var_sd,
                y='percentage',
                color='Etat_entreprise',
                barmode='group',
                text='percentage',
                color_discrete_map=color_map,
                title="Subvention / Don"
            )
            fig_sd.update_traces(texttemplate='%{text:.1f}%', textposition='inside')
            fig_sd.update_layout(
                yaxis_title="Pourcentage (%)",
                xaxis_title="",
                margin=dict(t=40, b=30),
                legend_title_text=""
            )
            st.plotly_chart(fig_sd, use_container_width=True)





    # 📌 Slider pour Age de l'entreprise
    min_age = base['Age_entreprise_reel'].min()
    max_age = base['Age_entreprise_reel'].max()

    seuil_age = st.slider(
        "👉 Seuil (années) pour catégoriser l'âge de l'entreprise :",
        min_value=int(min_age),
        max_value=int(max_age),
        value=int(max_age / 2),
        step=1
    )

    # 📌 Message d'alerte si seuil aux bornes
    if seuil_age == min_age or seuil_age == max_age:
        st.warning("⚠️ Veuillez choisir un seuil strictement compris entre le minimum et maximum de l'âge pour voir le graphique.")
    else:
        # 📌 Calcul des pourcentages avec seuil pour Age de l'entreprise
        def calcul_pourcentage_age(data, var_quant, seuil, max_val=None):
            if max_val is None:
                max_val = data[var_quant].max()
            
            cat_var = f"{var_quant}_cat"
            data = data.copy()
            data[cat_var] = pd.cut(
                data[var_quant],
                bins=[0, seuil, max_val],
                labels=[f"0-{seuil}", f"{seuil}-{int(max_val)}"],
                include_lowest=True
            )

            df_counts = data.groupby([cat_var, 'Etat_entreprise']).size().reset_index(name='count')
            total_par_cat = df_counts.groupby(cat_var)['count'].transform('sum')
            df_counts['percentage'] = round((df_counts['count'] / total_par_cat) * 100, 2)

            return df_counts, cat_var

        # 📌 Application et graphique
        df_age, var_age = calcul_pourcentage_age(base, 'Age_entreprise_reel', seuil_age, max_val=max_age)

        fig_age = px.bar(
            df_age,
            x=var_age,
            y='percentage',
            color='Etat_entreprise',
            barmode='group',
            text='percentage',
            color_discrete_map=color_map,
            title="Âge de l'entreprise"
        )
        fig_age.update_traces(texttemplate='%{text:.1f}%', textposition='inside')
        fig_age.update_layout(
            yaxis_title="Pourcentage (%)",
            margin=dict(t=40, b=30),
            legend_title_text=""
        )
        st.plotly_chart(fig_age, use_container_width=True)









    import streamlit as st
    import pandas as pd
    import plotly.express as px

    # 📌 Variables qualitatives à afficher
    variables_qualitatives = [
        'Diplome le plus élevé du promoteur',
        'Sexe du promoteur',
        'Nationalité du promoteur',
        'Etat matrimonial du promoteur',
        'Age du promoteur'
    ]

    # 📌 Fonction pour calculer les pourcentages par modalité et état
    def calcul_pourcentage(data, var):
        df_counts = data.groupby([var, 'Etat_entreprise']).size().reset_index(name='count')
        total_par_cat = df_counts.groupby(var)['count'].transform('sum')
        df_counts['percentage'] = round((df_counts['count'] / total_par_cat) * 100, 2)
        return df_counts

    # 📌 Filtres côte à côte
    col1, col2 = st.columns(2)

    with col1:
        types = ['Tous'] + sorted(base["Type d'entreprise"].dropna().unique().tolist())
        selected_types = st.multiselect("Sélectionnez le(s) type(s) d'entreprise :", types, default=['Tous'])

    with col2:
        secteurs = ['Tous'] + sorted(base["Secteur d'activités"].dropna().unique().tolist())
        selected_secteurs = st.multiselect("Sélectionnez le(s) secteur(s) d'activités :", secteurs, default=['Tous'])

    # 📌 Vérification si aucune sélection dans les deux filtres
    if len(selected_types) == 0 or len(selected_secteurs) == 0:
        st.error("⚠️ Veuillez sélectionner au moins un Type d’entreprise et un Secteur d’activités.")
    else:
        # 📌 Application des filtres
        df_filtre = base.copy()

        if 'Tous' not in selected_types:
            df_filtre = df_filtre[df_filtre["Type d'entreprise"].isin(selected_types)]

        if 'Tous' not in selected_secteurs:
            df_filtre = df_filtre[df_filtre["Secteur d'activités"].isin(selected_secteurs)]

        # 📌 Vérification si les filtres donnent un jeu de données vide
        if df_filtre.empty:
            st.warning("Aucune donnée disponible pour cette sélection. Veuillez ajuster vos filtres.")
        else:
            # 📊 Affichage des graphiques (2 par ligne)
            for i in range(0, len(variables_qualitatives), 2):
                cols = st.columns(2)
                for j in range(2):
                    if i + j < len(variables_qualitatives):
                        var = variables_qualitatives[i + j]
                        with cols[j]:
                            df_pct = calcul_pourcentage(df_filtre, var)

                            color_map = {
                                'En activité': '#003366',  # Bleu INS
                                'Cessation activités': '#D62728'  # Rouge
                            }

                            fig = px.bar(
                                df_pct,
                                x=var,
                                y='percentage',
                                color='Etat_entreprise',
                                text='percentage',
                                barmode='group',
                                title=var,
                                color_discrete_map=color_map
                            )
                            fig.update_traces(texttemplate='%{text:.1f}%', textposition='inside')
                            fig.update_layout(
                                yaxis_title='Pourcentage (%)',
                                xaxis_title='',
                                uniformtext_minsize=8,
                                uniformtext_mode='hide',
                                legend_title_text="État de l'entreprise",
                                margin=dict(t=30, b=30),
                                width=350,
                                height=350
                            )
                            st.plotly_chart(fig, use_container_width=True)


### Origine de dinancement :



# Onglet Analyse par région
with tabs[2]:
    st.header("🗺️   Analyse par région")
    regions = sorted(base['Région'].dropna().unique().tolist())
    cols = st.columns([1, 2, 1])

    with cols[1]:
        selected_region = st.selectbox("Sélectionnez une région :", regions)

    
    base = base[base['Région'] == selected_region]
    # Exemple : Calculs
    nb_total = len(base)
    nb_cessation = base[base["Etat_entreprise"] == "Cessation activités"].shape[0]
    taux_mortalite = (nb_cessation / nb_total) * 100


    # Indicateurs sous forme de cards (réduction de taille)
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
            <div style="background-color:#E6F0FF;padding:15px;border-radius:12px;text-align:center;box-shadow: 0px 1px 5px rgba(0,0,0,0.1)">
                <h5 style="color:#004080;margin-bottom:8px;">Nombre total de PME</h5>
                <h2 style="color:#007BFF;margin:0;">{nb_total:,}</h2>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div style="background-color:#FFF0F0;padding:15px;border-radius:12px;text-align:center;box-shadow: 0px 1px 5px rgba(0,0,0,0.1)">
                <h5 style="color:#800000;margin-bottom:8px;">PME en cessation</h5>
                <h2 style="color:#FF4B4B;margin:0;">{nb_cessation:,}</h2>
            </div>
            """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
            <div style="background-color:#FFF7E6;padding:15px;border-radius:12px;text-align:center;box-shadow: 0px 1px 5px rgba(0,0,0,0.1)">
                <h5 style="color:#804000;margin-bottom:8px;">Taux de mortalité</h5>
                <h2 style="color:#FF8800;margin:0;">{taux_mortalite:.2f} %</h2>
            </div>
            """, unsafe_allow_html=True)






    # Calcul du taux de mortalité par Région
    total_region = base.groupby('Région').size().reset_index(name='Total_PME')
    cessation_region = base[base['Etat_entreprise'] == 'Cessation activités'].groupby('Région').size().reset_index(name='Cessation_PME')
    region_stats = pd.merge(total_region, cessation_region, on='Région', how='left').fillna(0)
    region_stats['Taux_mortalite'] = (region_stats['Cessation_PME'] / region_stats['Total_PME']) * 100
    region_stats = region_stats.sort_values('Taux_mortalite', ascending=False)

    # Calcul du taux de mortalité par Type d’entreprise
    total_type = base.groupby("Type d'entreprise").size().reset_index(name='Total_PME')
    cessation_type = base[base['Etat_entreprise'] == 'Cessation activités'].groupby("Type d'entreprise").size().reset_index(name='Cessation_PME')
    type_stats = pd.merge(total_type, cessation_type, on="Type d'entreprise", how='left').fillna(0)
    type_stats['Taux_mortalite'] = (type_stats['Cessation_PME'] / type_stats['Total_PME']) * 100
    type_stats = type_stats.sort_values('Taux_mortalite', ascending=False)

    # 📊 Affichage côte à côte dans Streamlit
    col1, col2 = st.columns(2)

    with col1:
        fig_secteur = px.bar(
            secteur_stats,
            x='Secteur d\'activités',
            y='Taux_mortalite',
            color='Taux_mortalite',
            color_continuous_scale='Reds',
            text=secteur_stats['Taux_mortalite'].apply(lambda x: f"{x:.1f}%"),
        )
        fig_secteur.update_traces(textposition='inside')
        fig_secteur.update_coloraxes(showscale=False)
        fig_secteur.update_layout(
            title_text="Taux de mortalité par Secteur d'activités",
            yaxis_title="Taux de mortalité (%)",
            xaxis_title="Secteur d'activités",
            showlegend=False,
            margin=dict(l=20, r=20, t=50, b=50),
            height=350,
        )
        st.plotly_chart(fig_secteur, use_container_width=True,key="région1")

    with col2:
        fig_type = px.bar(
            type_stats,
            x="Type d'entreprise",
            y='Taux_mortalite',
            color='Taux_mortalite',
            color_continuous_scale='Reds',
            text=type_stats['Taux_mortalite'].apply(lambda x: f"{x:.1f}%"),
            labels={'Taux_mortalite': 'Taux de mortalité (%)'}
        )

        fig_type.update_traces(textposition='inside')
        fig_type.update_coloraxes(showscale=False)
        fig_type.update_layout(
            title="Taux de mortalité par Type d'entreprise",
            showlegend=False,
            yaxis_title="Taux de mortalité (%)",
            margin=dict(l=20, r=20, t=50, b=50),
            height=350
        )

        st.plotly_chart(fig_type, use_container_width=True,key="région2")



    import streamlit as st
    import plotly.express as px
    import plotly.graph_objects as go

    # Calcul taux mortalité par Secteur d’activités
    secteur_stats = base.groupby('Secteur d\'activités').agg(
        Total_PME=('Etat_entreprise', 'count'),
        Cessation_PME=('Etat_entreprise', lambda x: (x == 'Cessation activités').sum())
    ).reset_index()
    secteur_stats['Taux_mortalite'] = (secteur_stats['Cessation_PME'] / secteur_stats['Total_PME']) * 100
    secteur_stats = secteur_stats.sort_values('Taux_mortalite', ascending=False)

    # Calcul taux mortalité par Forme juridique
    forme_stats = base.groupby('Forme juridique').agg(
        Total_PME=('Etat_entreprise', 'count'),
        Cessation_PME=('Etat_entreprise', lambda x: (x == 'Cessation activités').sum())
    ).reset_index()
    forme_stats['Taux_mortalite'] = (forme_stats['Cessation_PME'] / forme_stats['Total_PME']) * 100
    forme_stats = forme_stats.sort_values('Taux_mortalite', ascending=False)

    # Calcul par Tenue d'une comptabilité écrite
    compta_stats = base.groupby("Tenue d'une comptabilité écrite").agg(
        Total_PME=('Etat_entreprise', 'count'),
        Cessation_PME=('Etat_entreprise', lambda x: (x == 'Cessation activités').sum())
    ).reset_index()
    compta_stats['Taux_mortalite'] = (compta_stats['Cessation_PME'] / compta_stats['Total_PME']) * 100

    # Création colonnes Streamlit
    col1, col2 = st.columns(2)


        

    with col1:
        fig_forme = px.bar(
            forme_stats,
            x='Forme juridique',
            y='Taux_mortalite',
            color='Taux_mortalite',
            color_continuous_scale='Reds',
            text=forme_stats['Taux_mortalite'].apply(lambda x: f"{x:.1f}%"),
        )
        fig_forme.update_traces(textposition='inside')
        fig_forme.update_coloraxes(showscale=False)
        fig_forme.update_layout(
            title_text="Taux de mortalité par Forme juridique",
            yaxis_title="Taux de mortalité (%)",
            xaxis_title="Forme juridique",
            showlegend=False,
            margin=dict(l=20, r=20, t=50, b=50),
            height=350,
        )
        st.plotly_chart(fig_forme, use_container_width=True,key="région3")

    with col2:
        fig_compta = px.bar(
            compta_stats,
            x="Tenue d'une comptabilité écrite",
            y='Taux_mortalite',
            color='Taux_mortalite',
            color_continuous_scale='Reds',
            text=compta_stats['Taux_mortalite'].apply(lambda x: f"{x:.1f}%"),
        )
        fig_compta.update_traces(textposition='inside')
        fig_compta.update_coloraxes(showscale=False)
        fig_compta.update_layout(
            title_text="Comptabilité écrite",
            yaxis_title="Taux de mortalité (%)",
            xaxis_title="Tenue d'une comptabilité écrite",
            showlegend=False,
            margin=dict(l=20, r=20, t=50, b=50),
            height=350,
        )
        st.plotly_chart(fig_compta, use_container_width=True, key='région4')


    ### Analyse selon les caractéristiques du promoteur




    import streamlit as st
    import pandas as pd
    import plotly.express as px

    # Exemple : ta base 'base' avec les colonnes suivantes (à adapter) :
    # 'Part Fonds propres', 'part Prêt bancaire/Prêt EMF', 'part Subvention/Don/Autre', 'Etat_entreprise'

    # Définition des couleurs Institut National de la Statistique Cameroun
    color_map = {'En activité': '#003366', 'Cessation activités': '#D62728'}

    # Fonction corrigée pour calculer les pourcentages en fonction du seuil
    def calcul_pourcentage_seuil(data, var, seuil):
        if seuil == 0 or seuil == 100:
            return None, None  # Pas de découpage possible

        cat_var = f'Cat_{var}'
        data[cat_var] = pd.cut(
            data[var],
            bins=[0, seuil, 100],
            labels=[f'0-{seuil} %', f'{seuil}-100 %'],
            include_lowest=True
        )
        df_counts = data.groupby([cat_var, 'Etat_entreprise']).size().reset_index(name='count')
        total_par_cat = df_counts.groupby(cat_var)['count'].transform('sum')
        df_counts['percentage'] = round((df_counts['count'] / total_par_cat) * 100, 2)
        return df_counts, cat_var

    # Titre
    st.title("Taux de mortalité selon les sources de financement")

    # Slider unique pour le seuil
    seuil = st.slider(
        "Choisissez le seuil (%) pour catégoriser les parts de financement :",
        min_value=0,
        max_value=100,
        value=50,
        step=5,key="Financ:ent_region"
    )

    # Message d'alerte si seuil = 0 ou 100
    if seuil == 0 or seuil == 100:
        st.warning("⚠️ Veuillez choisir un seuil strictement compris entre 0 et 100 pour afficher les graphiques.")
    else:
        col1, col2, col3 = st.columns(3)

        # Fonds propres
        with col1:
            df_fp, var_fp = calcul_pourcentage_seuil(base, 'Part Fonds propres', seuil)
            fig_fp = px.bar(
                df_fp,
                x=var_fp,
                y='percentage',
                color='Etat_entreprise',
                barmode='group',
                text='percentage',
                color_discrete_map=color_map,
                title="Fonds propres"
            )
            fig_fp.update_traces(texttemplate='%{text:.1f}%', textposition='inside')
            fig_fp.update_layout(
                yaxis_title="Pourcentage (%)",
                xaxis_title="",
                margin=dict(t=40, b=30),
                legend_title_text=""
            )
            st.plotly_chart(fig_fp, use_container_width=True,key='région5')

        # Prêt bancaire / EMF
        with col2:
            df_pb, var_pb = calcul_pourcentage_seuil(base, 'part Prêt bancaire/Prêt EMF', seuil)
            fig_pb = px.bar(
                df_pb,
                x=var_pb,
                y='percentage',
                color='Etat_entreprise',
                barmode='group',
                text='percentage',
                color_discrete_map=color_map,
                title="Prêt bancaire / EMF"
            )
            fig_pb.update_traces(texttemplate='%{text:.1f}%', textposition='inside')
            fig_pb.update_layout(
                yaxis_title="Pourcentage (%)",
                xaxis_title="",
                margin=dict(t=40, b=30),
                legend_title_text=""
            )
            st.plotly_chart(fig_pb, use_container_width=True,key="region6")

        # Subvention / Don
        with col3:
            df_sd, var_sd = calcul_pourcentage_seuil(base, 'part Subvention/Don/Autre', seuil)
            fig_sd = px.bar(
                df_sd,
                x=var_sd,
                y='percentage',
                color='Etat_entreprise',
                barmode='group',
                text='percentage',
                color_discrete_map=color_map,
                title="Subvention / Don"
            )
            fig_sd.update_traces(texttemplate='%{text:.1f}%', textposition='inside')
            fig_sd.update_layout(
                yaxis_title="Pourcentage (%)",
                xaxis_title="",
                margin=dict(t=40, b=30),
                legend_title_text=""
            )
            st.plotly_chart(fig_sd, use_container_width=True,key='region7')





    # 📌 Slider pour Age de l'entreprise
    min_age = base['Age_entreprise_reel'].min()
    max_age = base['Age_entreprise_reel'].max()

    seuil_age = st.slider(
        "👉 Seuil (années) pour catégoriser l'âge de l'entreprise :",
        min_value=int(min_age),
        max_value=int(max_age),
        value=int(max_age / 2),
        step=1,key="rgion_age"
    )

    # 📌 Message d'alerte si seuil aux bornes
    if seuil_age == min_age or seuil_age == max_age:
        st.warning("⚠️ Veuillez choisir un seuil strictement compris entre le minimum et maximum de l'âge pour voir le graphique.")
    else:
        # 📌 Calcul des pourcentages avec seuil pour Age de l'entreprise
        def calcul_pourcentage_age(data, var_quant, seuil, max_val=None):
            if max_val is None:
                max_val = data[var_quant].max()
            
            cat_var = f"{var_quant}_cat"
            data = data.copy()
            data[cat_var] = pd.cut(
                data[var_quant],
                bins=[0, seuil, max_val],
                labels=[f"0-{seuil}", f"{seuil}-{int(max_val)}"],
                include_lowest=True
            )

            df_counts = data.groupby([cat_var, 'Etat_entreprise']).size().reset_index(name='count')
            total_par_cat = df_counts.groupby(cat_var)['count'].transform('sum')
            df_counts['percentage'] = round((df_counts['count'] / total_par_cat) * 100, 2)

            return df_counts, cat_var

        # 📌 Application et graphique
        df_age, var_age = calcul_pourcentage_age(base, 'Age_entreprise_reel', seuil_age, max_val=max_age)

        fig_age = px.bar(
            df_age,
            x=var_age,
            y='percentage',
            color='Etat_entreprise',
            barmode='group',
            text='percentage',
            color_discrete_map=color_map,
            title="Âge de l'entreprise"
        )
        fig_age.update_traces(texttemplate='%{text:.1f}%', textposition='inside')
        fig_age.update_layout(
            yaxis_title="Pourcentage (%)",
            margin=dict(t=40, b=30),
            legend_title_text=""
        )
        st.plotly_chart(fig_age, use_container_width=True, key='region8')



    # 📌 Variables qualitatives à afficher
    variables_qualitatives = [
        'Diplome le plus élevé du promoteur',
        'Sexe du promoteur',
        'Nationalité du promoteur',
        'Etat matrimonial du promoteur',
        'Age du promoteur'
    ]

    # 📌 Fonction pour calculer les pourcentages par modalité et état
    def calcul_pourcentage(data, var):
        df_counts = data.groupby([var, 'Etat_entreprise']).size().reset_index(name='count')
        total_par_cat = df_counts.groupby(var)['count'].transform('sum')
        df_counts['percentage'] = round((df_counts['count'] / total_par_cat) * 100, 2)
        return df_counts

    # 📌 Filtres côte à côte
    col1, col2 = st.columns(2)

    with col1:
        types = ['Tous'] + sorted(base["Type d'entreprise"].dropna().unique().tolist())
        selected_types = st.multiselect("Sélectionnez le(s) type(s) d'entreprise :", types, default=['Tous'],key="Region_entreprise")

    with col2:
        secteurs = ['Tous'] + sorted(base["Secteur d'activités"].dropna().unique().tolist())
        selected_secteurs = st.multiselect("Sélectionnez le(s) secteur(s) d'activités :", secteurs, default=['Tous'],key="region_secteur")

    # 📌 Vérification si aucune sélection dans les deux filtres
    if len(selected_types) == 0 or len(selected_secteurs) == 0:
        st.error("⚠️ Veuillez sélectionner au moins un Type d’entreprise et un Secteur d’activités.")
    else:
        # 📌 Application des filtres
        df_filtre = base.copy()

        if 'Tous' not in selected_types:
            df_filtre = df_filtre[df_filtre["Type d'entreprise"].isin(selected_types)]

        if 'Tous' not in selected_secteurs:
            df_filtre = df_filtre[df_filtre["Secteur d'activités"].isin(selected_secteurs)]

        # 📌 Vérification si les filtres donnent un jeu de données vide
        if df_filtre.empty:
            st.warning("Aucune donnée disponible pour cette sélection. Veuillez ajuster vos filtres.")
        else:
            # 📊 Affichage des graphiques (2 par ligne)
            for i in range(0, len(variables_qualitatives), 2):
                cols = st.columns(2)
                for j in range(2):
                    if i + j < len(variables_qualitatives):
                        var = variables_qualitatives[i + j]
                        with cols[j]:
                            df_pct = calcul_pourcentage(df_filtre, var)

                            color_map = {
                                'En activité': '#003366',  # Bleu INS
                                'Cessation activités': '#D62728'  # Rouge
                            }

                            fig = px.bar(
                                df_pct,
                                x=var,
                                y='percentage',
                                color='Etat_entreprise',
                                text='percentage',
                                barmode='group',
                                title=var,
                                color_discrete_map=color_map
                            )
                            fig.update_traces(texttemplate='%{text:.1f}%', textposition='inside')
                            fig.update_layout(
                                yaxis_title='Pourcentage (%)',
                                xaxis_title='',
                                uniformtext_minsize=8,
                                uniformtext_mode='hide',
                                legend_title_text="État de l'entreprise",
                                margin=dict(t=30, b=30),
                                width=350,
                                height=350
                            )
                            st.plotly_chart(fig, use_container_width=True,key=var)


### Origine de dinancement :


