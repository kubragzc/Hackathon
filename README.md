# Coop-AI: KOBİ & Kooperatif Akıllı Operasyon Sistemi

**Coop-AI**, küçük ve orta ölçekli işletmeler (KOBİ) ile kooperatiflerin manuel yürütülen karmaşık operasyonlarını akıllı algoritmalar ile otomatiğe bağlayan uçtan uca bir yönetim sistemidir.

## 🚀 Problem Tanımı
Geleneksel KOBİ ve kooperatifler; sipariş takibi, stok kontrolü, kargo gecikmeleri ve müşteri soruları gibi süreçleri manuel (e-posta, telefon, Excel) yönetmektedir. Bu durum:
- Günde 2-3 saatlik iş gücü kaybına,
- Stok tükenmesi nedeniyle müşteri kaybına,
- Kargo gecikmelerinin fark edilmemesine neden olmaktadır.

**Coop-AI**, bu süreçleri merkezi bir yönetim paneli ve akıllı asistan ile otonom hale getirir.

## 🛠️ Teknik Mimari
Sistem modern ve modüler bir yapıda tasarlanmıştır:
- **Backend:** Python & FastAPI
- **Veritabanı:** SQLite & SQLAlchemy ORM
- **Zeka Katmanı:** Google Gemini (Function Calling destekli)
- **Frontend:** HTML5, Tailwind CSS, Vanilla JS (Bento Grid Tasarımı)

## 🧠 Temel Özellikler
Sistem, aşağıdaki araçları kullanarak operasyonu yönetir:
1. **Akıllı Stok Yönetimi:** Stok kritik eşiğin altına düştüğünde uyarı mekanizmalarını tetikler.
2. **Kargo Gecikme Tespiti:** Teslimat süresi geçen siparişleri otomatik tespit eder ve raporlar.
3. **Müşteri İçgörüleri:** Gelen mesajları analiz ederek hangi ürünlerin talep gördüğünü raporlar.
4. **Finansal Analiz:** Gelir, gider ve borç durumunu analiz ederek nakit akışı özeti sunar.

## 📦 Kurulum ve Çalıştırma

1. **Bağımlılıkları Yükleyin:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Çevresel Değişkenleri Ayarlayın (.env):**
   ```env
   GEMINI_API_KEY=your_api_key
   ```
3. **Örnek Verileri Oluşturun:**
   ```bash
   python scripts/generate_synthetic_data.py
   ```
4. **Sunucuyu Başlatın:**
   ```bash
   uvicorn backend.main:app --reload
   ```

## 🎯 Hedef Kitle
- E-ticaret işletmeleri
- Bölgesel üretim yapan kadın kooperatifleri
- Butik firmalar

---
*Bu proje Kübra Gezici tarafından Google Academy 2026 Hackathon'u  için geliştirilmiştir.*

