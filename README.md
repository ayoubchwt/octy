# Octy

> [!NOTE]
> Work in Progress: This project is actively under development. Features, data structures, and APIs are subject to change.

Octy is a Django-based job aggregation platform designed to collect, parse, and structure job postings across multiple sources using automated scrapers and AI-assisted processing.

---

## Features (In Development)

- **Job Aggregation**: Collects job listings with metadata (title, company, salary ranges, location, required skills).
- **Automated Scraping**: Infrastructure for extracting listings across multiple job portals.
- **AI Processing**: Google AI integration for parsing and structuring unstructured job details.
- **Data Export & Storage**: Structured persistence with Django ORM.

---

## Project Status & Roadmap

### Completed
- [x] Scraper sources implemented:
  - [x] Arbeitnow (`fetchArbeitJobs`)
  - [x] Nomado (`fetchNomadoJobs`)
  - [x] NoFluffJobs (`fetchNofluffjobs`)
- [x] Scraper pipeline orchestration (`run_scrapers.py`) with async execution
- [x] Data cleaning and normalization pipeline (`job_clean_normalize` with Pandas)
- [x] Google AI (Gemini) description cleaning integration
- [x] Core Django models (`Job`) and initial DB schema structure

### Todo
- [ ] Connect cleaned scraper output directly to database ingestion service (`JobService`)
- [ ] Add scheduled scraping tasks (e.g., Celery / background worker or cron)
- [ ] Implement REST API endpoints / views for querying and filtering jobs
- [ ] Build search, filtering, and pagination on the frontend/API
- [ ] Add unit and integration tests for scrapers, cleaners, and models
- [ ] Error alerting and scraper health monitoring

---

## Quickstart

### Prerequisites
- Python 3.10+
- Virtual environment (`venv`)

### Setup

1. **Clone the repository and navigate to the project directory:**
   ```bash
   cd octy
   ```

2. **Activate the virtual environment:**
   - **Windows:**
     ```powershell
     .venv\Scripts\activate
     ```
   - **Linux / macOS:**
     ```bash
     source .venv/bin/activate
     ```

3. **Configure environment variables:**
   Copy `.env.example` (or set up `.env` with required API keys and database settings).

4. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Start the development server:**
   ```bash
   python manage.py runserver
   ```
