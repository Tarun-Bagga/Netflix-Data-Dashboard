import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Netflix Data Dashboard",
    page_icon="🎬",
    layout="wide"
)


@st.cache_data
def load_data():
    return pd.read_csv("data/netflix_titles.csv")


@st.cache_data
def clean_data(df):
    clean_df = df.copy()

    clean_df["director"] = clean_df["director"].fillna("Unknown")
    clean_df["cast"] = clean_df["cast"].fillna("Unknown")
    clean_df["country"] = clean_df["country"].fillna("Unknown")
    clean_df["rating"] = clean_df["rating"].fillna("Not Rated")

    clean_df = clean_df.dropna(subset=["date_added", "duration"])

    return clean_df


# -----------------------------
# Load Data
# -----------------------------
df = load_data()
clean_df = clean_data(df)


# -----------------------------
# Title
# -----------------------------
st.title("🎬 Netflix Data Dashboard")
st.markdown("Analyze Netflix movies and TV shows using interactive visualizations.")


# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("Filters")

content_type = st.sidebar.selectbox(
    "Select Content Type",
    ["All", "Movie", "TV Show"]
)

country_list = (
    clean_df["country"]
    .str.split(",")
    .explode()
    .str.strip()
    .drop_duplicates()
    .sort_values()
    .tolist()
)

country_list.insert(0, "All Countries")

selected_country = st.sidebar.selectbox(
    "Select Country",
    country_list
)


# -----------------------------
# Apply Filters
# -----------------------------
filtered_df = clean_df.copy()

if content_type != "All":
    filtered_df = filtered_df[
        filtered_df["type"] == content_type
    ]

if selected_country != "All Countries":
    filtered_df = filtered_df[
        filtered_df["country"].str.contains(
            selected_country,
            case=False,
            na=False
        )
    ]


# -----------------------------
# KPI Metrics
# -----------------------------
total_titles = len(filtered_df)

movies = (filtered_df["type"] == "Movie").sum()

tv_shows = (filtered_df["type"] == "TV Show").sum()

countries = (
    filtered_df["country"]
    .str.split(",")
    .explode()
    .str.strip()
    .nunique()
)


# -----------------------------
# KPI Cards
# -----------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Titles", total_titles)
col2.metric("Movies", movies)
col3.metric("TV Shows", tv_shows)
col4.metric("Countries", countries)


# -----------------------------
# Dataset Preview
# -----------------------------
st.divider()

st.subheader("Dataset Preview")

st.dataframe(filtered_df, use_container_width=True)