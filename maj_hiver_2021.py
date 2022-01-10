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
import plotly.graph_objects as go
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
            "Loire-Atlantique (44)" : "Loire-Atlantique","Nord (59)":"Nord" , "Puy-de-Dôme (63)":"Puy-de-Dôme",
            "Bas-Rhin (67)":"Bas-Rhin", "Paris (75)" : "Paris", "Seine-Maritime (76)":"Seine-Maritime",
            "Seine-et-Marne (77)":'Seine-et-Marne', "Yvelines (78)":"Yvelines", "Essonne (91)" :"Essonne", 
            "Hauts-de-Seine (92)":"Hauts-de-Seine","Seine-Saint-Denis (93)": "Seine-Saint-Denis","Val-de-Marne (94)": "Val-de-Marne", 
            "Val-d'Oise (95)":"Val-d'Oise"}

cat_dict_2 = {"Alpes-Maritimes (06)" :"06", "Ardèche (07)":"07",
            "Bouches-du-Rhône (13)": "13","Cantal (15)":"15","Gironde (33)":"33","Hérault (34)":"34","Indre (36)":"36",
            "Loire-Atlantique (44)" : "44","Nord (59)":"59" , "Puy-de-Dôme (63)":"63",
            "Bas-Rhin (67)":"67", "Paris (75)" : "75", "Seine-Maritime (76)":"76",
            "Seine-et-Marne (77)":'77', "Yvelines (78)":"78", "Essonne (91)" :"91", 
            "Hauts-de-Seine (92)":"92","Seine-Saint-Denis (93)": "93","Val-de-Marne (94)": "94", 
            "Val-d'Oise (95)":"95"}


##########
## DATA ##
##########

# modifier selon la localisation de la BD
# Importation des fichier .csv en pandas

# Chiffres de la barre du haut
df_fiches_online_all = pd.read_csv('./ressource/df_fiches_online_all.csv')

# Données pour cartes :
HtmlFile = open("./ressource/France.html", 'r', encoding='utf-8')
HtmlFile_IDF = open("./ressource/IDF.html", 'r', encoding='utf-8')
HtmlFile_06 = open("./ressource/AM06.html", 'r', encoding='utf-8')
HtmlFile_13 = open("./ressource/BR13.html", 'r', encoding='utf-8')
HtmlFile_15 = open("./ressource/C15.html", 'r', encoding='utf-8')
HtmlFile_33= open("./ressource/G33.html", 'r', encoding='utf-8')
HtmlFile_34 = open("./ressource/H34.html", 'r', encoding='utf-8')
HtmlFile_36 = open("./ressource/I36.html", 'r', encoding='utf-8')
HtmlFile_44 = open("./ressource/LA44.html", 'r', encoding='utf-8')
HtmlFile_59 = open("./ressource/N59.html", 'r', encoding='utf-8')
HtmlFile_63 = open("./ressource/PdD63.html", 'r', encoding='utf-8')
HtmlFile_67 = open("./ressource/BR67.html", 'r', encoding='utf-8')
HtmlFile_75 = open("./ressource/P75.html", 'r', encoding='utf-8')
HtmlFile_76 = open("./ressource/SM76.html", 'r', encoding='utf-8')
HtmlFile_77 = open("./ressource/SM77.html", 'r', encoding='utf-8')
HtmlFile_78 = open("./ressource/Y78.html", 'r', encoding='utf-8')
HtmlFile_91 = open("./ressource/E91.html", 'r', encoding='utf-8')
HtmlFile_92 = open("./ressource/HS92.html", 'r', encoding='utf-8')
HtmlFile_93 = open("./ressource/SSD93.html", 'r', encoding='utf-8')
HtmlFile_94 = open("./ressource/VDM94.html", 'r', encoding='utf-8')
HtmlFile_95 = open("./ressource/VDO95.html", 'r', encoding='utf-8')

# Données pour le barchart horizontal:
df_categories_closed = pd.read_csv('./ressource/df_categories_closed.csv')

# Changement par catégorie de services
df_changes_vf = pd.read_csv('./ressource/df_changes_vf.csv')

# Données qui fait la màj
df_fiches_màj = pd.read_csv('https://raw.githubusercontent.com/Antoine-Carre/maj_hiver_soliguide/main/pilotage%20m%C3%A0j%20hiver%202021/df_fiches_data.csv')
df_history_campaign_users_final = df_fiches_màj[['status','created_at','territory']]

df_fiches_màj2 = pd.read_csv('./ressource/df_fiches_data2.csv')


# Mails.csv
df_mails = pd.read_csv('https://raw.githubusercontent.com/Antoine-Carre/maj_hiver_soliguide/main/pilotage%20m%C3%A0j%20hiver%202021/df_mails_data.csv')

# Appels
df_source_màj = pd.read_csv('https://raw.githubusercontent.com/Antoine-Carre/maj_hiver_soliguide/main/pilotage%20m%C3%A0j%20hiver%202021/df_source_m%C3%A0j.csv')

# Recherches en décembre
df_search = pd.read_csv('https://raw.githubusercontent.com/Antoine-Carre/bdd_python/main/data_csv/searchWithDatePresentation3.csv')
df_search_vf = df_search[df_search.datePresentation == "2021-12-01"]

#  pourcentage màj
df_fiches_màj_vf = df_fiches_màj2[['territory','sections.closed.updated','sections.hours.updated','sections.services.updated','sections.tempMessage.updated']]

# màj 6 mois
maj_6_tab = pd.read_csv('./ressource/maj_6_tab.csv')



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
    df_categories_closed = df_categories_closed
    df_changes_vf = df_changes_vf
    df_history_campaign_users_final = df_history_campaign_users_final
    df_source_màj_2 = pd.DataFrame(df_source_màj['❄️ Source de la mise à jour'].value_counts())
    df_search_vf = df_search_vf[['Recherches général']]
    df_fiches_màj_vf = df_fiches_màj_vf
    maj_6_tab = maj_6_tab[maj_6_tab.territoire == "Total"]


if categorie == 'Ile-De-France':

    df_fiches_online_all = df_fiches_online_all[(df_fiches_online_all.departement == 'Paris') | (df_fiches_online_all.departement == 'Seint-et-Marne') | (df_fiches_online_all.departement == 'Yvelines')
    | (df_fiches_online_all.departement == 'Essonne')| (df_fiches_online_all.departement == 'Hauts-de-Seine') | (df_fiches_online_all.departement == 'Seint-Saint-Denis')| (df_fiches_online_all.departement == "Val-d'Oise")
    | (df_fiches_online_all.departement == 'Val-de-Marne')]

    df_categories_closed = df_categories_closed[(df_categories_closed.departement == 'Paris') | (df_categories_closed.departement == 'Seint-et-Marne') | (df_categories_closed.departement == 'Yvelines')
    | (df_categories_closed.departement == 'Essonne')| (df_categories_closed.departement == 'Hauts-de-Seine') | (df_categories_closed.departement == 'Seint-Saint-Denis')| (df_categories_closed.departement == "Val-d'Oise")
    | (df_categories_closed.departement == 'Val-de-Marne')]

    df_changes_vf = df_changes_vf[(df_changes_vf.departement == 'Paris') | (df_changes_vf.departement == 'Seint-et-Marne') | (df_changes_vf.departement == 'Yvelines')
    | (df_changes_vf.departement == 'Essonne')| (df_changes_vf.departement == 'Hauts-de-Seine') | (df_changes_vf.departement == 'Seint-Saint-Denis')| (df_changes_vf.departement == "Val-d'Oise")
    | (df_changes_vf.departement == 'Val-de-Marne')]

    df_history_campaign_users_final = df_history_campaign_users_final[(df_history_campaign_users_final.territory == 75) | (df_history_campaign_users_final.territory == 77) | (df_history_campaign_users_final.territory == 78)
    | (df_history_campaign_users_final.territory == 91)| (df_history_campaign_users_final.territory == 92) | (df_history_campaign_users_final.territory == 93)| (df_history_campaign_users_final.territory == 94)
    | (df_history_campaign_users_final.territory == 95)]

    df_source_màj = df_source_màj[(df_source_màj.Territoire ==75) | (df_source_màj.Territoire ==77) | (df_source_màj.Territoire ==78) | (df_source_màj.Territoire ==91)
    | (df_source_màj.Territoire ==92) | (df_source_màj.Territoire ==93) | (df_source_màj.Territoire ==93) | (df_source_màj.Territoire ==94) | (df_source_màj.Territoire ==95)]

    df_source_màj_2 = pd.DataFrame(df_source_màj['❄️ Source de la mise à jour'].value_counts())

    df_search_vf = df_search_vf[['Recherches dep(75)','Recherches dep(77)','Recherches dep(78)','Recherches dep(91)','Recherches dep(92)','Recherches dep(93)',
    'Recherches dep(94)','Recherches dep(95)']].sum(axis=1)

    df_fiches_màj_vf = df_fiches_màj_vf[(df_fiches_màj_vf.territory == 75) | (df_fiches_màj_vf.territory == 77) | (df_fiches_màj_vf.territory == 78) | (df_fiches_màj_vf.territory == 91) 
    | (df_fiches_màj_vf.territory == 92) | (df_fiches_màj_vf.territory == 93) | (df_fiches_màj_vf.territory == 94) | (df_fiches_màj_vf.territory == 95)]

    maj_6_tab = maj_6_tab[(maj_6_tab.territoire == "75") | (maj_6_tab.territoire == "77") | (maj_6_tab.territoire == "78") | (maj_6_tab.territoire == "91") | (maj_6_tab.territoire == "92") |
    (maj_6_tab.territoire == "93") | (maj_6_tab.territoire == "94") | (maj_6_tab.territoire == "95")]

if categorie != 'Ile-De-France' and categorie != 'France':

    df_fiches_online_all = df_fiches_online_all[df_fiches_online_all.departement == (cat_dict[categorie])]
    df_categories_closed = df_categories_closed[df_categories_closed.departement == (cat_dict[categorie])]
    df_changes_vf = df_changes_vf[df_changes_vf.departement == (cat_dict[categorie])]
    df_history_campaign_users_final = df_history_campaign_users_final[df_history_campaign_users_final.territory == int(cat_dict_2[categorie])]
    df_source_màj = df_source_màj[df_source_màj.Territoire == float(cat_dict_2[categorie])]
    df_source_màj_2 = pd.DataFrame(df_source_màj['❄️ Source de la mise à jour'].value_counts())

    df_search_vf = df_search_vf.filter(regex='Recherches dep')
    df_search_vf = df_search_vf.filter(regex=cat_dict_2[categorie])

    df_fiches_màj_vf = df_fiches_màj_vf[df_fiches_màj_vf.territory == int(cat_dict_2[categorie])]

    maj_6_tab = maj_6_tab[maj_6_tab.territoire == cat_dict_2[categorie]]


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

# Horizontal graph

# Création d'une table avec le nombre total de services en ligne
df2 = df_categories_closed.groupby(['name_y'], as_index=False).agg({'categorie':'count'})

# Création d'une table du nombre de services fermés
df2b = df_categories_closed.groupby(['Fermeture_Estivale','close.actif', 'name_y'], as_index=False).agg({'categorie':'count'})
test = df2b[(df2b['close.actif']==True) | (df2b['Fermeture_Estivale']=='Fermé') ]
df3 = test.groupby(['name_y'], as_index=False).agg({'categorie':'sum'})

# Création d'un table de comparaison entre tous les services en ligne et les services fermés
df_comparaison = pd.merge(df2,df3, how='left', left_on='name_y', right_on='name_y')

# Ajout des taux de fermeture pour le graph
df_comparaison['percent'] = (df_comparaison['categorie_y'] / df_comparaison['categorie_x']) * 100
df_comparaison_sorted = df_comparaison.sort_values(by='categorie_x', ascending=False)

# Oter les services de specialiste médicaux de notre table de données
a = ["Spécialistes","Allergologie", "Cardiologie","Dermatologie",
                                    "Echographie","Endocrinologie","Gastro-entérologie", "Gynécologie", 
                                    "Kinésithérapie", "Mammographie", "Ophtalmologie","Oto-rhino-laryngologie",
                                    "Nutrition","Pédicure", "Phlébologie","Pneumologie", "Radiologie",
                                   "Rhumatologie","Urologie", "Orthophonie", "Stomatologie", "Osthéopathie","Accupuncture", "Fontaine", "Toilettes", "Wifi"]

df_comparaison_sorted = df_comparaison_sorted[~df_comparaison_sorted['name_y'].isin(a)]

# Calcul du nombre de services ouvert sans modification et changement des noms des variables
df_comparaison_sorted['ouvert'] = df_comparaison_sorted.categorie_x - df_comparaison_sorted.categorie_y
df_comparaison_sorted.rename(columns={'categorie_y':'Service fermé','name_y':'catégorie','categorie_x':'Nbre_de_services','percent':'Part de service fermé'}, inplace=True)

df_comparaison_sorted['Part de service fermé'] = df_comparaison_sorted['Part de service fermé'].round(1)

if df_fiches_online_all[df_fiches_online_all['sections.closed.changes'] == True].lieu_id.count() > 0:

    df_comparaison_sorted = df_comparaison_sorted[~df_comparaison_sorted['Service fermé'].isna()]

    fig = go.Figure(data=[
        go.Bar(name="Service ouvert", x=df_comparaison_sorted.head(10).sort_values(by='Part de service fermé', ascending=True)['ouvert'], 
            y=df_comparaison_sorted.head(10).sort_values(by='Part de service fermé', ascending=True)["catégorie"], marker_color='#3E3A71', orientation='h',
            hovertemplate='Catégorie de service: %{y}<br> Nbre de service: %{x}'),
        go.Bar(name="Service fermé", x=df_comparaison_sorted.head(10).sort_values(by='Part de service fermé', ascending=True)['Service fermé'], 
            y=df_comparaison_sorted.head(10).sort_values(by='Part de service fermé', ascending=True)["catégorie"], marker_color='#E65A46', orientation='h', customdata=df_comparaison_sorted.head(10).sort_values(by='Part de service fermé', ascending=True)['Part de service fermé'],
            hovertemplate='Catégorie de service: %{y}<br> Nbre de service: %{x}  <br>Taux de fermeture :%{customdata}%',
            text = df_comparaison_sorted.head(10).sort_values(by='Part de service fermé', ascending=True)['Part de service fermé'].astype(str) +"%", textposition = "outside",)
    ])
    # Change the bar mode
    fig.update_layout(barmode='stack')

    fig.update_layout(title="<b>Quels sont les services qui ferment le plus pendant l'hiver</b>",
                            margin=dict(l=10, r=10, b=10, t=40), title_x=0.5,
                                yaxis_title="",
                                xaxis_title="Nombre de services",
                                legend_title="Statut",)

    st.plotly_chart(fig, use_container_width=True)

# Pourcentage de changement par categorie

df_changes_percent = df_changes_vf.groupby('bigCategorie').sum()
df_changes_percent.drop(columns='Unnamed: 0', inplace=True)

df_changes_percent.reset_index(inplace=True)
df_changes_percent['sum'] = df_changes_percent.sum(axis=1)


cols=["Changement d'horaire", "Services fermés", "Fermé", "Ouvert"]
df_changes_percent[cols]=df_changes_percent[cols].div(df_changes_percent['sum'], axis=0)

df_changes_percent.iloc[:,1:] = df_changes_percent.iloc[:,1:]*100

import plotly.graph_objects as go
from datetime import datetime

fig3 = go.Figure(data=[
    go.Bar(name="Services fermés dans structures fermées", x=df_changes_percent['bigCategorie'], 
           y=df_changes_percent["Fermé"], marker_color='#231E3C', 
          hovertemplate=' Catégorie de services: %{x} <br>Pourcentage de service dans structures fermées: %{y:.2f}%'),
    go.Bar(name="Service fermé dans structures ouvertes", x=df_changes_percent['bigCategorie'], 
           y=df_changes_percent["Services fermés"], marker_color='#3E3A71', 
          hovertemplate='Catégorie de services: %{x} <br>Pourcentage de service fermé dans structures ouvertes: %{y:.2f}%'),
    go.Bar(name="Service dans structures ouvertes avec changement d'horaire", x=df_changes_percent['bigCategorie'], 
           y=df_changes_percent["Changement d'horaire"], marker_color='#E65A46', 
          hovertemplate='Catégorie de services: %{x} <br>Pourcentage de service dans structures avec changement d\'horaire: %{y:.2f}%'),
    go.Bar(name="Service ouvert dans structures ouvertes", x=df_changes_percent['bigCategorie'], 
           y=df_changes_percent["Ouvert"], marker_color='#2896A0', 
          hovertemplate='Catégorie de services: %{x} <br>Pourcentage de service ouvert dans structures ouvertes: %{y:.2f}%'),
])

# Change the bar mode
fig3.update_layout(barmode='stack')

fig3.update_layout(title="<b>Quels impacts a l'hiver sur les services</b>",
                          margin=dict(l=10, r=10, b=10, t=40), title_x=0.5,
                            yaxis_title="Part de services",
                            xaxis_title="",
                            legend_title="Statut",)

st.plotly_chart(fig3, use_container_width=True)

# Qui fait la màj

df_history_campaign_users_final.status.replace({'ADMIN_SOLIGUIDE':"l'équipe Solinum",'ADMIN_TERRITORY':"l'équipe territoiriale","PRO":"les acteurs"}, inplace=True)
tabs = pd.DataFrame(df_history_campaign_users_final.status.value_counts())
            
fig3bis = px.pie(values=tabs.status, names=tabs.index, color_discrete_sequence= ['#3E3A71', '#2896A0'])
fig3bis.update_traces(textinfo="percent+label")
fig3bis.update_traces(hovertemplate = "%{label}: <br>Nbre de fiches: %{value}")
                 
st.markdown("<center><b>Qui a réalisé les mises à jour pendant l'été ?</b>", unsafe_allow_html=True)
st.markdown("<center>Les mises à jour des structures référencées sur Soliguide peut se faire par deux biais :<br> soit directement par l\'organisation concernée, via son compte professionnel <br>(fonctionnalité sortie en décembre 2020), soit par l\'équipe Solinum locale.</center>", unsafe_allow_html=True)

st.plotly_chart(fig3bis, use_container_width=True)

# Fiche màj 6 mois
st.markdown("<center><b>Fiches mises à jour depuis moins de 6 mois</b>", unsafe_allow_html=True)

maj_6_tab.drop(columns='territoire',inplace=True)
maj_6_tab_tot = maj_6_tab.T

maj_6_tab_tot.rename(index={'status':'Nombre de fiches à jour (depuis moins de 6 mois)','non_maj_6_m':'Nombre de fiches avec une actualisation de plus de 6 mois'},inplace=True)

fig5 = px.pie(values=maj_6_tab_tot[(maj_6_tab_tot.columns.to_list()[0])], names=maj_6_tab_tot.index, color_discrete_sequence= [ '#7201a8', '#d8576b'],)
fig5.update_traces(hovertemplate = "%{label}: <br>Nombre de fiches: %{value}")

st.plotly_chart(fig5, use_container_width=True)

# Derniers chiffres

col1, col2, col3, col4 = st.columns(4)

if categorie == 'France':

    html_string_1 = f"<center><font face='Helvetica' size='6'>{int(df_mails.loc[df_mails['territory'] == 'Total', 'emails envoyés'].iloc[0]) + int(df_mails.loc[df_mails['territory'] == 'Total', 'Relance envoyées'].iloc[0])}</font><br><font size='2'>e-mails et relances envoyés par l'équipe Solinum</font></center>"

    html_string_3 = f"<center><font face='Helvetica' size='6'>{int(df_search_vf.iloc[0,0])}</font><br/><font size='2'>recherches réalisées sur Soliguide</font></center>"


elif categorie == 'Ile-De-France':

    idf_mails = (int(df_mails.loc[df_mails['territory'] == '75', 'emails envoyés'].iloc[0]) + int(df_mails.loc[df_mails['territory'] == '77', 'emails envoyés'].iloc[0]) + int(df_mails.loc[df_mails['territory'] == '78', 'emails envoyés'].iloc[0])
    + int(df_mails.loc[df_mails['territory'] == '91', 'emails envoyés'].iloc[0]) + int(df_mails.loc[df_mails['territory'] == '92', 'emails envoyés'].iloc[0]) + int(df_mails.loc[df_mails['territory'] == '93', 'emails envoyés'].iloc[0])
    + int(df_mails.loc[df_mails['territory'] == '94', 'emails envoyés'].iloc[0]) + int(df_mails.loc[df_mails['territory'] == '95', 'emails envoyés'].iloc[0]) + int(df_mails.loc[df_mails['territory'] == '75', 'Relance envoyées'].iloc[0])
    + int(df_mails.loc[df_mails['territory'] == '77', 'Relance envoyées'].iloc[0]) + int(df_mails.loc[df_mails['territory'] == '78', 'Relance envoyées'].iloc[0]) + int(df_mails.loc[df_mails['territory'] == '91', 'Relance envoyées'].iloc[0])
    + int(df_mails.loc[df_mails['territory'] == '92', 'Relance envoyées'].iloc[0]) + int(df_mails.loc[df_mails['territory'] == '93', 'Relance envoyées'].iloc[0]) + int(df_mails.loc[df_mails['territory'] == '94', 'Relance envoyées'].iloc[0])
    + int(df_mails.loc[df_mails['territory'] == '95', 'Relance envoyées'].iloc[0]))

    html_string_1 = f"<center><font face='Helvetica' size='6'>{idf_mails}</font><br><font size='2'>e-mails et relances envoyés par l'équipe Solinum</font></center>"

    html_string_3 = f"<center><font face='Helvetica' size='6'>{int(df_search_vf.iloc[0])}</font><br/><font size='2'>recherches réalisées sur Soliguide</font></center>"


else:
    html_string_1 = f"<center><font face='Helvetica' size='6'>{int(df_mails.loc[df_mails['territory'] == (cat_dict_2[categorie]), 'emails envoyés'].iloc[0]) + int(df_mails.loc[df_mails['territory'] == (cat_dict_2[categorie]), 'Relance envoyées'].iloc[0])}</font><br><font size='2'>e-mails et relances envoyés par l'équipe Solinum</font></center>"
  
    html_string_3 = f"<center><font face='Helvetica' size='6'>{int(df_search_vf.iloc[0,0])}</font><br/><font size='2'>recherches réalisées sur Soliguide</font></center>"


if 'Appel' in df_source_màj_2.index and not categorie == "Puy-de-Dôme":
    html_string_2 = f"<center><font face='Helvetica' size='6'>{int(df_source_màj_2.loc['Appel','❄️ Source de la mise à jour'])}</font><br/><font size='2'>appels effectués par l'équipe Solinum</font></center>"
    col2.markdown(html_string_2, unsafe_allow_html=True)



col1.markdown(html_string_1, unsafe_allow_html=True)
col3.markdown(html_string_3, unsafe_allow_html=True)
    
html_string = "<br>"

st.markdown(html_string, unsafe_allow_html=True)
            
df_fiches_màj_vf.replace({True:1, False:0}, inplace=True)
df_fiches_màj_vf['A jour'] = df_fiches_màj_vf[['sections.closed.updated','sections.hours.updated','sections.services.updated','sections.tempMessage.updated']].sum(axis=1)
df_fiches_màj_pie = df_fiches_màj_vf['A jour'].map(lambda x: 'Fiches totalement à jour' if x == 4 else ('Fiches totalement à jour' if x == 3 else ('Fiches totalement à jour' if x == 2 else ('Fiches totalement à jour' if x == 1 else x== 'à mettre à jour'))))    
df_fiches_màj_pie.replace({False : "Fiches à mettre à jour"}, inplace=True)
df_fiches_màj_pie = pd.DataFrame(df_fiches_màj_pie.value_counts())
df_fiches_màj_pie.loc["Total"] = df_fiches_màj_pie.sum()
percent_uodated = df_fiches_màj_pie.loc['Fiches totalement à jour','A jour']/ df_fiches_màj_pie.loc['Total','A jour'] * 100

html_string_4 = f"<center><font face='Helvetica' size='6'>{round(percent_uodated, 2)} %</font><br/><font size='2'>de la base de données mise à jour cet hiver</font></center>"

col4.markdown(html_string_4, unsafe_allow_html=True)
