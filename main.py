
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
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================
# 3. LOAD SAVED MODEL FILES
# ==========================================

movies = joblib.load("models/movies.pkl")
similarity = joblib.load("models/similarity.pkl")


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

    # Find similar movies using recommendation engine
    recommendations = recommend(
        movie_title,
        movies,
        similarity
    )

    # Check whether the searched movie exists
    if recommendations is None:

        raise HTTPException(
            status_code=404,
            detail="Movie not found in our dataset"
        )

    # Store enriched movie information
    enriched_recommendations = []

    # Retrieve additional details for each recommended movie
    for movie in recommendations:

        # Fetch movie details from OMDb
        movie_details = get_movie_details(movie["title"])

        # Extract additional metadata
        if movie_details:

            movie["year"] = movie_details.get("Year")
            movie["genre"] = movie_details.get("Genre")
            movie["poster"] = movie_details.get("Poster")
            movie["imdb_rating"] = movie_details.get("imdbRating")
            movie["director"] = movie_details.get("Director")

        else:

            # Use fallback values if OMDb cannot find the movie
            movie["year"] = None
            movie["genre"] = None
            movie["poster"] = None
            movie["imdb_rating"] = None
            movie["director"] = None

        enriched_recommendations.append(movie)

    # Return final response
    return {
        "movie": movie_title,
        "recommendations": enriched_recommendations
    }
