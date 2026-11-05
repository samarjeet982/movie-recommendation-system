
from sklearn.metrics.pairwise import cosine_similarity


def recommend(movie_title, movies, tfidf_matrix):

    # Remove extra spaces from the movie title
    movie_title = movie_title.strip()

    # Find the movie using a case-insensitive comparison
    matched_movies = movies[
        movies["title"].str.casefold() == movie_title.casefold()
    ]

    # Check whether the movie exists
    if matched_movies.empty:
        return None

    # Get the index of the selected movie
    movie_index = matched_movies.index[0]

    # Calculate similarity only for the selected movie
    distances = cosine_similarity(
        tfidf_matrix[movie_index],
        tfidf_matrix
    ).flatten()

    # Sort movies by similarity score in descending order
    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )

    # Store recommended movies
    recommendations = []

    # Skip the searched movie and select the next five
    for movie in movies_list[1:6]:

        recommended_movie = movies.iloc[movie[0]]

        recommendations.append({
            "id": int(recommended_movie["id"]),
            "title": recommended_movie["title"],
            "overview": recommended_movie["overview"],
            "genres": recommended_movie["genres"],
            "similarity_score": round(float(movie[1]), 3)
        })

    return recommendations
