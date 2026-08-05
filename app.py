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

# Load Data
df = load_data()
clean_df = clean_data(df)

# Title
st.title("🎬 Netflix Data Dashboard")
st.markdown("Interactive dashboard for exploring Netflix movies and TV shows.")

# Sidebar Filters
st.sidebar.title("🎛 Dashboard Filters")

st.sidebar.divider()
search_title = st.sidebar.text_input("🔍 Search Title",
                                     placeholder = "Search By Title...")

st.sidebar.divider()
content_type = st.sidebar.selectbox(
    "Select Content Type",
    ["All", "Movie", "TV Show"]
)

st.sidebar.divider()
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

st.sidebar.divider()
min_year = int(clean_df["release_year"].min())
max_year = int(clean_df["release_year"].max())

selected_year = st.sidebar.slider("Select Release Year",
                                  min_value = min_year,
                                  max_value = max_year,
                                  value = (min_year,max_year))

st.sidebar.divider()
st.sidebar.subheader("Ratings")
rating_list = sorted(clean_df["rating"].unique())

selected_ratings = []
with st.sidebar.expander("Select Ratings", expanded=False):
    col1, col2 = st.columns(2)

    mid = (len(rating_list) + 1) // 2
    left = rating_list[:mid]
    right = rating_list[mid:]

    with col1:
        for rating in left:
            if st.checkbox(rating, value = True, key = f"left_{rating}"):
                selected_ratings.append(rating)

    with col2:
        for rating in right:
            if st.checkbox(rating, value = True, key = f"right_{rating}"):
                selected_ratings.append(rating)

# Apply Filters
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
            na=False)
    ]

if selected_ratings:
    filtered_df = filtered_df[
        filtered_df["rating"].isin(selected_ratings)
    ]
else:
    filtered_df = filtered_df.iloc[0:0]

if search_title:
    filtered_df = filtered_df[
        filtered_df["title"].str.contains(
            search_title,
            case=False,
            na=False
        )
    ]

# KPI Metrics
total_titles = len(filtered_df)

movies = (filtered_df["type"] == "Movie").sum()
tv_shows = (filtered_df["type"] == "TV Show").sum()

countries = (
    filtered_df["country"]
    .str.split(",")
    .explode()
    .str.strip()
    .nunique())

# KPI Cards
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Titles", f"{total_titles:,}")
col2.metric("Movies", f"{movies:,}")
col3.metric("TV Shows", f"{tv_shows:,}")
col4.metric("Countries", f"{countries:,}")

# Plotting
st.divider()
col1, col2 = st.columns(2)
with col1:
    st.subheader("Content Distribution")

    type_counts = filtered_df["type"].value_counts().reset_index()
    type_counts.columns = ["Content Type", "Count"]

    fig = px.bar(type_counts, x = "Content Type", y = "Count",
                 color = "Content Type",
                 text = "Count",
                 color_discrete_sequence=["#E50914"])
    fig.update_layout(
        showlegend=False,
        xaxis_title="Content Type",
        yaxis_title="Number of Titles"
    )

    fig.update_traces(textposition="outside")

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displayModeBar": False}
    )

with col2:
    st.subheader("Netflix Releases Over Time")
    yearly_titles = filtered_df.groupby('release_year').size().reset_index(name = "Count")
    fig = px.line(
        yearly_titles,
        x="release_year",
        y="Count",
        markers=True
    )

    fig.update_layout(
        xaxis_title="Release Year",
        yaxis_title="Number of Titles"
    )

    fig.update_traces(
        line_color="#E50914",
        marker_color="#E50914"
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )

st.divider()
col3, col4 = st.columns(2)

with col3:
    st.subheader("Top 10 Countries")
    country_df = filtered_df['country'].str.split(",").explode().str.strip()

    country_counts = country_df.value_counts().head(10).reset_index()
    country_counts.columns = ["Country", "Titles"]

    fig = px.bar(country_counts, x = "Titles", y = "Country",
                 orientation = "h",
                 text = "Titles",
                 color_discrete_sequence=["#E50914"])
    fig.update_layout(
        yaxis = dict(categoryorder="total ascending",),
        showlegend=False,
        xaxis_title = "Titles",
        yaxis_title = "")
    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displayModeBar": False}
    )

with col4:
    st.subheader("Top 10 Genres")
    genres_df = filtered_df['listed_in'].str.split(",").explode().str.strip()

    genre_counts = genres_df.value_counts().head(10).reset_index()
    genre_counts.columns = ["Genre", "Titles"]

    fig = px.bar(genre_counts, x="Titles", y="Genre",
                 orientation="h",
                 text="Titles",
                 color_discrete_sequence=["#E50914"])

    fig.update_layout(
        yaxis=dict(categoryorder="total ascending", ),
        showlegend=False,
        xaxis_title="Titles",
        yaxis_title="")
    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displayModeBar": False}
    )

st.divider()
col5, col6 = st.columns(2)

with col5:
    st.subheader("Content Rating Distribution")
    rating_counts = filtered_df['rating'].value_counts().reset_index()

    rating_counts.columns = ["Rating", "Titles"]

    fig = px.bar(rating_counts, x="Titles", y="Rating",
                 orientation="h",
                 text="Titles",
                 color_discrete_sequence=["#E50914"])

    fig.update_layout(
        showlegend=False,
        xaxis_title="Titles",
        yaxis_title=""
    )
    fig.update_traces(textposition="outside")

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displayModeBar": False}
    )

with col6:
    st.subheader("Movie Runtime Distribution")

    movie_df = filtered_df[filtered_df["type"] == "Movie"].copy()

    movie_df['duration'] = (movie_df['duration']
                            .str.replace(" min", "",regex = False)
                            .astype(int))
    fig = px.histogram(movie_df, x="duration", nbins=30, color_discrete_sequence=["#E50914"])

    fig.update_layout(
        xaxis_title="Duration (Minutes)",
        yaxis_title="Number of Movies")

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displayModeBar": False}
    )

st.divider()
if search_title:

    st.divider()

    st.subheader("🔍 Search Results")

    st.caption(f"Found {len(filtered_df)} matching titles")

    st.dataframe(
        filtered_df[
            ["title", "type", "country", "release_year", "rating"]
        ],
        use_container_width=True
    )

st.divider()
st.download_button(
    label = "📥 Download Filtered Dataset (CSV)",
    data = filtered_df.to_csv(index = False),
    file_name = "filtered_netflix_data.csv",
    mime = "text/csv")

# Dataset Preview
st.divider()
st.subheader("📋 Filtered Dataset")

st.caption(
    f"Showing {len(filtered_df):,} titles"
)

st.divider()
st.markdown(
    """
    <center>
        Built with ❤️ using Streamlit, Pandas & Plotly
    </center>
    """,
    unsafe_allow_html=True
)