import os
import time  # Sistemi uyutmak için zaman modülünü ekledik
from crewai.tools import BaseTool
from tavily import TavilyClient

class AramaMotoru(BaseTool):
    name: str = "Internet_Arama_Araci"
    description: str = "İnternette güncel yapay zeka haberlerini bulmak için arama motoru."

    def _run(self, query: str) -> str:
        api_key = os.getenv("TAVILY_API_KEY")
        client = TavilyClient(api_key=api_key)
        
        # 'advanced' yerine 'basic' kullanarak hızı artırıyoruz
        response = client.search(
            query=query, 
            search_depth="basic", 
            max_results=3,
            topic="news",
            days=2
        )
        
        # Token tasarrufu: Sadece Başlık ve URL alıyoruz
        basit_sonuclar = []
        for res in response.get("results", []):
            basit_sonuclar.append(f"Başlık: {res.get('title')}\nURL: {res.get('url')}")
            
        sonuc_metni = "\n\n".join(basit_sonuclar)
        
        # SİHİRLİ DOKUNUŞ: Groq'un TPM (kelime) limitinin soğuması için bekliyoruz!
        print(f"\n⏳ '{query}' araması tamamlandı. API limiti için 15 saniye bekleniyor...\n")
        time.sleep(15)
        
        return sonuc_metni

class XAramaMotoru(BaseTool):
    name: str = "X_Twitter_Arama_Araci"
    description: str = "Sadece X (Twitter) platformundaki duyuruları bulur."

    def _run(self, query: str) -> str:
        api_key = os.getenv("TAVILY_API_KEY")
        client = TavilyClient(api_key=api_key)
        
        response = client.search(
            query=query, 
            search_depth="basic", 
            include_domains=["x.com", "twitter.com"], 
            max_results=3
        )
        
        basit_sonuclar = []
        for res in response.get("results", []):
            basit_sonuclar.append(f"Başlık: {res.get('title')}\nURL: {res.get('url')}")
            
        sonuc_metni = "\n\n".join(basit_sonuclar)
        
        print(f"\n⏳ X üzerinde '{query}' araması tamamlandı. API limiti için 15 saniye bekleniyor...\n")
        time.sleep(15)
        
        return sonuc_metni

arama_motoru = AramaMotoru()
x_arama_motoru = XAramaMotoru()