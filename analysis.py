import pandas as pd
import matplotlib.pyplot as plt


def load_data():
    """Load the Netflix dataset."""
    df = pd.read_csv("data/netflix_titles.csv")
    return df


def clean_data(df):
    """Clean missing values."""
    clean_df = df.copy()

    clean_df["director"] = clean_df["director"].fillna("Unknown")
    clean_df["cast"] = clean_df["cast"].fillna("Unknown")
    clean_df["country"] = clean_df["country"].fillna("Unknown")
    clean_df["rating"] = clean_df["rating"].fillna("Not Rated")

    clean_df = clean_df.dropna(subset=["date_added", "duration"])

    return clean_df

def plot_content_type(clean_df):
    type_counts = clean_df["type"].value_counts()

    print(type_counts)

    plt.figure(figsize = (6, 4))
    plt.bar(type_counts.index, type_counts.values)
    plt.title("TV Shows vs Movies on Netflix")
    plt.xlabel("Content type")
    plt.ylabel("Number of titles")
    plt.tight_layout()
    plt.savefig("images/charts/movies_vs_tvshows.png")
    plt.show()

def analyze_release_year(clean_df):
    release_year_counts = (clean_df.groupby("release_year").size().sort_index())
    print("\n Content released by year: ")
    print(release_year_counts.tail(10))

def plot_release_year(clean_df):
    release_year_counts = (clean_df.groupby("release_year").size().sort_index())

    plt.figure(figsize = (10, 5))
    plt.plot(release_year_counts.index, release_year_counts.values, marker = "o", linewidth = 2)

    plt.title("Netflix Content Released By Year")
    plt.xlabel("Release Year")
    plt.ylabel("Number of Titles")

    plt.grid(True)
    plt.tight_layout()
    plt.savefig("images/charts/content_by_release_year.png")

    plt.show()

def analyze_countries(clean_df):

    print("\n First 10 country values: ")
    print(clean_df['country'].head(10))

def transform_countries(clean_df):

    country_df = clean_df.copy()

    country_df["country"] = country_df["country"].str.split(",")
    country_df = country_df.explode("country")
    country_df["country"] = country_df["country"].str.strip()

    return country_df

def plot_top_countries(country_df):

    country_counts = (country_df[country_df["country"] != "Unknown"]
    ["country"].value_counts().head(10))

    print("\n Top 10 countries: ")
    print(country_counts)
    plt.figure(figsize = (10, 6))
    plt.bar(country_counts.index, country_counts.values)
    plt.title("Top 10 Countries Producing Netflix Content")
    plt.xlabel("Country")
    plt.ylabel("Number of Titles")

    plt.xticks(rotation = 45, ha = "right")
    plt.grid(axis = "y", linestyle = "--", alpha = 0.6)

    plt.tight_layout()

    plt.savefig("images/charts/top_10_countries.png")

    plt.show()

def main():
    df = load_data()
    clean_df = clean_data(df)
    plot_content_type(clean_df)

    analyze_release_year(clean_df)
    plot_release_year(clean_df)

    analyze_countries(clean_df)
    country_df = transform_countries(clean_df)
    plot_top_countries(country_df)

if __name__ == "__main__":
    main()