# Log Analyzer

Telaverge assessment 



## Required Features

- Parses DEBUG, INFO, WARN, ERROR, and FATAL log levels.
- Counts errors for each service.
- Identifies the service with the most errors.
- Reports total and unparseable log lines.
- Provides a REST API using FastAPI.
- Includes a CLI for analyzing local log files.
- Handles invalid files and API connection errors.

## Technologies Used

- Python
- FastAPI
- Uvicorn
- Requests
- Pytest

## Installation

Clone the repository and navigate to the project directory.

Create a virtual environment:

    python -m venv venv

Activate it on Windows:

    venv\Scripts\activate

Install dependencies:

    pip install -r requirements.txt

## Running the API

    uvicorn server.main:app --reload

The API will be available at:

    http://127.0.0.1:8000

Interactive API documentation:

    http://127.0.0.1:8000/docs

## Using the CLI

With the API running, open another terminal and execute:

    python client/cli.py sample_logs.txt

## Running Tests

    python -m pytest -v

## Assumptions

- Both ERROR and FATAL are counted as errors.
- Services with zero errors are included in the report.
- If multiple services have the same highest error count,
  the alphabetically first service is selected.
- Invalid log lines are counted as unparseable.

## Project Structure

    analyzer/
        
        parser.py
    server/
        
        main.py
    client/
        cli.py
    tests/
        test_analyzer.py
        test_api.py
    sample_logs.txt
    sample_logs2.txt
    requirements.txt
    README.md
    sample.csv