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

#UI

st.set_page_config(
    page_title='Recommandations',
    page_icon='🎥'
)

image = Image.open('head.png')
st.image(image)

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


#######################################################################################################################################

@st.cache_data
def load_data(csv):
    data = pd.read_csv(csv)
    return data
#st.title("Découvrez notre système de recommandation 🍿")

# Chargement des données des films depuis un fichier CSV par exemple
df_films = load_data('df_final_9.csv').dropna(subset='de 1970 à 1980')

# Création d'une nouvelle colonne avec le lien de redirection vers IMDB
df_films['IMDb_link'] = df_films['tconst'].apply(lambda x: f"https://www.imdb.com/title/{x}/")

# Création d'une nouvelle colonne avec l'image du film
df_films['IMDb_image'] = df_films['poster_path'].apply(lambda x: f"https://image.tmdb.org/t/p/w200{x}")


##Trier le dataframe par numvotes et average
df_films = df_films.sort_values(['vote_count', 'vote_average'], ascending=False)


## On ajoute une première ligne vide dans notre df pour qu'elle apparaisse dans la liste déroulante
options = [''] + df_films['title_year'].tolist()
search_term = st.selectbox("Saisissez le titre du film :", options=options, index=0, key='selectbox')

# Filtrer les films en fonction du titre recherché
#films_filtrés = df_films[df_films['title_year'].str.contains(search_term, case=False)]
films_tries = pd.DataFrame()

films_filtrés = df_films.where(df_films['title_year']==search_term).dropna(how='all')
if not films_filtrés.empty:
    # Trier les films filtrés selon la note moyenne et le nombre de votants
    films_tries = films_filtrés.sort_values(['vote_average', 'vote_count'], ascending=False)

# Afficher les détails du film sélectionné
if not films_tries.empty:
    film = films_tries.iloc[0]
    st.write("Titre :", film['originalTitle'])
    st.write("Année de sortie :", film['startYear'])
    st.write("Genre :", film['genres_x'])
    vertical_space = 50
    st.markdown(f"<style>div.stButton > button {{ margin-bottom: {vertical_space}px; }}</style>", unsafe_allow_html=True)
    # Ajoutez d'autres détails du film que vous souhaitez afficher

    
    vertical_space=20
    st.markdown(f"<style>div.stButton > button {{ margin-bottom: {vertical_space}px; }}</style>", unsafe_allow_html=True)
    st.write("<h2 style='font-size: 25px;'> 🎬 Voici les films que nous vous suggérons de regarder :</h2>", unsafe_allow_html=True)

    
    #Enregistrer le film choisi
    selection_utilisateur = film
    

    #Filtrer df_films pour enlever le film choisi par l'utilisateur
    # df_recommandation = df_films.where(df_films.tconst != film.tconst).dropna(how='all')
    df_recommandation = df_films


    ## On garde les films uniquement sup à 6,5
    # df_recommandation = df_recommandation.loc[df_recommandation['note_ponderee'] > 6.5]
    
    # Sélectionner les colonnes pour la recherche et la recommandation
    
    # X = df_recommandation.select_dtypes(include='number').drop(columns=['startYear', 'budget', 'revenue', 'vote_average','vote_count','popularity'])
    X = df_recommandation.select_dtypes(include='number').drop(columns=['budget', 'revenue', 'vote_average','vote_count'])

    ##On sélection la ligne concernée avec les features pour la donner à notre model
    recommandation_film_utilisateur = df_films.loc[df_films['tconst'] == film['tconst']]
    
#     recommandation_def = recommandation_film_utilisateur.select_dtypes(include='number').drop(columns=['startYear', 'budget', 'revenue', 'vote_average',
#    'vote_count','popularity'])
    recommandation_def = recommandation_film_utilisateur.select_dtypes(include='number').drop(columns=['budget', 'revenue', 'vote_average','vote_count'])

    ## Entraîner le modèle de recherche
    model = NearestNeighbors(n_neighbors=7).fit(X)

    ## On remonte les indices des voisins pour le film selectionné par l'utilisateur
    distances, indices = model.kneighbors(recommandation_def)
    indices = indices[0][1:]
    
    recommended_movies = df_recommandation.iloc[indices.flatten()][['originalTitle','startYear','IMDb_link','IMDb_image','vote_average','revenue','vote_count','popularity','runtimeMinutes','overview']]
    #recommended_movies = df_recommandation.iloc[indices.flatten()][['originalTitle','startYear','IMDb_link','IMDb_image','vote_average','revenue','vote_count','popularity','runtimeMinutes','overview']]

    #st.dataframe(recommended_movies)

    # Afficher le DataFrame dans Streamlit
    #Les films recommandés

    num_films = 6
    num_columns = 2
    films_per_column = num_films // num_columns
    

    columns = st.columns(num_columns)

    for i in range(num_films):
        film_index = i % films_per_column
        column_index = i // films_per_column

        with columns[column_index]:
            
            vertical_space = 20
            st.markdown(f"<div style='margin-bottom: {vertical_space}px'></div>", unsafe_allow_html=True)
            
            st.markdown("""
                <div style="margin: 0 auto; text-align: center;">
                    <h5>{}<h5>
                    <img src="{}">
                </div>
            """.format(recommended_movies.iloc[i]['originalTitle'], recommended_movies.iloc[i]['IMDb_image']), unsafe_allow_html=True)
            vertical_space = 10
            st.markdown(f"<div style='margin-bottom: {vertical_space}px'></div>", unsafe_allow_html=True)

            with st.container():
                st.markdown(
                    """
                    <style>
                    .stButton>button {
                        margin: 0 auto;
                        display: block;
                    }
                    </style>
                    """,
                    unsafe_allow_html=True
                )
                # Afficher l'année de sortie
                st.write("Année : ", str(recommended_movies.iloc[i]['startYear']).replace(",", ""))
                # Afficher la durée

                # Récupérer la durée en minutes
                #duration_minutes = int(recommended_movies.iloc[i]['runtimeMinutes'])
                # Convertir en heures et minutes
                #hours, minutes = divmod(duration_minutes, 60)
                # Afficher la durée en heures et minutes
                #st.write("Durée : ", hours, "heures", minutes, "minutes")

                ##Afficher la note moyenne IMDB : 
                st.write("Note moyenne : ", recommended_movies.iloc[i]['vote_average'])

                ## Afficher le decriptif du film
                if recommended_movies.iloc[i]['overview']:
                    st.write("Résumé : ", recommended_movies.iloc[i]['overview'][:150], "...")
                else:
                        st.write("Pas de résumé disponible pour ce film.")

                
                vertical_space = 20
                st.markdown(f"<div style='margin-bottom: {vertical_space}px'></div>", unsafe_allow_html=True)
                if st.button("En savoir plus", key="imdb_button_" + str(i)):
                    url = recommended_movies.iloc[i]['IMDb_link']
                    webbrowser.open_new_tab(url)
                
        
            if film_index < films_per_column - 1:
                # vertical_space = 5
                # st.markdown(f"<div style='margin-bottom: {vertical_space}px'></div>", unsafe_allow_html=True)
                st.markdown(
                    """
                    <hr style="border: 1px solid #F5F5DC;">
                    """,
                    unsafe_allow_html=True
                )
    
# Ajouter descriptif du film
