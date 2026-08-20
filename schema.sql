-- ============================================================================
-- Smart Crop Advisory System for Small and Marginal Farmers
-- Relational Database Schema DDL (MySQL 8.0+ / MariaDB Compatible)
-- ============================================================================

CREATE DATABASE IF NOT EXISTS smart_crop_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE smart_crop_db;

-- 1. Users Table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(20) UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    role ENUM('farmer', 'admin') NOT NULL DEFAULT 'farmer',
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_user_email (email),
    INDEX idx_user_role (role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 2. User Profiles Table
CREATE TABLE IF NOT EXISTS user_profiles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    full_name VARCHAR(255) NOT NULL,
    language_pref VARCHAR(10) DEFAULT 'en',
    state VARCHAR(100) DEFAULT 'Gujarat',
    district VARCHAR(100) DEFAULT 'Ahmedabad',
    village VARCHAR(100),
    avatar_url VARCHAR(500),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 3. Farms Table
CREATE TABLE IF NOT EXISTS farms (
    id INT AUTO_INCREMENT PRIMARY KEY,
    farmer_id INT NOT NULL,
    farm_name VARCHAR(255) NOT NULL,
    land_area_acres FLOAT NOT NULL DEFAULT 1.0,
    state VARCHAR(100) NOT NULL DEFAULT 'Gujarat',
    district VARCHAR(100) NOT NULL DEFAULT 'Ahmedabad',
    village VARCHAR(100),
    latitude FLOAT DEFAULT 23.0225,
    longitude FLOAT DEFAULT 72.5714,
    soil_type VARCHAR(100) NOT NULL DEFAULT 'Black Soil',
    irrigation_type VARCHAR(100) NOT NULL DEFAULT 'Drip',
    water_availability VARCHAR(50) NOT NULL DEFAULT 'Moderate',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (farmer_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_farm_farmer (farmer_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 4. Soil Records Table
CREATE TABLE IF NOT EXISTS soil_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    farm_id INT NOT NULL,
    nitrogen_n FLOAT NOT NULL DEFAULT 60.0,
    phosphorus_p FLOAT NOT NULL DEFAULT 30.0,
    potassium_k FLOAT NOT NULL DEFAULT 40.0,
    soil_ph FLOAT NOT NULL DEFAULT 6.5,
    organic_carbon FLOAT DEFAULT 0.6,
    test_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (farm_id) REFERENCES farms(id) ON DELETE CASCADE,
    INDEX idx_soil_farm (farm_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 5. Digital Yard Sheets Table
CREATE TABLE IF NOT EXISTS yard_sheets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    farm_id INT NOT NULL,
    crop_name VARCHAR(100) NOT NULL,
    crop_variety VARCHAR(100),
    sowing_date DATE,
    cultivated_area_acres FLOAT NOT NULL DEFAULT 1.0,
    crop_stage ENUM('Sowing', 'Germination', 'Vegetative', 'Flowering', 'Fruiting', 'Harvesting', 'Post-Harvest') DEFAULT 'Vegetative',
    expected_yield_kg FLOAT,
    actual_yield_kg FLOAT,
    season VARCHAR(50) DEFAULT 'Kharif',
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (farm_id) REFERENCES farms(id) ON DELETE CASCADE,
    INDEX idx_yard_farm (farm_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 6. Crop Recommendations Table
CREATE TABLE IF NOT EXISTS crop_recommendations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    farm_id INT NOT NULL,
    recommended_crop VARCHAR(100) NOT NULL,
    suitability_score FLOAT NOT NULL,
    reason TEXT NOT NULL,
    water_requirement VARCHAR(100) NOT NULL,
    fertilizer_advice TEXT,
    risk_factors TEXT,
    season VARCHAR(50),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (farm_id) REFERENCES farms(id) ON DELETE CASCADE,
    INDEX idx_rec_farm (farm_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 7. Diseases and Pests Database
CREATE TABLE IF NOT EXISTS diseases_pests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    scientific_name VARCHAR(255),
    target_crops VARCHAR(500) NOT NULL,
    symptoms TEXT NOT NULL,
    description TEXT NOT NULL,
    prevention_methods TEXT NOT NULL,
    severity_level VARCHAR(50) DEFAULT 'Medium',
    image_sample_url VARCHAR(500),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_disease_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 8. Disease Solutions Table
CREATE TABLE IF NOT EXISTS disease_solutions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    disease_id INT NOT NULL,
    crop_name VARCHAR(100) NOT NULL,
    recommended_action TEXT NOT NULL,
    organic_treatment TEXT,
    chemical_treatment TEXT,
    safety_notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (disease_id) REFERENCES diseases_pests(id) ON DELETE CASCADE,
    INDEX idx_sol_disease (disease_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 9. Products & Medicines Table
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    solution_id INT,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    manufacturer VARCHAR(255),
    active_ingredient VARCHAR(255),
    description TEXT,
    dosage_instructions TEXT NOT NULL,
    suitable_crops VARCHAR(500),
    price_estimate VARCHAR(100),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (solution_id) REFERENCES disease_solutions(id) ON DELETE SET NULL,
    INDEX idx_prod_cat (category),
    INDEX idx_prod_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 10. ML Image Predictions Table
CREATE TABLE IF NOT EXISTS ml_predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    farmer_id INT NOT NULL,
    farm_id INT,
    image_url VARCHAR(500) NOT NULL,
    crop_name VARCHAR(100),
    predicted_disease VARCHAR(255) NOT NULL,
    confidence_score FLOAT NOT NULL,
    symptoms TEXT,
    recommended_solution TEXT,
    prevention TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (farmer_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (farm_id) REFERENCES farms(id) ON DELETE SET NULL,
    INDEX idx_pred_farmer (farmer_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 11. Government Policies & Schemes Table
CREATE TABLE IF NOT EXISTS government_policies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    scheme_name VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    eligibility_criteria TEXT NOT NULL,
    applicable_state VARCHAR(100) DEFAULT 'All India',
    applicable_crops VARCHAR(500) DEFAULT 'All Crops',
    benefits TEXT NOT NULL,
    valid_until VARCHAR(100) DEFAULT 'Ongoing',
    official_portal_url VARCHAR(500),
    attachment_url VARCHAR(500),
    category VARCHAR(100) DEFAULT 'Subsidy',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_policy_state (applicable_state),
    INDEX idx_policy_cat (category)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 12. System Notifications Table
CREATE TABLE IF NOT EXISTS notifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    type VARCHAR(50) DEFAULT 'weather',
    is_read BOOLEAN DEFAULT FALSE,
    action_url VARCHAR(500),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_notif_user (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 13. Admin Audit Logs Table
CREATE TABLE IF NOT EXISTS admin_audit_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    admin_id INT NOT NULL,
    admin_email VARCHAR(255) NOT NULL,
    entity_type VARCHAR(100) NOT NULL,
    entity_id INT,
    action VARCHAR(50) NOT NULL,
    old_values_json TEXT,
    new_values_json TEXT,
    description TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_audit_admin (admin_id),
    INDEX idx_audit_entity (entity_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
