
import joblib
import pandas as pd
import json
import os

from sklearn.feature_extraction.text import TfidfVectorizer


# ==========================================
# 1. LOAD DATASETS
# ==========================================

movies = pd.read_csv("data/tmdb_5000_movies.csv")
credits = pd.read_csv("data/tmdb_5000_credits.csv")

print("Datasets loaded successfully!")


# ==========================================
# 2. HANDLE MISSING VALUES
# ==========================================

movies["overview"] = movies["overview"].fillna("")


# ==========================================
# 3. MERGE DATASETS
# ==========================================

movies = pd.merge(
    movies,
    credits,
    left_on="id",
    right_on="movie_id",
    how="inner"
)

movies = movies.rename(
    columns={"title_x": "title"}
)

movies = movies.drop(
    columns=["title_y", "movie_id"]
)

print("Datasets merged successfully!")
print("Merged dataset shape:", movies.shape)


# ==========================================
# 4. EXTRACT GENRES
# ==========================================

def extract_genres(genre_data):

    genres_list = json.loads(genre_data)

    genre_names = []

    for genre in genres_list:
        genre_names.append(genre["name"])

    return genre_names


movies["genres"] = movies["genres"].apply(extract_genres)


# ==========================================
# 5. EXTRACT KEYWORDS
# ==========================================

def extract_keywords(keyword_data):

    keywords_list = json.loads(keyword_data)

    keyword_names = []

    for keyword in keywords_list:
        keyword_names.append(keyword["name"])

    return keyword_names


movies["keywords"] = movies["keywords"].apply(extract_keywords)


# ==========================================
# 6. EXTRACT TOP THREE CAST MEMBERS
# ==========================================

def extract_cast(cast_data):

    cast_list = json.loads(cast_data)

    cast_names = []

    for actor in cast_list[:3]:
        cast_names.append(actor["name"])

    return cast_names


movies["cast"] = movies["cast"].apply(extract_cast)


# ==========================================
# 7. EXTRACT DIRECTOR
# ==========================================

def extract_director(crew_data):

    crew_list = json.loads(crew_data)

    for person in crew_list:

        if person["job"] == "Director":
            return person["name"]

    return ""


movies["director"] = movies["crew"].apply(extract_director)


# ==========================================
# 8. SELECT REQUIRED COLUMNS
# ==========================================

movies = movies[
    [
        "id",
        "title",
        "overview",
        "genres",
        "keywords",
        "cast",
        "director"
    ]
]

print("\nSelected movie features:")
print(movies.head())


# ==========================================
# 9. CONVERT LISTS INTO STRINGS
# ==========================================

movies["genres"] = movies["genres"].apply(
    lambda x: " ".join(x)
)

movies["keywords"] = movies["keywords"].apply(
    lambda x: " ".join(x)
)

movies["cast"] = movies["cast"].apply(
    lambda x: " ".join(x)
)


# ==========================================
# 10. CONVERT TEXT INTO LOWERCASE
# ==========================================

movies["director"] = movies["director"].apply(
    lambda x: x.lower()
)

movies["overview"] = movies["overview"].apply(
    lambda x: x.lower()
)


# ==========================================
# 11. CREATE COMBINED TAGS
# ==========================================

movies["tags"] = (
    movies["overview"] + " " +
    movies["genres"] + " " +
    movies["keywords"] + " " +
    movies["cast"] + " " +
    movies["director"]
)

print("\nMovie tags created successfully!")


# ==========================================
# 12. TF-IDF VECTORIZATION
# ==========================================

tfidf = TfidfVectorizer()

tfidf_matrix = tfidf.fit_transform(
    movies["tags"]
)

print("\nTF-IDF Matrix Shape:")
print(tfidf_matrix.shape)

print("\nTotal Features:")
print(len(tfidf.get_feature_names_out()))

print("\nNumber of Non-zero Values:")
print(tfidf_matrix.nnz)


# ==========================================
# 13. CREATE MODELS DIRECTORY
# ==========================================

os.makedirs("models", exist_ok=True)


# ==========================================
# 14. SAVE MODEL FILES
# ==========================================

# Save processed movie data
joblib.dump(
    movies,
    "models/movies.pkl"
)

# Save TF-IDF vectorizer
joblib.dump(
    tfidf,
    "models/tfidf.pkl"
)

# Save sparse TF-IDF matrix
joblib.dump(
    tfidf_matrix,
    "models/tfidf_matrix.pkl"
)


print("\n====================================")
print("MODEL FILES SAVED SUCCESSFULLY!")
print("====================================")

print("\nSaved Files:")
print("- models/movies.pkl")
print("- models/tfidf.pkl")
print("- models/tfidf_matrix.pkl")

print("\nPreprocessing completed successfully!")
