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

def main():
    df = load_data()
    clean_df = clean_data(df)
    plot_content_type(clean_df)


if __name__ == "__main__":
    main()