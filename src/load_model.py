import joblib

# Load processed movie data
movies = joblib.load("models/movies.pkl")

# Load TF-IDF vectorizer
tfidf = joblib.load("models/tfidf.pkl")

# Load similarity matrix
similarity = joblib.load("models/similarity.pkl")

print("All model files loaded successfully!")

print("\nMovies Shape:")
print(movies.shape)

print("\nSimilarity Matrix Shape:")
print(similarity.shape)