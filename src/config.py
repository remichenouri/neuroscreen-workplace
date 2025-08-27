"""Configuration centralisée pour l'application."""

import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"

# Database
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://localhost/ubisoft_analytics")

# ML Models
ADHD_MODEL_PATH = MODELS_DIR / "random_forest.pkl"
PREDICTION_THRESHOLD = 0.5

# Streamlit
APP_TITLE = "Ubisoft People Analytics"
APP_ICON = "🎯"

# API
API_VERSION = "v1"
API_PREFIX = f"/api/{API_VERSION}"
