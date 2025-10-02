# Kluster (Prototype)

Kluster is a Flask 3.0 web app to help collectors track their collections, estimate value over time, search for users/items, and message other collectors. This prototype implements four main screens: login, profile, collection, and search.

## Prerequisites

- Python 3.11+
- pip
- SQLite (default) or PostgreSQL (set SQLALCHEMY_DATABASE_URI)

## Setup

### Run this command:
source .venv/Scripts/activate
python -m flask --app wsgi:app run --debug
