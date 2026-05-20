import requests
from crewai.tools import BaseTool
import time

class MakaleOkuyucu(BaseTool):
    name: str = "Web_Makale_Okuyucu"
    description: str = "Verilen bir URL'nin içine girip sayfadaki makaleyi/haberi okur. RAG sistemi için veri toplar."

    def _run(self, url: str) -> str:
        try:
            # Sihirli Dokunuş: Jina AI Reader API (Bot korumalarını aşar, JS render eder, saf metin verir)
            jina_url = f"https://r.jina.ai/{url}"
            
            # API'ye istek atıyoruz
            response = requests.get(jina_url, timeout=20)
            metin = response.text
            
            # Eğer hala çok kısa bir metin döndüyse iptal et
            if len(metin) < 150:
                return "Makale okunamadı, sayfa içeriği çok kısa veya korumalı."
                
            print(f"\n⏳ {url} BAŞARIYLA KAZINDI! API limiti için 12 sn bekleniyor...\n")
            time.sleep(12)
            
            # Makalenin özünü (ilk 3500 karakterini) LLM'e gönderiyoruz
            return metin[:3500]
            
        except Exception as e:
            return f"Makaleye erişilemedi. Hata: {str(e)}"

# Aracımızı dışarı aktarıyoruz
makale_okuyucu = MakaleOkuyucu()