# Cybersecurity Research Engine

A specialized search engine that indexes and retrieves cybersecurity-related content.

## Features
- Web scraping of cybersecurity resources
- Content indexing and storage
- Advanced search functionality
- Web interface for easy access

## Setup
1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables:
Create a `.env` file with:
```
ELASTICSEARCH_HOST=localhost
ELASTICSEARCH_PORT=9200
```

3. Run the application:
```bash
python app.py
```

## Project Structure
- `app.py`: Main Flask application
- `scraper/`: Web scraping modules
- `indexer/`: Content indexing and storage
- `search/`: Search functionality
- `templates/`: HTML templates
- `static/`: CSS, JavaScript, and other static files
