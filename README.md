# Smart Crop Advisory System for Small and Marginal Farmers

An intelligent, explainable, and localized digital agricultural advisory platform specifically designed to empower small and marginal farmers. The platform unifies soil health metrics, weather data, machine learning vision diagnostics, digital farm records, government policies/subsidies, and verified agronomic solutions into actionable recommendations.

---

## 🌟 Core System Features

1. **🧑‍🌾 Multi-Role Authentication & Access Control**
   - **Farmer Portal**: Intuitive, mobile-first interface with large touch targets, simplified terminology, and voice/audio explanation.
   - **Admin Management Portal**: Data-rich executive dashboard, system analytics, scheme/product CRUD, and a tamper-evident audit logging engine.

2. **🌐 100% Multi-Language Localization**
   - Real-time dynamic toggling between **English**, **Hindi (हिंदी)**, and **Gujarati (ગુજરાતી)** across all forms, cards, and advisories.

3. **🧠 Explainable AI Crop Recommendation Engine**
   - Multi-criteria agronomic decision matrix analyzing Soil Type, pH, NPK nutrients, Temperature, Humidity, Season (Kharif/Rabi/Zaid), and Water Availability.
   - Outputs ranked recommendations with **suitability percentages**, **scientific justifications**, **irrigation strategies**, and **potential risk factors**.

4. **⚡ Action-Oriented Weather Advisory Engine**
   - Integrates live meteorological data from Open-Meteo API.
   - Transforms raw metrics into actionable farming instructions (e.g. *"Postpone irrigation for 24-48h due to 65% rain probability"* or *"High humidity alert: scout lower foliage for Early Blight"*).

5. **🔬 Modular ML Plant Disease Vision Service**
   - Farmers snap or upload photographs of diseased crop leaves/fruits.
   - Computer vision pipeline detects pathologies (Early Blight, Late Blight, Rice Blast, Cotton Leaf Curl, Rust, Mildew, Healthy), reporting confidence percentages, immediate actions, verified organic remedies, and chemical spray guidelines.

6. **📋 Digital Farm Yard Sheet & Yield Tracking**
   - Lifecycle stage progress tracking (*Sowing → Germination → Vegetative → Flowering → Fruiting → Harvesting → Post-Harvest*).
   - Historical yield records and field notes.

7. **🏛️ Government Policies, Subsidies & Schemes Directory**
   - Search and filter national & state schemes (PM-KISAN, PMFBY, Soil Health Card, SMAM Drone Subsidy, PMKSY Drip Subsidy, PM-KUSUM Solar Pumps) with direct links to official portals.

8. **🛡️ Admin Audit Logging Engine**
   - Every administrative modification (creating schemes, altering medicines, changing farmer status) generates a timestamped, tamper-evident audit log capturing old vs new state.

---

## 🚀 Quick Start Guide

### 1. Requirements
- Python 3.10+
- Installed packages: `fastapi`, `uvicorn`, `sqlalchemy`, `pydantic`, `pillow`, `requests`, `httpx`, `bcrypt`, `python-jose`

### 2. Launch the Application
Run the single starter script:
```bash
python run.py
```

### 3. Open in Browser
- **Farmer Portal**: [http://localhost:8000/](http://localhost:8000/)
- **Admin Portal**: [http://localhost:8000/admin](http://localhost:8000/admin)
- **API Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🔑 Demo Credentials

| Role | Email | Password |
| :--- | :--- | :--- |
| **Farmer** | `farmer@kisan.in` | `Farmer@123` |
| **Admin** | `admin@smartcrop.gov.in` | `Admin@123` |

---

## 🗄️ Database Architecture

The system uses a normalized relational architecture compatible with both SQLite (zero-setup out-of-the-box) and MySQL 8.0+:
- `schema.sql` provides the complete MySQL DDL script.
- For MySQL production, set: `DATABASE_URL="mysql+pymysql://user:password@localhost:3306/smart_crop_db"`
"# kishanmitra" 
