import streamlit as st
import pandas as pd

@st.cache_data
def load_data():

    df = pd.read_csv("data/netflix_titles.csv")
    return df

@st.cache_data
def clean_data(df):

    clean_df = df.copy()

    clean_df["director"] = clean_df["director"].fillna("Unknown")
    clean_df["cast"] = clean_df["cast"].fillna("Unknown")
    clean_df["country"] = clean_df["country"].fillna("Unknown")
    clean_df["rating"] = clean_df["rating"].fillna("Not Rated")

    clean_df = clean_df.dropna(subset=["date_added", "duration"])

    return clean_df

st.set_page_config(page_title = "Netflix Data Dashboard",
                   page_icon = "🎬",
                   layout = "wide")


st.title("🎬 Netflix Data Dashboard")
st.markdown("Analyze Netflix movies and TV shows using interactive visualizations.")

df = load_data()
clean_df = clean_data(df)

total_titles = len(clean_df)
movies = len(clean_df[clean_df['type'] == 'Movie'])
tv_shows = len(clean_df[clean_df['type'] == 'TV Show'])
countries = clean_df['country'].dropna().str.split(",").explode().str.strip().nunique()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Titles", total_titles)
with col2:
    st.metric("Movies", movies)
with col3:
    st.metric("TV Shows", tv_shows)
with col4:
    st.metric("Countries", countries)

st.divider()

st.subheader("Dataset Preview")
st.dataframe(df)


st.dataframe(df)
