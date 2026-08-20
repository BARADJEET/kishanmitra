// Farmer Application State & Controller
let currentFarmerFarms = [];
let activeFarmId = null;

document.addEventListener("DOMContentLoaded", async () => {
    setLanguage(currentLang);
    checkAuthSession();
    bindNavigation();
    await loadInitialData();
    setupEventListeners();
});

function checkAuthSession() {
    const user = Api.getUser();
    const token = Api.getToken();
    const authStatusEl = document.getElementById("auth-status-container");
    const farmerNameEl = document.getElementById("farmer-display-name");

    if (token && user) {
        if (farmerNameEl) {
            farmerNameEl.innerText = user.profile?.full_name || user.email;
        }
        if (authStatusEl) {
            authStatusEl.innerHTML = `
                <div class="flex items-center gap-3">
                    <span class="text-xs bg-emerald-100 text-emerald-800 font-semibold px-2.5 py-1 rounded-full">
                        🧑‍🌾 ${user.profile?.full_name || user.email.split('@')[0]}
                    </span>
                    <button onclick="handleLogout()" class="text-xs text-rose-600 hover:text-rose-800 font-semibold flex items-center gap-1">
                        <i data-lucide="log-out" class="w-3.5 h-3.5"></i> Logout
                    </button>
                </div>
            `;
            if (window.lucide) lucide.createIcons();
        }
    } else {
        if (authStatusEl) {
            authStatusEl.innerHTML = `
                <button onclick="openLoginModal()" class="text-xs bg-emerald-600 hover:bg-emerald-700 text-white font-bold px-4 py-2 rounded-xl shadow flex items-center gap-1.5 transition">
                    <i data-lucide="user" class="w-4 h-4"></i> Farmer Login
                </button>
            `;
            if (window.lucide) lucide.createIcons();
        }
    }
}

function bindNavigation() {
    document.querySelectorAll("[data-nav-target]").forEach(btn => {
        btn.addEventListener("click", () => {
            const target = btn.getAttribute("data-nav-target");
            switchTab(target);
        });
    });
}

function switchTab(tabId) {
    document.querySelectorAll(".view-section").forEach(sec => {
        sec.classList.add("hidden");
    });
    const activeSec = document.getElementById(`view-${tabId}`);
    if (activeSec) {
        activeSec.classList.remove("hidden");
    }

    document.querySelectorAll("[data-nav-target]").forEach(btn => {
        if (btn.getAttribute("data-nav-target") === tabId) {
            btn.classList.add("text-emerald-700", "bg-emerald-50", "font-bold");
            btn.classList.remove("text-slate-600", "hover:bg-slate-50");
        } else {
            btn.classList.remove("text-emerald-700", "bg-emerald-50", "font-bold");
            btn.classList.add("text-slate-600", "hover:bg-slate-50");
        }
    });

    if (tabId === "farms") loadFarmsView();
    if (tabId === "yard") loadYardSheetsView();
    if (tabId === "schemes") loadSchemesView();
    if (tabId === "products") loadProductsView();
    if (tabId === "doctor") loadDoctorHistory();

    window.scrollTo({ top: 0, behavior: "smooth" });
}

async function loadInitialData() {
    try {
        await Promise.all([
            loadWeatherAdvisories(),
            loadFarmerFarms(),
            loadNotifications()
        ]);
    } catch (e) {
        console.warn("Initial load error:", e);
    }
}

async function loadWeatherAdvisories() {
    try {
        const res = await Api.getWeather(23.0225, 72.5714, "Ahmedabad");
        const w = res.weather;
        const advList = res.advisories;

        const tempEl = document.getElementById("widget-temp");
        const condEl = document.getElementById("widget-cond");
        const humidityEl = document.getElementById("widget-humidity");
        const windEl = document.getElementById("widget-wind");
        const rainProbEl = document.getElementById("widget-rain-prob");

        if (tempEl) tempEl.innerText = `${w.temperature}°C`;
        if (condEl) condEl.innerText = w.weather_condition;
        if (humidityEl) humidityEl.innerText = `${w.humidity}%`;
        if (windEl) windEl.innerText = `${w.wind_speed} km/h`;
        if (rainProbEl) rainProbEl.innerText = `${w.precipitation_probability}%`;

        const advContainer = document.getElementById("advisories-container");
        if (advContainer) {
            advContainer.innerHTML = advList.map(a => {
                const borderClass = a.action_level === "CRITICAL_ACTION" ? "border-rose-500 bg-rose-50/50" : 
                                   (a.action_level === "HIGH_RISK" ? "border-amber-500 bg-amber-50/50" : 
                                   (a.action_level === "WARNING" ? "border-amber-400 bg-amber-50/30" : "border-emerald-500 bg-emerald-50/30"));
                const badgeClass = a.action_level === "CRITICAL_ACTION" ? "bg-rose-600 text-white" : 
                                  (a.action_level === "HIGH_RISK" ? "bg-amber-600 text-white" : 
                                  (a.action_level === "WARNING" ? "bg-amber-500 text-white" : "bg-emerald-600 text-white"));
                return `
                    <div class="p-4 rounded-2xl border-l-4 ${borderClass} glass-card flex flex-col md:flex-row items-start md:items-center justify-between gap-4 transition hover:shadow-md">
                        <div class="flex items-start gap-3">
                            <span class="text-xs font-bold px-2.5 py-1 rounded-lg ${badgeClass} uppercase tracking-wide shrink-0">
                                ${a.category}
                            </span>
                            <div>
                                <h4 class="font-bold text-slate-900 text-base flex items-center gap-2">
                                    ${a.title}
                                </h4>
                                <p class="text-slate-700 text-sm mt-1 leading-relaxed">${a.message}</p>
                            </div>
                        </div>
                        <button onclick="speakText('${a.title}. ${a.message}')" class="shrink-0 text-emerald-700 bg-emerald-100 hover:bg-emerald-200 px-3 py-1.5 rounded-xl text-xs font-bold flex items-center gap-1.5 transition">
                            <i data-lucide="volume-2" class="w-4 h-4"></i> <span data-i18n="listen_audio">Listen</span>
                        </button>
                    </div>
                `;
            }).join("");
            if (window.lucide) lucide.createIcons();
        }
    } catch (e) {
        console.error("Error loading weather:", e);
    }
}

// Farms Loading & Rendering
async function loadFarmerFarms() {
    try {
        const farms = await Api.getFarms();
        currentFarmerFarms = farms;
        if (farms.length > 0 && !activeFarmId) {
            activeFarmId = farms[0].id;
        }

        const farmSelects = [document.getElementById("rec-farm-select"), document.getElementById("scan-farm-select"), document.getElementById("yard-farm-select")];
        farmSelects.forEach(sel => {
            if (sel) {
                sel.innerHTML = `<option value="">-- Choose Farm (Auto-fill Soil & Climate) --</option>` +
                    farms.map(f => `<option value="${f.id}" ${f.id === activeFarmId ? 'selected' : ''}>${f.farm_name} (${f.land_area_acres} Acres, ${f.soil_type})</option>`).join("");
            }
        });

        const kpiFarms = document.getElementById("kpi-total-farms");
        if (kpiFarms) kpiFarms.innerText = farms.length;
    } catch (e) {
        console.warn("Could not load farms:", e);
    }
}

async function loadFarmsView() {
    const container = document.getElementById("farms-list-container");
    if (!container) return;

    try {
        const farms = await Api.getFarms();
        if (farms.length === 0) {
            container.innerHTML = `
                <div class="col-span-full p-8 text-center glass-card rounded-2xl">
                    <p class="text-slate-500">No farms registered yet. Click below to add your first farm.</p>
                    <button onclick="openAddFarmModal()" class="mt-4 bg-emerald-600 hover:bg-emerald-700 text-white px-5 py-2.5 rounded-xl font-bold text-sm">
                        + Add New Farm
                    </button>
                </div>
            `;
            return;
        }

        container.innerHTML = farms.map(f => {
            const latestSoil = f.soil_records && f.soil_records.length > 0 ? f.soil_records[f.soil_records.length - 1] : null;
            return `
                <div class="p-6 rounded-2xl glass-card border border-slate-200/80 shadow-sm hover:shadow-md transition">
                    <div class="flex items-start justify-between">
                        <div>
                            <span class="text-xs bg-emerald-100 text-emerald-800 font-bold px-2.5 py-0.5 rounded-full">${f.state}, ${f.district}</span>
                            <h3 class="text-lg font-extrabold text-slate-900 mt-2">${f.farm_name}</h3>
                            <p class="text-sm text-slate-500">${f.village ? f.village + ', ' : ''}${f.district}</p>
                        </div>
                        <span class="text-xl font-black text-emerald-700">${f.land_area_acres} <span class="text-xs font-normal text-slate-500">Acres</span></span>
                    </div>

                    <div class="grid grid-cols-2 gap-3 mt-4 pt-4 border-t border-slate-100 text-xs">
                        <div class="bg-slate-50 p-2.5 rounded-xl">
                            <span class="text-slate-500 block" data-i18n="soil_type">Soil Type</span>
                            <span class="font-bold text-slate-800">${f.soil_type}</span>
                        </div>
                        <div class="bg-slate-50 p-2.5 rounded-xl">
                            <span class="text-slate-500 block" data-i18n="irrigation_type">Irrigation</span>
                            <span class="font-bold text-slate-800">${f.irrigation_type}</span>
                        </div>
                        <div class="bg-slate-50 p-2.5 rounded-xl">
                            <span class="text-slate-500 block" data-i18n="water_avail">Water Supply</span>
                            <span class="font-bold text-slate-800">${f.water_availability}</span>
                        </div>
                        <div class="bg-slate-50 p-2.5 rounded-xl">
                            <span class="text-slate-500 block" data-i18n="soil_ph">Soil pH</span>
                            <span class="font-bold text-slate-800">${latestSoil ? latestSoil.soil_ph : '6.8'}</span>
                        </div>
                    </div>

                    ${latestSoil ? `
                        <div class="mt-4 p-3 bg-emerald-50/60 rounded-xl">
                            <span class="text-xs font-bold text-emerald-900 block mb-1">NPK Nutrients (kg/ha):</span>
                            <div class="flex items-center justify-between text-xs font-bold text-emerald-800">
                                <span>N: ${latestSoil.nitrogen_n}</span>
                                <span>P: ${latestSoil.phosphorus_p}</span>
                                <span>K: ${latestSoil.potassium_k}</span>
                            </div>
                        </div>
                    ` : ''}

                    <div class="flex items-center gap-2 mt-5">
                        <button onclick="quickRecommendForFarm(${f.id})" class="flex-1 bg-emerald-600 hover:bg-emerald-700 text-white py-2 rounded-xl text-xs font-bold transition shadow-sm flex items-center justify-center gap-1.5">
                            <i data-lucide="sparkles" class="w-3.5 h-3.5"></i> Get Advisory
                        </button>
                        <button onclick="openAddSoilModal(${f.id})" class="bg-slate-100 hover:bg-slate-200 text-slate-700 px-3 py-2 rounded-xl text-xs font-bold transition">
                            + Soil Test
                        </button>
                    </div>
                </div>
            `;
        }).join("");
        if (window.lucide) lucide.createIcons();
    } catch (e) {
        container.innerHTML = `<p class="text-rose-500">Failed to load farms.</p>`;
    }
}

// Digital Yard Sheet
async function loadYardSheetsView() {
    const container = document.getElementById("yard-sheets-container");
    if (!container) return;

    try {
        const sheets = await Api.getYardSheets();
        const activeCropsKpi = document.getElementById("kpi-total-crops");
        if (activeCropsKpi) activeCropsKpi.innerText = sheets.length;

        if (sheets.length === 0) {
            container.innerHTML = `
                <div class="p-8 text-center glass-card rounded-2xl">
                    <p class="text-slate-500">No active crops logged in your Yard Sheet.</p>
                    <button onclick="openAddYardSheetModal()" class="mt-4 bg-emerald-600 hover:bg-emerald-700 text-white px-5 py-2.5 rounded-xl font-bold text-sm">
                        + Add Sown Crop Record
                    </button>
                </div>
            `;
            return;
        }

        container.innerHTML = sheets.map(s => {
            const stages = ["Sowing", "Germination", "Vegetative", "Flowering", "Fruiting", "Harvesting", "Post-Harvest"];
            const currentIdx = stages.indexOf(s.crop_stage);

            return `
                <div class="p-6 rounded-2xl glass-card border border-slate-200 shadow-sm mb-4">
                    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
                        <div>
                            <div class="flex items-center gap-2">
                                <span class="text-xs bg-emerald-600 text-white font-bold px-2.5 py-0.5 rounded-full">${s.season}</span>
                                <span class="text-xs text-slate-500">Sown: ${s.sowing_date || 'N/A'}</span>
                            </div>
                            <h3 class="text-xl font-black text-slate-900 mt-1">${s.crop_name} ${s.crop_variety ? `(${s.crop_variety})` : ''}</h3>
                            <p class="text-xs text-slate-600 mt-0.5">Area: <strong>${s.cultivated_area_acres} Acres</strong> | Expected Yield: <strong>${s.expected_yield_kg ? s.expected_yield_kg + ' kg' : 'N/A'}</strong></p>
                        </div>

                        <div class="flex items-center gap-3">
                            <select onchange="updateCropStage(${s.id}, this.value)" class="bg-slate-100 text-slate-800 text-xs font-bold py-2 px-3 rounded-xl border-none focus:ring-2 focus:ring-emerald-500">
                                ${stages.map(stg => `<option value="${stg}" ${stg === s.crop_stage ? 'selected' : ''}>Stage: ${stg}</option>`).join("")}
                            </select>
                        </div>
                    </div>

                    <div class="mt-6 pt-4 border-t border-slate-100">
                        <div class="flex items-center justify-between relative">
                            <div class="absolute left-0 right-0 top-1/2 -translate-y-1/2 h-1 bg-slate-200 z-0"></div>
                            ${stages.map((stg, idx) => {
                                const isPassed = idx <= currentIdx;
                                const isCurrent = idx === currentIdx;
                                return `
                                    <div class="relative z-10 flex flex-col items-center">
                                        <div class="w-6 h-6 rounded-full flex items-center justify-center text-[10px] font-bold ${isCurrent ? 'bg-emerald-600 text-white ring-4 ring-emerald-100' : (isPassed ? 'bg-emerald-500 text-white' : 'bg-slate-200 text-slate-500')}">
                                            ${idx + 1}
                                        </div>
                                        <span class="text-[10px] mt-1 font-semibold ${isCurrent ? 'text-emerald-700 font-bold' : 'text-slate-500'} hidden sm:block">${stg}</span>
                                    </div>
                                `;
                            }).join("")}
                        </div>
                    </div>

                    ${s.notes ? `
                        <div class="mt-4 p-3 bg-slate-50 rounded-xl text-xs text-slate-700">
                            <strong>Notes & Log:</strong> ${s.notes}
                        </div>
                    ` : ''}
                </div>
            `;
        }).join("");
    } catch (e) {
        console.error("Error loading yard sheets:", e);
    }
}

async function updateCropStage(sheetId, newStage) {
    try {
        await Api.updateYardSheetStage(sheetId, { crop_stage: newStage });
        showToast(`Crop stage updated to ${newStage}`);
        loadYardSheetsView();
    } catch (e) {
        showToast(e.message || "Failed to update stage", "error");
    }
}

// Crop Recommendations
async function generateRecommendations(e) {
    if (e) e.preventDefault();

    const data = {
        farm_id: document.getElementById("rec-farm-select")?.value ? parseInt(document.getElementById("rec-farm-select").value) : null,
        soil_type: document.getElementById("rec-soil-type")?.value || "Black Soil",
        soil_ph: parseFloat(document.getElementById("rec-soil-ph")?.value || 6.8),
        nitrogen_n: parseFloat(document.getElementById("rec-n")?.value || 70),
        phosphorus_p: parseFloat(document.getElementById("rec-p")?.value || 35),
        potassium_k: parseFloat(document.getElementById("rec-k")?.value || 45),
        temperature: parseFloat(document.getElementById("rec-temp")?.value || 27),
        season: document.getElementById("rec-season")?.value || "Kharif",
        water_availability: document.getElementById("rec-water")?.value || "Moderate"
    };

    const resultsContainer = document.getElementById("recommendations-results");
    if (resultsContainer) {
        resultsContainer.innerHTML = `
            <div class="p-12 text-center">
                <div class="inline-block w-8 h-8 border-4 border-emerald-600 border-t-transparent rounded-full animate-spin"></div>
                <p class="text-sm font-bold text-slate-700 mt-3">Analyzing Soil, Weather & Agronomic Matrix...</p>
            </div>
        `;
    }

    try {
        const res = await Api.getRecommendations(data);
        renderRecommendations(res.recommendations);
    } catch (err) {
        if (resultsContainer) {
            resultsContainer.innerHTML = `<div class="p-6 bg-rose-50 text-rose-700 rounded-2xl">Error: ${err.message}</div>`;
        }
    }
}

function renderRecommendations(items) {
    const container = document.getElementById("recommendations-results");
    if (!container) return;

    if (!items || items.length === 0) {
        container.innerHTML = `<p class="text-slate-500 p-6 text-center">No matching crops found for this criteria.</p>`;
        return;
    }

    container.innerHTML = items.map((c, idx) => {
        const isTop = idx === 0;
        return `
            <div class="p-6 rounded-2xl glass-card border-2 ${isTop ? 'border-emerald-500 shadow-md ring-2 ring-emerald-100' : 'border-slate-200'} transition hover:shadow-lg">
                <div class="flex items-start justify-between gap-4">
                    <div>
                        ${isTop ? '<span class="text-xs bg-emerald-600 text-white font-extrabold px-3 py-1 rounded-full uppercase tracking-wider">🌟 Best Fit Recommended</span>' : ''}
                        <h3 class="text-xl font-black text-slate-900 mt-2">${c.crop_name}</h3>
                        <span class="text-xs text-slate-500 font-semibold">${c.expected_yield_range}</span>
                    </div>
                    <div class="text-right shrink-0">
                        <span class="text-2xl font-black text-emerald-700">${c.suitability_score}%</span>
                        <span class="text-xs block text-slate-500 font-bold uppercase">${c.confidence_level} Confidence</span>
                    </div>
                </div>

                <div class="mt-4 p-4 bg-emerald-50/70 rounded-xl border border-emerald-100">
                    <h5 class="text-xs font-bold text-emerald-950 uppercase tracking-wide flex items-center gap-1.5 mb-1" data-i18n="reason">
                        <i data-lucide="info" class="w-4 h-4 text-emerald-700"></i> Scientific Justification
                    </h5>
                    <p class="text-slate-800 text-xs leading-relaxed">${c.reason}</p>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-3 gap-3 mt-4 text-xs">
                    <div class="p-3 bg-slate-50 rounded-xl">
                        <span class="text-slate-500 block font-semibold mb-1" data-i18n="water_demand">Water & Irrigation</span>
                        <p class="text-slate-800 font-bold">${c.water_requirement}</p>
                    </div>
                    <div class="p-3 bg-slate-50 rounded-xl">
                        <span class="text-slate-500 block font-semibold mb-1" data-i18n="fertilizer_tip">Fertilizer Advice</span>
                        <p class="text-slate-800 leading-snug">${c.fertilizer_advice}</p>
                    </div>
                    <div class="p-3 bg-slate-50 rounded-xl">
                        <span class="text-slate-500 block font-semibold mb-1" data-i18n="potential_risks">Potential Risks</span>
                        <p class="text-amber-900 leading-snug font-medium">${c.potential_risks}</p>
                    </div>
                </div>

                <div class="mt-4 flex items-center justify-between pt-3 border-t border-slate-100">
                    <span class="text-xs text-slate-500">Market: <strong>${c.market_outlook}</strong></span>
                    <button onclick="speakText('${c.crop_name}. Suitability score ${c.suitability_score} percent. ${c.reason}')" class="text-emerald-700 hover:text-emerald-900 text-xs font-bold flex items-center gap-1">
                        <i data-lucide="volume-2" class="w-3.5 h-3.5"></i> Audio Explain
                    </button>
                </div>
            </div>
        `;
    }).join("");
    if (window.lucide) lucide.createIcons();
}

function quickRecommendForFarm(farmId) {
    switchTab("recommend");
    const sel = document.getElementById("rec-farm-select");
    if (sel) {
        sel.value = farmId;
        generateRecommendations();
    }
}

// Plant Doctor ML Vision
async function handleImageUpload(e) {
    const file = e.target.files[0];
    if (!file) return;

    const previewImg = document.getElementById("scan-preview-img");
    const previewContainer = document.getElementById("scan-preview-container");
    const laser = document.getElementById("scan-laser");
    const scanResultContainer = document.getElementById("scan-result-container");

    const reader = new FileReader();
    reader.onload = function(evt) {
        if (previewImg) previewImg.src = evt.target.result;
        if (previewContainer) previewContainer.classList.remove("hidden");
        if (laser) laser.classList.remove("hidden");
    };
    reader.readAsDataURL(file);

    if (scanResultContainer) {
        scanResultContainer.innerHTML = `
            <div class="p-8 text-center">
                <div class="inline-block w-8 h-8 border-4 border-emerald-600 border-t-transparent rounded-full animate-spin"></div>
                <p class="text-sm font-bold text-slate-800 mt-3">Scanning leaf pathology with Computer Vision Model...</p>
                <p class="text-xs text-slate-500 mt-1">Analyzing necrotic spots, fungal pustules, and foliar texture.</p>
            </div>
        `;
    }

    const formData = new FormData();
    formData.append("file", file);
    const farmId = document.getElementById("scan-farm-select")?.value;
    if (farmId) formData.append("farm_id", farmId);

    try {
        const result = await Api.uploadCropScan(formData);
        if (laser) laser.classList.add("hidden");
        renderDiagnosisResult(result);
        loadDoctorHistory();
    } catch (err) {
        if (laser) laser.classList.add("hidden");
        if (scanResultContainer) {
            scanResultContainer.innerHTML = `<div class="p-4 bg-rose-50 text-rose-700 rounded-xl text-sm font-bold">Analysis Failed: ${err.message}</div>`;
        }
    }
}

function renderDiagnosisResult(diag) {
    const container = document.getElementById("scan-result-container");
    if (!container) return;

    const isHealthy = diag.predicted_disease.toLowerCase().includes("healthy");

    container.innerHTML = `
        <div class="p-6 rounded-2xl glass-card border-2 ${isHealthy ? 'border-emerald-500 bg-emerald-50/30' : 'border-rose-500 bg-rose-50/20'} shadow-lg">
            <div class="flex items-start justify-between gap-4">
                <div>
                    <span class="text-xs ${isHealthy ? 'bg-emerald-600' : 'bg-rose-600'} text-white font-extrabold px-3 py-1 rounded-full uppercase tracking-wide">
                        ${isHealthy ? '✅ Healthy Tissue' : '⚠️ Pathogen Detected'}
                    </span>
                    <h3 class="text-2xl font-black text-slate-900 mt-2">${diag.predicted_disease}</h3>
                    <p class="text-sm font-bold text-slate-600">${diag.crop_name}</p>
                </div>
                <div class="text-right">
                    <span class="text-3xl font-black text-emerald-700">${diag.confidence_score}%</span>
                    <span class="text-xs text-slate-500 font-bold block uppercase">Confidence</span>
                </div>
            </div>

            <div class="mt-4 p-4 bg-white/80 rounded-xl border border-slate-200">
                <h5 class="text-xs font-bold text-slate-900 uppercase tracking-wide mb-1">Identified Symptoms:</h5>
                <p class="text-xs text-slate-700 leading-relaxed">${diag.symptoms || 'No abnormal symptoms observed.'}</p>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4 text-xs">
                <div class="p-4 bg-emerald-50/80 rounded-xl border border-emerald-100">
                    <h5 class="font-extrabold text-emerald-950 uppercase tracking-wide flex items-center gap-1.5 mb-1.5" data-i18n="organic_solution">
                        🌿 Organic / Biological Remedy
                    </h5>
                    <p class="text-emerald-900 leading-relaxed">${diag.recommended_solution?.split('\n\nOrganic: ')[1]?.split('\n\nChemical: ')[0] || diag.recommended_solution}</p>
                </div>

                <div class="p-4 bg-blue-50/80 rounded-xl border border-blue-100">
                    <h5 class="font-extrabold text-blue-950 uppercase tracking-wide flex items-center gap-1.5 mb-1.5" data-i18n="chemical_solution">
                        🧪 Verified Chemical Treatment
                    </h5>
                    <p class="text-blue-900 leading-relaxed">${diag.recommended_solution?.split('\n\nChemical: ')[1] || 'Maintain preventative foliar sprays.'}</p>
                </div>
            </div>

            <div class="mt-4 p-3 bg-amber-50/70 rounded-xl text-xs text-amber-950 border border-amber-200">
                <strong>🛡️ Prevention for Next Cycle:</strong> ${diag.prevention}
            </div>

            <div class="mt-5 flex items-center justify-between pt-3 border-t border-slate-200">
                <button onclick="speakText('${diag.predicted_disease}. Detected with ${diag.confidence_score} percent confidence. Recommended remedy: ${diag.symptoms}')" class="text-emerald-700 bg-emerald-100 hover:bg-emerald-200 px-4 py-2 rounded-xl text-xs font-bold flex items-center gap-2 transition">
                    <i data-lucide="volume-2" class="w-4 h-4"></i> <span data-i18n="listen_audio">Listen to Treatment</span>
                </button>
            </div>
        </div>
    `;
    if (window.lucide) lucide.createIcons();
}

async function loadDoctorHistory() {
    const container = document.getElementById("scan-history-container");
    if (!container) return;

    try {
        const history = await Api.getScanHistory();
        if (history.length === 0) {
            container.innerHTML = `<p class="text-slate-400 text-xs text-center py-4">No scans uploaded yet.</p>`;
            return;
        }

        container.innerHTML = history.slice(0, 6).map(h => `
            <div class="p-3 bg-white rounded-xl border border-slate-200 shadow-sm flex items-center gap-3">
                <img src="${h.image_url}" alt="scan" class="w-12 h-12 rounded-lg object-cover bg-slate-100 shrink-0">
                <div class="flex-1 min-w-0">
                    <h5 class="text-xs font-bold text-slate-900 truncate">${h.predicted_disease}</h5>
                    <p class="text-[10px] text-slate-500">${h.crop_name || 'Crop'} • <span class="text-emerald-700 font-bold">${h.confidence_score}%</span></p>
                </div>
            </div>
        `).join("");
    } catch (e) {
        console.warn("Error loading scan history:", e);
    }
}

// Schemes & Products
async function loadSchemesView() {
    const container = document.getElementById("schemes-container");
    if (!container) return;

    const stateFilter = document.getElementById("scheme-state-filter")?.value || "";
    const catFilter = document.getElementById("scheme-cat-filter")?.value || "";
    const search = document.getElementById("scheme-search-input")?.value || "";

    try {
        const schemes = await Api.getPolicies(stateFilter, null, catFilter, search);
        if (schemes.length === 0) {
            container.innerHTML = `<p class="text-slate-500 text-center col-span-full p-8">No government policies matched your search criteria.</p>`;
            return;
        }

        container.innerHTML = schemes.map(s => `
            <div class="p-6 rounded-2xl glass-card border border-slate-200 shadow-sm hover:shadow-md transition flex flex-col justify-between">
                <div>
                    <div class="flex items-center justify-between gap-2">
                        <span class="text-xs bg-blue-100 text-blue-800 font-bold px-2.5 py-0.5 rounded-full">${s.category}</span>
                        <span class="text-xs text-slate-500">${s.applicable_state}</span>
                    </div>
                    <h3 class="text-lg font-black text-slate-900 mt-2">${s.title}</h3>
                    <p class="text-xs text-slate-600 mt-2 leading-relaxed">${s.description}</p>

                    <div class="mt-4 space-y-2 text-xs">
                        <div class="p-2.5 bg-slate-50 rounded-xl">
                            <span class="text-slate-500 font-semibold block" data-i18n="scheme_eligibility">Eligibility:</span>
                            <span class="text-slate-800 font-medium">${s.eligibility_criteria}</span>
                        </div>
                        <div class="p-2.5 bg-emerald-50/70 rounded-xl">
                            <span class="text-emerald-800 font-semibold block" data-i18n="scheme_benefits">Benefits:</span>
                            <span class="text-emerald-950 font-bold">${s.benefits}</span>
                        </div>
                    </div>
                </div>

                <div class="mt-5 pt-4 border-t border-slate-100 flex items-center justify-between">
                    <span class="text-[11px] text-slate-400">Validity: ${s.valid_until}</span>
                    ${s.official_portal_url ? `
                        <a href="${s.official_portal_url}" target="_blank" class="bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold px-3 py-1.5 rounded-xl transition flex items-center gap-1">
                            <span data-i18n="apply_portal">Official Portal</span> <i data-lucide="external-link" class="w-3.5 h-3.5"></i>
                        </a>
                    ` : ''}
                </div>
            </div>
        `).join("");
        if (window.lucide) lucide.createIcons();
    } catch (e) {
        container.innerHTML = `<p class="text-rose-500 col-span-full">Failed to load schemes.</p>`;
    }
}

async function loadProductsView() {
    const container = document.getElementById("products-container");
    if (!container) return;

    const cat = document.getElementById("product-cat-filter")?.value || "";
    const search = document.getElementById("product-search-input")?.value || "";

    try {
        const prods = await Api.getProducts(cat, null, search);
        if (prods.length === 0) {
            container.innerHTML = `<p class="text-slate-500 text-center col-span-full p-8">No agricultural products found.</p>`;
            return;
        }

        container.innerHTML = prods.map(p => `
            <div class="p-5 rounded-2xl glass-card border border-slate-200 shadow-sm flex flex-col justify-between">
                <div>
                    <div class="flex items-center justify-between">
                        <span class="text-xs bg-emerald-100 text-emerald-800 font-bold px-2.5 py-0.5 rounded-full">${p.category}</span>
                        <span class="text-xs font-bold text-slate-700">${p.price_estimate || ''}</span>
                    </div>
                    <h4 class="text-base font-extrabold text-slate-900 mt-2">${p.name}</h4>
                    <p class="text-[11px] text-slate-500">Mfr: ${p.manufacturer || 'Approved Agrochemicals'}</p>
                    <p class="text-xs text-slate-600 mt-2">${p.description || ''}</p>

                    <div class="mt-3 p-2.5 bg-slate-50 rounded-xl text-xs">
                        <span class="text-slate-500 font-semibold block">Dosage & Application:</span>
                        <span class="text-slate-800 font-medium">${p.dosage_instructions}</span>
                    </div>
                </div>

                <div class="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
                    <span>Crops: <strong>${p.suitable_crops || 'All Crops'}</strong></span>
                </div>
            </div>
        `).join("");
    } catch (e) {
        container.innerHTML = `<p class="text-rose-500 col-span-full">Failed to load products.</p>`;
    }
}

async function loadNotifications() {
    const listEl = document.getElementById("notifications-list");
    const badgeEl = document.getElementById("notif-unread-badge");
    if (!listEl) return;

    try {
        const notifs = await Api.getNotifications();
        const unreadCount = notifs.filter(n => !n.is_read).length;
        
        if (badgeEl) {
            if (unreadCount > 0) {
                badgeEl.innerText = unreadCount;
                badgeEl.classList.remove("hidden");
            } else {
                badgeEl.classList.add("hidden");
            }
        }

        if (notifs.length === 0) {
            listEl.innerHTML = `<p class="text-slate-400 text-xs text-center py-4">No notifications.</p>`;
            return;
        }

        listEl.innerHTML = notifs.map(n => `
            <div class="p-3 ${n.is_read ? 'bg-white' : 'bg-emerald-50/50'} rounded-xl border border-slate-100 flex items-start gap-2.5">
                <span class="w-2 h-2 rounded-full mt-1.5 ${n.is_read ? 'bg-slate-300' : 'bg-emerald-600'} shrink-0"></span>
                <div class="flex-1">
                    <h6 class="text-xs font-bold text-slate-900">${n.title}</h6>
                    <p class="text-[11px] text-slate-600 mt-0.5 leading-snug">${n.message}</p>
                </div>
            </div>
        `).join("");
    } catch (e) {
        console.warn("Could not load notifications:", e);
    }
}

function setupEventListeners() {
    const recForm = document.getElementById("recommendation-form");
    if (recForm) recForm.addEventListener("submit", generateRecommendations);

    const imageInput = document.getElementById("crop-image-file-input");
    if (imageInput) imageInput.addEventListener("change", handleImageUpload);

    const cameraBtn = document.getElementById("btn-camera-trigger");
    if (cameraBtn && imageInput) {
        cameraBtn.addEventListener("click", () => imageInput.click());
    }
}

function openLoginModal() {
    document.getElementById("login-modal")?.classList.remove("hidden");
}
function closeLoginModal() {
    document.getElementById("login-modal")?.classList.add("hidden");
}
async function handleLoginSubmit(e) {
    e.preventDefault();
    const email = document.getElementById("login-email").value;
    const pass = document.getElementById("login-password").value;

    try {
        const res = await Api.login(email, pass);
        Api.setToken(res.access_token);
        Api.setUser(res.user);
        showToast("Logged in successfully!");
        closeLoginModal();
        checkAuthSession();
        loadInitialData();
    } catch (err) {
        showToast(err.message || "Invalid login credentials", "error");
    }
}
function handleLogout() {
    Api.clearAuth();
    showToast("Logged out");
    checkAuthSession();
}

function openAddFarmModal() {
    document.getElementById("add-farm-modal")?.classList.remove("hidden");
}
function closeAddFarmModal() {
    document.getElementById("add-farm-modal")?.classList.add("hidden");
}
async function handleAddFarmSubmit(e) {
    e.preventDefault();
    const data = {
        farm_name: document.getElementById("new-farm-name").value,
        land_area_acres: parseFloat(document.getElementById("new-farm-area").value || 1),
        state: document.getElementById("new-farm-state").value,
        district: document.getElementById("new-farm-district").value,
        soil_type: document.getElementById("new-farm-soil").value,
        irrigation_type: document.getElementById("new-farm-irrigation").value,
        water_availability: document.getElementById("new-farm-water").value,
        initial_soil: {
            soil_ph: parseFloat(document.getElementById("new-farm-ph").value || 6.8),
            nitrogen_n: parseFloat(document.getElementById("new-farm-n").value || 60),
            phosphorus_p: parseFloat(document.getElementById("new-farm-p").value || 30),
            potassium_k: parseFloat(document.getElementById("new-farm-k").value || 40)
        }
    };

    try {
        await Api.createFarm(data);
        showToast("Farm added successfully!");
        closeAddFarmModal();
        loadFarmerFarms();
        loadFarmsView();
    } catch (err) {
        showToast(err.message || "Failed to add farm", "error");
    }
}

function openAddYardSheetModal() {
    document.getElementById("add-yard-modal")?.classList.remove("hidden");
}
function closeAddYardSheetModal() {
    document.getElementById("add-yard-modal")?.classList.add("hidden");
}
async function handleAddYardSheetSubmit(e) {
    e.preventDefault();
    const data = {
        farm_id: parseInt(document.getElementById("yard-farm-select").value),
        crop_name: document.getElementById("yard-crop-name").value,
        crop_variety: document.getElementById("yard-crop-variety").value,
        cultivated_area_acres: parseFloat(document.getElementById("yard-crop-area").value || 1),
        crop_stage: document.getElementById("yard-crop-stage").value,
        season: document.getElementById("yard-crop-season").value,
        expected_yield_kg: parseFloat(document.getElementById("yard-crop-yield").value || 0)
    };

    try {
        await Api.createYardSheet(data);
        showToast("Yard Sheet record created!");
        closeAddYardSheetModal();
        loadYardSheetsView();
    } catch (err) {
        showToast(err.message || "Failed to create yard sheet", "error");
    }
}
