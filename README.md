# RegionGuard

RegionGuard is a minimal local-first cybersecurity engagement preparation toolkit built with Python, FastAPI, and Jinja2.

## Setup

1. Open a terminal and change into the project folder:
   ```bash
   cd regionguard
   ```
2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Start the application:
   ```bash
   python run.py
   ```
4. Open your browser at `http://127.0.0.1:8000`

## Architecture overview

- `app/main.py`: FastAPI application startup and router registration
- `app/routes/`: HTML pages, generation endpoint, and health check
- `app/services/`: YAML loading, Jinja2 rendering, jurisdiction summaries, and render payload builder
- `app/library/`: Local YAML data for jurisdictions, cloud providers, and rules of engagement
- `app/templates/`: Jinja2 templates for the web UI and result page
- `generated/`: Output folders for future DOCX/PDF generation

## Features

- Fully runnable local FastAPI backend
- Minimal professional HTML/CSS frontend
- YAML-driven library for jurisdiction, cloud provider, and RoE data
- Deterministic rendering with Jinja2 templates
- No database, no authentication, no cloud dependencies

## Disclaimer

RegionGuard does not provide legal advice.
