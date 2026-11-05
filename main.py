
import joblib

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from src.recommend import recommend
from src.movie_service import get_movie_details


# ==========================================
# 1. CREATE FASTAPI APPLICATION
# ==========================================

app = FastAPI(
    title="CineMatch API",
    description="AI-powered Movie Recommendation System",
    version="1.0.0"
)


# ==========================================
# 2. CONFIGURE CORS
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================
# 3. LOAD SAVED MODEL FILES
# ==========================================

movies = joblib.load("models/movies.pkl")

tfidf_matrix = joblib.load(
    "models/tfidf_matrix.pkl"
)


# ==========================================
# 4. HOME API
# ==========================================

@app.get("/")
def home():

    return {
        "message": "Welcome to CineMatch Movie Recommendation System"
    }


# ==========================================
# 5. MOVIE RECOMMENDATION API
# ==========================================

@app.get("/recommend/{movie_title}")
def get_recommendations(movie_title: str):

    recommendations = recommend(
        movie_title,
        movies,
        tfidf_matrix
    )

    if recommendations is None:

        raise HTTPException(
            status_code=404,
            detail="Movie not found in our dataset"
        )

    enriched_recommendations = []

    for movie in recommendations:

        movie_details = get_movie_details(
            movie["title"]
        )

        if movie_details:

            movie["year"] = movie_details.get("Year")
            movie["genre"] = movie_details.get("Genre")
            movie["poster"] = movie_details.get("Poster")
            movie["imdb_rating"] = movie_details.get("imdbRating")
            movie["director"] = movie_details.get("Director")

        else:

            movie["year"] = None
            movie["genre"] = None
            movie["poster"] = None
            movie["imdb_rating"] = None
            movie["director"] = None

        enriched_recommendations.append(movie)

    return {
        "movie": movie_title,
        "recommendations": enriched_recommendations
    }
