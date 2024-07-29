#!/bin/bash
set -e

# Initialize the database
python -c "from app import create_app, db; app, _ = create_app(); app.app_context().push(); db.create_all()"

# Run the Flask application
exec python /app/app.py