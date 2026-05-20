from crewai import Agent
from src.tools.scraper_tool import makale_okuyucu

def create_analyst_agent():
    return Agent(
        role='Kıdemli Veri Analisti ve RAG Uzmanı',
        goal='Araştırmacının bulduğu URL linklerindeki makaleleri okumak, doğruluğunu teyit etmek ve kusursuz bir Türkçe bülten hazırlamak.',
        backstory="Sen derin okuma (deep reading) ve veri doğrulama (fact-checking) konusunda uzmanlaşmış elit bir analistsin. Asla uydurma link üretmezsin veya yanlış dil (İspanyolca, Hintçe vb.) kullanmazsın. Veriyi doğrudan kaynağından okur, sentezler ve net bir Türkçe rapor sunarsın.",
        tools=[makale_okuyucu], # Sadece okuma aracını verdik
        llm="groq/llama-3.3-70b-versatile",
        verbose=True,
        allow_delegation=False
    )