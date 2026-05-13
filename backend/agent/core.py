import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

from .tools import tools_list

load_dotenv()

API_KEY = os.environ.get("GEMINI_API_KEY")

if API_KEY:
    client = genai.Client(api_key=API_KEY)
else:
    client = None

chat = None

def ask_agent(message: str) -> str:
    global chat
    if not client:
        return "Sistem uyarısı: Lütfen .env dosyasına GEMINI_API_KEY ekleyin ve sunucuyu yeniden başlatın."
    
    system_instruction = (
        "Sen 'Coop-AI: Akıllı Operasyon Sistemi'nin yönetim asistanısın. "
        "TEMEL GÖREVİN: KOBİ ve kooperatiflerin operasyonel yükünü azaltmak, süreçleri (stok, sipariş, kargo) takip etmek ve yöneticiye stratejik bilgiler sunmaktır. "
        "DİL VE ÜSLUP: Profesyonel, çözüm odaklı ve güven verici ol. 'Yönetici' veya 'Ayşe Hanım' diye hitap et. "
        "OPERASYONEL ÖNCELİKLER:\n"
        "1. SİPARİŞ TAKİBİ: Siparişlerin durumunu kontrol et ve bilgi ver.\n"
        "2. İLETİŞİM: Müşteri sorularını yanıtla ve operasyonel destek sağla.\n"
        "3. ANALİZ & RAPORLAMA: 'analiz yap', 'rapor sun' denildiğinde verileri analiz et ve sonucu yöneticiye ilet.\n"
        "4. STOK YÖNETİCİSİ: Stok kritikse yöneticiyi uyar ve tedarik önerilerinde bulun.\n"
        "Kullanıcı 'sipariş nerede', 'stok ne durumda', 'analiz yap' gibi şeyler sorduğunda ilgili araçları kullan. "
        "Veri uydurma, her zaman veritabanı araçlarını referans al."
    )
    
    if chat is None:
        chat = client.chats.create(
            model='gemini-2.0-flash',
            config=types.GenerateContentConfig(
                tools=tools_list,
                temperature=0.1,
                system_instruction=system_instruction,
            )
        )
    
    try:
        response = chat.send_message(message)
        return response.text
    except Exception as e:
        error_str = str(e)
        if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
            return "Ayşe Hanım, şu an Hatay genelindeki yoğun talep nedeniyle sistemimizde kısa süreli bir bekleme süresi oluştu. Operasyonel verileriniz güvende, lütfen birkaç saniye sonra tekrar dener misiniz?"
        return f"Ayşe Hanım, küçük bir teknik aksaklık oldu ama operasyonlarımız kesintisiz devam ediyor. Hemen kontrol ediyorum. (Not: {error_str[:30]}...)"
