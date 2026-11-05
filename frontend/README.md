# CineMatch – Movie Recommendation System

CineMatch is a movie recommendation project built using Python and React.

The idea behind this project is simple: instead of spending time searching for what to watch next, a user can enter a movie name and get five similar movie recommendations.

I built the recommendation system using movie information such as genres, keywords, cast, director, and overview. It uses TF-IDF and cosine similarity to find movies with similar content.

## What it does

- Takes a movie name as input.
- Finds the movie in the dataset.
- Compares it with other movies.
- Returns the five most similar movies.
- Displays movie posters and additional details such as release year, genre, director, and IMDb rating.

## Technologies Used

**Backend and Machine Learning**
- Python
- Pandas and NumPy
- Scikit-learn
- FastAPI
- Joblib

**Frontend**
- React
- Vite
- JavaScript
- CSS
- Lucide React

**External API**
- OMDb API – used to retrieve movie details and posters.

## How the Recommendation System Works

I used the TMDB 5000 Movie Dataset for this project. It contains information about movies, including their genres, keywords, cast, and other details.

First, I combined useful movie information into one column called `tags`.

Then I used `TfidfVectorizer` from Scikit-learn to convert the text into numerical vectors.

After that, I calculated cosine similarity between the movie vectors. When someone searches for a movie, the system finds its similarity scores and returns the top five matching movies.

This is a content-based recommendation system. It recommends movies based on their content rather than user ratings or viewing history.

## Project Structure

```text
movie-recommendation-system/
│
├── data/                  # Movie datasets
│
├── models/                # Saved ML model files
│
├── src/
│   ├── inspect_data.py
│   ├── clean_data.py
│   ├── merge_data.py
│   ├── preprocess_data.py
│   ├── recommend.py
│   ├── load_model.py
│   └── movie_service.py
│
├── frontend/
│   └── src/
│       ├── components/
│       │   ├── Navbar.jsx
│       │   ├── Navbar.css
│       │   ├── Hero.jsx
│       │   └── Hero.css
│       ├── App.jsx
│       ├── App.css
│       └── index.css
│
├── main.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

## Running the Project Locally

### 1. Clone the repository

```bash
git clone https://github.com/samarjeet982/movie-recommendation-system.git

cd movie-recommendation-system
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
```

For Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Download the dataset

Download the TMDB 5000 Movie Dataset from Kaggle:

https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata

Place these two files inside the `data` folder:

- `tmdb_5000_movies.csv`
- `tmdb_5000_credits.csv`

### 5. Add your OMDb API key

Create a `.env` file in the main project directory:

```env
OMDB_API_KEY=your_api_key
```

You can get an API key from https://www.omdbapi.com/apikey.aspx.

Do not upload your `.env` file to GitHub.

### 6. Generate the recommendation data

```bash
python src/preprocess_data.py
```

This creates the saved files required by the recommendation system inside the `models` folder.

### 7. Run the backend

```bash
uvicorn main:app --reload
```

The backend will be available at:

http://127.0.0.1:8000

API documentation:

http://127.0.0.1:8000/docs

### 8. Run the frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the application at:

http://localhost:5173

## API Endpoint

**Get movie recommendations**

```http
GET /recommend/{movie_title}
```

Example:

```http
GET /recommend/Avatar
```

The API returns five recommended movies along with the available movie information.

## What I Learned

While building CineMatch, I worked with:

- Cleaning and combining datasets using Pandas.
- Extracting useful information from movie metadata.
- Text preprocessing and feature engineering.
- TF-IDF vectorization.
- Cosine similarity.
- Saving and loading ML objects using Joblib.
- Creating REST APIs using FastAPI.
- Connecting a React frontend with a Python backend.
- Working with an external API using Python.

## Current Status

The basic recommendation system, FastAPI backend, and React frontend are implemented and connected.

I plan to improve the recommendation logic and add more features as I continue working on the project.

## Author

**Samarjeet Singh**

GitHub: [samarjeet982](https://github.com/samarjeet982)

---

This project was built as a hands-on way to learn Python, machine learning, and full-stack development.