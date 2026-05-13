from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime

DATABASE_URL = "sqlite:///./kooperatif.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    details = Column(String, nullable=True) # Ürünün hikayesi, yapılış şekli
    production_date = Column(DateTime, nullable=True) # Ne zaman üretildi
    price = Column(Float)
    stock = Column(Integer)
    category = Column(String)
    producer_member = Column(String) # Üreten kooperatif üyesi
    reorder_threshold = Column(Integer, default=50) # Stok bu seviyeye inince uyarı ver

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    phone = Column(String, unique=True, index=True)
    address = Column(String)
    join_date = Column(DateTime, default=datetime.utcnow) # CRM: Ne zamandır üye

    orders = relationship("Order", back_populates="customer")

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    order_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="Hazırlanıyor") # Hazırlanıyor, Kargoya Verildi, Teslim Edildi
    total_amount = Column(Float)
    tracking_number = Column(String, nullable=True)
    customer_note = Column(String, nullable=True) # Sipariş Notu
    estimated_delivery = Column(DateTime, nullable=True) # Tahmini Teslimat Tarihi
    payment_method = Column(String, default="Havale/EFT")
    payment_status = Column(Boolean, default=False) # Ödendi mi?

    customer = relationship("Customer", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    price_at_time = Column(Float)

    order = relationship("Order", back_populates="items")
    product = relationship("Product")

class Worker(Base):
    __tablename__ = "workers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    role = Column(String)
    daily_wage = Column(Float)
    total_unpaid = Column(Float, default=0.0)

class Expense(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    amount = Column(Float)
    expense_date = Column(DateTime, default=datetime.utcnow)
    category = Column(String) # İşçi Maaşı, Hammadde, Lojistik, Fatura

class Debt(Base):
    __tablename__ = "debts"
    id = Column(Integer, primary_key=True, index=True)
    creditor_name = Column(String) # Kime borcumuz var (Tedarikçi vb.)
    amount = Column(Float)
    due_date = Column(DateTime)
    is_paid = Column(Boolean, default=False)

class MessageLog(Base):
    __tablename__ = "message_logs"
    id = Column(Integer, primary_key=True, index=True)
    customer_phone = Column(String, index=True)
    message = Column(String)
    intent = Column(String) # İçerik analizi (Soru, Şikayet, Ürün Bilgisi)
    created_at = Column(DateTime, default=datetime.utcnow)
    resulted_in_order = Column(Boolean, default=False)

def init_db():
    # Base.metadata.drop_all(bind=engine) # Her seferinde silmesini istemiyoruz
    Base.metadata.create_all(bind=engine)
    
    # Veri yoksa örnek verileri ekleyelim
    db = SessionLocal()
    try:
        if db.query(Product).count() == 0:
            print("📦 Veritabanı boş, örnek veriler yükleniyor...")
            # 1. Örnek Ürünler
            p1 = Product(name="Halhalı Zeytinyağı (5L)", price=1250.0, stock=85, category="Zeytinyağı Grubu", producer_member="Ayşe Teyze - Belen", reorder_threshold=20)
            p2 = Product(name="Geleneksel Nar Ekşisi (500ml)", price=350.0, stock=12, category="Gıda", producer_member="Fatma Hanım - Samandağ", reorder_threshold=15)
            p3 = Product(name="Defne Sabunu (4'lü)", price=180.0, stock=150, category="Kozmetik", producer_member="Zeynep Hanım - Defne", reorder_threshold=30)
            p4 = Product(name="Hatay İpek Şal", price=950.0, stock=5, category="Tekstil", producer_member="Meryem Hanım - Harbiye", reorder_threshold=10)
            p5 = Product(name="Doğal Ev Tarhanası", price=220.0, stock=45, category="Gıda", producer_member="Ayşe Hanım - Antakya", reorder_threshold=100)
            
            db.add_all([p1, p2, p3, p4, p5])
            db.commit()

            # 2. Örnek Müşteriler
            c1 = Customer(name="Mehmet Yılmaz", phone="05321112233", address="Kadıköy, İstanbul")
            c2 = Customer(name="Zeynep Kaya", phone="05445556677", address="Çankaya, Ankara")
            db.add_all([c1, c2])
            db.commit()

            # 3. Örnek Siparişler
            o1 = Order(customer_id=c1.id, total_amount=1600.0, status="Hazırlanıyor", customer_note="Cam şişeler kırılabilecek ürün, lütfen özenli paketlensin.")
            o2 = Order(customer_id=c2.id, total_amount=350.0, status="Kargoya Verildi", tracking_number="HATAY-123456")
            db.add_all([o1, o2])
            db.commit()
            print("✅ Örnek veriler başarıyla yüklendi.")
    finally:
        db.close()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
