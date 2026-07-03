import pandas as pd
df = pd.read_csv("data/netflix_titles.csv")

print("=" * 50)
print("Netflix Dataset")
print("=" * 50)

print("\n Dataset shape")
print(df.shape)

print("\n First 5 rows: ")
print(df.head(5))

print("\n Column names")
print(df.columns.tolist())