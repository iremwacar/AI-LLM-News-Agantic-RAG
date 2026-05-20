import os
from dotenv import load_dotenv
from datetime import datetime
from crewai import Agent, Task, Crew, Process

# Ajan ve Araç İçe Aktarmaları
from src.agents.researcher import create_researcher_agent
from src.agents.analyst import create_analyst_agent
from src.tools.email_tool import mail_tool

# 1. Çevresel Değişkenleri Yükle ve Tarihi Belirle
load_dotenv()
bugunun_tarihi = datetime.now().strftime("%Y-%m-%d")

# 2. Ajanları Sahaya Çağır
# Not: researcher ve analyst ajanlarını kendi dosyalarından çekiyoruz
researcher_agent = create_researcher_agent()
analyst_agent = create_analyst_agent()

# Üçüncü Ajan: İletişim Uzmanı (Doğrudan burada tanımlıyoruz)
communicator_agent = Agent(
    role='Kurumsal İletişim ve Operasyon Uzmanı',
    goal='Analistin hazırladığı teknik raporu alıp, İrem Acar için profesyonel bir mail formatına dönüştürerek göndermek.',
    backstory="""Sen bir bülten editörüsün. Yazılım mühendisliği jargonuna hakimsin. 
    Görevin, karmaşık analizleri temiz, okunabilir ve profesyonel bir mail haline getirmek.""",
    tools=[mail_tool],
    llm="groq/llama-3.3-70b-versatile",
    verbose=True,
    allow_delegation=False
)

# 3. Görevleri Tanımla

# GÖREV 1: Araştırmacı (Taze Link Bulucu)
research_task = Task(
    description=f"Bugünün tarihi {bugunun_tarihi}. İnternette son 24 saatteki en önemli 3 yapay zeka haberinin URL linkini bul.",
    expected_output="Sadece 3 adet haber URL linki içeren bir liste.",
    agent=researcher_agent
)

# GÖREV 2: Analist (Derin RAG Analizi)
analysis_task = Task(
    description="""
    'Web_Makale_Okuyucu' aracını kullanarak Araştırmacının bulduğu linklerin içine gir.
    
    ANALİZ KRİTERLERİ:
    - Haberi yüzeysel geçme, en az 100-150 kelimelik teknik derinliği olan bir özet yaz.
    - Makaledeki rakamları, şirket isimlerini ve teknik terimleri (RAG, Token, Inference vb.) mutlaka kullan.
    - Gelişmenin yazılım dünyası için stratejik önemini açıkla.
    - Okuyamadığın veya bot korumasına takılan linkleri 'Geçersiz Link' olarak işaretle.
    """,
    expected_output="3 farklı haber için zengin içerikli, teknik ve Türkçe bir rapor.",
    agent=analyst_agent,
    context=[research_task]
)

# GÖREV 3: İletişim Uzmanı (Mail Operasyonu)
email_task = Task(
    description=f"""
    Analistten gelen raporu al.
    İçeriğin başına şu cümleyi ekle: 'Merhaba İrem, İşte {bugunun_tarihi} tarihli günlük global yapay zeka bültenin:'
    Elde ettiğin tüm metni tek bir 'icerik' parametresi haline getir.
    Bu içeriği 'Email_Gonderme_Araci' aracını kullanarak gönder.
    """,
    expected_output="Mailin başarıyla gönderildiğine dair onay mesajı.",
    agent=communicator_agent,
    context=[analysis_task]
)

# 4. Ekibi Kur ve Çalıştır
news_crew = Crew(
    agents=[researcher_agent, analyst_agent, communicator_agent],
    tasks=[research_task, analysis_task, email_task],
    process=Process.sequential, 
    verbose=True,
    cache=False,
    max_rpm=10 # Groq API limitlerini aşmamak için hızı sınırlıyoruz
)

print(f"### {bugunun_tarihi} Tarihli Global AI Taraması Başlatıldı... ###")
result = news_crew.kickoff()

print("\n\n########################")
print("## OPERASYON TAMAMLANDI ##")
print("########################\n")
print(result)