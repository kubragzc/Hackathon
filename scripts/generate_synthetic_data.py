import sys
import os
import random
from datetime import datetime, timedelta

# Add the parent directory to sys.path to import backend modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.database import SessionLocal, init_db, Product, Customer, Order, OrderItem, Worker, Expense, Debt, MessageLog

def create_mock_data():
    init_db()
    db = SessionLocal()

    # Clear existing data
    db.query(OrderItem).delete()
    db.query(Order).delete()
    db.query(Customer).delete()
    db.query(Product).delete()
    db.query(Worker).delete()
    db.query(Expense).delete()
    db.query(Debt).delete()
    db.query(MessageLog).delete()

    # 1. Products (Expanded Hatay Yöresel Ürünler)
    products_data = [
        {"name": "Geleneksel Turunç Reçeli (750g)", "category": "Reçeller", "price": 140.0, "stock": 45, "producer_member": "Yeniden Hatay Kadın Koop.", "reorder_threshold": 20, "production_date": datetime.utcnow() - timedelta(days=10), "details": "Odun ateşinde bakır kazanlarda yapıldı."}, 
        {"name": "Samandağ Acı Biber Salçası (1kg)", "category": "Baharat/Salça", "price": 180.0, "stock": 12, "producer_member": "Defne Kadın Kooperatifi", "reorder_threshold": 15, "production_date": datetime.utcnow() - timedelta(days=5), "details": "Güneşte kurutulmuş Samandağ biberi."},
        {"name": "Vakıfköy İncir Reçeli (500g)", "category": "Reçeller", "price": 130.0, "stock": 80, "producer_member": "Vakıfköy Kadın Kooperatifi", "reorder_threshold": 25, "production_date": datetime.utcnow() - timedelta(days=2), "details": "Şeker ilavesiz dağ inciri."},
        {"name": "Hatay Halhalı Zeytinyağı (1L)", "category": "Yağlar", "price": 380.0, "stock": 60, "producer_member": "Yeniden Hatay Kadın Koop.", "reorder_threshold": 20, "production_date": datetime.utcnow() - timedelta(days=45), "details": "Soğuk sıkım, meyvemsi tad."},
        {"name": "Nar Ekşisi (500ml) - Hakiki", "category": "Soslar", "price": 220.0, "stock": 35, "producer_member": "Belenli Üreticiler", "reorder_threshold": 10, "production_date": datetime.utcnow() - timedelta(days=20), "details": "%100 saf nar suyu, katkısız."},
        {"name": "Zahter (Kuru - 250g)", "category": "Baharatlar", "price": 85.0, "stock": 120, "producer_member": "Yayladağı Koop.", "reorder_threshold": 30, "production_date": datetime.utcnow() - timedelta(days=15), "details": "Dağ kekikli özel karışım."},
        {"name": "Tuzlu Yoğurt (1kg)", "category": "Süt Ürünleri", "price": 160.0, "stock": 18, "producer_member": "Antakya Kadın Girişimi", "reorder_threshold": 15, "production_date": datetime.utcnow() - timedelta(days=3), "details": "Keçi sütünden geleneksel yöntem."},
        {"name": "Sürk Peyniri (Kurutulmuş)", "category": "Süt Ürünleri", "price": 120.0, "stock": 40, "producer_member": "Altınözü Koop.", "reorder_threshold": 10, "production_date": datetime.utcnow() - timedelta(days=10), "details": "Bol baharatlı zeytinyağında saklanabilir."},
        {"name": "Kabak Tatlısı (750g)", "category": "Tatlılar", "price": 190.0, "stock": 25, "producer_member": "Payas Üreten Kadınlar", "reorder_threshold": 5, "production_date": datetime.utcnow() - timedelta(days=1), "details": "Kireçte bekletilmiş çıtır kabak."},
        {"name": "Defne Sabunu (4'lü Paket)", "category": "Kozmetik", "price": 150.0, "stock": 100, "producer_member": "Daphne El Sanatları", "reorder_threshold": 20, "production_date": datetime.utcnow() - timedelta(days=60), "details": "Geleneksel kazanlarda soğuk üretim."},
    ]
    
    # Add more random products to reach 40
    producers = ["Arsuz Kadınları", "Kırıkhan Girişim", "Dörtyol Portakal Koop.", "Hassa Zeytin Birliği"]
    categories = ["Kuru Gıda", "Meyve Kurusu", "Dokuma", "Bakliyat"]
    for i in range(30):
        products_data.append({
            "name": f"Yöresel Ürün {i+11}",
            "category": random.choice(categories),
            "price": float(random.randint(50, 500)),
            "stock": random.randint(5, 150),
            "producer_member": random.choice(producers),
            "reorder_threshold": 15,
            "production_date": datetime.utcnow() - timedelta(days=random.randint(5, 90)),
            "details": "Tamamen doğal ve geleneksel yöntemlerle üretilmiştir."
        })

    db_products = []
    for p_data in products_data:
        p = Product(**p_data)
        db.add(p)
        db_products.append(p)
    db.commit()

    # 2. Customers (Scale to 50)
    customer_names = [f"Müşteri {i+1}" for i in range(50)]
    cities = ["İstanbul", "Ankara", "İzmir", "Bursa", "Antalya", "Adana", "Konya", "Kayseri", "Hatay", "Gaziantep"]
    
    db_customers = []
    for i, name in enumerate(customer_names):
        phone = f"0555111{str(2000 + i)}"
        city = random.choice(cities)
        c = Customer(name=name, phone=phone, address=f"Sokak No: {random.randint(1, 100)}, {city}")
        db.add(c)
        db_customers.append(c)
    db.commit()

    # 3. Orders (Scale to 250)
    statuses = ["Hazırlanıyor", "Kargoya Verildi", "Teslim Edildi", "İptal Edildi"]
    notes = ["Hızlı teslimat lütfen", "Komşuya bırakın", "Hediye paketi", ""]
    
    for i in range(250):
        customer = random.choice(db_customers)
        status = random.choices(statuses, weights=[10, 20, 65, 5])[0]
        order_date = datetime.utcnow() - timedelta(days=random.randint(0, 60), hours=random.randint(0, 23))
        tracking = f"TR{random.randint(10000000, 99999999)}" if status in ["Kargoya Verildi", "Teslim Edildi"] else None
        
        # Create some DELAYED orders (Shipping check logic)
        # If order was created > 5 days ago and still preparing, it's delayed
        estimated_delivery = order_date + timedelta(days=random.randint(2, 4))
        
        order = Order(
            customer_id=customer.id,
            order_date=order_date,
            status=status,
            tracking_number=tracking,
            customer_note=random.choice(notes),
            estimated_delivery=estimated_delivery,
            payment_method=random.choice(["Kredi Kartı", "Havale", "Nakit"]),
            payment_status=True if status != "Yeni" else False,
            total_amount=0.0
        )
        db.add(order)
        db.commit()
        
        total = 0.0
        num_items = random.randint(1, 4)
        selected_products = random.sample(db_products, num_items)
        
        for product in selected_products:
            qty = random.randint(1, 3)
            item = OrderItem(order_id=order.id, product_id=product.id, quantity=qty, price_at_time=product.price)
            total += qty * product.price
            db.add(item)
        order.total_amount = total
        db.commit()

    # 4. Workers (Scale to 10)
    for i in range(10):
        w = Worker(
            name=f"Emekçi Kadın {i+1}",
            role=random.choice(["Üretim", "Paketleme", "Lojistik", "Kalite Kontrol"]),
            daily_wage=random.randint(400, 700),
            total_unpaid=random.randint(0, 3000)
        )
        db.add(w)
    
    # 5. Expenses (Scale to 15)
    for i in range(15):
        e = Expense(
            description=f"Gider Kalemi {i+1}",
            amount=random.randint(500, 5000),
            category=random.choice(["Fatura", "Hammadde", "Lojistik", "Kira"]),
            expense_date=datetime.utcnow() - timedelta(days=random.randint(1, 30))
        )
        db.add(e)
        
    # 6. Debts (Scale to 10)
    for i in range(10):
        d = Debt(
            creditor_name=f"Tedarikçi {i+1}",
            amount=random.randint(2000, 20000),
            due_date=datetime.utcnow() + timedelta(days=random.randint(-5, 20)),
            is_paid=random.choice([True, False])
        )
        db.add(d)
        
    # 7. Message Logs (Müşteri Mesajları Simülasyonu)
    message_samples = [
        {"msg": "Tarhananın içinde neler var organik mi?", "intent": "Ürün Bilgisi", "result": False},
        {"msg": "Balın üretim tarihi nedir, taze mi?", "intent": "Ürün Bilgisi", "result": False},
        {"msg": "Zeytinyağı asit oranı çok mu düşük?", "intent": "Ürün Bilgisi", "result": False},
        {"msg": "Kargo ücreti ne kadar?", "intent": "Lojistik Sorgusu", "result": True},
        {"msg": "Neden bu kadar pahalı markette daha ucuz?", "intent": "Fiyat Sorgusu", "result": False},
        {"msg": "Toptan alım yapabiliyor muyuz?", "intent": "Fiyat Sorgusu", "result": True},
        {"msg": "Salçanın içinde koruyucu var mı?", "intent": "Ürün Bilgisi", "result": False},
        {"msg": "İncirler beyazlamış bozuk mu?", "intent": "Şikayet", "result": False},
        {"msg": "Daha önce aldım çok güzeldi tekrar istiyorum", "intent": "Sipariş Talebi", "result": True},
        {"msg": "Üretimden video atar mısınız güvenemedim", "intent": "Güven Sorgusu", "result": False},
    ]
    
    for i in range(150):
        sample = random.choice(message_samples)
        log = MessageLog(
            customer_phone=f"0555{random.randint(1000000, 9999999)}",
            message=sample["msg"],
            intent=sample["intent"],
            created_at=datetime.utcnow() - timedelta(days=random.randint(0, 45)),
            resulted_in_order=random.choice([True, False])
        )
        db.add(log)
        
    db.commit()
    print("✅ Akıllı Kooperatif Yönetim Sistemi için veri seti hazır!")
    db.close()
if __name__ == "__main__":
    create_mock_data()
