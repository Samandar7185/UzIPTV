# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

UzIPTV is a Flask-based web platform for searching, parsing, and streaming IPTV playlists from various internet sources. It supports M3U/M3U8 playlist formats and provides a web interface for browsing and playing IPTV channels.

## Essential Development Commands

### Environment Setup
```bash
# Create and activate virtual environment
python -m venv venv

# Windows activation
venv\Scripts\activate

# Linux/Mac activation  
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
copy .env.example .env
# Edit .env with your configuration
```

### Running the Application

#### Quick Start (Recommended)
```bash
# Single file startup - handles all setup automatically
python run.py

# Windows users - double click this file
UzIPTV.bat
```

#### Manual Development Server
```bash
# Development server (run from src directory)
cd src
python main.py

# Alternative: run from root directory
python -m src.main

# With specific host/port
cd src
HOST=127.0.0.1 PORT=8000 python main.py
```

#### What run.py does automatically:
- Checks Python version (3.8+)
- Creates virtual environment if needed
- Installs all dependencies from requirements.txt
- Creates .env file from .env.example
- Initializes database
- Starts Flask development server

### Database Operations
```bash
# Initialize database (automatically done on first run)
python -c "from src.main import app; from src.database import init_database; init_database(app)"
```

### Testing and Code Quality
```bash
# Run tests (if test files exist)
pytest tests/

# Code formatting
black src/

# Linting
flake8 src/
```

## Architecture Overview

### Core Components

**Flask Application (`src/main.py`)**
- Main entry point with REST API endpoints
- Routes: `/api/search`, `/api/parse`, `/api/channels`
- Template rendering for web interface
- Database initialization and Flask-SQLAlchemy integration

**IPTV Search Engine (`src/iptv_search.py`)**
- `IPTVSearcher` class handles playlist discovery
- Multi-source search: GitHub repositories, IPTV aggregators, paste sites
- Built-in support for country-specific searches (especially Uzbekistan)
- Rate limiting and respectful API usage patterns

**M3U Parser (`src/iptv_parser.py`)**
- `IPTVParser` class for M3U/M3U8 playlist parsing
- Handles both standard M3U and streaming M3U8 formats
- Extracts channel metadata: names, categories, logos, URLs
- URL resolution for relative paths

**Database Models (`src/database.py`)**
- SQLAlchemy models: `Channel`, `Playlist`, `Favorite`, `SearchHistory`, `ChannelCategory`
- Utility functions for common database operations
- Default category initialization system

### Key Data Flow
1. User searches for IPTV content via web interface
2. `IPTVSearcher` queries multiple sources (GitHub API, aggregators)
3. Found playlists are parsed by `IPTVParser` 
4. Channel data is stored in SQLite database
5. Web interface displays channels with playback capabilities

### Frontend Architecture
- Bootstrap 5 + FontAwesome for responsive UI
- JavaScript (`static/js/app.js`) handles API interactions
- Template-based rendering with Jinja2
- Modal-based playlist browsing workflow

## Development Patterns

### Configuration Management
- Environment variables via `python-dotenv`
- Required vars: `SECRET_KEY`, `DATABASE_URL`, optional `GITHUB_TOKEN`
- Configuration centralized in `src/main.py` app setup

### Error Handling
- All API endpoints return structured JSON responses
- Database operations wrapped in try-catch with rollback
- Network requests include timeout and retry logic

### Search Strategy
The application uses a multi-tier search approach:
1. GitHub Code Search API for M3U files
2. IPTV-ORG curated playlists for reliable content
3. Extensible system for additional aggregator sources

### Database Design
- Session-based user identification (no user accounts)
- Channel categorization with emoji icons and color coding
- Soft deletion pattern (`is_active` flags)
- Timestamp tracking for all entities

## Project-Specific Notes

### API Rate Limiting
GitHub API calls include delays (`time.sleep(random.uniform(1, 2))`) to respect rate limits. Consider implementing proper rate limiting for production use.

### URL Validation
All playlist and stream URLs are validated using the `validators` library before database storage.

### Uzbekistan Focus  
The application has built-in optimization for Uzbek content:
- Special handling for 'uzbek'/'uz' search queries
- Direct integration with IPTV-ORG Uzbekistan playlist
- UI includes Uzbek language strings alongside English

### Static File Organization
```
static/
├── css/style.css    # Custom styling
└── js/app.js        # Frontend JavaScript
```

### Template Structure
```
templates/
└── index.html       # Main application interface
```

## Environment Variables Reference

```bash
# Flask Configuration
SECRET_KEY=your-secret-key
DEBUG=True
HOST=0.0.0.0
PORT=5000

# Database
DATABASE_URL=sqlite:///uziptv.db

# GitHub API (optional, for enhanced search)
GITHUB_TOKEN=your-github-token

# Search Configuration  
MAX_SEARCH_RESULTS=50
SEARCH_TIMEOUT=30

# Caching
CACHE_TIMEOUT=3600
ENABLE_CACHE=True

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/uziptv.log

# Security
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```
