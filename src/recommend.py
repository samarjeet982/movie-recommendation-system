
def recommend(movie_title, movies, similarity):

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

    # Get similarity scores for the selected movie
    distances = similarity[movie_index]

    # Sort movies by similarity score in descending order
    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )

    # Store recommended movies
    recommendations = []

    # Skip the first movie because it is the movie searched by the user
    # Select the next five similar movies
    for movie in movies_list[1:6]:

        # Get the complete movie information
        recommended_movie = movies.iloc[movie[0]]

        # Add movie information to recommendations
        recommendations.append({
            "id": int(recommended_movie["id"]),
            "title": recommended_movie["title"],
            "overview": recommended_movie["overview"],
            "genres": recommended_movie["genres"],
            "similarity_score": round(float(movie[1]), 3)
        })

    # Return the final recommendations
    return recommendations
