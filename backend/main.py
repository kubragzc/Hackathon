from fastapi import FastAPI, Depends, HTTPException, Form, Request
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, Response, StreamingResponse
from typing import List
import os
import httpx
import pandas as pd
from io import BytesIO
from datetime import datetime

from . import database, schemas
from .agent.core import ask_agent

app = FastAPI(title="Akıllı Kooperatif Yönetim Paneli")

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    database.init_db()

@app.get("/api/products", response_model=List[schemas.Product])
@app.get("/api/stock", response_model=List[schemas.Product])
def get_products(db: Session = Depends(database.get_db)):
    return db.query(database.Product).all()

from pydantic import BaseModel
class ChatRequest(BaseModel):
    message: str
    
class ChatResponse(BaseModel):
    reply: str

@app.post("/api/chat", response_model=ChatResponse)
def chat_with_agent(req: ChatRequest):
    # Asistan ile iletişim
    try:
        reply = ask_agent(req.message)
        return {"reply": reply}
    except Exception as e:
        error_str = str(e)
        if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
            return {"reply": "Ayşe Hanım, şu an sistemde kısa süreli bir yoğunluk yaşanıyor. Talebinizi aldım, lütfen birkaç saniye sonra tekrar dener misiniz? Tüm operasyonel verileriniz güvende."}
        return {"reply": f"Ayşe Hanım, küçük bir teknik aksaklık oldu ama hemen bakıyorum. (Hata: {error_str[:50]}...)"}

@app.post("/api/whatsapp")
async def whatsapp_webhook(Body: str = Form(...), From: str = Form(...)):
    """WhatsApp mesajlarını karşılar ve yanıt döner."""
    try:
        # Gelen mesajı asistan yanıtlasın
        reply = ask_agent(Body)
        
        # Twilio'nun anlayacağı TwiML (XML) formatında yanıt dön
        twiml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{reply}</Message>
</Response>"""
        return Response(content=twiml_response, media_type="application/xml")
    except Exception as e:
        error_msg = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>Sistemde bir hata oluştu, lütfen Ayşe Hanım ile iletişime geçin.</Message>
</Response>"""
        return Response(content=error_msg, media_type="application/xml")

@app.get("/api/orders", response_model=List[schemas.OrderWithCustomer])
def get_orders(db: Session = Depends(database.get_db)):
    return db.query(database.Order).order_by(database.Order.order_date.desc()).all()

class StatusUpdateRequest(BaseModel):
    status: str

@app.put("/api/orders/{order_id}/status")
def update_order_status(order_id: int, req: StatusUpdateRequest, db: Session = Depends(database.get_db)):
    order = db.query(database.Order).filter(database.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Sipariş bulunamadı")
    order.status = req.status
    db.commit()
    return {"message": "Durum güncellendi", "new_status": order.status}

@app.get("/api/dashboard-stats")
def get_dashboard_stats(db: Session = Depends(database.get_db)):
    total = db.query(database.Order).count()
    delivered = db.query(database.Order).filter(database.Order.status == "Teslim Edildi").count()
    preparing = db.query(database.Order).filter(database.Order.status == "Hazırlanıyor").count()
    shipped = db.query(database.Order).filter(database.Order.status == "Kargoya Verildi").count()
    
    return {
        "total_orders": total,
        "delivered_orders": delivered,
        "preparing_orders": preparing,
        "shipped_orders": shipped
    }

@app.get("/api/reports/excel")
def export_orders_excel(db: Session = Depends(database.get_db)):
    orders = db.query(database.Order).all()
    data = []
    for o in orders:
        data.append({
            "Sipariş ID": o.id,
            "Müşteri": o.customer.name,
            "Telefon": o.customer.phone,
            "Tutar (TL)": o.total_amount,
            "Durum": o.status,
            "Ödeme": o.payment_status,
            "Tarih": o.order_date.strftime("%Y-%m-%d %H:%M") if o.order_date else ""
        })
    
    df = pd.DataFrame(data)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Siparişler')
    
    output.seek(0)
    headers = {
        'Content-Disposition': 'attachment; filename="kooperatif_rapor.xlsx"'
    }
    return StreamingResponse(output, headers=headers, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

@app.get("/api/analytics/chart-data")
def get_chart_data(db: Session = Depends(database.get_db)):
    from sqlalchemy import func
    # Son 7 günü çekelim
    stats = db.query(func.date(database.Order.order_date), func.count(database.Order.id))\
              .group_by(func.date(database.Order.order_date))\
              .order_by(func.date(database.Order.order_date))\
              .all()
    
    labels = [str(s[0]) for s in stats]
    values = [s[1] for s in stats]
    
    return {
        "labels": labels,
        "values": values
    }

@app.get("/api/imece/network")
def get_imece_network():
    # Bölgedeki diğer kooperatifler ve paylaşıma açık kaynakları
    return [
        {
            "id": 1,
            "name": "Mudanya Kadın Kooperatifi",
            "location": "Bursa",
            "resources": ["Zeytin (200kg)", "Domates Salçası (50 Kavanoz)"],
            "status": "Aktif / Paylaşıma Açık",
            "contact": "Fatma Hanım",
            "image": "https://ui-avatars.com/api/?name=Mudanya+Koop&background=4CAF50&color=fff"
        },
        {
            "id": 2,
            "name": "Ayvalık Üretim Kooperatifi",
            "location": "Balıkesir",
            "resources": ["Zeytinyağı (500L)", "Sabun (100 Paket)"],
            "status": "Aktif / Lojistik Paylaşımı Mevcut",
            "contact": "Ahmet Bey",
            "image": "https://ui-avatars.com/api/?name=Ayvalik+Koop&background=FF9800&color=fff"
        },
        {
            "id": 3,
            "name": "Uşak Tarhana İmece Grubu",
            "location": "Uşak",
            "resources": ["Tarhana (150kg)", "Kuru Biber (20kg)"],
            "status": "Aktif / Hammadde Desteği",
            "contact": "Zeynep Hanım",
            "image": "https://ui-avatars.com/api/?name=Usak+Imece&background=F44336&color=fff"
        },
        {
            "id": 4,
            "name": "Hatay Defne Girişimi",
            "location": "Hatay / Defne",
            "resources": ["Lojistik Araç (2 Kamyonet)", "Depo Alanı (50m2)"],
            "status": "Aktif / Lojistik Destek",
            "contact": "Mehmet Can",
            "image": "https://ui-avatars.com/api/?name=Hatay+Defne&background=2196F3&color=fff"
        }
    ]

# Mount static files at the end so it doesn't override API routes
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
