import streamlit as st
import pandas as pd
import plotly.express as px

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

min_year = int(clean_df["release_year"].min())
max_year = int(clean_df["release_year"].max())

selected_year = st.sidebar.slider("Select Release Year",
                                  min_value = min_year,
                                  max_value = max_year,
                                  value = (min_year,max_year))

st.sidebar.subheader("Ratings")
rating_list = sorted(clean_df["rating"].unique())

selected_ratings = []
for rating in rating_list:
    if st.sidebar.checkbox(rating, value=True):
        selected_ratings.append(rating)

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

if selected_ratings:
    filtered_df = filtered_df[
        filtered_df["rating"].isin(selected_ratings)
    ]
else:
    filtered_df = filtered_df.iloc[0:0]

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

#------------------------------
# Plotting
#------------------------------

st.divider()
st.subheader("Movies vs TV Shows")

type_counts = filtered_df["type"].value_counts().reset_index()
type_counts.columns = ["Content Type", "Count"]

fig = px.bar(type_counts, x = "Content Type", y = "Count",
             color = "Content Type",
             text = "Count",
             title = "Movies vs TV Shows")
fig.update_layout(
    showlegend=False,
    xaxis_title="Content Type",
    yaxis_title="Number of Titles"
)

fig.update_traces(textposition="outside")

st.plotly_chart(
    fig,
    use_container_width=True
)

# -----------------------------
# Dataset Preview
# -----------------------------
st.divider()

st.subheader("Dataset Preview")

st.dataframe(filtered_df, use_container_width=True)