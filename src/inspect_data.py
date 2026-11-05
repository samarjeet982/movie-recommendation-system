import pandas as pd

# Load movie dataset
movies = pd.read_csv("data/tmdb_5000_movies.csv")

# Load credits dataset
credits = pd.read_csv("data/tmdb_5000_credits.csv")

# Display first five rows
print("MOVIES DATASET")
print(movies.head())

print("\nCREDITS DATASET")
print(credits.head())

# Display dataset dimensions
print("\nMovies Shape:", movies.shape)
print("Credits Shape:", credits.shape)

# Display column names
print("\nMovies Columns:")
print(movies.columns.tolist())

print("\nCredits Columns:")
print(credits.columns.tolist())

# 1. Check dataset dimensions
print("\n--- DATASET SHAPES ---")
print("Movies:", movies.shape)
print("Credits:", credits.shape)


# 2. Check missing values
print("\n--- MISSING VALUES IN MOVIES ---")
print(movies.isnull().sum())

print("\n--- MISSING VALUES IN CREDITS ---")
print(credits.isnull().sum())


# 3. Check duplicate records
print("\n--- DUPLICATE RECORDS ---")
print("Movies duplicates:", movies.duplicated().sum())
print("Credits duplicates:", credits.duplicated().sum())


# 4. Check data types
print("\n--- MOVIES DATA TYPES ---")
print(movies.dtypes)

print("\n--- CREDITS DATA TYPES ---")
print(credits.dtypes)


# 5. Display selected movie information
print("\n--- SAMPLE MOVIES ---")
print(movies[["id", "title", "genres", "overview"]].head(5))

# Find movies with missing overviews

missing_overviews = movies[movies["overview"].isnull()]

print("\n--- MOVIES WITH MISSING OVERVIEWS ---")

print(
    missing_overviews[
        ["id", "title", "genres", "overview"]
    ]
)