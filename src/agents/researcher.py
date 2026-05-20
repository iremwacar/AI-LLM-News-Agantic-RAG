from crewai import Agent
from src.tools.search_tool import arama_motoru, x_arama_motoru

def create_researcher_agent():
    return Agent(
        role='Global AI Veri Madencisi',
        goal='En güncel yapay zeka haber linklerini hatasız bulmak.',
        backstory="""Sen sadece sana verilen araçları kullanan bir robotsun. 
        ASLA kendi kafandan 'brave_search' gibi araç isimleri uydurma. 
        Sadece 'Internet_Arama_Araci' veya 'X_Twitter_Arama_Araci' isimlerini kullan.
        Araçları çağırırken JSON formatına sadık kal, asla <function> gibi işaretler kullanma.""",
        tools=[arama_motoru, x_arama_motoru],
        llm="groq/llama-3.3-70b-versatile", # Daha akıllı ve yüksek limitli modele döndük
        verbose=True,
        max_rpm=5, 
        allow_delegation=False
    )