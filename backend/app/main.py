import os
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse

from .config import APP_NAME, APP_VERSION, UPLOAD_DIR, BASE_DIR
from .database import engine, Base
from .seed_data import seed_database
from .routers import (
    auth_router,
    farms_router,
    yard_sheets_router,
    recommendations_router,
    weather_router,
    disease_diagnosis_router,
    catalog_router,
    policies_router,
    notifications_router,
    admin_router,
    analytics_router,
)

# Initialize FastAPI application
app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="Smart Crop Advisory System for Small and Marginal Farmers - REST API & Intelligent Agriculture Engine"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables & seed initial data on startup
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    seed_database()

# Register API Routers
app.include_router(auth_router)
app.include_router(farms_router)
app.include_router(yard_sheets_router)
app.include_router(recommendations_router)
app.include_router(weather_router)
app.include_router(disease_diagnosis_router)
app.include_router(catalog_router)
app.include_router(policies_router)
app.include_router(notifications_router)
app.include_router(admin_router)
app.include_router(analytics_router)

# Mount Uploads directory
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# Mount Frontend static files
FRONTEND_DIR = BASE_DIR.parent / "frontend"
if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")

    @app.get("/", response_class=FileResponse)
    async def serve_farmer_app():
        return FileResponse(str(FRONTEND_DIR / "index.html"))

    @app.get("/admin", response_class=FileResponse)
    async def serve_admin_app():
        return FileResponse(str(FRONTEND_DIR / "admin.html"))

@app.get("/api/health")
def health_check():
    return {"status": "online", "app": APP_NAME, "version": APP_VERSION}
