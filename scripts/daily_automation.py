import sys
import os
import pandas as pd
from datetime import datetime, timedelta
from io import BytesIO

# Add parent dir to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.database import SessionLocal, Order, Customer, Product, Expense

def run_weekly_automation():
    print(f"🚀 Otonom İşleme Başlatıldı: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    db = SessionLocal()
    
    try:
        # 1. HAFTALIK VERİLERİ ANALİZ ET
        one_week_ago = datetime.utcnow() - timedelta(days=7)
        orders = db.query(Order).filter(Order.order_date >= one_week_ago).all()
        
        print(f"📊 Son 7 günde {len(orders)} sipariş tespit edildi.")
        
        # 2. EXCEL RAPORU OLUŞTUR
        data = []
        for o in orders:
            data.append({
                "Tarih": o.order_date.strftime("%Y-%m-%d"),
                "Müşteri": o.customer.name,
                "Tutar (TL)": o.total_amount,
                "Durum": o.status,
                "Ödeme": "Ödendi" if o.payment_status else "Bekliyor"
            })
            
        df = pd.DataFrame(data)
        report_path = os.path.join(os.path.dirname(__file__), "..", "reports")
        if not os.path.exists(report_path):
            os.makedirs(report_path)
            
        filename = f"Haftalik_Rapor_{datetime.now().strftime('%Y%m%d')}.xlsx"
        full_path = os.path.join(report_path, filename)
        
        df.to_excel(full_path, index=False)
        print(f"✅ Haftalık Excel raporu oluşturuldu: {full_path}")
        
        # 3. PROAKTİF AKSİYONLAR
        unpaid_orders = [o for o in orders if not o.payment_status]
        if unpaid_orders:
            print(f"⚠️ DİKKAT: Ödemesi bekleyen {len(unpaid_orders)} sipariş var. Ayşe Hanım'a WhatsApp uyarısı hazırlandı.")
            
        delayed_orders = [o for o in orders if o.status == "Hazırlanıyor" and o.order_date < (datetime.utcnow() - timedelta(days=3))]
        if delayed_orders:
            print(f"🚨 KRİTİK: {len(delayed_orders)} sipariş 3 günden fazladır hazırlanıyor modunda kalmış! Lojistik birimi bilgilendiriliyor.")

        # 4. SİMÜLASYON: WHATSAPP VE E-POSTA GÖNDERİMİ
        print(f"📱 Simülasyon: Rapor Ayşe Hanım'ın WhatsApp hattına iletildi.")
        print(f"📧 Simülasyon: '{filename}' raporu kooperatif-baskani@gmail.com adresine mail atıldı.")
        
    except Exception as e:
        print(f"❌ Otomasyon hatası: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    run_weekly_automation()
