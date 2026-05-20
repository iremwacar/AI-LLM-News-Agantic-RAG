import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from crewai.tools import BaseTool

class MailGonderici(BaseTool):
    name: str = "Email_Gonderme_Araci"
    description: str = "Hazırlanan yapay zeka bültenini belirtilen adrese mail olarak gönderir."

    def _run(self, icerik: str) -> str:
        gonderen = os.getenv("EMAIL_USER")
        sifre = os.getenv("EMAIL_PASSWORD")
        alici = gonderen # Şimdilik kendine gönderiyorsun

        msg = MIMEMultipart()
        msg['From'] = gonderen
        msg['To'] = alici
        msg['Subject'] = "🚀 Günlük Global AI Bülteni"

        # Markdown'ı mailde düzgün görünmesi için HTML'e çevirmeden düz metin olarak gönderiyoruz
        msg.attach(MIMEText(icerik, 'plain'))

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(gonderen, sifre)
                server.sendmail(gonderen, alici, msg.as_string())
            return "Bülten başarıyla mail adresine gönderildi!"
        except Exception as e:
            return f"Mail gönderilirken hata oluştu: {str(e)}"

mail_tool = MailGonderici()