import pandas as pd

# Load datasets
movies = pd.read_csv("data/tmdb_5000_movies.csv")
credits = pd.read_csv("data/tmdb_5000_credits.csv")

# Handle missing overview values
movies["overview"] = movies["overview"].fillna("")

# Verify missing values
print("Missing overviews after cleaning:")
print(movies["overview"].isnull().sum())

# Verify movie count
print("Movies after cleaning:", movies.shape)