// Admin Dashboard & Management Controller
let analyticsChart = null;

document.addEventListener("DOMContentLoaded", async () => {
    checkAdminAuth();
    bindAdminNav();
    await loadAdminDashboard();
});

function checkAdminAuth() {
    const user = Api.getUser();
    const token = Api.getToken();

    if (!token || !user || user.role !== "admin") {
        openAdminLoginModal();
    } else {
        const emailEl = document.getElementById("admin-user-email");
        if (emailEl) emailEl.innerText = user.email;
        closeAdminLoginModal();
    }
}

function openAdminLoginModal() {
    document.getElementById("admin-login-modal")?.classList.remove("hidden");
}
function closeAdminLoginModal() {
    document.getElementById("admin-login-modal")?.classList.add("hidden");
}

async function handleAdminLogin(e) {
    e.preventDefault();
    const email = document.getElementById("admin-login-email").value;
    const pass = document.getElementById("admin-login-password").value;

    try {
        const res = await Api.login(email, pass);
        if (res.user.role !== "admin") {
            throw new Error("Access Denied: This account is not an administrator.");
        }
        Api.setToken(res.access_token);
        Api.setUser(res.user);
        showToast("Admin authenticated successfully!");
        closeAdminLoginModal();
        checkAdminAuth();
        loadAdminDashboard();
    } catch (err) {
        showToast(err.message, "error");
    }
}

function handleAdminLogout() {
    Api.clearAuth();
    window.location.reload();
}

function bindAdminNav() {
    document.querySelectorAll("[data-admin-tab]").forEach(btn => {
        btn.addEventListener("click", () => {
            const target = btn.getAttribute("data-admin-tab");
            switchAdminTab(target);
        });
    });
}

function switchAdminTab(tabId) {
    document.querySelectorAll(".admin-tab-content").forEach(sec => sec.classList.add("hidden"));
    document.getElementById(`admin-tab-${tabId}`)?.classList.remove("hidden");

    document.querySelectorAll("[data-admin-tab]").forEach(btn => {
        if (btn.getAttribute("data-admin-tab") === tabId) {
            btn.classList.add("bg-emerald-600", "text-white");
            btn.classList.remove("text-slate-400", "hover:bg-slate-800");
        } else {
            btn.classList.remove("bg-emerald-600", "text-white");
            btn.classList.add("text-slate-400", "hover:bg-slate-800");
        }
    });

    if (tabId === "dashboard") loadAdminDashboard();
    if (tabId === "farmers") loadAdminFarmers();
    if (tabId === "policies") loadAdminPolicies();
    if (tabId === "products") loadAdminProducts();
    if (tabId === "audits") loadAdminAuditLogs();
}

async function loadAdminDashboard() {
    try {
        const data = await Api.getDashboardAnalytics();
        
        // Update KPIs
        document.getElementById("kpi-admin-farmers").innerText = data.total_farmers;
        document.getElementById("kpi-admin-farms").innerText = data.total_farms;
        document.getElementById("kpi-admin-acreage").innerText = `${data.total_acreage} Ac`;
        document.getElementById("kpi-admin-scans").innerText = data.total_ml_predictions;

        // Render Chart.js
        renderCropChart(data.crops_distribution);

        // Render Recent Predictions
        const predEl = document.getElementById("admin-recent-preds");
        if (predEl) {
            predEl.innerHTML = data.recent_predictions.map(p => `
                <div class="p-3 bg-slate-800/80 rounded-xl border border-slate-700/60 flex items-center justify-between text-xs">
                    <div>
                        <span class="font-bold text-white">${p.disease}</span>
                        <span class="text-slate-400 block">${p.crop || 'Crop'} • ${p.date}</span>
                    </div>
                    <span class="text-emerald-400 font-bold bg-emerald-950/80 px-2 py-1 rounded-md">${p.confidence}</span>
                </div>
            `).join("");
        }

        // Render Recent Farmer Activity
        const actEl = document.getElementById("admin-recent-activity");
        if (actEl) {
            actEl.innerHTML = data.recent_farmer_activity.map(a => `
                <div class="p-3 bg-slate-800/80 rounded-xl border border-slate-700/60 flex items-center justify-between text-xs">
                    <div>
                        <span class="font-bold text-white">${a.name}</span>
                        <span class="text-slate-400 block">${a.district}, ${a.state} • ${a.date}</span>
                    </div>
                    <span class="text-blue-400 font-semibold">${a.action}</span>
                </div>
            `).join("");
        }

    } catch (e) {
        console.warn("Failed to load dashboard analytics:", e);
    }
}

function renderCropChart(dist) {
    const ctx = document.getElementById("cropDistributionChart");
    if (!ctx) return;

    if (analyticsChart) {
        analyticsChart.destroy();
    }

    const labels = Object.keys(dist);
    const values = Object.values(dist);

    analyticsChart = new Chart(ctx, {
        type: "doughnut",
        data: {
            labels: labels.length ? labels : ["Cotton", "Wheat", "Tomato", "Groundnut"],
            datasets: [{
                data: values.length ? values : [4, 3, 2, 2],
                backgroundColor: ["#10b981", "#3b82f6", "#f59e0b", "#8b5cf6", "#ec4899", "#06b6d4"]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: "bottom", labels: { color: "#cbd5e1" } }
            }
        }
    });
}

// Admin Farmers Table
async function loadAdminFarmers() {
    const tableBody = document.getElementById("admin-farmers-table-body");
    if (!tableBody) return;

    try {
        const farmers = await Api.getAdminFarmers();
        tableBody.innerHTML = farmers.map(f => `
            <tr class="border-b border-slate-700/60 hover:bg-slate-800/40 text-xs">
                <td class="py-3.5 px-4 font-bold text-white">${f.id}</td>
                <td class="py-3.5 px-4 font-medium text-slate-200">
                    <span class="block font-bold">${f.profile?.full_name || 'N/A'}</span>
                    <span class="text-slate-400 text-[11px]">${f.email} • ${f.phone || ''}</span>
                </td>
                <td class="py-3.5 px-4 text-slate-300">${f.profile?.district || 'N/A'}, ${f.profile?.state || 'N/A'}</td>
                <td class="py-3.5 px-4">
                    <span class="px-2.5 py-1 rounded-full font-bold ${f.is_active ? 'bg-emerald-900/60 text-emerald-300' : 'bg-rose-900/60 text-rose-300'}">
                        ${f.is_active ? 'Active' : 'Disabled'}
                    </span>
                </td>
                <td class="py-3.5 px-4">
                    <button onclick="toggleFarmerStatus(${f.id}, ${!f.is_active})" class="px-3 py-1 bg-slate-700 hover:bg-slate-600 rounded-lg text-white font-bold transition">
                        ${f.is_active ? 'Deactivate' : 'Activate'}
                    </button>
                </td>
            </tr>
        `).join("");
    } catch (e) {
        showToast("Failed to load farmers: " + e.message, "error");
    }
}

async function toggleFarmerStatus(userId, status) {
    try {
        await Api.toggleFarmerStatus(userId, status);
        showToast("Farmer status updated");
        loadAdminFarmers();
        loadAdminAuditLogs();
    } catch (e) {
        showToast(e.message, "error");
    }
}

// Policies Management
async function loadAdminPolicies() {
    const listEl = document.getElementById("admin-policies-list");
    if (!listEl) return;

    try {
        const policies = await Api.getPolicies();
        listEl.innerHTML = policies.map(p => `
            <div class="p-4 bg-slate-800/80 rounded-xl border border-slate-700/60 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
                <div>
                    <div class="flex items-center gap-2">
                        <span class="text-[10px] bg-blue-900/80 text-blue-300 px-2 py-0.5 rounded font-bold uppercase">${p.category}</span>
                        <span class="text-xs text-slate-400 font-semibold">${p.applicable_state}</span>
                    </div>
                    <h4 class="text-sm font-extrabold text-white mt-1">${p.title}</h4>
                    <p class="text-xs text-slate-300 mt-1 line-clamp-2">${p.description}</p>
                </div>
                <div class="flex items-center gap-2 shrink-0">
                    <button onclick="deletePolicy(${p.id})" class="px-3 py-1.5 bg-rose-600/80 hover:bg-rose-600 text-white rounded-lg text-xs font-bold transition">
                        Delete
                    </button>
                </div>
            </div>
        `).join("");
    } catch (e) {
        showToast("Failed to load policies", "error");
    }
}

function openAddPolicyModal() {
    document.getElementById("add-policy-modal")?.classList.remove("hidden");
}
function closeAddPolicyModal() {
    document.getElementById("add-policy-modal")?.classList.add("hidden");
}

async function handleAddPolicySubmit(e) {
    e.preventDefault();
    const data = {
        title: document.getElementById("pol-title").value,
        scheme_name: document.getElementById("pol-scheme-name").value,
        category: document.getElementById("pol-category").value,
        applicable_state: document.getElementById("pol-state").value,
        description: document.getElementById("pol-desc").value,
        eligibility_criteria: document.getElementById("pol-eligibility").value,
        benefits: document.getElementById("pol-benefits").value,
        official_portal_url: document.getElementById("pol-url").value
    };

    try {
        await Api.createPolicy(data);
        showToast("Government policy added & audit logged!");
        closeAddPolicyModal();
        loadAdminPolicies();
    } catch (err) {
        showToast(err.message, "error");
    }
}

async function deletePolicy(id) {
    if (!confirm("Are you sure you want to delete this government policy? This action is audited.")) return;
    try {
        await Api.deletePolicy(id);
        showToast("Policy deleted and audit record created");
        loadAdminPolicies();
    } catch (e) {
        showToast(e.message, "error");
    }
}

// Products Management
async function loadAdminProducts() {
    const listEl = document.getElementById("admin-products-list");
    if (!listEl) return;

    try {
        const prods = await Api.getProducts();
        listEl.innerHTML = prods.map(p => `
            <div class="p-4 bg-slate-800/80 rounded-xl border border-slate-700/60 flex items-center justify-between text-xs">
                <div>
                    <span class="text-[10px] bg-emerald-900/80 text-emerald-300 font-bold px-2 py-0.5 rounded uppercase">${p.category}</span>
                    <h5 class="font-extrabold text-white text-sm mt-1">${p.name}</h5>
                    <p class="text-slate-400 mt-0.5">${p.dosage_instructions}</p>
                </div>
                <button onclick="deleteProduct(${p.id})" class="px-3 py-1.5 bg-rose-600/80 hover:bg-rose-600 text-white rounded-lg font-bold transition">
                    Delete
                </button>
            </div>
        `).join("");
    } catch (e) {
        showToast("Failed to load products", "error");
    }
}

function openAddProductModal() {
    document.getElementById("add-product-modal")?.classList.remove("hidden");
}
function closeAddProductModal() {
    document.getElementById("add-product-modal")?.classList.add("hidden");
}
async function handleAddProductSubmit(e) {
    e.preventDefault();
    const data = {
        name: document.getElementById("prod-name").value,
        category: document.getElementById("prod-category").value,
        manufacturer: document.getElementById("prod-mfr").value,
        active_ingredient: document.getElementById("prod-ai").value,
        dosage_instructions: document.getElementById("prod-dosage").value,
        price_estimate: document.getElementById("prod-price").value,
        suitable_crops: document.getElementById("prod-crops").value
    };

    try {
        await Api.createProduct(data);
        showToast("Product added and audit log generated!");
        closeAddProductModal();
        loadAdminProducts();
    } catch (err) {
        showToast(err.message, "error");
    }
}

async function deleteProduct(id) {
    if (!confirm("Are you sure you want to delete this product?")) return;
    try {
        await Api.deleteProduct(id);
        showToast("Product removed");
        loadAdminProducts();
    } catch (e) {
        showToast(e.message, "error");
    }
}

// Admin Audit Logs Viewer
async function loadAdminAuditLogs() {
    const tableBody = document.getElementById("admin-audit-table-body");
    if (!tableBody) return;

    try {
        const logs = await Api.getAuditLogs();
        tableBody.innerHTML = logs.map(l => {
            const actionBadge = l.action === "CREATE" ? "bg-emerald-900/60 text-emerald-300" :
                               (l.action === "UPDATE" ? "bg-blue-900/60 text-blue-300" : "bg-rose-900/60 text-rose-300");
            return `
                <tr class="border-b border-slate-700/60 hover:bg-slate-800/40 text-xs">
                    <td class="py-3 px-4 text-slate-400">${l.created_at?.replace("T", " ").slice(0, 19)}</td>
                    <td class="py-3 px-4 font-bold text-white">${l.admin_email}</td>
                    <td class="py-3 px-4 font-semibold text-slate-300">${l.entity_type} (#${l.entity_id || 'N/A'})</td>
                    <td class="py-3 px-4">
                        <span class="px-2.5 py-0.5 rounded-md font-extrabold ${actionBadge}">${l.action}</span>
                    </td>
                    <td class="py-3 px-4 text-slate-200">${l.description}</td>
                </tr>
            `;
        }).join("");
    } catch (e) {
        console.warn("Could not load audit logs:", e);
    }
}
