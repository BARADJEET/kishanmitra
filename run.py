import os
import sys
import uvicorn
from pathlib import Path

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent / "backend"
sys.path.insert(0, str(backend_dir))

from app.database import engine, Base
from app.seed_data import seed_database

def main():
    print("=" * 70)
    print("  🌱 SMART CROP ADVISORY SYSTEM FOR SMALL & MARGINAL FARMERS  🌱")
    print("=" * 70)
    print("Initializing Database & Seed Data...")
    Base.metadata.create_all(bind=engine)
    seed_database()
    print("-" * 70)
    print("  🚀 Farmer Web Application: http://localhost:8000/")
    print("  🛡️ Admin Management Portal: http://localhost:8000/admin")
    print("  📚 OpenAPI Interactive Docs: http://localhost:8000/docs")
    print("-" * 70)
    print("Demo Credentials:")
    print("  🧑‍🌾 Farmer: farmer@kisan.in / Farmer@123")
    print("  🛡️ Admin:  admin@smartcrop.gov.in / Admin@123")
    print("=" * 70)

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=False, app_dir=str(backend_dir))

if __name__ == "__main__":
    main()
