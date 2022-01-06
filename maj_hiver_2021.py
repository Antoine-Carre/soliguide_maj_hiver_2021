import streamlit as st 
from streamlit_folium import folium_static
import pandas as pd
import numpy as np
from numpy import nan
import re
import numpy as np
from datetime import timedelta
import datetime
import time
import plotly.express as px
from bson import ObjectId
import folium
from folium.plugins import MarkerCluster
from folium.plugins import FloatImage
import streamlit.components.v1 as components


@st.cache
def load_df(url):
    df = pd.read_csv(url)
    return df

# option
st.set_page_config(page_title="Soliguide 2021 - Mise à jour hiver",
                   page_icon="https://pbs.twimg.com/profile_images/1321098074765361153/F4UFTeix.png",
                   initial_sidebar_state="expanded",
                   layout="wide",)

#############
## sidebar ##
############# 
st.sidebar.image("https://soliguide.fr/assets/images/logo.png", use_column_width=True)
st.sidebar.title('Soliguide 2021')
st.sidebar.subheader('Mise à jour hiver')

categorie = st.sidebar.selectbox("Choisissez votre territoire :", ("France",  "Ile-De-France", "Alpes-Maritimes (06)", 
                                            "Bouches-du-Rhône (13)", "Cantal (15)", "Gironde (33)", "Hérault (34)", "Indre (36)",
                                            "Loire-Atlantique (44)", "Nord (59)", "Puy-de-Dôme (63)", "Bas-Rhin (67)", 
                                            "Paris (75)", "Seine-Maritime (76)", "Seine-et-Marne (77)","Yvelines (78)",
                                            "Essonne (91)", "Hauts-de-Seine (92)",
                                            "Seine-Saint-Denis (93)","Val-de-Marne (94)",
                                            "Val-d'Oise (95)"))

cat_dict = {"Alpes-Maritimes (06)" :"Alpes-Maritimes", "Ardèche (07)":"Ardèche",
            "Bouches-du-Rhône (13)": "Bouches-du-Rhône","Cantal (15)":"Cantal","Gironde (33)":"Gironde","Hérault (34)":"Hérault","Indre (36)":"Indre",
            "Loire-Atlantique (44)" : "Loire-Atlantique","- Nord (59)":"Nord" , "Puy-de-Dôme (63)":"Puy-de-Dôme",
            "Bas-Rhin (67)":"Bas-Rhin", "Paris (75)" : "Paris", "Seine-Maritime (76)":"Seine-Maritime",
            "Seine-et-Marne (77)":'Seine-et-Marne', "Yvelines (78)":"Yvelines", "Essonne (91)" :"Essonne", 
            "Hauts-de-Seine (92)":"Hauts-de-Seine","Seine-Saint-Denis (93)": "Seine-Saint-Denis","Val-de-Marne (94)": "Val-de-Marne", 
            "Val-d'Oise (95)":"Val-d'Oise"}


##########
## DATA ##
##########

# modifier selon la localisation de la BD
# Importation des fichier .csv en pandas

# Chiffres de la barre du haut
df_fiches_online_all = pd.read_csv('/home/antoine/Bureau/Streamlit/màj hiver 2021/df_fiches_online_all.csv')

# Données pour cartes :
HtmlFile = open("/home/antoine/Bureau/Streamlit/màj hiver 2021/France.html", 'r', encoding='utf-8')
HtmlFile_IDF = open("/home/antoine/Bureau/Streamlit/màj hiver 2021/IDF.html", 'r', encoding='utf-8')
HtmlFile_06 = open("/home/antoine/Bureau/Streamlit/màj hiver 2021/AM06.html", 'r', encoding='utf-8')
HtmlFile_13 = open("/home/antoine/Bureau/Streamlit/màj hiver 2021/BR13.html", 'r', encoding='utf-8')
HtmlFile_15 = open("/home/antoine/Bureau/Streamlit/màj hiver 2021/C15.html", 'r', encoding='utf-8')
HtmlFile_33= open("/home/antoine/Bureau/Streamlit/màj hiver 2021/G33.html", 'r', encoding='utf-8')
HtmlFile_34 = open("/home/antoine/Bureau/Streamlit/màj hiver 2021/H34.html", 'r', encoding='utf-8')
HtmlFile_36 = open("/home/antoine/Bureau/Streamlit/màj hiver 2021/I36.html", 'r', encoding='utf-8')
HtmlFile_44 = open("/home/antoine/Bureau/Streamlit/màj hiver 2021/LA44.html", 'r', encoding='utf-8')
HtmlFile_59 = open("/home/antoine/Bureau/Streamlit/màj hiver 2021/N59.html", 'r', encoding='utf-8')
HtmlFile_63 = open("/home/antoine/Bureau/Streamlit/màj hiver 2021/PdD63.html", 'r', encoding='utf-8')
HtmlFile_67 = open("/home/antoine/Bureau/Streamlit/màj hiver 2021/BR67.html", 'r', encoding='utf-8')
HtmlFile_75 = open("/home/antoine/Bureau/Streamlit/màj hiver 2021/P75.html", 'r', encoding='utf-8')
HtmlFile_76 = open("/home/antoine/Bureau/Streamlit/màj hiver 2021/SM76.html", 'r', encoding='utf-8')
HtmlFile_77 = open("/home/antoine/Bureau/Streamlit/màj hiver 2021/SM77.html", 'r', encoding='utf-8')
HtmlFile_78 = open("/home/antoine/Bureau/Streamlit/màj hiver 2021/Y78.html", 'r', encoding='utf-8')
HtmlFile_91 = open("/home/antoine/Bureau/Streamlit/màj hiver 2021/E91.html", 'r', encoding='utf-8')
HtmlFile_92 = open("/home/antoine/Bureau/Streamlit/màj hiver 2021/HS92.html", 'r', encoding='utf-8')
HtmlFile_93 = open("/home/antoine/Bureau/Streamlit/màj hiver 2021/SSD93.html", 'r', encoding='utf-8')
HtmlFile_94 = open("/home/antoine/Bureau/Streamlit/màj hiver 2021/VDM94.html", 'r', encoding='utf-8')
HtmlFile_95 = open("/home/antoine/Bureau/Streamlit/màj hiver 2021/VDO95.html", 'r', encoding='utf-8')



# Données pour le barchart horizontal:
#df_comparaison_France = pd.read_csv('ressources/Fig2.csv')
#df_comparaison_IDF = pd.read_csv('ressources/Fig2_IDF.csv')
#df_comparaison_06 = pd.read_csv('ressources/Fig2_06.csv')
#df_comparaison_33 = pd.read_csv('ressources/Fig2_33.csv')
#df_comparaison_44 = pd.read_csv('ressources/Fig2_44.csv')
#df_comparaison_67 = pd.read_csv('ressources/Fig2_67.csv')
#df_comparaison_75 = pd.read_csv('ressources/Fig2_75.csv')
#df_comparaison_77 = pd.read_csv('ressources/Fig2_77.csv')
#df_comparaison_78 = pd.read_csv('ressources/Fig2_78.csv')
#df_comparaison_91 = pd.read_csv('ressources/Fig2_91.csv')
#df_comparaison_92 = pd.read_csv('ressources/Fig2_92.csv')
#df_comparaison_93 = pd.read_csv('ressources/Fig2_93.csv')
#df_comparaison_94 = pd.read_csv('ressources/Fig2_94.csv')
#df_comparaison_95 = pd.read_csv('ressources/Fig2_95.csv')

# Données pour le stacked chart:
#df_stacked_per_france = pd.read_csv('ressources/Fig3.csv')
#df_stacked_per_IDF = pd.read_csv('ressources/Fig3_IDF.csv')
#df_stacked_per_06 = pd.read_csv('ressources/Fig3_06.csv')
#df_stacked_per_33 = pd.read_csv('ressources/Fig3_33.csv')
#df_stacked_per_44 = pd.read_csv('ressources/Fig3_44.csv')
#df_stacked_per_67 = pd.read_csv('ressources/Fig3_67.csv')
#df_stacked_per_75 = pd.read_csv('ressources/Fig3_75.csv')
#df_stacked_per_77 = pd.read_csv('ressources/Fig3_77.csv')
#df_stacked_per_78 = pd.read_csv('ressources/Fig3_78.csv')
#df_stacked_per_91 = pd.read_csv('ressources/Fig3_91.csv')
#df_stacked_per_92 = pd.read_csv('ressources/Fig3_92.csv')
#df_stacked_per_93 = pd.read_csv('ressources/Fig3_93.csv')
#df_stacked_per_94 = pd.read_csv('ressources/Fig3_94.csv')
#df_stacked_per_95 = pd.read_csv('ressources/Fig3_95.csv')

# Données pour le pie chart:
#res_france = pd.read_csv('ressources/Fig4.csv')
#res_IDF = pd.read_csv('ressources/Fig4_IDF.csv')
#res_06 = pd.read_csv('ressources/Fig4_06.csv')
#res_33 = pd.read_csv('ressources/Fig4_33.csv')
#res_44 = pd.read_csv('ressources/Fig4_44.csv')
#res_67 = pd.read_csv('ressources/Fig4_67.csv')
#res_75 = pd.read_csv('ressources/Fig4_75.csv')
#res_77 = pd.read_csv('ressources/Fig4_77.csv')
#res_78 = pd.read_csv('ressources/Fig4_78.csv')
#res_91 = pd.read_csv('ressources/Fig4_91.csv')
#res_92 = pd.read_csv('ressources/Fig4_92.csv')
#res_93 = pd.read_csv('ressources/Fig4_93.csv')
#res_94 = pd.read_csv('ressources/Fig4_94.csv')
#res_95 = pd.read_csv('ressources/Fig4_95.csv')


#####################
##  INTRODUCTION   ##
#####################

st.markdown("<center><h1> Soliguide - Mise à jour hiver 2021</h1></center>", unsafe_allow_html=True)
st.markdown("Chaque été et chaque hiver, l'équipe de Solinum met à jour la totalité de la base de données de Soliguide sur ses territoires d'implantation, afin d'orienter les publics en situation de précarité au mieux dans ces périodes de changement. Retrouvez ici toutes les statistiques de cette mise à jour été !  <br>(réalisée du 1<sup>er</sup> au 31 décembre)", unsafe_allow_html=True)  
    
#st.markdown("**Attention**, sur certains grands territoires le dashboard peut mettre quelques minutes à charger : profitez-en pour prendre un café ☕, ça arrive tout de suite.")
                
html_string = "<br>"

st.markdown(html_string, unsafe_allow_html=True)

if categorie == 'France':

    df_fiches_online_all = df_fiches_online_all

if categorie == 'Ile-De-France':

    df_fiches_online_all = df_fiches_online_all[(df_fiches_online_all.departement == 'Paris') | (df_fiches_online_all.departement == 'Seint-et-Marne') | (df_fiches_online_all.departement == 'Yvelines')
    | (df_fiches_online_all.departement == 'Essonne')| (df_fiches_online_all.departement == 'Hauts-de-Seine') | (df_fiches_online_all.departement == 'Seint-Saint-Denis')| (df_fiches_online_all.departement == "Val-d'Oise")
    | (df_fiches_online_all.departement == 'Val-de-Marne')]

if categorie != 'Ile-De-France' and categorie != 'France':

    df_fiches_online_all = df_fiches_online_all[df_fiches_online_all.departement == (cat_dict[categorie])]

#####################
## PREMIERE PARTIE ##
#####################

col1, col2, col3 = st.columns(3)

html_string = f"<center><font face='Helvetica' size='6'>{df_fiches_online_all.lieu_id.count()}</font><br><font size='2'>structures en ligne sur Soliguide au 31 décembre 2021</font></center>"

col1.markdown(html_string, unsafe_allow_html=True)

html_string = f"<center><font face='Helvetica' size='6'>{df_fiches_online_all[df_fiches_online_all['sections.closed.changes'] == True].lieu_id.count()}</font><br/><font size='2'>structures ont fermé</font></center>"

col2.markdown(html_string, unsafe_allow_html=True)

html_string = f"<center><font face='Helvetica' size='6'>{df_fiches_online_all[(df_fiches_online_all['sections.services.changes']== True)|(df_fiches_online_all['sections.hours.changes']== True)].lieu_id.count()}</font><br/><font size='2'>structures ont effectué des changements</font></center>"

col3.markdown(html_string, unsafe_allow_html=True)

html_string = "<br>"

st.markdown(html_string, unsafe_allow_html=True)

# Création de la carte

if categorie == 'France':

    source_code = HtmlFile.read() 
    components.html(source_code, height = 600)

if categorie == 'Ile-De-France':

    source_code = HtmlFile_IDF.read() 
    components.html(source_code, height = 600)

if categorie == 'Alpes-Maritimes (06)':

    source_code = HtmlFile_06.read() 
    components.html(source_code, height = 600)

if categorie == "Bouches-du-Rhône (13)":

    source_code = HtmlFile_13.read() 
    components.html(source_code, height = 600)

if categorie == "Cantal (15)":

    source_code = HtmlFile_15.read() 
    components.html(source_code, height = 600)

if categorie == "Gironde (33)":

    source_code = HtmlFile_33.read() 
    components.html(source_code, height = 600)

if categorie == "Hérault (34)":

    source_code = HtmlFile_34.read() 
    components.html(source_code, height = 600)

if categorie == "Indre (36)":

    source_code = HtmlFile_36.read() 
    components.html(source_code, height = 600)

if categorie == "Loire-Atlantique (44)":

    source_code = HtmlFile_44.read() 
    components.html(source_code, height = 600)

if categorie == "Nord (59)":

    source_code = HtmlFile_59.read() 
    components.html(source_code, height = 600)

if categorie == "Puy-de-Dôme (63)":

    source_code = HtmlFile_63.read() 
    components.html(source_code, height = 600)

if categorie == "Bas-Rhin (67)":

    source_code = HtmlFile_67.read() 
    components.html(source_code, height = 600)

if categorie == "Paris (75)":

    source_code = HtmlFile_75.read() 
    components.html(source_code, height = 600)

if categorie == "Seine-Maritime (76)":

    source_code = HtmlFile_76.read() 
    components.html(source_code, height = 600)

if categorie == "Seine-et-Marne (77)":

    source_code = HtmlFile_77.read() 
    components.html(source_code, height = 600)

if categorie == "Yvelines (78)":

    source_code = HtmlFile_78.read() 
    components.html(source_code, height = 600)

if categorie == "Essonne (91)":

    source_code = HtmlFile_91.read() 
    components.html(source_code, height = 600)

if categorie == "Hauts-de-Seine (92)":

    source_code = HtmlFile_92.read() 
    components.html(source_code, height = 600)

if categorie == "Seine-Saint-Denis (93)":

    source_code = HtmlFile_93.read() 
    components.html(source_code, height = 600)

if categorie == "Val-de-Marne (94)":

    source_code = HtmlFile_94.read() 
    components.html(source_code, height = 600)

if categorie == "Val-d'Oise (95)":

    source_code = HtmlFile_95.read() 
    components.html(source_code, height = 600)
