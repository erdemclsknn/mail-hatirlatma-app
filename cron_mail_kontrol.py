from app import app, db
from models import Gorev, MailLog
from datetime import datetime, timedelta
from email.mime.text import MIMEText
import smtplib
import json

# SMTP ayarları doğrudan tanımlandı
SMTP_SERVER = "mail.kebirsut.com.tr"
SMTP_PORT = 587
SMTP_USERNAME = "hatirlatma@kebirsut.com.tr"
SMTP_PASSWORD = "Erdem61"

def mail_gonder(gorev, email):
    subject = f"Hatırlatma: {gorev.baslik}"
    body = f"""
Merhaba,

{gorev.baslik} başlıklı görev için hatırlatma:

Açıklama: {gorev.aciklama}
Yapılması gereken tarih: {gorev.hedef_tarih.strftime('%d.%m.%Y')}

Saygılar,
Kebir Makine Takip Sistemi
"""
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = SMTP_USERNAME
    msg['To'] = email

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(SMTP_USERNAME, email, msg.as_string())
        server.quit()

        log = MailLog(gorev_id=gorev.id, email=email, gonderim_tarihi=datetime.now(), durum='gonderildi')
        db.session.add(log)
        print(f"[OK] Gönderildi: {email} → {gorev.baslik}")

    except Exception as e:
        log = MailLog(gorev_id=gorev.id, email=email, gonderim_tarihi=datetime.now(), durum='basarisiz')
        db.session.add(log)
        print(f"[HATA] {email} → {gorev.baslik} gönderilemedi: {e}")

def gorevleri_kontrol_et():
    with app.app_context():
        bugun = datetime.today().date()
        gorevler = Gorev.query.filter_by(durum='aktif').all()

        for gorev in gorevler:
            try:
                hedef = gorev.hedef_tarih
                hatirlatma_gunleri = json.loads(gorev.hatirlatma_gunleri)
                mailler = json.loads(gorev.mailler)

                for gun in hatirlatma_gunleri:
                    if not gun.strip().isdigit():
                        continue

                    kalan_gun = (hedef - bugun).days
                    if kalan_gun == int(gun):
                        for email in mailler:
                            onceki = MailLog.query.filter_by(gorev_id=gorev.id, email=email)\
                                .filter(MailLog.gonderim_tarihi >= datetime.combine(bugun, datetime.min.time()))\
                                .first()
                            if not onceki:
                                mail_gonder(gorev, email)
            except Exception as e:
                print(f"[HATA] Görev işlenemedi: {e}")
                continue

        db.session.commit()

if __name__ == '__main__':
    gorevleri_kontrol_et()
