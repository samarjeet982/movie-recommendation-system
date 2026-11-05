import joblib
import pandas as pd
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from recommend import recommend

# Load datasets
movies = pd.read_csv("data/tmdb_5000_movies.csv")
credits = pd.read_csv("data/tmdb_5000_credits.csv")

# Handle missing overviews
movies["overview"] = movies["overview"].fillna("")

# Merge datasets
movies = pd.merge(
    movies,
    credits,
    left_on="id",
    right_on="movie_id",
    how="inner"
)

# Rename and remove unnecessary columns
movies = movies.rename(columns={"title_x": "title"})

movies = movies.drop(
    columns=["title_y", "movie_id"]
)

# Display original genres data
print("Original genres value:")
print(movies["genres"][0])

# Convert JSON string into Python object
genres = json.loads(movies["genres"][0])

print("\nConverted genres:")
print(genres)

print("\nData type after conversion:")
print(type(genres))


# Function to extract genre names

def extract_genres(genre_data):

    genres_list = json.loads(genre_data)

    genre_names = []

    for genre in genres_list:
        genre_names.append(genre["name"])

    return genre_names


# Apply function to all movies

movies["genres"] = movies["genres"].apply(extract_genres)


# Display results

print("\nExtracted Genres:")

print(movies[["title", "genres"]].head(10))

print("\nOriginal Keywords:")
print(movies["keywords"][0])

# Function to extract keyword names

def extract_keywords(keyword_data):

    keywords_list = json.loads(keyword_data)

    keyword_names = []

    for keyword in keywords_list:
        keyword_names.append(keyword["name"])

    return keyword_names


# Apply function to all movies

movies["keywords"] = movies["keywords"].apply(extract_keywords)


# Display extracted keywords

print("\nExtracted Keywords:")

print(movies[["title", "keywords"]].head(10))

print("\nOriginal Cast:")
print(movies["cast"][0])

# Function to extract top three actors

def extract_cast(cast_data):

    cast_list = json.loads(cast_data)

    cast_names = []

    for actor in cast_list[:3]:
        cast_names.append(actor["name"])

    return cast_names


# Apply function to all movies

movies["cast"] = movies["cast"].apply(extract_cast)


# Display results

print("\nExtracted Cast:")

print(movies[["title", "cast"]].head(10))

# Function to extract director name

def extract_director(crew_data):

    crew_list = json.loads(crew_data)

    for person in crew_list:

        if person["job"] == "Director":

            return person["name"]

    return ""


# Apply function to all movies

movies["director"] = movies["crew"].apply(extract_director)


# Display extracted directors

print("\nExtracted Directors:")

print(movies[["title", "director"]].head(10))

# Select important columns for recommendation

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

print("\nSelected Movie Features:")

print(movies.head(5))

print("\nSelected Dataset Shape:")

print(movies.shape)

# Convert list values into strings

movies["genres"] = movies["genres"].apply(
    lambda x: " ".join(x)
)

movies["keywords"] = movies["keywords"].apply(
    lambda x: " ".join(x)
)

movies["cast"] = movies["cast"].apply(
    lambda x: " ".join(x)
)

# Convert director and overview to lowercase

movies["director"] = movies["director"].apply(
    lambda x: x.lower()
)

movies["overview"] = movies["overview"].apply(
    lambda x: x.lower()
)

# Display updated data

print("\nUpdated Movie Features:")

print(
    movies[
        ["title", "genres", "keywords", "cast", "director"]
    ].head(5)
)

# Combine all text features into one column

movies["tags"] = (
    movies["overview"] + " " +
    movies["genres"] + " " +
    movies["keywords"] + " " +
    movies["cast"] + " " +
    movies["director"]
)

# Display the combined features

print("\nMovie Tags:")
print(movies[["title", "tags"]].head(5))



# Create TF-IDF vectorizer
tfidf = TfidfVectorizer()

# Convert movie tags into numerical vectors
tfidf_matrix = tfidf.fit_transform(movies["tags"])

# Display matrix information
print("\nTF-IDF Matrix Shape:")
print(tfidf_matrix.shape)

print("\nTotal Features (Unique Words):")
print(len(tfidf.get_feature_names_out()))

# Get all unique words
feature_names = tfidf.get_feature_names_out()

# Get TF-IDF vector for the first movie
first_movie_vector = tfidf_matrix[0]

print("\nTF-IDF Scores for Avatar:")

for index, score in zip(
    first_movie_vector.indices,
    first_movie_vector.data
):
    print(feature_names[index], round(score, 3))



# Calculate similarity between all movies
similarity = cosine_similarity(tfidf_matrix)

# Save processed movie data
joblib.dump(movies, "models/movies.pkl")

# Save TF-IDF vectorizer
joblib.dump(tfidf, "models/tfidf.pkl")

# Save similarity matrix
joblib.dump(similarity, "models/similarity.pkl")

print("\nModel files saved successfully!")

# Display similarity matrix shape
print("\nSimilarity Matrix Shape:")
print(similarity.shape)





# Test imported recommendation function

recommend("Avatar", movies, similarity)

recommend("Titanic", movies, similarity)

recommend("Avatr", movies, similarity)