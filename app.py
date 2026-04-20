import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import requests

TMDB_API_KEY = "enter your api key"

@st.cache_data
def get_poster(movie_title):
    try:
        url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={movie_title}"
        response = requests.get(url, timeout=5)
        data = response.json()
        if "results" in data and data["results"]:
            poster_path = data["results"][0]["poster_path"]
            if poster_path:
                return f"https://image.tmdb.org/t/p/w500{poster_path}"
    except Exception:
        return None
    return None


if "search_history" not in st.session_state:
    st.session_state.search_history = []

# load data
df = pd.read_csv("data.csv")

df["title_lower"] = df["Series_Title"].str.lower()

df["Genre"] = df["Genre"].apply(lambda x: x.lower().replace(",",""))
df["Director"] = df["Director"].apply(lambda x: x.lower().replace(" ",""))
df["Star1"] = df["Star1"].apply(lambda x: x.lower().replace(" ",""))
df["Star2"] = df["Star2"].apply(lambda x: x.lower().replace(" ",""))
df["Star3"] = df["Star3"].apply(lambda x: x.lower().replace(" ",""))

df["tag"] = df["Genre"] + " " + df["Director"] + " " + df["Star1"] + " " + df["Star2"] + " " + df["Star3"]

# vectorization
cv = CountVectorizer(max_features=5000, stop_words="english")
vectors = cv.fit_transform(df["tag"]).toarray()

# similarity
similarity = cosine_similarity(vectors)

from difflib import get_close_matches

def recommend(movie):
    movie = movie.lower().strip()
    
    all_titles = df["title_lower"].tolist() 
    close = get_close_matches(movie, all_titles, n=1, cutoff=0.6)
    
    if not close:
        return [], None
    
    matched_title = close[0] 
    index = df[df["title_lower"] == matched_title].index[0]
    
    distances = similarity[index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:10]
    
    return [df.iloc[i[0]]["Series_Title"] for i in movie_list], df.iloc[index]["Series_Title"]


# UI
st.title("🎬 Movie Recommendation System")
movie_name = st.text_input("Enter movie name")

if st.button("Recommend"):
    result, matched = recommend(movie_name)

    if not result:
        st.error("Movie not found 😢")
    else:
        if matched not in st.session_state.search_history:
            st.session_state.search_history.insert(0, matched)  
            st.session_state.search_history = st.session_state.search_history[:5]  

        st.info(f"Showing results for: **{matched}**")
        st.success("Top Recommendations:")

        # 3x3 grid (9 movies)
        rows = [result[i:i+3] for i in range(0, len(result), 3)]

        for row in rows:
            cols = st.columns(3)
            for i, movie in enumerate(row):
                with cols[i]:
                    poster_url = get_poster(movie)
                    if poster_url:
                        st.image(poster_url, use_container_width=True)
                    else:
                        st.markdown(f"""
                        <div style="
                            background-color:#1e1e1e;
                            width:100%;
                            aspect-ratio: 2/3;
                            border-radius:12px;
                            display:flex;
                            flex-direction:column;
                            align-items:center;
                            justify-content:center;
                            font-size:40px;
                            gap:10px;
                        ">
                            🎬
                            <span style="
                                font-size:14px;
                                color:white;
                                font-weight:600;
                                text-align:center;
                                padding:0 10px;
                            ">{movie}</span>
                        </div>
                        """, unsafe_allow_html=True)

with st.sidebar:
    st.header("🕘 Recent Searches")
    if st.session_state.search_history:
        for title in st.session_state.search_history:
            if st.button(f"🎬 {title}", key=title):
                result, matched = recommend(title)
    else:
        st.write("No searches yet!")
