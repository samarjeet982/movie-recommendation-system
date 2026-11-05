import pandas as pd

# Load datasets
movies = pd.read_csv("data/tmdb_5000_movies.csv")
credits = pd.read_csv("data/tmdb_5000_credits.csv")

# Handle missing overviews
movies["overview"] = movies["overview"].fillna("")

# Merge both datasets
merged_data = pd.merge(
    movies,
    credits,
    left_on="id",
    right_on="movie_id",
    how="inner"
)

# Display results
print("Original Movies Shape:", movies.shape)
print("Original Credits Shape:", credits.shape)
print("Merged Dataset Shape:", merged_data.shape)

# Display selected columns
print("\nMerged Dataset Sample:")

print(
    merged_data[
        ["id", "title_x", "genres", "overview", "cast", "crew"]
    ].head()
)

# Display all column names
print("\nMerged Columns:")
print(merged_data.columns.tolist())

# Rename title_x to title
merged_data = merged_data.rename(
    columns={"title_x": "title"}
)

# Remove unnecessary columns
merged_data = merged_data.drop(
    columns=["title_y", "movie_id"]
)
# Check updated columns
print("\nUpdated Columns:")
print(merged_data.columns.tolist())

print("\nUpdated Shape:")
print(merged_data.shape)