
import { Film, Search, Sparkles } from "lucide-react";
import "./Navbar.css";

function Navbar() {
  return (
    <nav className="navbar">

      {/* Logo */}
      <div className="navbar-logo">
        <div className="logo-icon">
          <Film size={24} />
        </div>

        <span>
          Cine<span className="logo-highlight">Match</span>
        </span>
      </div>

      {/* Navigation links */}
      <div className="navbar-links">
        <a href="#home" className="nav-link active">
          Home
        </a>

        <a href="#discover" className="nav-link">
          Discover
        </a>

        <a href="#how-it-works" className="nav-link">
          How It Works
        </a>
      </div>

      {/* Navigation actions */}
      <div className="navbar-actions">

        <button className="search-icon-btn" aria-label="Search movies">
          <Search size={20} />
        </button>

        <button className="get-started-btn">
          <Sparkles size={17} />
          <span>Get Started</span>
        </button>

      </div>

    </nav>
  );
}

export default Navbar;
