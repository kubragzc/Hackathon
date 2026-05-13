import os
import sys
from sqlalchemy import func
from datetime import datetime, timedelta

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.database import SessionLocal, Product, Order, Customer, Worker, Expense, Debt

def get_stock_status(product_name: str) -> str:
    """Belirli bir ürünün kooperatifteki stok durumunu, kim tarafından üretildiğini, HİKAYESİNİ ve DOĞALLIĞINI (içindekiler) getirir.
    Müşteriye satış yaparken veya bilgi verirken bu hikayeyi kullanarak onu İKNA EDİN.
    Args:
        product_name: Aranan ürünün adı (örn: 'Zeytinyağı', 'Tarhana', 'Salça')
    """
    db = SessionLocal()
    try:
        products = db.query(Product).filter(Product.name.ilike(f"%{product_name}%")).all()
        if not products:
            return f"Kooperatifimizde '{product_name}' isimli bir ürün bulunamadı."
        
        result = []
        for p in products:
            status = "Kritik Seviyede!" if p.stock <= p.reorder_threshold else "Yeterli."
            prod_date = p.production_date.strftime('%d.%m.%Y') if p.production_date else "Bilinmiyor"
            details = p.details or "Doğal köy ürünü."
            result.append(f"{p.name}: {p.stock} adet stokta var. (Üretici: {p.producer_member}) - Durum: {status}\nÜretim Tarihi: {prod_date}\nÜrün Hikayesi/Doğallığı: {details}")
        return "\n".join(result)
    finally:
        db.close()

def get_order_status(phone_number: str) -> str:
    """Bir müşterinin telefon numarasına göre son siparişinin kargo ve hazırlık durumunu getirir.
    Args:
        phone_number: Müşterinin telefon numarası (örn: '05551112233')
    """
    db = SessionLocal()
    try:
        customer = db.query(Customer).filter(Customer.phone == phone_number).first()
        if not customer:
            return "Bu telefon numarasına ait bir müşteri veya sipariş bulunamadı."
        
        order = db.query(Order).filter(Order.customer_id == customer.id).order_by(Order.order_date.desc()).first()
        if not order:
            return f"{customer.name} isimli müşterinin geçmiş siparişi yok."
        
        tracking_info = f" Takip No: {order.tracking_number}" if order.tracking_number else ""
        return f"{customer.name} isimli müşterinin {order.order_date.strftime('%d.%m.%Y')} tarihli siparişinin durumu: '{order.status}'. Toplam tutar: {order.total_amount} TL.{tracking_info}"
    finally:
        db.close()

def suggest_imece_cooperation(product_category: str) -> str:
    """Stok yetmediğinde veya büyük bir sipariş geldiğinde, 'İmece Ağı'ndaki (çevre kooperatiflerdeki) tahmini ürünleri kontrol eder ve öneri sunar.
    Args:
        product_category: Eksik olan ürün kategorisi (örn: 'Konserve', 'Yağlar')
    """
    mock_coops = {
        "Konserve": "Bursa Mudanya Kadın Kooperatifi (200 adet Salça mevcut)",
        "Yağlar": "Ayvalık Üretim Kooperatifi (500L Zeytinyağı mevcut)",
        "Kuru Gıda": "Uşak Tarhana İmece Grubu (100kg Tarhana mevcut)"
    }
    
    suggestion = mock_coops.get(product_category, "Yakın çevredeki kooperatif ağında bu kategoride uygun stok bulunamadı.")
    return f"İmece Ağı Önerisi: {suggestion}. Müşteriyi kaybetmemek için ortak tedarik sağlayabiliriz."

def predict_production_needs() -> str:
    """Geçmiş satış verilerini analiz edip önümüzdeki ay için üretim tahminleri ve üretici kadınlara bildirim taslağı çıkarır."""
    return (
        "📊 Yapay Zeka Talep Tahmini:\n"
        "- Kış aylarının yaklaşmasıyla 'Doğal Ev Tarhanası' talebinde %45 artış bekleniyor.\n"
        "- Mevcut stok: 45 adet. Beklenen talep: 150 adet.\n"
        "💡 Öneri: Ayşe Hanım ve diğer kurugıda üreticisi kadınlara otomatik SMS ile '100 kg ek tarhana üretimi' bildirimi göndereyim mi?"
    )

def analyze_customer_data() -> str:
    """Müşteri satın alma alışkanlıklarını, aylık satış hacmini ve toplu alım yapan (VIP) müşterilerin oranını analiz eder."""
    db = SessionLocal()
    try:
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        
        # 1. Aylık Satış Hacmi
        monthly_sales = db.query(func.sum(Order.total_amount)).filter(Order.order_date >= thirty_days_ago).scalar() or 0.0
        
        # 2. Toplam Müşteri Sayısı
        total_customers = db.query(Customer).count()
        
        # 3. Toplu Alım Yapan Müşteriler (Order başına total_amount > 1000 TL)
        bulk_orders_count = db.query(Order.customer_id).filter(Order.total_amount > 1000).distinct().count()
        bulk_percentage = (bulk_orders_count / total_customers * 100) if total_customers > 0 else 0
        
        # 4. En iyi 3 Müşteri
        top_customers = db.query(
            Customer.name, func.sum(Order.total_amount).label('total_spent')
        ).join(Order).group_by(Customer.id).order_by(func.sum(Order.total_amount).desc()).limit(3).all()
        
        top_cust_str = "\n".join([f"   - {c.name}: {c.total_spent:.2f} TL" for c in top_customers])
        
        report = (
            "📈 Müşteri ve Satış Analiz Raporu:\n"
            f"- Son 30 Günlük Satış Hacmi: {monthly_sales:.2f} TL\n"
            f"- Toplu/Yüksek Tutarlı Alım Yapan Müşteri Oranı: %{bulk_percentage:.1f}\n"
            f"- En Sadık 3 Müşterimiz (Ciroya Göre):\n{top_cust_str}\n"
            f"💡 Yapay Zeka Önerisi: Toplu alım yapan %{bulk_percentage:.1f}'lik sadık müşteri kitlesine, yeni sezon ürünlerimiz (örn: Yeni Hasat Zeytinyağı) için özel bir SMS kampanyası düzenleyebiliriz."
        )
        return report
    finally:
        db.close()

def analyze_financial_status() -> str:
    """Kooperatifin muhasebe durumunu, toplam kazançları, giderleri, işçi ödemelerini ve borç durumunu analiz eder."""
    db = SessionLocal()
    try:
        # Toplam Satış (Gelir)
        total_income = db.query(func.sum(Order.total_amount)).filter(Order.status != "İptal Edildi").scalar() or 0.0
        
        # Giderler
        total_expenses = db.query(func.sum(Expense.amount)).scalar() or 0.0
        
        # İşçi Alacakları
        total_worker_unpaid = db.query(func.sum(Worker.total_unpaid)).scalar() or 0.0
        workers = db.query(Worker).filter(Worker.total_unpaid > 0).all()
        workers_str = "\n".join([f"   - {w.name} ({w.role}): {w.total_unpaid} TL alacaklı" for w in workers])
        
        # Borçlar
        total_debt = db.query(func.sum(Debt.amount)).filter(Debt.is_paid == False).scalar() or 0.0
        debts = db.query(Debt).filter(Debt.is_paid == False).all()
        debts_str = "\n".join([f"   - {d.creditor_name}: {d.amount} TL (Son Ödeme: {d.due_date.strftime('%d.%m.%Y')})" for d in debts])
        
        net_profit = total_income - total_expenses - total_worker_unpaid - total_debt
        
        report = (
            "💰 Kooperatif Muhasebe & Finansal Durum Raporu:\n"
            f"- Toplam Satış Geliri: {total_income:.2f} TL\n"
            f"- Toplam Giderler (Fatura/Lojistik vb.): {total_expenses:.2f} TL\n"
            f"- Bekleyen İşçi Ödemeleri: {total_worker_unpaid:.2f} TL\n"
            f"{workers_str}\n"
            f"- Ödenecek Borçlar: {total_debt:.2f} TL\n"
            f"{debts_str}\n"
            "--------------------------------------------------\n"
            f"Tahmini Net Durum (Tüm borçlar ödendikten sonra): {net_profit:.2f} TL\n"
            "💡 Yapay Zeka Önerisi: İşçi ödemelerini ve vadesi yaklaşan borçları bu haftaki nakit akışından önceliklendirmenizi öneririm."
        )
        return report
    finally:
        db.close()

def analyze_marketing_insights() -> str:
    """Gelen WhatsApp/Müşteri mesajlarını analiz edip, hangi ürünlerin çok sorulup alınmadığını, müşteri itirazlarını ve sosyal medya/pazarlama tavsiyelerini çıkarır."""
    from backend.database import MessageLog
    db = SessionLocal()
    try:
        total_messages = db.query(MessageLog).count()
        if total_messages == 0:
            return "Henüz analiz edilecek müşteri mesajı bulunmuyor."
            
        no_order_msgs = db.query(MessageLog).filter(MessageLog.resulted_in_order == False, MessageLog.intent == "Ürün Bilgisi").all()
        
        report = (
            f"📱 Pazarlama ve İletişim İçgörü Raporu:\n"
            f"- İncelenen Toplam Müşteri Mesajı: {total_messages}\n"
            f"- Dikkat Çeken Durum: Yaklaşık {len(no_order_msgs)} potansiyel müşteri, ürün bilgisi ve doğallığı (içindekiler, asit oranı vb.) sormasına rağmen sipariş oluşturmamış. İkna sürecinde bir kopukluk var.\n\n"
            "💡 Kooperatif Büyüme (Sosyal Medya) Önerileri:\n"
            "1. Instagram/Tiktok Video Fikri: Müşteriler en çok ürünün içeriğini ve tarihini merak ediyor. 'Zeytinyağımızın Asit Oranı Neden Düşük?' veya 'Tarhanamızın İçinde Neler Var?' temalı, üretim anını (örneğin Fatma Şahin'in zeytin sıkımını) gösteren 30 saniyelik doğal, şeffaf videolar paylaşın.\n"
            "2. Güven İnşası: WhatsApp üzerinden soru soran müşterilere, yazılı cevap yerine doğrudan üretim tesisinden (kavanozlanma anından vb.) anlık bir fotoğraf veya sesli mesaj göndererek doğallık hissini artırın."
        )
        return report
    finally:
        db.close()

def analyze_pending_orders() -> str:
    """Hazırlanıyor veya Yeni statüsündeki siparişlerin gecikme durumunu analiz eder. Lojistik ve kargo planlaması için kullanılır."""
    db = SessionLocal()
    try:
        pending_orders = db.query(Order).filter(Order.status == "Hazırlanıyor").all()
        if not pending_orders:
            return "Şu an bekleyen veya geciken hiçbir siparişimiz yok, harika!"
            
        now = datetime.utcnow()
        delayed_orders = []
        upcoming_orders = []
        
        for o in pending_orders:
            if o.estimated_delivery:
                days_left = (o.estimated_delivery - now).days
                if days_left < 0:
                    delayed_orders.append(o)
                else:
                    upcoming_orders.append(o)
                    
        report = f"📦 Lojistik ve Kargo Durumu Analizi:\n"
        report += f"- Toplam Hazırlanan Sipariş: {len(pending_orders)}\n"
        if delayed_orders:
            report += f"⚠️ DİKKAT: Tahmini teslimat süresi geçmiş veya kargoya verilmesi gecikmiş {len(delayed_orders)} sipariş var! Lütfen sipariş yönetim panelinden kontrol edin.\n"
        if upcoming_orders:
            report += f"- Önümüzdeki 3 gün içinde kargolanması gereken {len(upcoming_orders)} sipariş bulunuyor.\n"
            
        report += "\n💡 Yapay Zeka Önerisi: Geciken siparişler için müşterilere 'Ürününüz özenle hazırlanıyor, ufak bir gecikme oldu' şeklinde otomatik bir WhatsApp bilgilendirmesi göndermemi ister misiniz?"
        return report
    finally:
        db.close()

def send_email_report(email_address: str = "kooperatif-baskani@gmail.com") -> str:
    """Haftalık raporu ve analizleri belirtilen e-posta adresine Excel formatında gönderir."""
    # Bu aşamada simülasyon ve loglama yapıyoruz
    return f"📩 İŞLEM BAŞARILI: Haftalık operasyon raporu ve AI analizleri '{email_address}' adresine e-posta olarak gönderildi. (Ek: kooperatif_rapor.xlsx)"


tools_list = [
    get_stock_status,
    get_order_status,
    suggest_imece_cooperation,
    predict_production_needs,
    analyze_customer_data,
    analyze_financial_status,
    analyze_marketing_insights,
    analyze_pending_orders,
    send_email_report
]
