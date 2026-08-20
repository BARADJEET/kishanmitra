from typing import List, Dict, Any

CROP_AGRONOMIC_DATABASE = [
    {
        "name": "Cotton (कपास / કપાસ)",
        "soil_types": ["Black Soil", "Alluvial Soil", "Clay Loam"],
        "min_ph": 6.0, "max_ph": 8.0, "opt_ph": 7.0,
        "n_range": (60, 140), "p_range": (30, 70), "k_range": (30, 80),
        "temp_range": (21, 35), "opt_temp": 28,
        "rainfall_range": (500, 1000),
        "water_req": "Moderate",
        "seasons": ["Kharif"],
        "yield_range": "1500 - 2500 kg/ha",
        "market_outlook": "High commercial value in textile hubs (Gujarat, Maharashtra, Telangana)",
        "fertilizer_advice": "Apply N:P:K @ 100:50:50 kg/ha with Zinc Sulphate foliar spray at squaring.",
        "basic_req": "Warm climate, deep black soil with good drainage, 180-200 frost-free days.",
        "risks": "Susceptible to Pink Bollworm and Whitefly. Avoid water stagnation."
    },
    {
        "name": "Wheat (गेहूं / ઘઉં)",
        "soil_types": ["Alluvial Soil", "Loamy Soil", "Clay Loam", "Black Soil"],
        "min_ph": 6.0, "max_ph": 7.5, "opt_ph": 6.8,
        "n_range": (80, 140), "p_range": (40, 70), "k_range": (30, 60),
        "temp_range": (12, 25), "opt_temp": 18,
        "rainfall_range": (300, 800),
        "water_req": "Moderate",
        "seasons": ["Rabi"],
        "yield_range": "3500 - 5500 kg/ha",
        "market_outlook": "High government MSP procurement support across all states",
        "fertilizer_advice": "Basal application of DAP + MOP; top-dress with Urea at Crown Root Initiation (CRI) stage (21 days).",
        "basic_req": "Cool growing period and warm sunny weather during ripening. 4-6 critical irrigations.",
        "risks": "Terminal heat stress during grain filling; Yellow rust in humid winter zones."
    },
    {
        "name": "Paddy / Rice (धान / ડાંગર)",
        "soil_types": ["Clay Soil", "Clay Loam", "Alluvial Soil"],
        "min_ph": 5.0, "max_ph": 7.2, "opt_ph": 6.2,
        "n_range": (80, 160), "p_range": (30, 60), "k_range": (30, 60),
        "temp_range": (20, 37), "opt_temp": 27,
        "rainfall_range": (1000, 2500),
        "water_req": "High",
        "seasons": ["Kharif", "Rabi"],
        "yield_range": "3000 - 5000 kg/ha",
        "market_outlook": "Staple crop with steady wholesale market demand and MSP",
        "fertilizer_advice": "Apply Urea in 3 splits (Basal, Tillering, Panicle initiation) + Zinc Sulphate 25 kg/ha.",
        "basic_req": "High standing water availability, high humidity, heavy clayey soil with low permeability.",
        "risks": "Blast disease and Stem Borer. Extreme water dependency."
    },
    {
        "name": "Groundnut / Peanut (मूंगफली / મગફળી)",
        "soil_types": ["Sandy Loam", "Red Soil", "Alluvial Soil", "Light Black Soil"],
        "min_ph": 5.8, "max_ph": 7.5, "opt_ph": 6.5,
        "n_range": (20, 45), "p_range": (40, 70), "k_range": (30, 60),
        "temp_range": (22, 33), "opt_temp": 26,
        "rainfall_range": (450, 750),
        "water_req": "Low",
        "seasons": ["Kharif", "Zaid"],
        "yield_range": "1800 - 2800 kg/ha",
        "market_outlook": "High oilseed demand in domestic oil processing units",
        "fertilizer_advice": "Apply Gypsum @ 400 kg/ha at pegging stage for rich pod development and oil content.",
        "basic_req": "Well-aerated sandy loam soil for easy peg penetration and pod expansion.",
        "risks": "Tikka leaf spot and collar rot. Excess rainfall at harvesting leads to aflatoxin."
    },
    {
        "name": "Mustard (सरसों / રાઈ)",
        "soil_types": ["Loamy Soil", "Alluvial Soil", "Sandy Loam"],
        "min_ph": 6.0, "max_ph": 7.8, "opt_ph": 7.0,
        "n_range": (50, 90), "p_range": (25, 50), "k_range": (20, 40),
        "temp_range": (10, 25), "opt_temp": 17,
        "rainfall_range": (250, 500),
        "water_req": "Low",
        "seasons": ["Rabi"],
        "yield_range": "1400 - 2200 kg/ha",
        "market_outlook": "Excellent remunerative price due to edible oil import substitution",
        "fertilizer_advice": "Elemental Sulphur @ 20-30 kg/ha increases oil percentage by 10-15%.",
        "basic_req": "Cool dry winter season; 2-3 light irrigations at flowering and pod formation.",
        "risks": "Mustard Aphid attack during cloudy weather; White rust."
    },
    {
        "name": "Tomato (टमाटर / ટામેટા)",
        "soil_types": ["Sandy Loam", "Red Soil", "Alluvial Soil", "Black Soil"],
        "min_ph": 6.0, "max_ph": 7.2, "opt_ph": 6.5,
        "n_range": (80, 150), "p_range": (50, 90), "k_range": (60, 120),
        "temp_range": (18, 32), "opt_temp": 24,
        "rainfall_range": (400, 800),
        "water_req": "Moderate",
        "seasons": ["Kharif", "Rabi", "Zaid"],
        "yield_range": "25000 - 45000 kg/ha",
        "market_outlook": "High daily cash-flow vegetable in peri-urban and local markets",
        "fertilizer_advice": "Drip fertigation with 19:19:19 and Calcium Nitrate to prevent blossom end rot.",
        "basic_req": "Raised bed cultivation with drip irrigation and staking for indeterminate varieties.",
        "risks": "Early/Late Blight and Leaf Curl Virus transmitted by whitefly."
    },
    {
        "name": "Maize / Corn (मक्का / મકાઈ)",
        "soil_types": ["Alluvial Soil", "Loamy Soil", "Red Soil", "Black Soil"],
        "min_ph": 5.8, "max_ph": 7.5, "opt_ph": 6.5,
        "n_range": (90, 160), "p_range": (40, 75), "k_range": (30, 60),
        "temp_range": (18, 35), "opt_temp": 25,
        "rainfall_range": (500, 900),
        "water_req": "Moderate",
        "seasons": ["Kharif", "Rabi", "Zaid"],
        "yield_range": "4000 - 6500 kg/ha",
        "market_outlook": "Robust demand from poultry feed, starch industry, and silage feed",
        "fertilizer_advice": "Split Nitrogen into 3 doses (Knee-high, Tasseling, Grain filling).",
        "basic_req": "Well-drained deep fertile soils; sensitive to waterlogging at early stages.",
        "risks": "Fall Armyworm (Spodoptera frugiperda) infestation requires pheromone traps."
    },
    {
        "name": "Potato (आलू / બટાકા)",
        "soil_types": ["Sandy Loam", "Alluvial Soil", "Loamy Soil"],
        "min_ph": 5.0, "max_ph": 6.8, "opt_ph": 5.8,
        "n_range": (100, 180), "p_range": (60, 100), "k_range": (80, 150),
        "temp_range": (12, 24), "opt_temp": 18,
        "rainfall_range": (300, 600),
        "water_req": "Moderate",
        "seasons": ["Rabi"],
        "yield_range": "20000 - 35000 kg/ha",
        "market_outlook": "Strong cold-storage and processing (chips/fries) demand",
        "fertilizer_advice": "High Potash requirement (SOP preferred over MOP for better starch and storage).",
        "basic_req": "Friable, loose, organically rich soil with ridge and furrow planting.",
        "risks": "Late Blight during cold foggy nights; Potato tuber moth in storage."
    },
    {
        "name": "Sugarcane (गन्ना / શેરડી)",
        "soil_types": ["Black Soil", "Alluvial Soil", "Clay Loam"],
        "min_ph": 6.0, "max_ph": 8.0, "opt_ph": 6.8,
        "n_range": (120, 250), "p_range": (50, 100), "k_range": (60, 140),
        "temp_range": (20, 38), "opt_temp": 30,
        "rainfall_range": (1100, 2200),
        "water_req": "High",
        "seasons": ["Kharif", "Rabi"],
        "yield_range": "70000 - 110000 kg/ha",
        "market_outlook": "Guaranteed FRP (Fair and Remunerative Price) from sugar mills",
        "fertilizer_advice": "Basal FYM + split NPK application; micronutrients Iron and Zinc essential in calcareous soils.",
        "basic_req": "Long warm sunny season with assured perennial irrigation (prefer drip irrigation).",
        "risks": "Red rot and Early shoot borer. High water consumption."
    },
    {
        "name": "Chickpea / Gram (चना / ચણા)",
        "soil_types": ["Black Soil", "Loamy Soil", "Sandy Loam"],
        "min_ph": 6.0, "max_ph": 8.0, "opt_ph": 7.2,
        "n_range": (15, 30), "p_range": (35, 60), "k_range": (20, 40),
        "temp_range": (12, 28), "opt_temp": 20,
        "rainfall_range": (250, 500),
        "water_req": "Low",
        "seasons": ["Rabi"],
        "yield_range": "1500 - 2500 kg/ha",
        "market_outlook": "Key protein pulse with strong national buffer stock procurement",
        "fertilizer_advice": "Seed treatment with Rhizobium culture; single dose of DAP @ 50 kg/ha at sowing.",
        "basic_req": "Cool dry climate, residual moisture in deep black soils, minimal nitrogen dependency.",
        "risks": "Pod borer (Helicoverpa armigera) and Fusarium wilt."
    },
    {
        "name": "Soybean (सोयाबीन / સોયાબીન)",
        "soil_types": ["Black Soil", "Clay Loam", "Alluvial Soil"],
        "min_ph": 6.0, "max_ph": 7.5, "opt_ph": 6.5,
        "n_range": (20, 40), "p_range": (40, 80), "k_range": (30, 60),
        "temp_range": (20, 32), "opt_temp": 26,
        "rainfall_range": (600, 1000),
        "water_req": "Moderate",
        "seasons": ["Kharif"],
        "yield_range": "1800 - 2800 kg/ha",
        "market_outlook": "High oil extraction and de-oiled cake (DOC) export demand",
        "fertilizer_advice": "Apply Single Super Phosphate (SSP) for Phosphorus + Sulphur supplement.",
        "basic_req": "Good drainage, warm monsoon climate, seed inoculation with Bradyrhizobium.",
        "risks": "Yellow Mosaic Virus spread by whiteflies; Girdle beetle."
    },
    {
        "name": "Pearl Millet / Bajra (बाजरा / બાજરી)",
        "soil_types": ["Sandy Soil", "Sandy Loam", "Red Soil", "Light Black Soil"],
        "min_ph": 6.5, "max_ph": 8.5, "opt_ph": 7.5,
        "n_range": (40, 80), "p_range": (20, 40), "k_range": (20, 40),
        "temp_range": (25, 40), "opt_temp": 32,
        "rainfall_range": (200, 500),
        "water_req": "Low",
        "seasons": ["Kharif", "Zaid"],
        "yield_range": "2000 - 3200 kg/ha",
        "market_outlook": "Surging national demand under National Nutri-Cereal & Shree Anna initiatives",
        "fertilizer_advice": "Apply 60 kg N in 2 splits; low P & K requirements.",
        "basic_req": "Highly drought-tolerant, thrives in arid and semi-arid low-fertility soils.",
        "risks": "Downy mildew (Green ear disease) and Ergot."
    },
    {
        "name": "Onion (प्याज / ડુંગળી)",
        "soil_types": ["Sandy Loam", "Alluvial Soil", "Clay Loam"],
        "min_ph": 6.0, "max_ph": 7.5, "opt_ph": 6.8,
        "n_range": (80, 140), "p_range": (40, 75), "k_range": (60, 100),
        "temp_range": (13, 30), "opt_temp": 21,
        "rainfall_range": (350, 700),
        "water_req": "Moderate",
        "seasons": ["Kharif", "Rabi"],
        "yield_range": "18000 - 30000 kg/ha",
        "market_outlook": "Daily high-velocity kitchen staple with periodic price surges",
        "fertilizer_advice": "Sulphur application (30 kg/ha) increases pungency and storage shelf life.",
        "basic_req": "Well-drained friable loamy soil, shallow root zone requiring frequent light irrigation.",
        "risks": "Thrips attack and Purple Blotch disease."
    },
    {
        "name": "Chilli / Pepper (मिर्च / મરચાં)",
        "soil_types": ["Black Soil", "Red Loam", "Sandy Loam"],
        "min_ph": 6.0, "max_ph": 7.8, "opt_ph": 6.8,
        "n_range": (80, 150), "p_range": (40, 80), "k_range": (50, 100),
        "temp_range": (20, 35), "opt_temp": 26,
        "rainfall_range": (500, 1000),
        "water_req": "Moderate",
        "seasons": ["Kharif", "Rabi"],
        "yield_range": "2000 - 3500 kg/ha (Dry)",
        "market_outlook": "High value spice export crop with prominent spice park hubs",
        "fertilizer_advice": "Foliar application of Micronutrients (Fe, Zn, B) prevents flower and fruit drop.",
        "basic_req": "Warm humid climate for vegetative growth and dry warm weather for fruit maturation.",
        "risks": "Chilli leaf curl virus, Thrips, and Mites causing leaf upward/downward curling."
    }
]

def score_crop(crop: Dict[str, Any], params: Dict[str, Any]) -> float:
    score = 0.0

    soil_type = params.get("soil_type", "Black Soil")
    if any(s.lower() in soil_type.lower() for s in crop["soil_types"]):
        score += 20.0
    elif "loam" in soil_type.lower() and any("loam" in s.lower() for s in crop["soil_types"]):
        score += 15.0
    else:
        score += 8.0

    ph = params.get("soil_ph", 6.8)
    if crop["min_ph"] <= ph <= crop["max_ph"]:
        diff = abs(ph - crop["opt_ph"])
        score += max(5.0, 15.0 - (diff * 8.0))
    else:
        score += 3.0

    n = params.get("nitrogen_n", 60.0)
    p = params.get("phosphorus_p", 30.0)
    k = params.get("potassium_k", 40.0)

    n_min, n_max = crop["n_range"]
    p_min, p_max = crop["p_range"]
    k_min, k_max = crop["k_range"]

    n_score = 7.0 if n_min <= n <= n_max + 30 else max(1.0, 7.0 - abs(n - (n_min + n_max) / 2) * 0.05)
    p_score = 6.5 if p_min <= p <= p_max + 20 else max(1.0, 6.5 - abs(p - (p_min + p_max) / 2) * 0.08)
    k_score = 6.5 if k_min <= k <= k_max + 20 else max(1.0, 6.5 - abs(k - (k_min + k_max) / 2) * 0.08)
    score += (n_score + p_score + k_score)

    temp = params.get("temperature", 26.0)
    t_min, t_max = crop["temp_range"]
    if t_min <= temp <= t_max:
        t_diff = abs(temp - crop["opt_temp"])
        score += max(5.0, 15.0 - (t_diff * 1.0))
    else:
        score += 2.0

    water_avail = params.get("water_availability", "Moderate")
    if water_avail == "Scarce":
        if crop["water_req"] == "Low":
            score += 15.0
        elif crop["water_req"] == "Moderate":
            score += 8.0
        else:
            score += 2.0
    elif water_avail == "Abundant":
        if crop["water_req"] == "High":
            score += 15.0
        elif crop["water_req"] == "Moderate":
            score += 13.0
        else:
            score += 10.0
    else:
        if crop["water_req"] in ["Moderate", "Low"]:
            score += 15.0
        else:
            score += 9.0

    req_season = params.get("season", "Kharif")
    if req_season in crop["seasons"] or "All" in crop["seasons"]:
        score += 15.0
    else:
        score += 4.0

    return min(98.5, max(35.0, round(score, 1)))

def generate_reason(crop: Dict[str, Any], params: Dict[str, Any], score: float) -> str:
    soil_type = params.get("soil_type", "Black Soil")
    ph = params.get("soil_ph", 6.8)
    season = params.get("season", "Kharif")
    water = params.get("water_availability", "Moderate")

    reasons = []
    reasons.append(f"High agronomic compatibility with your {soil_type} and soil pH {ph}.")
    if season in crop["seasons"]:
        reasons.append(f"Ideal physiological growth cycle for the current {season} season.")
    if water == "Scarce" and crop["water_req"] == "Low":
        reasons.append("Requires minimal irrigation, perfectly matching scarce water resources.")
    elif water == "Abundant" and crop["water_req"] in ["High", "Moderate"]:
        reasons.append("Capitalizes on abundant water supply to maximize harvest yield.")
    reasons.append(crop["market_outlook"] + ".")
    return " ".join(reasons)

def recommend_crops(params: Dict[str, Any]) -> List[Dict[str, Any]]:
    scored_crops = []
    for crop in CROP_AGRONOMIC_DATABASE:
        score = score_crop(crop, params)
        confidence = "High" if score >= 80 else ("Moderate" if score >= 65 else "Good")
        reason = generate_reason(crop, params, score)

        scored_crops.append({
            "crop_name": crop["name"],
            "suitability_score": score,
            "confidence_level": confidence,
            "reason": reason,
            "water_requirement": f"{crop['water_req']} Irrigation Demand",
            "fertilizer_advice": crop["fertilizer_advice"],
            "basic_requirements": crop["basic_req"],
            "potential_risks": crop["risks"],
            "expected_yield_range": crop["yield_range"],
            "market_outlook": crop["market_outlook"]
        })

    scored_crops.sort(key=lambda x: x["suitability_score"], reverse=True)
    return scored_crops[:4]
