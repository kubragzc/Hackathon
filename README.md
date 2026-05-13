# Coop-Panel: KOBİ & Kooperatif Akıllı Yönetim Portalı

**Coop-Panel**, küçük ve orta ölçekli işletmeler (KOBİ) ile kooperatiflerin manuel yürütülen karmaşık operasyonlarını akıllı algoritmalar ve merkezi bir yönetim anlayışı ile otomatiğe bağlayan uçtan uca bir yönetim sistemidir. Özellikle bölgesel üretim yapan kooperatiflerin dijitalleşmesi ve operasyonel verimliliklerinin artırılması hedeflenmiştir.

## 🚀 Problem Tanımı
Geleneksel KOBİ ve kooperatifler; sipariş takibi, stok kontrolü, kargo gecikmeleri ve müşteri soruları gibi süreçleri manuel (e-posta, telefon, Excel) yönetmektedir. Bu durum:
- Günde 2-3 saatlik iş gücü kaybına,
- Stok tükenmesi nedeniyle müşteri kaybına,
- Kargo gecikmelerinin fark edilmemesine ve müşteri memnuniyetsizliğine neden olmaktadır.

**Coop-Panel**, bu süreçleri akıllı bir asistan ve veri odaklı bir dashboard ile otonom hale getirerek yöneticinin üzerindeki operasyonel yükü %80 oranında azaltır.

## 🛠️ Teknik Mimari
Sistem modern, modüler ve ölçeklenebilir bir yapıda tasarlanmıştır:
- **Backend:** Python & FastAPI (Yüksek performanslı ve asenkron API katmanı)
- **Veritabanı:** SQLite & SQLAlchemy ORM (Dinamik ve ilişkisel veri yönetimi)
- **Zeka Katmanı:** Google Gemini (Function Calling desteği ile veritabanı araçlarını kullanabilen akıllı asistan)
- **Frontend:** HTML5, Tailwind CSS, Vanilla JS (Modern Bento Grid tasarımı ve responsive arayüz)
- **Veri Analizi:** Pandas & Openpyxl (Gelişmiş raporlama ve Excel dışa aktarım desteği)

## 🧠 Temel Özellikler & Fonksiyonel Kapasite

Sistem, işletmenin tüm damarlarını kontrol eden bir "Merkezi Sinir Sistemi" gibi çalışır:

### 1. Akıllı Stok ve Envanter Yönetimi
- **Kritik Eşik Takibi:** Stoklar belirlenen threshold değerinin altına düştüğünde sistem otomatik "Kritik" uyarısı verir.
- **Üretim Planlama:** Geçmiş satış verilerini analiz ederek hangi üründen ne kadar üretilmesi gerektiğini tahmin eder.
- **Üretici Takibi:** Her ürünün hangi kooperatif üyesi (kadın üretici) tarafından, ne zaman üretildiğini hikayesiyle birlikte saklar.

### 2. Kritik Sevkiyat ve Lojistik Takibi
- **Gecikme Tespiti:** Teslimat süresi geçen siparişleri otomatik tespit eder.
- **Proaktif Bilgilendirme:** Geciken siparişler için asistan üzerinden müşteriye otomatik bilgilendirme taslakları oluşturur.
- **Raporlama:** Tüm lojistik süreçlerini tek tıkla Excel formatında raporlar.

### 3. İmece Ağı (Kooperatifler Arası Dayanışma)
- **Stok Paylaşımı:** Eğer bir kooperatifte stok biterse, sistem çevredeki diğer paydaş kooperatiflerin stoklarını kontrol eder ve "İmece Ağı" üzerinden ürün tedarik edilmesini önerir.
- **Kaynak Optimizasyonu:** Büyük siparişlerde birden fazla kooperatifin güçlerini birleştirerek siparişi tamamlamasını sağlar.
- **Bölgesel Kalkınma:** Hatay genelindeki tüm kadın kooperatiflerini tek bir akıllı ağda birleştirerek lojistik ve hammadde maliyetlerini düşürür.

### 4. Akıllı Asistan (Operasyon Merkezi)
- **Doğal Dil İşleme:** Yönetici "Siparişler ne durumda?", "Stokta ne azaldı?" veya "Bana geçen ayın finansal analizini sun" dediğinde asistan veritabanına sorgu atarak anlamlı raporlar sunar.
- **Pazarlama İçgörüleri:** Müşteri mesajlarını analiz ederek hangi ürünlerin çok sorulduğunu ancak satılmadığını tespit eder, buna yönelik sosyal medya içerik fikirleri (Tiktok/Instagram reels) üretir.
- **Finansal Zeka:** Gelir-gider dengesini, işçi alacaklarını ve vadesi gelen borçları analiz ederek nakit akışı önerileri sunar.

## 📦 Kurulum ve Çalıştırma

1. **Bağımlılıkları Yükleyin:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Çevresel Değişkenleri Ayarlayın (.env):**
   ```env
   GEMINI_API_KEY=your_api_key
   ```
3. **Örnek Verileri Oluşturun (250+ Sipariş ve Analitik Veri):**
   ```bash
   python scripts/generate_synthetic_data.py
   ```
4. **Sunucuyu Başlatın:**
   ```bash
   uvicorn backend.main:app --reload
   ```

## 🎯 Hedef Kitle
- E-ticaret yapan yerel üreticiler
- Bölgesel kalkınma hedefleyen kadın kooperatifleri
- Operasyonlarını dijitalleştirmek isteyen butik işletmeler

---
*Bu proje Kübra Gezici tarafından Google Academy 2026 Hackathon'u kapsamında, kooperatiflerin dijital dönüşümüne katkı sağlamak amacıyla geliştirilmiştir.*
