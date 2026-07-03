import pandas as pd
df = pd.read_csv("data/netflix_titles.csv")

"""print("=" * 50)
print("Netflix Dataset")
print("=" * 50)

print("\n Dataset shape: ")
print(df.shape)

print("\n First 5 rows: ")
print(df.head(5))

print("\n Column names: ")
print(df.columns.tolist())

print("\n Dataset Information: ")
print(df.info())

print("\n Missing values: ")
print(df.isnull().sum())

print("\n Duplicate rows: ")
print(df.duplicated().sum())"""

# Create a copy for cleaning
clean_df = df.copy()

clean_df['director'] = clean_df['director'].fillna("Unknown")
clean_df['cast'] = clean_df['cast'].fillna("Unknown")
clean_df['country'] = clean_df['country'].fillna("Unknown")
clean_df['rating'] = clean_df['rating'].fillna("Not rated")

clean_df = clean_df.dropna(subset=['date_added', 'duration'])

print("\n Missing values after CleanUp: ")
print(clean_df.isnull().sum())