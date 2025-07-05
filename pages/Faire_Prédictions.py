import streamlit as st
import pandas as pd
import numpy as np
import joblib
from sksurv.functions import StepFunction
import plotly.express as px
import os
import io
import plotly.express as px
import plotly.graph_objects as go
                
              
                
import pickle
import json

   
import json
import plotly.graph_objects as go

import folium
import plotly.express as px
from streamlit_folium import st_folium

import plotly.express as px
import pandas as pd
import plotly.express as px
    #st.header("Suivi des PME - Carte Plotly avec labels fixes")

if "acces_autorise" not in st.session_state or not st.session_state["acces_autorise"]:
    st.error("🔒 Accès refusé. Veuillez d'abord vous connecter depuis la page d'accueil.")
    st.stop()

st.set_page_config(page_title="résultats Predictions", layout="wide")


# --- Configuration page ---


st.markdown("""
    <style>
    /* Arrière-plan général de la page */
    .stApp {
        background-color: #f4f6f8;
    }

    /* Style des cartes/blocs */
    .card {
        background-color: #ffffff;
        padding: 25px 30px;
        border-radius: 12px;
        border: 1px solid #e0e0e0;
        margin-bottom: 20px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
    }

    /* Inputs, selectbox et textarea */
    input, select, textarea {
        background-color: #eaf4fc;
        border: 2px solid #c2d6e5;
        border-radius: 10px;
        padding: 10px 14px;
        font-size: 15px;
        color: #003366;
        transition: border 0.3s ease, background-color 0.3s ease;
    }

    /* Focus et hover sur input */
    input:focus, select:focus, textarea:focus {
        border: 2px solid #007acc;
        background-color: #ffffff;
        outline: none;
    }

    input:hover, select:hover, textarea:hover {
        border: 2px solid #66b2ff;
    }

    /* Slider personnalisé */
    .stSlider > div {
        background: #ffffff;
        padding: 8px;
        border-radius: 10px;
        border: 1px solid #cccccc;
    }

    /* Bouton stylisé */
    .stButton button {
        background-color: #003366;
        color: #ffffff;
        border-radius: 8px;
        padding: 12px 20px;
        font-size: 16px;
        border: none;
        transition: background-color 0.3s ease;
    }
    .stButton button:hover {
        background-color: #002244;
        color: #f0f0f0;
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
        background: #f4f6f8;
    }
    </style>
""", unsafe_allow_html=True)
# Bloquer l'accès si l'utilisateur n'est pas connecté

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




##Définitions une fonction pour visual

## Fonctionn globale 

st.markdown("""
    <style>
    .stTabs [data-baseweb="tab-list"] {
        justify-content: space-around;
    }
    </style>
    """, unsafe_allow_html=True)


def afficher_tableau_de_bord(base, geo):
            
            # Création des onglets
            tabs = st.tabs(["Répartitions des PME", "Analyse mortalité globale", "Analyse par région"])

            # Onglet Statistiques descriptives
            with tabs[0]:
                

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
                min_age = base['Age_entreprise'].min()
                max_age = base['Age_entreprise'].max()

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
                    df_age, var_age = calcul_pourcentage_age(base, 'Age_entreprise', seuil_age, max_val=max_age)

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









               

                # 📌 Variables qualitatives à afficher
                variables_qualitatives = [
                    'Sexe du promoteur',
                    'Nationalité du promoteur',
                    'Etat matrimonial du promoteur'
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
                min_age = base['Age_entreprise'].min()
                max_age = base['Age_entreprise'].max()

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
                    df_age, var_age = calcul_pourcentage_age(base, 'Age_entreprise', seuil_age, max_val=max_age)

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
                    
                    'Sexe du promoteur',
                    'Nationalité du promoteur',
                    'Etat matrimonial du promoteur'
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




import requests
import joblib
import pickle
import os
import streamlit as st

# --- Fichiers et IDs Drive à charger ---
FILES_INFO = {
    "RSF_MODEL_FILE": {
        "path": "Models/rsf_model.joblib",
        "drive_id": "1_-urCD8kKJk5q2OTXl0pGAlbB5hDeDjJ"  # Ton vrai ID Drive ici
    },
    "SEUILS_FILE": {
        "path": "Models/seuils_region_temps_match_taux.pkl",
        "drive_id": "TON_ID_SEUILS"  # à remplacer
    },
    "MAPPINGS_FILE": {
        "path": "Models/category_mappings.joblib",
        "drive_id": "TON_ID_MAPPINGS"  # à remplacer
    }
}

# --- Fonction de téléchargement depuis Google Drive ---
def download_file_from_drive(file_id, destination_path):
    url = f"https://drive.google.com/uc?export=download&id={file_id}"
    response = requests.get(url)
    if response.status_code == 200:
        os.makedirs(os.path.dirname(destination_path), exist_ok=True)
        with open(destination_path, "wb") as f:
            f.write(response.content)
        print(f"✅ Fichier téléchargé : {destination_path}")
    else:
        st.error(f"❌ Échec téléchargement : {destination_path}")
        st.stop()

# --- Chargement des ressources ---
@st.cache_resource
def load_resources():
    # Vérifie et télécharge si nécessaire
    for file_info in FILES_INFO.values():
        if not os.path.exists(file_info["path"]):
            download_file_from_drive(file_info["drive_id"], file_info["path"])

    # Charge les ressources
    model = joblib.load(FILES_INFO["RSF_MODEL_FILE"]["path"])
    with open(FILES_INFO["SEUILS_FILE"]["path"], "rb") as f:
        seuils = pickle.load(f)
    mappings = joblib.load(FILES_INFO["MAPPINGS_FILE"]["path"])

    return model, seuils, mappings


rsf_model, seuils_dict, category_mappings = load_resources()

# --- Colonnes du modèle ---
CATEGORICAL_COLS = [
    'Région',
    "Régime d'imposition",                        # accent corrigé
    "Tenue d'une comptabilité écrite",
    'Promoteur principal gérant',
    'Sexe du promoteur',
    'Etat matrimonial du promoteur',
    'Nationalité du promoteur',
    "Type d'entreprise",                          # apostrophe normale
    'Forme juridique',
    'Activités principales'
]


MODELE_COLS = [
    'Région',
    "Régime d'imposition",
    "Tenue d'une comptabilité écrite",
    'Promoteur principal gérant',
    'Sexe du promoteur',
    'Etat matrimonial du promoteur',
    'Nationalité du promoteur',
    "Type d'entreprise",
    'Forme juridique',
    'Activités principales',
    "Nombre d'année du promoteur au sein de l'entreprise",
    'Effectifs permanents employé',                     # nom réel dans ta base
    "Chiffre d'affaire de l'exercice",                  # nom réel dans ta base
    'Part Fonds propres',
    'part Prêt bancaire/Prêt EMF',
    'part Subvention/Don/Autre',
    'Ratio_Hommes_Femmes',
    'Age_entreprise',                                   # nom réel dans ta base
    'Productivite_par_employe',
    'Indicateur_CA_Capital_Age',
    'densité_orga_par_hab'
]


# --- Dictionnaire densité organisationnelle par activité ---
densite_orga_dict = {
    ('SUD OUEST', 'Autres'): 3.4202e-05,
    ('SUD OUEST', 'Commerce'): 0.00013799,
    ('SUD OUEST', 'Industrie / Artisanat'): 1.3848e-05,
    ('SUD OUEST', 'Services aux entreprises'): 4.8151e-05,
    ('SUD OUEST', 'Services à la personne'): 0.00014645,
    ('SUD OUEST', 'Transport / HCR'): 5.9872e-05,
    ('NORD OUEST', 'Autres'): 1.2043e-05,
    ('NORD OUEST', 'Commerce'): 6.3486e-05,
    ('NORD OUEST', 'Industrie / Artisanat'): 2.8149e-06,
    ('NORD OUEST', 'Services aux entreprises'): 1.7574e-05,
    ('NORD OUEST', 'Services à la personne'): 8.2096e-05,
    ('NORD OUEST', 'Transport / HCR'): 1.3344e-05,
    ('SUD', 'Autres'): 4.8012e-06,
    ('SUD', 'Commerce'): 3.3232e-05,
    ('SUD', 'Industrie / Artisanat'): 6.1912e-07,
    ('SUD', 'Services aux entreprises'): 1.3252e-05,
    ('SUD', 'Services à la personne'): 4.6014e-05,
    ('SUD', 'Transport / HCR'): 5.3696e-06,
    ('EXTREME NORD', 'Autres'): 4.5935e-06,
    ('EXTREME NORD', 'Commerce'): 2.0393e-05,
    ('EXTREME NORD', 'Industrie / Artisanat'): 3.3173e-07,
    ('EXTREME NORD', 'Services aux entreprises'): 2.0185e-06,
    ('EXTREME NORD', 'Services à la personne'): 2.9305e-05,
    ('EXTREME NORD', 'Transport / HCR'): 3.3604e-06,
    ('ADAMAOUA', 'Autres'): 3.2474e-05,
    ('ADAMAOUA', 'Commerce'): 4.7045e-04,
    ('ADAMAOUA', 'Industrie / Artisanat'): 1.5821e-05,
    ('ADAMAOUA', 'Services aux entreprises'): 1.3323e-05,
    ('ADAMAOUA', 'Services à la personne'): 1.0575e-04,
    ('ADAMAOUA', 'Transport / HCR'): 1.8319e-05,
    ('LITTORAL', 'Autres'): 7.4555e-05,
    ('LITTORAL', 'Commerce'): 0.00039745,
    ('LITTORAL', 'Industrie / Artisanat'): 4.5919e-05,
    ('LITTORAL', 'Services aux entreprises'): 1.4016e-05,
    ('LITTORAL', 'Services à la personne'): 0.00021234,
    ('LITTORAL', 'Transport / HCR'): 2.9144e-05,
    ('EST', 'Autres'): 3.3289e-05,
    ('EST', 'Commerce'): 7.2641e-05,
    ('EST', 'Industrie / Artisanat'): 5.2962e-06,
    ('EST', 'Services aux entreprises'): 6.0714e-06,
    ('EST', 'Services à la personne'): 2.4896e-05,
    ('EST', 'Transport / HCR'): 2.0347e-05,
    ('CENTRE', 'Agri / Mines / Énergie'): 7.2124e-07,
    ('CENTRE', 'Autres'): 8.6068e-05,
    ('CENTRE', 'Commerce'): 0.00023561,
    ('CENTRE', 'Industrie / Artisanat'): 2.2839e-05,
    ('CENTRE', 'Services aux entreprises'): 1.8993e-05,
    ('CENTRE', 'Services à la personne'): 0.00011900,
    ('CENTRE', 'Transport / HCR'): 5.5776e-05,
    ('NORD', 'Autres'): 3.9735e-06,
    ('NORD', 'Commerce'): 3.2372e-05,
    ('NORD', 'Industrie / Artisanat'): 1.1969e-06,
    ('NORD', 'Services aux entreprises'): 2.0655e-06,
    ('NORD', 'Services à la personne'): 8.0216e-06,
    ('NORD', 'Transport / HCR'): 1.3765e-05,
    ('OUEST', 'Autres'): 2.3996e-05,
    ('OUEST', 'Commerce'): 0.00013494,
    ('OUEST', 'Industrie / Artisanat'): 7.0716e-06,
    ('OUEST', 'Services aux entreprises'): 1.0121e-05,
    ('OUEST', 'Services à la personne'): 4.7207e-05,
    ('OUEST', 'Transport / HCR'): 5.1995e-05
}

# --- Fonction ajustement de seuil ---
def ajuster_seuil(row, t):
    region = str(row['Région']).strip().upper()
    cle = f"Région_{region}"
    seuil = seuils_dict.get(cle, {}).get(t, {}).get('seuil', 0.5)

    if t < 5:
        seuil += 0.13
    else :
        seuil += 0.13

    return seuil

# --- Choix du mode ---
mode = st.radio("📝 Voulez-vous prédire pour :", ["Plusieurs entreprises (via fichier)", "Une entreprise (via formulaire)"])

# --- Sélection de l'horizon de prédiction ---
t = st.slider("⏳ Horizon de prédiction (années)", min_value=1, max_value=7, value=5)

# --- Mode fichier ---
if mode == "Plusieurs entreprises (via fichier)":
    uploaded_file = st.file_uploader("📤 Importez votre fichier Excel", type=["xlsx"])
    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        missing_cols = [col for col in MODELE_COLS if col not in df.columns]
        if missing_cols:
            st.error(f"Colonnes manquantes : {', '.join(missing_cols)}")
            st.stop()

        df_model = df[MODELE_COLS].copy()

        for col in CATEGORICAL_COLS:
            mapping = category_mappings[col]
            df_model[col] = df_model[col].astype(str).map(mapping).fillna(-1).astype(int)

        X_pred = df_model.copy()
        X_pred = X_pred.astype(np.float64)

        surv_funcs = rsf_model.predict_survival_function(X_pred)
        probas = np.array([fn(t) for fn in surv_funcs])
        df[f"Proba_survie_J+{t}_ans"] = probas

        df["Etat_entreprise"] = df.apply(
            lambda row: "En activités" if row[f"Proba_survie_J+{t}_ans"] >= ajuster_seuil(row, t)
            else "Cessation activités",
            axis=1
        )

        st.success(f"✅ Prédictions réalisées pour {len(df)} entreprises")
      


        # Supposons que df est ton DataFrame
        # df = ...
        col=st.columns(2)
        # Préparer le fichier CSV
        with col[0]:
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Télécharger le CSV",
                data=csv,
                file_name=f"resultats_J+{t}_ans.csv",
                mime="text/csv"
            )

        # Préparer le fichier Excel en mémoire
        with col[1]:
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='Résultats')

            # Récupérer les données Excel depuis le buffer
            processed_data = output.getvalue()

            st.download_button(
                label="📥 Télécharger le Excel",
                data=processed_data,
                file_name=f"resultats_J+{t}_ans.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

                # 📊 Calcul des stats par région
        st.subheader(f"📈 Visualisation des résultats de prédiction à {t} ans")


        # Harmoniser les noms de région pour éviter les incohérences
        df['Région'] = df['Région'].astype(str).str.strip().str.upper()

        

        # 📦 Fonction de chargement et préparation de la base
        @st.cache_data
        def charger_base(path):
            base = pd.read_excel(path)
            base['Age_entreprise'] = base.groupby('Type d\'entreprise')['Age_entreprise'].transform(
                lambda x: x.fillna(x.median())
            )
            return base

        # 📂 Chargement une seule fois via le cache
        #base_path = "C://Users//TIAO ELIASSE//Desktop//Mémoire//TIAO_mémoire//code_mémoire//base_finalPME_Annee_demaragetraité_en_attentant_confirmation13_modelisation.xlsx"
        #base = charger_base(base_path)
        base=df.copy()

        base['Région'] = base['Région'].str.upper().replace('SUD OUEST', 'SUD-OUEST')

            # Renommer 'AUTRES FORMES JURIDIQUE' en 'AUTRES'
        base["Forme juridique"] = base["Forme juridique"].replace("Autres formes juridiques", "AUTRES")

        # Configuration
        #

        # Titre général
        #st.title("📊 Tableau de bord PME Cameroun")
       

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

        
        ### Origine de dinancement :
        afficher_tableau_de_bord(base, geo)
# --- Mode individuel ---
else:
    
    st.subheader("📝 Informations sur l'entreprise")

    # Variables qualitatives
    qual_cols = st.columns(3)
    inputs = {}
    for idx, col in enumerate(CATEGORICAL_COLS):
        options = list(category_mappings[col].keys())
        with qual_cols[idx % 3]:
            inputs[col] = st.selectbox(col, options)
    quant_cols = st.columns(3)

    quant_vars = [
    "Nombre d'année du promoteur au sein de l'entreprise",
    'Effectifs permanents employé',               # fusion hommes/femmes → variable disponible
    "Chiffre d'affaire de l'exercice",            # nom réel dans ta base
    'Capital social au 31/12/2022 (en FCFA)',     # nom réel dans ta base
    'Age_entreprise'                              # nom réel dans ta base
]


    labels_personnalises = {
    "Nombre d'année du promoteur au sein de l'entreprise": "Années du promoteur dans l'entreprise",
    "Effectifs permanents employé": "Effectif permanent total",
    "Chiffre d'affaire de l'exercice": "Chiffre d'affaire de l'année passée",
    "Capital social au 31/12/2022 (en FCFA)": "Capital social de l'entreprise",
    "Age_entreprise": "Âge de l'entreprise depuis démarrage des activités"
}


    quant_inputs = {}

    # Supposons que quant_cols est défini ainsi (exemple 3 colonnes)
    quant_cols = st.columns(3)

    for idx, var in enumerate(quant_vars):
        with quant_cols[idx % 3]:
            label = labels_personnalises.get(var, var)
            quant_inputs[var] = st.number_input(label, min_value=0.0, value=0.0)


    st.markdown("###  Répartition du financement (%) origine de la création de l'entreprise")
    part_cols = st.columns(3)
    parts = ['Part Fonds propres', 'part Prêt bancaire/Prêt EMF', 'part Subvention/Don/Autre']
    for idx, col in enumerate(parts):
        with part_cols[idx]:
            quant_inputs[col] = st.number_input(col, min_value=0.0, value=0.0, step=1.0)

    total_part = sum(quant_inputs[p] for p in parts)
    if total_part > 100:
        st.error(f"🚨 La somme des parts ({total_part:.1f}%) dépasse 100%. Corrigez avant de prédire.")
    else:
        if st.button("🔍 Prédire la survie de l'entreprise"):
            # On suppose que l'utilisateur entre directement le total
            effectifs_total = quant_inputs['Effectifs permanents employé']
            ratio_hf = effectifs_total / (quant_inputs['Effectifs permanents employé'] + 1)  # approximatif si pas H/F
            productivite = quant_inputs["Chiffre d'affaire de l'exercice"] / (effectifs_total + 1)
            indicateur_ca_cap_age = quant_inputs["Chiffre d'affaire de l'exercice"] / (
                (quant_inputs["Capital social au 31/12/2022 (en FCFA)"] * quant_inputs["Age_entreprise"]) + 1)

            densite_orga = densite_orga_dict.get(
                (inputs['Région'].strip().upper(), inputs['Activités principales'].strip()),
                10.0
            )

            data = {
                **{col: category_mappings[col].get(inputs[col], -1) for col in CATEGORICAL_COLS},
                "Nombre d'année du promoteur au sein de l'entreprise": quant_inputs["Nombre d'année du promoteur au sein de l'entreprise"],
                'Effectifs permanents employé': effectifs_total,
                "Chiffre d'affaire de l'exercice": quant_inputs["Chiffre d'affaire de l'exercice"],
                'Part Fonds propres': quant_inputs['Part Fonds propres'],
                'part Prêt bancaire/Prêt EMF': quant_inputs['part Prêt bancaire/Prêt EMF'],
                'part Subvention/Don/Autre': quant_inputs['part Subvention/Don/Autre'],
                'Ratio_Hommes_Femmes': ratio_hf,
                'Age_entreprise': quant_inputs['Age_entreprise'],
                'Productivite_par_employe': productivite,
                'Indicateur_CA_Capital_Age': indicateur_ca_cap_age,
                'densité_orga_par_hab': densite_orga
            }

            X_pred = pd.DataFrame([data])
            surv_func = rsf_model.predict_survival_function(X_pred)[0]
            proba = surv_func(t)
            seuil = ajuster_seuil({'Région': inputs['Région']}, t)
            etat = "En activités" if proba >= seuil else "Cessation activités"

            st.success(f"📊 Probabilité de survie à {t} ans : {proba:.2%}")
            st.info(f"📌 État prédit dans {t} ans : **{etat}**")


