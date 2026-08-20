// Unified API Client with JWT Bearer Token Injection
const API_BASE = "";

const Api = {
    getToken() {
        return localStorage.getItem("smart_crop_token");
    },
    setToken(token) {
        localStorage.setItem("smart_crop_token", token);
    },
    getUser() {
        try {
            return JSON.parse(localStorage.getItem("smart_crop_user"));
        } catch {
            return null;
        }
    },
    setUser(user) {
        localStorage.setItem("smart_crop_user", JSON.stringify(user));
    },
    clearAuth() {
        localStorage.removeItem("smart_crop_token");
        localStorage.removeItem("smart_crop_user");
    },

    async request(endpoint, options = {}) {
        const headers = options.headers || {};
        const token = this.getToken();

        if (token && !headers["Authorization"]) {
            headers["Authorization"] = `Bearer ${token}`;
        }

        if (!(options.body instanceof FormData) && !headers["Content-Type"]) {
            headers["Content-Type"] = "application/json";
        }

        options.headers = headers;

        try {
            const resp = await fetch(`${API_BASE}${endpoint}`, options);
            if (resp.status === 401) {
                // If unauthorized, clear auth and redirect to login if needed
                console.warn("Session expired or unauthorized request.");
            }
            if (!resp.ok) {
                const errData = await resp.json().catch(() => ({ detail: resp.statusText }));
                throw new Error(errData.detail || "Request failed");
            }
            if (resp.status === 204) return null;
            return await resp.json();
        } catch (err) {
            console.error(`API Error on ${endpoint}:`, err);
            throw err;
        }
    },

    // Auth
    login(email, password) {
        return this.request("/api/auth/login", {
            method: "POST",
            body: JSON.stringify({ email, password })
        });
    },
    register(userData) {
        return this.request("/api/auth/register", {
            method: "POST",
            body: JSON.stringify(userData)
        });
    },
    getProfile() {
        return this.request("/api/auth/profile");
    },
    updateProfile(data) {
        return this.request("/api/auth/profile", {
            method: "PUT",
            body: JSON.stringify(data)
        });
    },

    // Farms
    getFarms() {
        return this.request("/api/farms/");
    },
    createFarm(farmData) {
        return this.request("/api/farms/", {
            method: "POST",
            body: JSON.stringify(farmData)
        });
    },
    addSoilRecord(farmId, soilData) {
        return this.request(`/api/farms/${farmId}/soil`, {
            method: "POST",
            body: JSON.stringify(soilData)
        });
    },

    // Yard Sheets
    getYardSheets() {
        return this.request("/api/yard-sheets/");
    },
    createYardSheet(sheetData) {
        return this.request("/api/yard-sheets/", {
            method: "POST",
            body: JSON.stringify(sheetData)
        });
    },
    updateYardSheetStage(sheetId, stageData) {
        return this.request(`/api/yard-sheets/${sheetId}/stage`, {
            method: "PATCH",
            body: JSON.stringify(stageData)
        });
    },

    // Recommendations
    getRecommendations(reqData) {
        return this.request("/api/recommendations/generate", {
            method: "POST",
            body: JSON.stringify(reqData)
        });
    },

    // Weather
    getWeather(lat, lon, district) {
        return this.request(`/api/weather/current?lat=${lat}&lon=${lon}&district=${encodeURIComponent(district)}`);
    },
    getFarmWeather(farmId) {
        return this.request(`/api/weather/farm/${farmId}`);
    },

    // ML Disease Vision
    uploadCropScan(formData) {
        return this.request("/api/disease-diagnosis/upload", {
            method: "POST",
            body: formData
        });
    },
    getScanHistory() {
        return this.request("/api/disease-diagnosis/history");
    },

    // Catalog & Policies
    getDiseases(crop, search) {
        let q = [];
        if (crop) q.push(`crop=${encodeURIComponent(crop)}`);
        if (search) q.push(`search=${encodeURIComponent(search)}`);
        return this.request(`/api/catalog/diseases?${q.join("&")}`);
    },
    getProducts(category, crop, search) {
        let q = [];
        if (category) q.push(`category=${encodeURIComponent(category)}`);
        if (crop) q.push(`crop=${encodeURIComponent(crop)}`);
        if (search) q.push(`search=${encodeURIComponent(search)}`);
        return this.request(`/api/catalog/products?${q.join("&")}`);
    },
    getPolicies(state, crop, category, search) {
        let q = [];
        if (state) q.push(`state=${encodeURIComponent(state)}`);
        if (crop) q.push(`crop=${encodeURIComponent(crop)}`);
        if (category) q.push(`category=${encodeURIComponent(category)}`);
        if (search) q.push(`search=${encodeURIComponent(search)}`);
        return this.request(`/api/policies/?${q.join("&")}`);
    },

    // Notifications
    getNotifications() {
        return this.request("/api/notifications/");
    },
    markNotificationRead(id) {
        return this.request(`/api/notifications/${id}/read`, { method: "PATCH" });
    },
    markAllNotificationsRead() {
        return this.request("/api/notifications/read-all", { method: "POST" });
    },

    // Admin
    getDashboardAnalytics() {
        return this.request("/api/analytics/dashboard");
    },
    getAdminFarmers() {
        return this.request("/api/admin/farmers");
    },
    toggleFarmerStatus(userId, isActive) {
        return this.request(`/api/admin/farmers/${userId}/status?is_active=${isActive}`, { method: "PATCH" });
    },
    createPolicy(data) {
        return this.request("/api/admin/policies", { method: "POST", body: JSON.stringify(data) });
    },
    updatePolicy(id, data) {
        return this.request(`/api/admin/policies/${id}`, { method: "PUT", body: JSON.stringify(data) });
    },
    deletePolicy(id) {
        return this.request(`/api/admin/policies/${id}`, { method: "DELETE" });
    },
    createProduct(data) {
        return this.request("/api/admin/products", { method: "POST", body: JSON.stringify(data) });
    },
    updateProduct(id, data) {
        return this.request(`/api/admin/products/${id}`, { method: "PUT", body: JSON.stringify(data) });
    },
    deleteProduct(id) {
        return this.request(`/api/admin/products/${id}`, { method: "DELETE" });
    },
    getAuditLogs() {
        return this.request("/api/admin/audit-logs");
    }
};

// UI Toast Notification Helper
function showToast(msg, type = "success") {
    const container = document.getElementById("toast-container");
    if (!container) return;
    const toast = document.createElement("div");
    const bgClass = type === "success" ? "bg-emerald-600" : (type === "error" ? "bg-rose-600" : "bg-blue-600");
    toast.className = `${bgClass} text-white px-5 py-3 rounded-xl shadow-lg flex items-center gap-3 text-sm font-medium transition-all duration-300 transform translate-y-2 opacity-0`;
    toast.innerHTML = `<span>${msg}</span>`;
    container.appendChild(toast);

    setTimeout(() => {
        toast.classList.remove("translate-y-2", "opacity-0");
    }, 10);

    setTimeout(() => {
        toast.classList.add("opacity-0", "translate-y-2");
        setTimeout(() => toast.remove(), 300);
    }, 3500);
}
