import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Database configuration: SQLite default for 0-setup; MySQL fully supported
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR}/smart_crop.db")

SECRET_KEY = os.getenv("SECRET_KEY", "smart-crop-advisory-secret-key-2026-secure-jwt-token-alpha")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

UPLOAD_DIR = os.getenv("UPLOAD_DIR", str(BASE_DIR / "uploads"))
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Application metadata
APP_NAME = "Smart Crop Advisory System"
APP_VERSION = "2.0.0"
