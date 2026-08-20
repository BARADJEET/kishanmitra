from datetime import datetime, date, timedelta
from sqlalchemy.orm import Session
from .database import engine, Base, SessionLocal
from .models.user import User, UserProfile
from .models.farm import Farm, SoilRecord
from .models.yard_sheet import YardSheet
from .models.disease import DiseasePest, DiseaseSolution, Product, MLPrediction
from .models.policy import GovernmentPolicy
from .models.notification import Notification
from .models.audit import AdminAuditLog
from .services.auth_service import hash_password

def seed_database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # Check if already seeded
        if db.query(User).filter(User.email == "admin@smartcrop.gov.in").first():
            print("Database already seeded. Skipping.")
            return

        print("Seeding Smart Crop Advisory System database...")

        # 1. Create Admin User
        admin_user = User(
            email="admin@smartcrop.gov.in",
            phone="9876543210",
            hashed_password=hash_password("Admin@123"),
            role="admin",
            is_active=True
        )
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)

        admin_profile = UserProfile(
            user_id=admin_user.id,
            full_name="Dr. Rajesh Patel (Chief Agronomist)",
            language_pref="en",
            state="Gujarat",
            district="Gandhinagar",
            village="Krishi Bhavan"
        )
        db.add(admin_profile)

        # 2. Create Demo Farmer User
        farmer_user = User(
            email="farmer@kisan.in",
            phone="9123456780",
            hashed_password=hash_password("Farmer@123"),
            role="farmer",
            is_active=True
        )
        db.add(farmer_user)
        db.commit()
        db.refresh(farmer_user)

        farmer_profile = UserProfile(
            user_id=farmer_user.id,
            full_name="Ramesh Bhai Patel (રમેશભાઈ પટેલ)",
            language_pref="gu",
            state="Gujarat",
            district="Ahmedabad",
            village="Sanand"
        )
        db.add(farmer_profile)

        # 3. Create Farms for Demo Farmer
        farm1 = Farm(
            farmer_id=farmer_user.id,
            farm_name="Sanand Green Acres (સાનંદ ગ્રીન એકર્સ)",
            land_area_acres=3.5,
            state="Gujarat",
            district="Ahmedabad",
            village="Sanand",
            latitude=22.9856,
            longitude=72.3812,
            soil_type="Black Soil",
            irrigation_type="Drip",
            water_availability="Moderate"
        )
        db.add(farm1)

        farm2 = Farm(
            farmer_id=farmer_user.id,
            farm_name="Narmada Canal Plot (નર્મદા નહેર પ્લોટ)",
            land_area_acres=2.0,
            state="Gujarat",
            district="Vadodara",
            village="Karjan",
            latitude=22.0467,
            longitude=73.1234,
            soil_type="Alluvial Soil",
            irrigation_type="Canal",
            water_availability="Abundant"
        )
        db.add(farm2)
        db.commit()
        db.refresh(farm1)
        db.refresh(farm2)

        # 4. Soil Records
        soil1 = SoilRecord(
            farm_id=farm1.id,
            nitrogen_n=85.0,
            phosphorus_p=42.0,
            potassium_k=65.0,
            soil_ph=7.2,
            organic_carbon=0.75,
            test_date=datetime.utcnow() - timedelta(days=20),
            notes="Healthy organic matter. Moderate nitrogen reserve."
        )
        soil2 = SoilRecord(
            farm_id=farm2.id,
            nitrogen_n=110.0,
            phosphorus_p=55.0,
            potassium_k=48.0,
            soil_ph=6.8,
            organic_carbon=0.82,
            test_date=datetime.utcnow() - timedelta(days=15),
            notes="High alluvial fertility, ideal for cereal or vegetable crop."
        )
        db.add_all([soil1, soil2])

        # 5. Yard Sheets
        yard1 = YardSheet(
            farm_id=farm1.id,
            crop_name="Cotton (કપાસ)",
            crop_variety="Bt RCH-659",
            sowing_date=date.today() - timedelta(days=60),
            cultivated_area_acres=2.5,
            crop_stage="Flowering",
            expected_yield_kg=2200.0,
            season="Kharif",
            notes="Flowering stage initiated. Monitored for bollworm; drip fertigation 19-19-19 applied."
        )
        yard2 = YardSheet(
            farm_id=farm1.id,
            crop_name="Groundnut (મગફળી)",
            crop_variety="GG-20",
            sowing_date=date.today() - timedelta(days=75),
            cultivated_area_acres=1.0,
            crop_stage="Fruiting",
            expected_yield_kg=1100.0,
            season="Kharif",
            notes="Pegging and pod formation underway. Applied Gypsum 400kg/ha."
        )
        yard3 = YardSheet(
            farm_id=farm2.id,
            crop_name="Wheat (ઘઉં)",
            crop_variety="GW-496",
            sowing_date=date.today() - timedelta(days=150),
            cultivated_area_acres=2.0,
            crop_stage="Post-Harvest",
            expected_yield_kg=3800.0,
            actual_yield_kg=4050.0,
            season="Rabi",
            notes="Harvest completed successfully. High grain quality achieved."
        )
        db.add_all([yard1, yard2, yard3])

        # 6. Government Policies & Schemes
        policies = [
            GovernmentPolicy(
                title="PM-KISAN (Pradhan Mantri Kisan Samman Nidhi)",
                scheme_name="PM-KISAN",
                description="Direct financial income support of Rs. 6,000 per year in three equal installments of Rs. 2,000 directly into farmer bank accounts.",
                eligibility_criteria="All landholding small and marginal farmer families with cultivable land holdings.",
                applicable_state="All India",
                applicable_crops="All Crops",
                benefits="Rs. 6,000 annually via Direct Benefit Transfer (DBT).",
                valid_until="Ongoing",
                official_portal_url="https://pmkisan.gov.in/",
                category="Financial Aid"
            ),
            GovernmentPolicy(
                title="PM Fasal Bima Yojana (Crop Insurance Scheme)",
                scheme_name="PMFBY",
                description="Comprehensive risk insurance cover against crop loss caused by natural calamities, unseasonal rainfall, pests and diseases.",
                eligibility_criteria="All farmers growing notified crops in notified areas including sharecroppers and tenant farmers.",
                applicable_state="All India",
                applicable_crops="Food crops, Oilseeds, Annual Commercial/Horticultural crops",
                benefits="Maximum premium payable by farmer: 2% for Kharif, 1.5% for Rabi, 5% for Horticultural crops.",
                valid_until="Ongoing",
                official_portal_url="https://pmfby.gov.in/",
                category="Insurance"
            ),
            GovernmentPolicy(
                title="Sub-Mission on Agricultural Mechanization (SMAM - Tractor & Drone Subsidy)",
                scheme_name="SMAM",
                description="Financial assistance and subsidy ranging from 40% to 50% for purchasing tractors, power tillers, rotavators and agricultural drones.",
                eligibility_criteria="Small, marginal, SC/ST, women farmers with verified land records.",
                applicable_state="All India",
                applicable_crops="All Crops",
                benefits="40% to 50% capital subsidy on farm machinery up to Rs. 5 Lakhs.",
                valid_until="2026-2027",
                official_portal_url="https://agrimachinery.nic.in/",
                category="Equipment"
            ),
            GovernmentPolicy(
                title="Soil Health Card Scheme (SHC)",
                scheme_name="Soil Health Card",
                description="Free soil testing issued every 2 years containing nutrient status (12 parameters: N, P, K, S, Zn, Fe, Cu, Mn, Bo, pH, EC, OC).",
                eligibility_criteria="All farmers across all districts.",
                applicable_state="All India",
                applicable_crops="All Crops",
                benefits="Free computerized soil health report + personalized fertilizer dosage recommendation.",
                valid_until="Ongoing",
                official_portal_url="https://soilhealth.dac.gov.in/",
                category="Soil Health"
            ),
            GovernmentPolicy(
                title="Pradhan Mantri Krishi Sinchayee Yojana (Per Drop More Crop - Drip & Sprinkler)",
                scheme_name="PMKSY - Micro Irrigation",
                description="Subsidy up to 70% for small & marginal farmers to install precision drip and micro-sprinkler systems.",
                eligibility_criteria="Farmers having assured water source for micro-irrigation installation.",
                applicable_state="Gujarat, Maharashtra, Rajasthan, MP, UP",
                applicable_crops="Cotton, Sugarcane, Banana, Vegetables, Orchard crops",
                benefits="55% to 70% direct government subsidy on certified micro-irrigation equipment.",
                valid_until="Ongoing",
                official_portal_url="https://pmksy.gov.in/",
                category="Subsidy"
            ),
            GovernmentPolicy(
                title="PM-KUSUM Solar Agriculture Pump Scheme",
                scheme_name="PM-KUSUM",
                description="Solar powered water pumps with 60% subsidy for off-grid and grid-connected farm tube wells.",
                eligibility_criteria="Individual farmers, water user associations, FPOs.",
                applicable_state="All India",
                applicable_crops="All Crops",
                benefits="Up to 60% subsidy (30% Central + 30% State Govt) on standalone solar pumps.",
                valid_until="2026-12-31",
                official_portal_url="https://pmkusum.mnre.gov.in/",
                category="Subsidy"
            ),
            GovernmentPolicy(
                title="Paramparagat Krishi Vikas Yojana (PKVY Organic Farming)",
                scheme_name="PKVY",
                description="Financial support of Rs. 50,000 per hectare for 3 years to adopt chemical-free natural/organic farming.",
                eligibility_criteria="Farmers forming clusters of 20 or more farmers over 50 acres.",
                applicable_state="All India",
                applicable_crops="Pulses, Spices, Cereals, Fruits",
                benefits="Rs. 31,000/ha for organic inputs + free PGS-India organic certification.",
                valid_until="Ongoing",
                official_portal_url="https://pgsindia-ncof.gov.in/",
                category="Organic"
            )
        ]
        db.add_all(policies)

        # 7. Diseases, Solutions & Verified Products
        d1 = DiseasePest(
            name="Early Blight (Alternaria solani)",
            scientific_name="Alternaria solani",
            target_crops="Tomato, Potato, Eggplant",
            symptoms="Dark brown spots with concentric target-rings on older leaves; yellow halos and defoliation.",
            description="Fungal pathogen surviving in crop residue and soil splash during warm, humid conditions.",
            prevention_methods="Avoid overhead irrigation; practice 3-year crop rotation; use disease-free seeds; mulch soil.",
            severity_level="High"
        )
        db.add(d1)
        db.commit()
        db.refresh(d1)

        sol1 = DiseaseSolution(
            disease_id=d1.id,
            crop_name="Tomato",
            recommended_action="Prune lower 12 inches of infected leaves. Apply protective bio-fungicide or contact fungicide.",
            organic_treatment="Trichoderma viride @ 10g/liter or Neem Oil (Azadirachtin 3000 ppm) @ 5ml/liter.",
            chemical_treatment="Mancozeb 75% WP @ 2.5g/liter or Azoxystrobin 23% SC @ 1ml/liter water.",
            safety_notes="Observe 7-day pre-harvest interval (PHI) after chemical spray."
        )
        db.add(sol1)
        db.commit()
        db.refresh(sol1)

        p1 = Product(
            solution_id=sol1.id,
            name="Mancozeb 75% WP (Indofil M-45)",
            category="Fungicide",
            manufacturer="Indofil Industries",
            active_ingredient="Mancozeb 75% WP",
            description="Broad spectrum contact protective fungicide with multi-site action.",
            dosage_instructions="Mix 2.5g per 1 Liter water (500g per 200L tank per acre). Spray thoroughly on foliage.",
            suitable_crops="Tomato, Potato, Chilli, Groundnut, Wheat",
            price_estimate="Rs. 380 / 500g"
        )
        p2 = Product(
            solution_id=sol1.id,
            name="Bio-Rakshak Trichoderma Viride",
            category="Bio-Pesticide",
            manufacturer="ICAR Bio-Tech",
            active_ingredient="Trichoderma viride 1.5% WP (2x10^8 CFU/g)",
            description="Eco-friendly antagonist bio-control fungus preventing soil-borne and foliar blights.",
            dosage_instructions="10g per liter water for foliar spray; 2.5 kg mixed with 100 kg FYM for soil application.",
            suitable_crops="All Vegetable Crops, Cotton, Pulses",
            price_estimate="Rs. 180 / 1 kg"
        )
        db.add_all([p1, p2])

        d2 = DiseasePest(
            name="Rice Blast (Magnaporthe oryzae)",
            scientific_name="Magnaporthe oryzae",
            target_crops="Paddy / Rice",
            symptoms="Spindle-shaped diamond lesions with grey-white centers; neck rot at panicle emergence.",
            description="Devastating fungal disease causing up to 80% yield loss in susceptible varieties.",
            prevention_methods="Avoid excess nitrogen fertilizer; maintain field sanitation; use certified resistant seeds.",
            severity_level="Critical"
        )
        db.add(d2)
        db.commit()
        db.refresh(d2)

        sol2 = DiseaseSolution(
            disease_id=d2.id,
            crop_name="Paddy / Rice",
            recommended_action="Drain standing water for 2 days. Avoid evening irrigation.",
            organic_treatment="Pseudomonas fluorescens @ 10g/L or Fermented Buttermilk decoction (5%).",
            chemical_treatment="Tricyclazole 75% WP @ 0.6g/L or Isoprothiolane 40% EC @ 1.5ml/L.",
            safety_notes="Do not spray during full bloom to protect honeybees."
        )
        db.add(sol2)
        db.commit()
        db.refresh(sol2)

        p3 = Product(
            solution_id=sol2.id,
            name="Beam 75 WP (Tricyclazole)",
            category="Fungicide",
            manufacturer="Corteva Agriscience",
            active_ingredient="Tricyclazole 75% WP",
            description="Systemic blast fungicide with preventative and curative activity.",
            dosage_instructions="120g to 150g in 200 Liters of water per acre.",
            suitable_crops="Paddy / Rice",
            price_estimate="Rs. 520 / 120g"
        )
        db.add(p3)

        # 8. Notifications
        n1 = Notification(
            user_id=farmer_user.id,
            title="Weather Alert: Rainfall Forecasted",
            message="Light to moderate rain expected within 48 hours. Postpone irrigation and pesticide spray operations.",
            type="weather",
            is_read=False
        )
        n2 = Notification(
            user_id=farmer_user.id,
            title="Yard Sheet Reminder: Flowering Stage",
            message="Your Cotton on 'Sanand Green Acres' is in Flowering Stage. Apply micronutrient foliar boost.",
            type="stage",
            is_read=False
        )
        n3 = Notification(
            user_id=farmer_user.id,
            title="Government Subsidy: Solar Pumps",
            message="PM-KUSUM subsidy portal is accepting applications for Gujarat farmers.",
            type="scheme",
            is_read=True
        )
        db.add_all([n1, n2, n3])

        # 9. Admin Audit Log entry
        audit = AdminAuditLog(
            admin_id=admin_user.id,
            admin_email=admin_user.email,
            entity_type="SystemInit",
            entity_id=1,
            action="CREATE",
            description="System initialized with standard agronomic knowledge base and government policies."
        )
        db.add(audit)

        db.commit()
        print("Database seeded successfully with comprehensive agricultural records!")

    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
