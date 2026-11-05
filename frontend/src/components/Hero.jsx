
import { useState } from "react";

import {
  ArrowRight,
  Sparkles,
  Search,
  Film,
  AlertCircle,
  LoaderCircle,
  X,
  Star,
  Clapperboard
} from "lucide-react";

import "./Hero.css";

function Hero() {

  // Store movie title
  const [movie, setMovie] = useState("");

  // Store recommendations from FastAPI
  const [recommendations, setRecommendations] = useState([]);

  // Loading state
  const [loading, setLoading] = useState(false);

  // Error state
  const [error, setError] = useState("");

  // Search movie function
  const handleSearch = async () => {

    if (!movie.trim()) {
      setError("Please enter a movie name.");
      setRecommendations([]);
      return;
    }

    try {
      setLoading(true);
      setError("");
      setRecommendations([]);

      // Send request to FastAPI
      const response = await fetch(
        `https://cinematch-api-5r26.onrender.com/recommend//${encodeURIComponent(movie.trim())}`
      );

      // Convert response into JSON
      const data = await response.json();

      // Handle API errors
      if (!response.ok) {
        throw new Error(data.detail || "Something went wrong.");
      }

      // Store recommendations
      setRecommendations(data.recommendations);

    } catch (err) {

      setError(
        err.message === "Failed to fetch"
          ? "Unable to connect to the server. Please try again."
          : err.message
      );

    } finally {
      setLoading(false);
    }
  };

  // Clear search and results
  const clearSearch = () => {
    setMovie("");
    setRecommendations([]);
    setError("");
  };

  return (
    <section className="hero" id="home">

      {/* Background effects */}
      <div className="hero-glow hero-glow-one"></div>
      <div className="hero-glow hero-glow-two"></div>
      <div className="hero-grid"></div>

      <div className="hero-content">

        {/* AI Badge */}
        <div className="hero-badge">
          <Sparkles size={16} />
          <span>AI-POWERED MOVIE DISCOVERY</span>
        </div>

        {/* Main Heading */}
        <h1 className="hero-title">
          Discover Movies
          <br />
          Beyond Your
          <br />
          <span>Imagination.</span>
        </h1>

        {/* Description */}
        <p className="hero-description">
          Stop scrolling. Start discovering.
          Find your next favourite movie with our
          intelligent movie recommendation engine.
        </p>

        {/* Search Container */}
        <div className="hero-search">

          <Search size={21} className="search-icon" />

          <input
            type="text"
            placeholder="Search for a movie... e.g. Avatar"
            value={movie}
            onChange={(e) => {
              setMovie(e.target.value);
              setError("");
            }}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !loading) {
                handleSearch();
              }
            }}
            aria-label="Enter movie title"
          />

          {movie && (
            <button
              className="clear-search-btn"
              onClick={clearSearch}
              aria-label="Clear search"
              type="button"
            >
              <X size={17} />
            </button>
          )}

          <button
            className="hero-search-btn"
            onClick={handleSearch}
            disabled={loading}
            type="button"
          >
            {loading ? (
              <>
                Searching...
                <LoaderCircle size={17} className="loading-icon" />
              </>
            ) : (
              <>
                Explore
                <ArrowRight size={18} />
              </>
            )}
          </button>

        </div>

        {/* Error Message */}
        {error && (
          <div className="search-error">
            <AlertCircle size={17} />
            <span>{error}</span>
          </div>
        )}

        {/* Loading Message */}
        {loading && (
          <p className="loading-message">
            Finding movies you'll love...
          </p>
        )}

        {/* Footer */}
        <div className="hero-footer">
          <Sparkles size={14} />
          <p>Discover movies based on what you love.</p>
        </div>

        {/* Recommendation Results */}
        {recommendations.length > 0 && (
          <div className="recommendation-results">

            <div className="results-heading">

              <div>
                <span className="results-eyebrow">
                  YOUR MOVIE DISCOVERIES
                </span>

                <h2>
                  Because you searched for{" "}
                  <span>{movie}</span>
                </h2>

                <p>
                  Here are some movies you might want to explore.
                </p>
              </div>

              <div className="results-count">
                <Film size={15} />
                {recommendations.length} MOVIES
              </div>

            </div>

            {/* Recommendation Cards */}
            <div className="recommendation-grid">

              {recommendations.map((item, index) => {

                const score = Number(item.similarity_score);

                const percentage = Math.max(
                  0,
                  Math.min(100, score * 100)
                );

                // Get genres from OMDb
                const genres = item.genre
                  ? item.genre.split(",").map((genre) => genre.trim())
                  : [];

                return (
                  <article
                    className="recommendation-card"
                    key={item.id}
                    style={{
                      animationDelay: `${index * 120}ms`
                    }}
                  >

                    {/* Movie Poster */}
                    <div className="movie-poster-container">

                      {item.poster && item.poster !== "N/A" ? (
                        <img
                          src={item.poster}
                          alt={`${item.title} movie poster`}
                          className="movie-poster"
                          loading="lazy"
                          onError={(e) => {
                            e.currentTarget.style.display = "none";
                          }}
                        />
                      ) : (
                        <div className="poster-placeholder">
                          <Film size={40} />
                          <span>Poster unavailable</span>
                        </div>
                      )}

                      <div className="poster-rank">
                        #{String(index + 1).padStart(2, "0")}
                      </div>

                      <div className="poster-overlay">
                        <Clapperboard size={22} />
                        <span>Recommended for you</span>
                      </div>

                    </div>

                    {/* Movie Information */}
                    <div className="movie-card-content">

                      <div className="movie-title-row">
                        <h3>{item.title}</h3>

                        {item.year && (
                          <span className="movie-year">
                            {item.year}
                          </span>
                        )}
                      </div>

                      {/* IMDb Rating */}
                      {item.imdb_rating && item.imdb_rating !== "N/A" && (
                        <div className="movie-rating">
                          <Star size={15} fill="currentColor" />
                          <strong>{item.imdb_rating}/10</strong>
                          <span>IMDb</span>
                        </div>
                      )}

                      {/* Movie Overview */}
                      <p className="movie-overview">
                        {item.overview}
                      </p>

                      {/* Genres */}
                      <div className="movie-genres">
                        {genres.map((genre) => (
                          <span key={genre}>{genre}</span>
                        ))}
                      </div>

                      {/* Director */}
                      {item.director && item.director !== "N/A" && (
                        <div className="movie-director">
                          <span>Director</span>
                          <strong>{item.director}</strong>
                        </div>
                      )}

                      {/* Similarity Score */}
                      <div className="similarity-details">

                        <span>Content similarity</span>

                        <strong>
                          {percentage.toFixed(1)}%
                        </strong>

                      </div>

                      <div className="similarity-track">

                        <div
                          className="similarity-fill"
                          style={{
                            width: `${percentage}%`,
                            animationDelay: `${index * 120 + 300}ms`
                          }}
                        />

                      </div>

                    </div>

                  </article>
                );
              })}

            </div>

            <p className="results-disclaimer">
              Similarity scores measure content similarity.
              They are not predictions of personal enjoyment.
            </p>

          </div>
        )}

      </div>
    </section>
  );
}

export default Hero;
