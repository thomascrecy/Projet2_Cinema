import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import streamlit as st
from sklearn.neighbors import KNeighborsClassifier, NearestNeighbors
from sklearn.preprocessing import StandardScaler
import webbrowser
import streamlit as st
from PIL import Image
import streamlit as st
import matplotlib.pyplot as plt
from urllib.request import urlopen
import json
from copy import deepcopy
from plotly.subplots import make_subplots

#UI

st.set_page_config(
    page_title='Dashboard',
    page_icon='🎥'
)
#st.sidebar.error('20th Century Pandas', icon='🎥')

# import base64
# def add_bg_from_local(image_file):
#     with open(image_file, "rb") as image_file:
#         encoded_string = base64.b64encode(image_file.read())
#     st.markdown(
#     f"""
#     <style>
#     .stApp {{
#         background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
#         background-size: cover
#     }}
#     </style>
#     """,
#     unsafe_allow_html=True
#     )
# add_bg_from_local('Popcorn.png')

image = Image.open('head.png')
st.image(image)


################################################DASHBOARD############################################################################################################################

##Chiffres généraux

@st.cache_data
def load_data(csv):
    data = pd.read_csv(csv)
    return data

chiffres_globaux = load_data('Chiffres_globaux.csv')

nombre_films_tot = load_data('Nb_tot_films.csv')


#Évolution du volume des films dispos en France par décénnie de 1950 à nos jours

movies_1950_2020 = load_data('movies_1950_2020.csv')

# NBR DE FILMS
f_comptage = movies_1950_2020.groupby(['decennie']).size().reset_index(name='COUNT')

colors1 = ['#FF0000']

fig = px.bar(f_comptage, x=f_comptage['decennie'], y=f_comptage['COUNT'],barmode='stack', color_discrete_sequence=colors1)
#fig.update(layout=dict(title=dict(x=0.5)))    # ça c'est pour centre le titre
fig.update_yaxes(title_text='Nombre de films')
fig.update_xaxes(title_text='Décennies')



#Répartition des genres selon la décennie
genres_par_dec = pd.read_csv('genres_par_dec.csv')

## Graphique

# fig_genre_purcent = px.bar(genres_par_dec, x = "decennie", y = "value",
#              color = "split_genres", category_orders={'decennie':['1950-1960','1960-1970','1970-1980',
#                  '1980-1990','1990-2000','2000-2010','2010-2020', '2020-2030']})
fig_genre_purcent = px.bar(genres_par_dec, x = "decennie", y = "value",
       color = "split_genres",
       category_orders={'decennie':['de 1950 à 1960','de 1960 à 1970','de 1970 à 1980','de 1980 à 1990','de 1990 à 2000','de 2000 à 2010','de 2010 à 2020', 'de 2020 à 2030']})
                #  text=f_comptage['Percentage'].apply(lambda x: '{0:1.0f}%'.format(x)),)
#fig_genre_purcent.update(layout=dict(title=dict(x=0.5)))    # ça c'est pour centre le titre
# fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
# fig_genre_purcent.update_traces(texttemplate='%{text:.2s}', textposition='outside')

# print(fig_genre_purcent.data.text)
# old_labels=fig_genre_purcent.data[0].text
# new_labels=[f"{ol}%"  for ol  in old_labels[:-10]]
# new_labels.extend(old_labels[-10:])
# fig_genre_purcent.update_traces(labels=new_labels)

fig_genre_purcent.update_layout(uniformtext_minsize=8, uniformtext_mode='hide', xaxis_title="Décennies", yaxis_title="Pourcentages", legend=dict(
        title='Genres'))




## TOP10 - TOUS GENRES CONFONDUS

classement_movie_top10_votessup50000= load_data('classement_movie_top10_votessup50000.csv')
classement_movie_top10_votessup50000['startYear'] = classement_movie_top10_votessup50000['startYear'].astype(str).str.replace(',', '')
classement_movie_top10_votessup50000['numVotes'] = classement_movie_top10_votessup50000['numVotes'].astype(str).str.replace(',', '')

## TOP10 - POUR LES GENRES LES + POPULAIRES
filtre_movie_genres_votessup50000 =  load_data("filtre_movie_genres_votessup50000.csv")

## TOP100 - REPARTITION PAR GENRE

top_100 = load_data('Top100_movies.csv')

## OBTENIR LE TOP 10 DES ACTEURS PAR GENRE

# Charger les données initiales
# Remplacez ceci par le chargement de votre propre fichier de données
jointure_4 = load_data('jointure_4.csv')

#st.title("Bienvenue sur votre tableau de bord")
#st.image("https://image.tmdb.org/t/p/w500/bGksau9GGu0uJ8DJQ8DYc9JW5LM.jpg", use_column_width=True)
# Contenu de la page d'accueil
vertical_space = 20

###################1ER GRAPH
# st.write("<h2 style='font-size: 25px;'> 📊 Évolution du volume des films disponibles en France par décénnie de 1950 à nos jours</h2>", unsafe_allow_html=True)
# st.plotly_chart(fig)

#st.markdown(f"<div style='margin-bottom: {vertical_space}px'></div>", unsafe_allow_html=True)

#####################2E GRAPH
# st.write("<h2 style='font-size: 25px;'> 🔎 Répartition des genres selon la décennie</h2>", unsafe_allow_html=True)         
# st.plotly_chart(fig_genre_purcent)

#st.markdown(f"<div style='margin-bottom: {vertical_space}px'></div>", unsafe_allow_html=True)

# st.write("<h2 style='font-size: 25px;'> 📈 Évolution du temps des films par genre les + populaires </h2>", unsafe_allow_html=True)
# #Temps moyen des films par genre

# temps_moy_film = pd.read_csv('Temps_film.csv')
# fig_2 = px.line(temps_moy_film, x='Temps_moyen_années', y=temps_moy_film.columns)
# st.plotly_chart(fig_2)

#st.markdown(f"<div style='margin-bottom: {vertical_space}px'></div>", unsafe_allow_html=True)

# st.write("<h2 style='font-size: 25px;'> TOP 🔟 des films tous genres confondus</h2>", unsafe_allow_html=True)
# st.markdown(f"<div style='margin-bottom: {vertical_space}px'></div>", unsafe_allow_html=True)
# st.write(classement_movie_top10_votessup50000.head(11))

#st.markdown(f"<div style='margin-bottom: {vertical_space}px'></div>", unsafe_allow_html=True)
# st.write("<h2 style='font-size: 25px;'> Classement des films par genre(s) selectionné(s) </h2>", unsafe_allow_html=True)
# st.markdown(f"<div style='margin-bottom: {vertical_space}px'></div>", unsafe_allow_html=True)
# # Genres les + populaires
# genres_options = ['Comedy', 'Drama', 'Horror','Thriller','Action','Documentary']

# # Widget de sélection de genres
# genres_selectionnes = st.multiselect("Sélectionner les genres", genres_options)

# # Widget de sélection du nombre de films à afficher
# nombre_films = st.slider("Nombre de films à afficher", min_value=1, max_value=30, value=10, step=5)

# for genre in genres_selectionnes:

#     # Filtrer le DataFrame par genre et conditions supplémentaires
#     filtre_movie = filtre_movie_genres_votessup50000['split_genres'].str.contains(genre)
#     filtre_votessup50000 = filtre_movie_genres_votessup50000['numVotes'] > 50000
#     filtre_movie_thriller_votessup50000 = filtre_movie_genres_votessup50000[filtre_movie & filtre_votessup50000]

#     # Trier le DataFrame filtré
#     classement_movie_thriller_votessup50000 = filtre_movie_thriller_votessup50000.sort_values(by=['averageRating','numVotes'], ascending=False)
#     classement_movie_thriller_votessup50000 = classement_movie_thriller_votessup50000.reset_index()
#     classement_movie_thriller_votessup50000.drop(columns=['index', 'titleType', 'originalTitle','isAdult', 'runtimeMinutes', 'ordering','region', 'language', 'types', 'attributes', 'isOriginalTitle','decennie', 'split_genres'], inplace=True)
    
#     # Sélectionner le nombre de films à afficher
#     classement_movie_thriller_top_n = classement_movie_thriller_votessup50000.head(nombre_films)

#     # Formater la colonne startYear
#     #classement_movie_thriller_top_n['startYear'] = classement_movie_thriller_top_n['startYear'].astype(int)
#     classement_movie_thriller_top_n['startYear'] = classement_movie_thriller_top_n['startYear'].astype(str).str.replace(',', '')
#     classement_movie_thriller_top_n['numVotes'] = classement_movie_thriller_top_n['numVotes'].astype(str).str.replace(',', '')
#     # Afficher le tableau avec Streamlit Components
#     st.write(classement_movie_thriller_top_n)


tab1, tab2, tab3, tab4= st.tabs(["Général", "Genres", "Top10", "Classement",])
with tab1:
    #Affichage des chiffres généraux
    # Créer les objets dp.BigNumber
    # Récupérer les valeurs nécessaires
    nombre_acteurs_actrices = chiffres_globaux.values[0] + chiffres_globaux.values[1]
    nombre_acteurs_actrices_formate = "{:,}".format(nombre_acteurs_actrices.item())

    nombre_ecrivains = chiffres_globaux.values[2]
    nombre_ecrivains_formate = "{:,}".format(nombre_ecrivains.item())

    nombre_producteurs = chiffres_globaux.values[3]
    nombre_producteurs_formate = "{:,}".format(nombre_producteurs.item())


    nombre_films = nombre_films_tot['tconst'].size
    nombre_films_formate = "{:,}".format(nombre_films)


    nombre_directeurs = chiffres_globaux.values[4]
    nombre_directeurs_formate = "{:,}".format(nombre_directeurs.item())


    nombre_cinematographes = chiffres_globaux.values[6]
    nombre_cinematographes_formate = "{:,}".format(nombre_cinematographes.item())

    # Afficher les "big numbers" 
    st.write("<h2 style='font-size: 25px;'> Chiffres généraux (1950-2020)</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)

    col1.metric("Nombre d'acteurs/actrices", nombre_acteurs_actrices_formate)
    col2.metric("Nombre de scenaristes", nombre_ecrivains_formate)
    col3.metric("Nombre de producteurs", nombre_producteurs_formate)


    col1, col2, col3 = st.columns(3)

    col1.metric("Nombre de films", nombre_films_formate)
    col2.metric("Nombre de réalisateurs", nombre_directeurs_formate)
    col3.metric("Nombre de cinématographes", nombre_cinematographes_formate)

    vertical_space = 50
    
    st.divider()

    st.write("<h2 style='font-size: 25px;'> 📊 Évolution du volume des films disponibles en France par décénnie (1950-2030)</h2>", unsafe_allow_html=True)
    st.plotly_chart(fig)

    st.divider()
    
    movies_1950_2020 = load_data('movies_and_series2.csv')

    st.write("<h2 style='font-size: 25px;'> 📊 Comparaison entre séries et films par décennie (1950-2020)</h2>", unsafe_allow_html=True)
    # Group by 'Temps_moyen_années' and count the occurrences
    f_comptage = movies_1950_2020.groupby(['Decennie', 'titleType']).size().reset_index(name='COUNT')

    colors = {'movie': '#FF0000', 'tvSeries': '#FFE187'}

    # Plot the stacked bar chart
    fig = px.bar(f_comptage, x='Decennie', y='COUNT', color='titleType', barmode='stack', color_discrete_map=colors)

    # Update axis labels
    fig.update_xaxes(title_text='Décennies')
    fig.update_yaxes(title_text='Nombre total')

    fig.for_each_trace(lambda t: t.update(name='Films') if t.name == 'movie' else None)
    fig.for_each_trace(lambda t: t.update(name='Séries') if t.name == 'tvSeries' else None)
    fig.update_layout(legend=dict(title=''))

    # Display the figure using Streamlit
    st.plotly_chart(fig)

    st.divider()

    st.write("<h2 style='font-size: 25px;'> 📊 Note moyenne des films par nombres de votes (1950-2020)</h2>", unsafe_allow_html=True)
    #data = pd.read_csv('tmdb_full.csv')

    jointure_4_filtree = load_data('jointure_4_filtree.csv')
    #jointure_4_filtree=pd.read_csv('jointure_4_filtree.csv')
    fig = px.scatter(jointure_4_filtree, x="averageRating", y="numVotes", marginal_x="histogram", marginal_y="rug", color_discrete_sequence=colors1)
    
    # Nom de l'axe des x
    fig.update_xaxes(title_text='Note moyenne')
    
    # Nom de l'axe des y
    fig.update_yaxes(title_text='Nombre de votes')
    
    fig.update_layout(
    width=800,  
    height=600)

    st.plotly_chart(fig)

    st.divider()
    #data = pd.read_csv('tmdb_full.csv')


    ###########MAP
    map_movies = load_data('tmdb_full.csv')

    iso_mapping = {'AD': 'AND',
    'AE': 'ARE', 'AF': 'AFG', 'AG': 'ATG', 'AI': 'AIA', 'AL': 'ALB', 'AM': 'ARM', 'AN': 'ANT', 'AO': 'AGO',
    'AQ': 'ATA', 'AR': 'ARG', 'AS': 'ASM', 'AT': 'AUT', 'AU': 'AUS', 'AW': 'ABW', 'AZ': 'AZE', 'BA': 'BIH',
    'BB': 'BRB', 'BD': 'BGD', 'BE': 'BEL', 'BF': 'BFA', 'BG': 'BGR', 'BH': 'BHR', 'BI': 'BDI', 'BJ': 'BEN',
    'BM': 'BMU', 'BN': 'BRN', 'BO': 'BOL', 'BR': 'BRA', 'BS': 'BHS', 'BT': 'BTN', 'BU': 'BUR', 'BV': 'BVT',
    'BW': 'BWA', 'BY': 'BLR', 'BZ': 'BLZ', 'CA': 'CAN', 'CC': 'CCK', 'CF': 'CAF', 'CG': 'COG', 'CH': 'CHE',
    'CI': 'CIV', 'CK': 'COK', 'CL': 'CHL', 'CM': 'CMR', 'CN': 'CHN', 'CO': 'COL', 'CR': 'CRI', 'CS': 'CSK',
    'CU': 'CUB', 'CV': 'CPV', 'CX': 'CXR', 'CY': 'CYP', 'CZ': 'CZE', 'DD': 'DDR', 'DE': 'DEU', 'DJ': 'DJI',
    'DK': 'DNK', 'DM': 'DMA', 'DO': 'DOM', 'DZ': 'DZA', 'EC': 'ECU', 'EE': 'EST', 'EG': 'EGY', 'EH': 'ESH',
    'ER': 'ERI', 'ES': 'ESP', 'ET': 'ETH', 'FI': 'FIN', 'FJ': 'FJI', 'FK': 'FLK', 'FM': 'FSM', 'FO': 'FRO',
    'FR': 'FRA', 'FX': 'FXX', 'GA': 'GAB', 'GB': 'GBR', 'GD': 'GRD', 'GE': 'GEO', 'GF': 'GUF', 'GH': 'GHA',
    'GI': 'GIB', 'GL': 'GRL', 'GM': 'GMB', 'GN': 'GIN', 'GP': 'GLP', 'GQ': 'GNQ', 'GR': 'GRC', 'GS': 'SGS',
    'GT': 'GTM', 'GU': 'GUM', 'GW': 'GNB', 'GY': 'GUY', 'HK': 'HKG', 'HM': 'HMD', 'HN': 'HND', 'HR': 'HRV',
    'HT': 'HTI', 'HU': 'HUN', 'ID': 'IDN', 'IE': 'IRL', 'IL': 'ISR', 'IN': 'IND', 'IO': 'IOT', 'IQ': 'IRQ',
    'IR': 'IRN', 'IS': 'ISL', 'IT': 'ITA', 'JM': 'JAM', 'JO': 'JOR', 'JP': 'JPN', 'KE': 'KEN', 'KG': 'KGZ',
    'KH': 'KHM', 'KI': 'KIR', 'KM': 'COM', 'KN': 'KNA', 'KP': 'PRK', 'KR': 'KOR', 'KW': 'KWT', 'KY': 'CYM',
    'KZ': 'KAZ', 'LA': 'LAO', 'LB': 'LBN', 'LC': 'LCA', 'LI': 'LIE', 'LK': 'LKA', 'LR': 'LBR', 'LS': 'LSO',
    'LT': 'LTU', 'LU': 'LUX', 'LV': 'LVA', 'LY': 'LBY', 'MA': 'MAR', 'MC': 'MCO', 'MD': 'MDA', 'MG': 'MDG',
    'MH': 'MHL', 'ML': 'MLI', 'MN': 'MNG', 'MM': 'MMR', 'MO': 'MAC', 'MP': 'MNP', 'MQ': 'MTQ', 'MR': 'MRT',
    'MS': 'MSR', 'MT': 'MLT', 'MU': 'MUS', 'MV': 'MDV', 'MW': 'MWI', 'MX': 'MEX', 'MY': 'MYS', 'MZ': 'MOZ',
    'NA': 'NAM', 'NC': 'NCL', 'NE': 'NER', 'NF': 'NFK', 'NG': 'NGA', 'NI': 'NIC', 'NL': 'NLD', 'NO': 'NOR',
    'NP': 'NPL', 'NR': 'NRU', 'NT': 'NTZ', 'NU': 'NIU', 'NZ': 'NZL', 'OM': 'OMN', 'PA': 'PAN', 'PE': 'PER',
    'PF': 'PYF', 'PG': 'PNG', 'PH': 'PHL', 'PK': 'PAK', 'PL': 'POL', 'PM': 'SPM', 'PN': 'PCN', 'PR': 'PRI',
    'PT': 'PRT', 'PW': 'PLW', 'PY': 'PRY', 'QA': 'QAT', 'RE': 'REU', 'RO': 'ROU', 'RU': 'RUS', 'RW': 'RWA',
    'SA': 'SAU', 'SB': 'SLB', 'SC': 'SYC', 'SD': 'SDN', 'SE': 'SWE', 'SG': 'SGP', 'SH': 'SHN', 'SI': 'SVN',
    'SJ': 'SJM', 'SK': 'SVK', 'SL': 'SLE', 'SM': 'SMR', 'SN': 'SEN', 'SO': 'SOM', 'SR': 'SUR', 'ST': 'STP',
    'SU': 'SUN', 'SV': 'SLV', 'SY': 'SYR', 'SZ': 'SWZ', 'TC': 'TCA', 'TD': 'TCD', 'TF': 'ATF', 'TG': 'TGO',
    'TH': 'THA', 'TJ': 'TJK', 'TK': 'TKL', 'TM': 'TKM', 'TN': 'TUN', 'TO': 'TON', 'TP': 'TMP', 'TR': 'TUR',
    'TT': 'TTO', 'TV': 'TUV', 'TW': 'TWN', 'TZ': 'TZA', 'UA': 'UKR', 'UG': 'UGA', 'UM': 'UMI', 'US': 'USA',
    'UY': 'URY', 'UZ': 'UZB', 'VA': 'VAT', 'VC': 'VCT', 'VE': 'VEN', 'VG': 'VGB', 'VI': 'VIR', 'VN': 'VNM',
    'VU': 'VUT', 'WF': 'WLF', 'WS': 'WSM', 'YD': 'YDD', 'YE': 'YEM', 'YT': 'MYT', 'YU': 'YUG', 'ZA': 'ZAF',
    'ZM': 'ZMB', 'ZR': 'ZAR', 'ZW': 'ZWE', 'ZZ': 'ZZZ'}

    map_movies['production_companies_country'] = map_movies['production_companies_country']\
        .str.replace("'", "").str.replace('[', '').str.replace(']', '').str.strip()
    map_movies['split_countries'] = map_movies['production_companies_country'].str.split(",")
    map_movies = map_movies.explode('split_countries')

    # Transform ISO 2 codes to ISO 3 codes and replace unknown codes with NaN
    map_movies['iso_alpha'] = map_movies['split_countries'].map(iso_mapping).replace('', np.nan)

    # Drop rows with unknown ISO codes
    map_movies.dropna(subset=['iso_alpha'], inplace=True)

    country_movies = map_movies['iso_alpha'].value_counts().reset_index()
    country_movies.columns = ['iso_alpha', 'movies_count']
    print(country_movies)


    
    st.write("<h2 style='font-size: 25px;'> 🗺️ Nombre de films par région (1950-2020)</h2>", unsafe_allow_html=True)

    fig = px.choropleth(country_movies, locations="iso_alpha",
                        color="movies_count",
                        hover_name="iso_alpha",
                        color_continuous_scale=px.colors.sequential.Peach,
                        range_color=(0, 20000)
                        )

    fig.update_layout(coloraxis_colorbar_title="Number of Movies")

    fig.update_traces(colorbar=dict(
        title="Nombre de films",
    ))
    fig.update_layout(geo=dict(bgcolor= 'rgba(0,0,0,0)'))

    st.plotly_chart(fig)


with tab2:
    st.write("<h2 style='font-size: 25px;'> 🔎 Répartition des genres selon la décennie (1950-2020)</h2>", unsafe_allow_html=True)         
    st.plotly_chart(fig_genre_purcent)

    st.divider()

    st.write("<h2 style='font-size: 25px;'> 📊 Répartition par genre pour les 100 meilleurs films (1950-2020)</h2>", unsafe_allow_html=True)
    ##Répartition des genres pour les 100 films les mieux notés
    # Comptage des genres
    genre_counts = top_100['genres'].str.split(',', expand=True).stack().value_counts().reset_index()
    genre_counts.columns = ['Genre', 'Count']

    # Créer le graphique à barres 
    fig = px.bar(genre_counts, x='Genre', y='Count', labels={'Genre': 'Genres', 'Count': 'Nombre de films'}, color_discrete_sequence=colors1)

    # Afficher le graphique
    st.plotly_chart(fig)

    st.divider()

    st.write("<h2 style='font-size: 25px;'> 📈 Évolution de la durée des films par genre les + populaires (1950-2020)</h2>", unsafe_allow_html=True)
    temps_moy_film = load_data('Temps_film.csv')
    fig_2 = px.line(temps_moy_film, x='Temps_moyen_années', y=temps_moy_film.columns)
    fig_2.update_layout(xaxis_title="Décennies",yaxis_title="Durée des films (en minutes)", legend=dict(title='Genres'))
    st.plotly_chart(fig_2)

    st.divider()

    st.write("<h2 style='font-size: 25px;'> 📊 Durée moyenne des films (1950-2020)</h2>", unsafe_allow_html=True)

    dis_runtim = load_data('Distribution_runtime.csv')
    
   
    fig = px.histogram(dis_runtim, x='runtimeMinutes', nbins=50, color_discrete_sequence=colors1)
    
    # Nom de l'axe des x
    fig.update_xaxes(title_text='Durée des films')
    
    # Nom l'axe des y
    fig.update_yaxes(title_text='Nombre de films')
        
    fig.update_layout(xaxis_range=[0, 300])
    
    st.plotly_chart(fig)

with tab3:
    st.write("<h2 style='font-size: 25px;'> TOP 🔟 des films tous genres confondus (1950-2020)</h2>", unsafe_allow_html=True)
    st.markdown(f"<div style='margin-bottom: {vertical_space}px'></div>", unsafe_allow_html=True)
    st.write(classement_movie_top10_votessup50000.head(11))

    st.divider()

     ##Affichage_Top_10 des acteurs par genre
    st.markdown(f"<div style='margin-bottom: {vertical_space}px'></div>", unsafe_allow_html=True)
    st.write("<h2 style='font-size: 25px;'> Top 🔟 des acteurs par genre selectionné (1950-2020)</h2>", unsafe_allow_html=True)
    st.markdown(f"<div style='margin-bottom: {vertical_space}px'></div>", unsafe_allow_html=True)

    ## Filtrer sur 'actor' and 'actress'
    filtre_actors = jointure_4.loc[(jointure_4['category']=='actor')|(jointure_4['category']=='actress')]

    # Options de filtre disponibles (à titre d'exemple)
    genres_options = ['Comedy', 'Action', 'Drama','Documentary','Horror', 'Thriller']

    # Sélection du genre à filtrer
    selected_genre = st.selectbox('Sélectionnez un genre', genres_options)

    #Filtrer le dataframe par genre sélectionné
    filtered_df = filtre_actors[filtre_actors['genres'].str.contains(selected_genre)]

    #Pivoter les données par décennie et acteur
    test_2 = pd.pivot_table(filtered_df, values='tconst', index='primaryName', columns='decennie', aggfunc='count')
    test_2['Total'] = test_2.sum(axis=1)
    test_2 = test_2.sort_values(by='Total', ascending=False).reset_index()

    top_10 = test_2.head(10)

 
    fig = px.bar(top_10, x='primaryName', y='Total', labels={'primaryName': 'Acteurs', 'Total': 'Nombre de films'},
                title=f'Top 10 des acteurs de {selected_genre} avec le plus grand nombre de films total', color_discrete_sequence=colors1)

    fig.update_layout(xaxis_tickangle=-45)

    #Afficher le plot avec Streamlit
    st.plotly_chart(fig)
   
    st.divider()

    ##Affichage_Top_10 des reals par genre
    st.markdown(f"<div style='margin-bottom: {vertical_space}px'></div>", unsafe_allow_html=True)
    st.write("<h2 style='font-size: 25px;'> Top 🔟 des réalisateurs par genre selectionné (1950-2020)</h2>", unsafe_allow_html=True)
    st.markdown(f"<div style='margin-bottom: {vertical_space}px'></div>", unsafe_allow_html=True)

    
    # Filtrer le DataFrame pour les directors
    filtre_writers = jointure_4.loc[jointure_4['category'] == 'director']

    # Obtenir les genres uniques dans le DataFrame filtré
    genres_options = ['Comedy', 'Action', 'Drama','Documentary','Horror', 'Thriller']

    # Sélection du genre à filtrer
    selected_genre = st.selectbox('Sélectionnez un genre', genres_options, key='selection_genre')

    # Filtrer le DataFrame par genre sélectionné
    filtered_df = filtre_writers[filtre_writers['genres'].str.contains(selected_genre)]

    # Pivoter les données par décennie et écrivain
    test_3 = pd.pivot_table(filtered_df, values='tconst', index='primaryName', columns='decennie', aggfunc='count')
    test_3['Total'] = test_3.sum(axis=1)
    test_3 = test_3.sort_values(by='Total', ascending=False).reset_index()

    top_10_2 = test_3.head(10)

    colors2 = ['#FFE187']

    fig = px.bar(top_10_2, x='primaryName', y='Total', labels={'primaryName': 'Réalisateurs', 'Total': 'Nombre de films'},
                title=f'Top 10 des réalisateurs de {selected_genre} avec le plus grand nombre de films', color_discrete_sequence=colors2)

    fig.update_layout(xaxis_tickangle=-45)

  
    st.plotly_chart(fig)

with tab4:
    st.write("<h2 style='font-size: 25px;'> ✅ Classement des films par genre(s) selectionné(s) (1950-2020)</h2>", unsafe_allow_html=True)
    st.markdown(f"<div style='margin-bottom: {vertical_space}px'></div>", unsafe_allow_html=True)
    # Genres les + populaires
    genres_options = ['Comedy', 'Drama', 'Horror','Thriller','Action','Documentary']

    # Widget de sélection de genres
    genres_selectionnes = st.multiselect("Sélectionner les genres", genres_options)

    # Widget de sélection du nombre de films à afficher
    nombre_films = st.slider("Nombre de films à afficher", min_value=1, max_value=30, value=10, step=5)

    for genre in genres_selectionnes:

        # Filtrer le DataFrame par genre et conditions supplémentaires
        filtre_movie = filtre_movie_genres_votessup50000['split_genres'].str.contains(genre)
        filtre_votessup50000 = filtre_movie_genres_votessup50000['numVotes'] > 50000
        filtre_movie_thriller_votessup50000 = filtre_movie_genres_votessup50000[filtre_movie & filtre_votessup50000]

        # Trier le DataFrame filtré
        classement_movie_thriller_votessup50000 = filtre_movie_thriller_votessup50000.sort_values(by=['averageRating','numVotes'], ascending=False)
        classement_movie_thriller_votessup50000 = classement_movie_thriller_votessup50000.reset_index()
        classement_movie_thriller_votessup50000.drop(columns=['index', 'titleType', 'originalTitle','isAdult', 'runtimeMinutes', 'ordering','region', 'language', 'types', 'attributes', 'isOriginalTitle','decennie', 'split_genres'], inplace=True)
        
        # Sélectionner le nombre de films à afficher
        classement_movie_thriller_top_n = classement_movie_thriller_votessup50000.head(nombre_films)

        # Formater la colonne startYear
        #classement_movie_thriller_top_n['startYear'] = classement_movie_thriller_top_n['startYear'].astype(int)
        classement_movie_thriller_top_n['startYear'] = classement_movie_thriller_top_n['startYear'].astype(str).str.replace(',', '')
        classement_movie_thriller_top_n['numVotes'] = classement_movie_thriller_top_n['numVotes'].astype(str).str.replace(',', '')
        # Afficher le tableau avec Streamlit Components
        st.write(classement_movie_thriller_top_n)

    st.divider()

    #st.write("<h2 style='font-size: 25px;'> ✅ Classements des films par acteur sélectionné (1950-2020)</h2>", unsafe_allow_html=True)
    #actors= jointure_4.loc[jointure_4['category']=='actor']
    
    #film_names = actors['primaryName'].unique()
    
    #jointure_4['startYear'] = jointure_4['startYear'].astype(str).str.replace(',', '')
    #actors = jointure_4.loc[jointure_4['category'] == 'actor']
    #film_names = [''] + list(actors['primaryName'].unique())
    # Sélection de l'acteur avec la SelectBox
    #selected_film = st.selectbox("Sélectionnez le nom de l'acteur :", film_names)
    # Vérification si une option a été sélectionnée
    #if selected_film != '':
        # Filtre des films pour l'acteur sélectionné
        #filtered_df = jointure_4[jointure_4['primaryName'] == selected_film]
        # Tri du DF par note et num_votes décroissant
        #sorted_df = filtered_df.sort_values(by=['averageRating', 'numVotes'], ascending=False)
        # On prend les 10 meilleurs
        #top_10_films = sorted_df.head(10)
        
        #st.dataframe(top_10_films[['tconst', 'originalTitle', 'averageRating', 'startYear']])
