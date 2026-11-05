
import os
import requests

from dotenv import load_dotenv


# ==========================================
# 1. LOAD ENVIRONMENT VARIABLES
# ==========================================

load_dotenv()

OMDB_API_KEY = os.getenv("OMDB_API_KEY")

if not OMDB_API_KEY:
    raise ValueError("OMDB_API_KEY is missing from the .env file")


# ==========================================
# 2. FETCH MOVIE DETAILS FROM OMDb
# ==========================================

def get_movie_details(movie_title: str):

    # OMDb API endpoint
    url = "https://www.omdbapi.com/"

    # Parameters sent to the API
    params = {
        "apikey": OMDB_API_KEY,
        "t": movie_title
    }

    try:
        # Send GET request with a 10-second timeout
        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        # Check HTTP response status
        response.raise_for_status()

        # Convert JSON response into Python dictionary
        data = response.json()

        # Check whether OMDb found the movie
        if data.get("Response") == "False":
            print("OMDb Error:", data.get("Error"))
            return None

        # Return movie details
        return data

    except requests.exceptions.Timeout:
        print("Error: OMDb request timed out.")
        return None

    except requests.exceptions.ConnectionError:
        print("Error: Unable to connect to OMDb.")
        return None

    except requests.exceptions.HTTPError as error:
        print("HTTP Error:", error)
        return None

    except requests.exceptions.RequestException as error:
        print("API request error:", error)
        return None


# ==========================================
# 3. TEST THE FUNCTION
# ==========================================

if __name__ == "__main__":

    movie = get_movie_details("Avatar")

    if movie:
        print("\nMovie:", movie.get("Title"))
        print("Year:", movie.get("Year"))
        print("Genre:", movie.get("Genre"))
        print("Director:", movie.get("Director"))
        print("IMDb Rating:", movie.get("imdbRating"))
        print("Poster:", movie.get("Poster"))
    else:
        print("\nMovie details could not be retrieved.")
