import pickle
import streamlit as st
import requests


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=bf1d8a5f0f007057b89e0f52a5d0d778&language=en-US".format(movie_id)  #8265bd1679663a7ea12ac168da84d2e8
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters


st.header('Movie Recommender System')
movies = pickle.load(open('model/movie_list.pkl','rb'))
similarity = pickle.load(open('model/similarity.pkl','rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    num_recommendations = 5

    # Create a list of column elements
    columns = st.columns(num_recommendations)

    # Loop through each column and display the recommendations
    for i in range(num_recommendations):
        with columns[i]:
            st.text(recommended_movie_names[i])
            st.image(recommended_movie_posters[i])






