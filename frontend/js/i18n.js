// Multi-Language Localization Engine (English, Hindi, Gujarati)
const TRANSLATIONS = {
    en: {
        app_title: "Smart Crop Advisory System",
        tagline: "Empowering Small & Marginal Farmers with Personalized Agricultural Intelligence",
        nav_home: "Dashboard",
        nav_farms: "My Farms & Soil",
        nav_yard: "Yard Sheet",
        nav_recommend: "Crop Advisory",
        nav_weather: "Weather Actions",
        nav_doctor: "Crop Doctor (ML)",
        nav_schemes: "Govt Policies",
        nav_products: "Agri Solutions",
        nav_login: "Farmer Login",
        nav_admin: "Admin Portal",
        nav_logout: "Logout",
        hello: "Namaste",
        welcome_farmer: "Welcome to your Digital Agricultural Assistant",
        kpi_farms: "My Active Farms",
        kpi_crops: "Cultivated Crops",
        kpi_weather: "Current Weather",
        kpi_alerts: "Critical Alerts",
        btn_add_farm: "Add New Farm",
        btn_get_advisory: "Get Crop Recommendations",
        btn_upload_scan: "Scan Plant Disease",
        btn_view_schemes: "Explore Subsidies",
        sec_action_advisories: "Action-Oriented Weather Advisories",
        sec_active_crops: "Currently Growing Crops",
        sec_soil_health: "Soil Health Matrix",
        soil_type: "Soil Type",
        soil_ph: "Soil pH",
        irrigation_type: "Irrigation Type",
        water_avail: "Water Availability",
        nitrogen: "Nitrogen (N)",
        phosphorus: "Phosphorus (P)",
        potassium: "Potassium (K)",
        crop_stage: "Crop Stage",
        expected_yield: "Expected Yield",
        actual_yield: "Actual Yield",
        suitability_score: "Suitability Score",
        confidence: "Confidence",
        reason: "Agronomic Justification",
        water_demand: "Water Demand",
        fertilizer_tip: "Fertilizer Schedule",
        potential_risks: "Potential Risks",
        immediate_action: "Immediate Action",
        organic_solution: "Organic / Bio Remedy",
        chemical_solution: "Chemical Treatment",
        prevention: "Prevention for Next Cycle",
        listen_audio: "Listen in Voice",
        switch_lang: "Language",
        scheme_eligibility: "Eligibility",
        scheme_benefits: "Benefits",
        apply_portal: "Visit Official Portal",
        filter_state: "Filter by State",
        filter_category: "Category",
        all: "All",
        admin_portal_title: "Smart Crop Admin Management & Audit Portal"
    },
    hi: {
        app_title: "स्मार्ट फसल सलाहकार प्रणाली",
        tagline: "छोटे और सीमांत किसानों के लिए व्यक्तिगत कृषि सलाह और समाधान",
        nav_home: "डैशबोर्ड",
        nav_farms: "मेरे खेत और मिट्टी",
        nav_yard: "डिजिटल यार्ड शीट",
        nav_recommend: "फसल सलाह (AI)",
        nav_weather: "मौसम और कार्य",
        nav_doctor: "फसल डॉक्टर (ML)",
        nav_schemes: "सरकारी योजनाएं",
        nav_products: "दवाएं व खाद",
        nav_login: "किसान लॉगिन",
        nav_admin: "एडमिन पोर्टल",
        nav_logout: "लॉगआउट",
        hello: "नमस्ते",
        welcome_farmer: "आपके डिजिटल कृषि सहायक में आपका स्वागत है",
        kpi_farms: "सक्रिय खेत",
        kpi_crops: "बोई गई फसलें",
        kpi_weather: "वर्तमान मौसम",
        kpi_alerts: "ज़रूरी अलर्ट",
        btn_add_farm: "नया खेत जोड़ें",
        btn_get_advisory: "फसल की सिफारिश प्राप्त करें",
        btn_upload_scan: "पौधे का रोग स्कैन करें",
        btn_view_schemes: "सब्सिडी और योजनाएं देखें",
        sec_action_advisories: "मौसम आधारित तुरंत करने योग्य कार्य",
        sec_active_crops: "वर्तमान में उगाई जा रही फसलें",
        sec_soil_health: "मिट्टी स्वास्थ्य रिपोर्ट",
        soil_type: "मिट्टी का प्रकार",
        soil_ph: "मिट्टी का पीएच (pH)",
        irrigation_type: "सिंचाई का प्रकार",
        water_avail: "पानी की उपलब्धता",
        nitrogen: "नाइट्रोजन (N)",
        phosphorus: "फास्फोरस (P)",
        potassium: "पोटैशियम (K)",
        crop_stage: "फसल का चरण",
        expected_yield: "अनुमानित उपज",
        actual_yield: "वास्तविक उपज",
        suitability_score: "अनुकूलता स्कोर",
        confidence: "सटीकता",
        reason: "सिफारिश का कारण",
        water_demand: "पानी की आवश्यकता",
        fertilizer_tip: "खाद व पोषण सलाह",
        potential_risks: "संभावित जोखिम",
        immediate_action: "तुरंत करने योग्य कार्रवाई",
        organic_solution: "जैविक / देसी उपचार",
        chemical_solution: "रासायनिक उपचार व दवा",
        prevention: "भविष्य में बचाव के उपाय",
        listen_audio: "आवाज़ में सुनें",
        switch_lang: "भाषा बदलें",
        scheme_eligibility: "पात्रता",
        scheme_benefits: "योजना के लाभ",
        apply_portal: "आधिकारिक पोर्टल पर जाएं",
        filter_state: "राज्य के अनुसार फ़िल्टर",
        filter_category: "श्रेणी",
        all: "सभी",
        admin_portal_title: "स्मार्ट क्रॉप एडमिन व ऑडिट प्रबंधन"
    },
    gu: {
        app_title: "સ્માર્ટ પાક સલાહકાર પ્રણાલી",
        tagline: "નાના અને સીમાંત ખેડૂતો માટે વ્યક્તિગત કૃષિ બુદ્ધિમત્તા અને ઉકેલો",
        nav_home: "ડેશબોર્ડ",
        nav_farms: "મારા ખેતરો અને જમીન",
        nav_yard: "યાર્ડ શીટ (રેકોર્ડ)",
        nav_recommend: "પાકની ભલામણ (AI)",
        nav_weather: "હવામાન અને ખેતી પગલાં",
        nav_doctor: "પાક ડૉક્ટર (રોગ નિદાન)",
        nav_schemes: "સરકારી યોજનાઓ",
        nav_products: "દવાઓ અને ખાતર",
        nav_login: "ખેડૂત લૉગિન",
        nav_admin: "એડમિન પોર્ટલ",
        nav_logout: "લૉગઆઉટ",
        hello: "નમસ્તે",
        welcome_farmer: "તમારા ડિજિટલ કૃષિ સહાયકમાં આપનું સ્વાગત છે",
        kpi_farms: "મારા સક્રિય ખેતરો",
        kpi_crops: "વાવેતર કરેલ પાક",
        kpi_weather: "હાલનું હવામાન",
        kpi_alerts: "મહત્વપૂર્ણ ચેતવણી",
        btn_add_farm: "નવું ખેતર ઉમેરો",
        btn_get_advisory: "યોગ્ય પાકની સલાહ મેળવો",
        btn_upload_scan: "છોડનો ફોટો સ્કેન કરો",
        btn_view_schemes: "સબસિડી અને સહાય જુઓ",
        sec_action_advisories: "હવામાન આધારિત ખેતી પગલાં",
        sec_active_crops: "હાલમાં ઉગતા પાક",
        sec_soil_health: "જમીન આરોગ્ય અહેવાલ",
        soil_type: "જમીનનો પ્રકાર",
        soil_ph: "જમીનનું pH",
        irrigation_type: "પિયત પદ્ધતિ",
        water_avail: "પાણીની ઉપલબ્ધતા",
        nitrogen: "નાઇટ્રોજન (N)",
        phosphorus: "ફોસ્ફરસ (P)",
        potassium: "પોટાશ (K)",
        crop_stage: "પાકનો તબક્કો",
        expected_yield: "અંદાજિત ઉત્પાદન",
        actual_yield: "વાસ્તવિક ઉત્પાદન",
        suitability_score: "યોગ્યતા સ્કોર",
        confidence: "ચોકસાઈ",
        reason: "સલાહ પાછળનું વૈજ્ઞાનિક કારણ",
        water_demand: "પાણીની જરૂરિયાત",
        fertilizer_tip: "ખાતર વ્યવસ્થાપન",
        potential_risks: "સંભવિત જોખમો",
        immediate_action: "તાત્કાલિક લેવાના પગલાં",
        organic_solution: "જૈવિક / દેશી ઉપચાર",
        chemical_solution: "રાસાયણિક દવા અને માપ",
        prevention: "આગામી વાવેતરમાં સાવચેતી",
        listen_audio: "અવાજમાં સાંભળો",
        switch_lang: "ભાષા બદલો",
        scheme_eligibility: "પાત્રતા",
        scheme_benefits: "યોજનાના ફાયદા",
        apply_portal: "સત્તાવાર પોર્ટલ પર જાઓ",
        filter_state: "રાજ્ય પ્રમાણે",
        filter_category: "કેટેગરી",
        all: "બધા",
        admin_portal_title: "સ્માર્ટ ક્રોપ એડમિન અને ઓડિટ પોર્ટલ"
    }
};

let currentLang = localStorage.getItem("smart_crop_lang") || "en";

function setLanguage(lang) {
    if (TRANSLATIONS[lang]) {
        currentLang = lang;
        localStorage.setItem("smart_crop_lang", lang);
        applyTranslations();
    }
}

function t(key) {
    return TRANSLATIONS[currentLang]?.[key] || TRANSLATIONS["en"]?.[key] || key;
}

function applyTranslations() {
    document.querySelectorAll("[data-i18n]").forEach(el => {
        const key = el.getAttribute("data-i18n");
        if (TRANSLATIONS[currentLang] && TRANSLATIONS[currentLang][key]) {
            el.innerText = TRANSLATIONS[currentLang][key];
        }
    });

    document.querySelectorAll("[data-i18n-placeholder]").forEach(el => {
        const key = el.getAttribute("data-i18n-placeholder");
        if (TRANSLATIONS[currentLang] && TRANSLATIONS[currentLang][key]) {
            el.setAttribute("placeholder", TRANSLATIONS[currentLang][key]);
        }
    });

    // Update active state in language selector
    document.querySelectorAll(".lang-btn").forEach(btn => {
        const lang = btn.getAttribute("data-lang");
        if (lang === currentLang) {
            btn.classList.add("bg-emerald-600", "text-white", "font-bold");
            btn.classList.remove("text-slate-600", "bg-slate-100");
        } else {
            btn.classList.remove("bg-emerald-600", "text-white", "font-bold");
            btn.classList.add("text-slate-600", "bg-slate-100");
        }
    });
}

// Text-to-Speech Accessibility for Marginal Farmers
function speakText(text, langOverride) {
    if (!("speechSynthesis" in window)) {
        alert("Text-to-speech is not supported on this browser.");
        return;
    }
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    const lang = langOverride || currentLang;
    if (lang === "hi") utterance.lang = "hi-IN";
    else if (lang === "gu") utterance.lang = "gu-IN";
    else utterance.lang = "en-IN";
    utterance.rate = 0.9;
    window.speechSynthesis.speak(utterance);
}
