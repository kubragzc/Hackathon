// HATAY KADIN KOOPERATİFLERİ YÖNETİM SİSTEMİ - PANEL MANTIĞI

document.addEventListener('DOMContentLoaded', () => {
    console.log("Sistem başlatılıyor...");

    // ==========================================
    // Element Selectors
    // ==========================================
    const chatBox = document.getElementById('chat-box');
    const sendBtn = document.getElementById('send-btn');
    const micBtn = document.getElementById('mic-btn');
    const userInput = document.getElementById('user-input');

    const navItems = {
        'nav-dashboard': document.getElementById('dashboard-section'),
        'nav-stock': document.getElementById('stock-section'),
        'nav-orders': document.getElementById('orders-section'),
        'nav-imece': document.getElementById('imece-section'),
        'nav-assistant': document.getElementById('chat-section')
    };

    // ==========================================
    // Navigation & Tab Management
    // ==========================================
    function switchTab(clickedId) {
        console.log("Sekme değiştiriliyor:", clickedId);
        Object.keys(navItems).forEach(id => {
            const navLink = document.getElementById(id);
            const section = navItems[id];
            
            if (id === clickedId) {
                navLink.className = 'flex items-center gap-3 bg-primary-container text-white rounded-r-full font-bold py-3 px-6 my-1 transition-all nav-item active';
                section.classList.remove('hidden');
            } else {
                navLink.className = 'flex items-center gap-3 text-on-surface-variant hover:text-primary py-3 px-6 my-1 transition-colors hover:bg-surface-container-high rounded-r-full nav-item';
                section.classList.add('hidden');
            }
        });

        if (clickedId === 'nav-orders') loadLogistics();
        if (clickedId === 'nav-stock') loadEnvanter();
        if (clickedId === 'nav-imece') loadImeceNetwork();
    }

    Object.keys(navItems).forEach(id => {
        const el = document.getElementById(id);
        if (el) {
            el.addEventListener('click', (e) => {
                e.preventDefault();
                switchTab(id);
            });
        }
    });

    // ==========================================
    // AI Assistant (Chat) Logic
    // ==========================================
    function addMessage(text, sender) {
        if (!chatBox) return;
        const isAi = sender === 'ai';
        const messageDiv = document.createElement('div');
        messageDiv.className = `flex items-start gap-4 ${isAi ? 'max-w-[85%]' : 'max-w-[85%] ml-auto flex-row-reverse'}`;

        const iconHtml = isAi 
            ? `<div class="w-10 h-10 rounded-full bg-gradient-to-br from-secondary to-primary p-0.5 shrink-0 shadow-lg">
                 <div class="w-full h-full rounded-full bg-white flex items-center justify-center overflow-hidden">
                    <span class="material-symbols-outlined text-primary text-[20px]">psychology</span>
                 </div>
               </div>`
            : `<div class="w-10 h-10 rounded-full overflow-hidden shrink-0 border-2 border-primary/20 shadow-lg">
                 <img src="https://ui-avatars.com/api/?name=Ayşe+Yılmaz&background=4CAF50&color=fff" class="w-full h-full object-cover">
               </div>`;

        const contentHtml = `
            <div class="${isAi ? 'glass-card p-6 rounded-2xl rounded-tl-none shadow-sm' : 'bg-primary p-6 rounded-2xl rounded-tr-none shadow-xl shadow-primary/10 text-white'}">
                <p class="font-serif italic text-lg leading-relaxed">${text.replace(/\n/g, '<br>').replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')}</p>
            </div>
        `;

        messageDiv.innerHTML = iconHtml + contentHtml;
        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    async function sendMessage(customText = null) {
        const text = customText || userInput.value.trim();
        if (!text) return;

        addMessage(text, 'user');
        if (!customText) userInput.value = '';
        
        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: text })
            });
            const data = await response.json();
            addMessage(data.reply, 'ai');
        } catch (e) { addMessage("Sistem şu an yanıt veremiyor, lütfen daha sonra tekrar deneyiniz.", 'ai'); }
    }

    if (sendBtn) sendBtn.addEventListener('click', () => sendMessage());
    if (userInput) userInput.addEventListener('keypress', (e) => { if (e.key === 'Enter') sendMessage(); });

    // ==========================================
    // Dashboard & Global Actions
    // ==========================================
    const btnStartOps = document.getElementById('btn-start-ops');
    const btnDetailedReport = document.getElementById('btn-detailed-report');
    const otonomToggle = document.getElementById('otonom-toggle');
    const otonomDot = document.getElementById('otonom-dot');
    const globalFab = document.getElementById('global-fab');

    if (btnStartOps) {
        btnStartOps.addEventListener('click', () => {
            console.log("Operasyon başlatılıyor...");
            switchTab('nav-assistant');
            sendMessage("Tüm kooperatif operasyonlarını başlat ve bugünkü kritik onayları benim için incele.");
        });
    }

    if (btnDetailedReport) {
        btnDetailedReport.addEventListener('click', () => {
            switchTab('nav-orders');
        });
    }

    let otonomActive = true;
    if (otonomToggle && otonomDot) {
        otonomToggle.addEventListener('click', () => {
            otonomActive = !otonomActive;
            console.log("Otonom Mod Değişti:", otonomActive);
            if (otonomActive) {
                otonomDot.classList.remove('mr-auto');
                otonomDot.classList.add('ml-auto');
                otonomToggle.classList.replace('bg-outline-variant', 'bg-primary/20');
                addMessage("Akıllı Yönetim Sistemi aktif edildi. Tüm lojistik rotalar sistem tarafından optimize ediliyor.", 'ai');
            } else {
                otonomDot.classList.remove('ml-auto');
                otonomDot.classList.add('mr-auto');
                otonomToggle.classList.replace('bg-primary/20', 'bg-outline-variant');
                addMessage("Akıllı mod devre dışı. Sistem manuel kontrol moduna geçti.", 'ai');
            }
        });
    }

    if (globalFab) {
        globalFab.addEventListener('click', () => {
            switchTab('nav-assistant');
            sendMessage("Yeni bir kayıt (ürün, sipariş veya üye) eklemek istiyorum.");
        });
    }

    // ==========================================
    // Data Loading (Logistics & Stock)
    // ==========================================
    async function loadLogistics() {
        try {
            const res = await fetch('/api/orders');
            const orders = await res.json();
            const tbody = document.getElementById('orders-table-body');
            if (!tbody) return;
            tbody.innerHTML = '';

            orders.forEach(order => {
                const tr = document.createElement('tr');
                tr.className = 'hover:bg-surface-container-low transition-colors group border-b border-outline-variant/5';
                
                let statusBadge = '';
                if (order.status === 'Hazırlanıyor' || order.status === 'Yeni') statusBadge = '<span class="px-3 py-1 bg-secondary/10 text-secondary rounded-full text-[10px] font-bold">HAZIRLANIYOR</span>';
                else if (order.status === 'Kargoya Verildi') statusBadge = '<span class="px-3 py-1 bg-primary/10 text-primary rounded-full text-[10px] font-bold">YOLDA</span>';
                else statusBadge = '<span class="px-3 py-1 bg-surface-container-high text-on-surface-variant rounded-full text-[10px] font-bold">TESLİM EDİLDİ</span>';

                tr.innerHTML = `
                    <td class="p-6 font-bold text-primary text-xs">#ORD-${order.id}</td>
                    <td class="p-6">
                        <div class="flex items-center gap-2">
                            <span class="material-symbols-outlined text-on-surface-variant text-sm">location_on</span>
                            <span class="text-sm font-medium">${order.customer.name}</span>
                        </div>
                    </td>
                    <td class="p-6">${statusBadge}</td>
                    <td class="p-6 text-xs text-on-surface-variant">${new Date(order.order_date).toLocaleDateString('tr-TR')}</td>
                    <td class="p-6">
                        <button onclick="updateOrderStatus(${order.id}, 'Kargoya Verildi')" class="text-[10px] font-bold text-secondary hover:underline">GÜNCELLE</button>
                    </td>
                `;
                tbody.appendChild(tr);
            });
        } catch (e) { console.error("Lojistik yükleme hatası:", e); }
    }

    async function loadEnvanter() {
        try {
            const res = await fetch('/api/stock');
            const stocks = await res.json();
            const stockList = document.getElementById('stock-list');
            if (!stockList) return;
            stockList.innerHTML = '';

            stocks.forEach(item => {
                const isCritical = item.stock < 20;
                const card = document.createElement('div');
                card.className = 'glass-card rounded-xl overflow-hidden flex flex-col group transition-transform hover:-translate-y-1';
                
                const progressColor = isCritical ? 'bg-error' : 'bg-primary';
                const badge = isCritical 
                    ? '<div class="absolute top-4 right-4 bg-error text-white px-3 py-1 rounded-full text-[10px] font-bold">KRİTİK</div>'
                    : '<div class="absolute top-4 right-4 bg-primary text-white px-3 py-1 rounded-full text-[10px] font-bold">NORMAL</div>';

                card.innerHTML = `
                    <div class="h-32 bg-cover bg-center relative" style="background-image: url('https://ui-avatars.com/api/?name=${item.name}&background=random&color=fff&size=512')">
                        ${badge}
                    </div>
                    <div class="p-6 space-y-4">
                        <div class="flex justify-between items-start">
                            <div>
                                <h4 class="font-serif text-xl text-primary font-bold">${item.name}</h4>
                                <p class="text-[10px] uppercase tracking-widest text-on-surface-variant font-bold">${item.category}</p>
                            </div>
                            <div class="text-right">
                                <p class="text-[10px] text-on-surface-variant font-bold">STOK</p>
                                <p class="font-serif text-lg font-bold">${item.stock} Birim</p>
                            </div>
                        </div>
                        <div class="w-full bg-surface-container rounded-full h-1.5 overflow-hidden">
                            <div class="${progressColor} h-full" style="width: ${Math.min(100, item.stock)}%"></div>
                        </div>
                        <div class="flex justify-between gap-2 pt-2">
                            <button class="flex-1 bg-primary text-white py-2.5 rounded-full text-[10px] font-bold hover:opacity-90 transition-all prod-btn" data-name="${item.name}">ÜRETİM TASLAĞI</button>
                            <button class="p-2.5 border border-outline-variant rounded-full text-on-surface-variant hover:bg-surface-container transition-colors hub-btn" data-name="${item.name}" data-stock="${item.stock}">
                                <span class="material-symbols-outlined text-[18px]">hub</span>
                            </button>
                        </div>
                    </div>
                `;
                stockList.appendChild(card);
            });

            // Re-bind dynamic buttons
            document.querySelectorAll('.prod-btn').forEach(btn => {
                btn.addEventListener('click', () => {
                    switchTab('nav-assistant');
                    sendMessage(`${btn.dataset.name} üretimi için planlama başlatılsın.`);
                });
            });
            document.querySelectorAll('.hub-btn').forEach(btn => {
                btn.addEventListener('click', () => {
                    switchTab('nav-assistant');
                    sendMessage(`${btn.dataset.name} stoğu yetersiz (${btn.dataset.stock}). İmece Ağı'ndan çözüm bul.`);
                });
            });

        } catch (e) { console.error("Envanter yükleme hatası:", e); }
    }

    window.updateOrderStatus = async function(id, status) {
        await fetch(`/api/orders/${id}/status`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ status })
        });
        loadLogistics();
    };

    window.downloadExcelReport = () => { window.location.href = '/api/reports/excel'; };

    // ==========================================
    // Dashboard & Stats Loading
    // ==========================================
    async function loadDashboardStats() {
        try {
            const res = await fetch('/api/dashboard-stats');
            const stats = await res.json();
            
            const effEl = document.getElementById('stat-efficiency');
            const capTextEl = document.getElementById('stat-capacity-text');
            const capBarEl = document.getElementById('stat-capacity-bar');
            const morningBrief = document.getElementById('morning-brief');

            // Calculate mock efficiency and capacity based on real counts
            const total = stats.total_orders || 0;
            const delivered = stats.delivered_orders || 0;
            const shipped = stats.shipped_orders || 0;
            const efficiency = total > 0 ? Math.round(((delivered + shipped) / total) * 100) : 98;
            const capacity = 70 + Math.floor(Math.random() * 25); // Simulating load

            if (effEl) effEl.innerText = `Verimlilik: %${efficiency}`;
            if (capTextEl) capTextEl.innerText = `%${capacity}`;
            if (capBarEl) capBarEl.style.width = `${capacity}%`;

            if (morningBrief && total > 0) {
                morningBrief.innerHTML = `"Bugün sistemde toplam <strong>${total}</strong> sipariş yönetiliyor. <strong>${stats.shipped_orders}</strong> sipariş yolda, <strong>${stats.preparing_orders}</strong> sipariş paketleme kuyruğunda bekliyor. Tüm operasyonlar optimize edildi."`;
            }
            initSalesChart();
        } catch (e) { console.error("Stats yükleme hatası:", e); }
    }

    let salesChart = null;
    async function initSalesChart() {
        try {
            const res = await fetch('/api/analytics/chart-data');
            const data = await res.json();
            const ctx = document.getElementById('salesChart');
            if (!ctx) return;

            if (salesChart) salesChart.destroy();

            salesChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: 'Sipariş Sayısı',
                        data: data.values,
                        borderColor: '#154212',
                        backgroundColor: 'rgba(21, 66, 18, 0.1)',
                        fill: true,
                        tension: 0.4,
                        borderWidth: 3,
                        pointBackgroundColor: '#154212',
                        pointRadius: 4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            grid: { color: 'rgba(0,0,0,0.05)' },
                            ticks: { font: { family: 'Inter' } }
                        },
                        x: {
                            grid: { display: false },
                            ticks: { font: { family: 'Inter' } }
                        }
                    }
                }
            });
        } catch (e) { console.error("Chart yükleme hatası:", e); }
    }

    async function loadImeceNetwork() {
        try {
            const res = await fetch('/api/imece/network');
            const network = await res.json();
            const imeceList = document.getElementById('imece-network-list');
            if (!imeceList) return;
            imeceList.innerHTML = '';

            network.forEach(item => {
                const card = document.createElement('div');
                card.className = 'glass-card p-8 rounded-3xl flex flex-col gap-6 hover:shadow-2xl transition-all border-none bg-white/40';
                
                card.innerHTML = `
                    <div class="flex items-center gap-4">
                        <img src="${item.image}" class="w-16 h-16 rounded-2xl shadow-lg">
                        <div>
                            <h4 class="font-serif text-xl text-primary font-bold">${item.name}</h4>
                            <p class="text-xs text-on-surface-variant flex items-center gap-1">
                                <span class="material-symbols-outlined text-sm">location_on</span> ${item.location}
                            </p>
                        </div>
                    </div>
                    <div class="space-y-3">
                        <p class="text-[10px] font-bold text-secondary uppercase tracking-widest">Paylaşıma Açık Kaynaklar</p>
                        <div class="flex flex-wrap gap-2">
                            ${item.resources.map(r => `<span class="px-3 py-1 bg-secondary/10 text-secondary text-[10px] rounded-full font-bold">${r}</span>`).join('')}
                        </div>
                    </div>
                    <div class="pt-4 border-t border-outline-variant/10 flex justify-between items-center">
                        <div>
                            <p class="text-[9px] text-on-surface-variant font-bold uppercase">Sorumlu</p>
                            <p class="text-xs font-bold text-primary">${item.contact}</p>
                        </div>
                        <button onclick="switchTab('nav-assistant'); sendMessage('${item.name} ile ${item.resources[0]} için iletişime geçmek istiyorum.')" class="bg-primary text-white px-4 py-2 rounded-xl text-[10px] font-bold hover:scale-105 transition-transform">TALEP ET</button>
                    </div>
                `;
                imeceList.appendChild(card);
            });
        } catch (e) { console.error("Imece yükleme hatası:", e); }
    }

    // Initial load
    loadDashboardStats();
    loadEnvanter(); // Pre-load stock

    // Initial AI Welcome Message
    setTimeout(() => {
        addMessage("Hoş geldiniz Ayşe Hanım. Hatay Kolektifi operasyonları bugün verimlilikle devam ediyor. Sistem, Samandağ yolundaki yoğunluk için sevkiyatları güncelledi. Diğer kooperatiflerin stok durumunu kontrol etmemi ister misiniz?", 'ai');
    }, 1000);
});
