import streamlit as st
import pickle
import pandas as pd
import requests
import gdown
import gzip
import os

def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=64b5061683800550d8933b2fde9ff326&language=en-US')
    data = response.json()
    poster_path = data.get('poster_path')
    if poster_path:
        return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    else:
        return "https://via.placeholder.com/500x750.png?text=No+Image"


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key = lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster from API
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies , recommended_movies_poster

movie_dict = pickle.load(open('movie_dict.pkl' , 'rb'))
movies = pd.DataFrame(movie_dict)




# File ID from Google Drive
file_id = "1vSzZDZxQOQiL4kq1TW5feSyDAtkHfidR"
output = "similarity.pkl.gz"

# Download the file only if not already present
if not os.path.exists(output):
    gdown.download(f"https://drive.google.com/uc?id={file_id}", output, quiet=False)

# Load the similarity matrix
with gzip.open(output, "rb") as f:
    similarity = pickle.load(f)



st.title('Movies Recommender System')

selected_movie_name = st.selectbox(
'Select a movie to get recommendations',
movies['title'].values
)

if st.button('Recommend'):
    names , posters = recommend(selected_movie_name)
    col1 , col2 , col3 , col4 , col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])