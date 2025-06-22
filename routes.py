from flask import render_template, request, redirect, url_for, flash
from app import app, db
from models import Gorev, MailAdres, MailLog
from config import Config
from datetime import datetime
import json

@app.route('/')
def index():
    gorevler = Gorev.query.filter(Gorev.durum != 'silindi').all()
    toplam = Gorev.query.count()
    gonderilen = MailLog.query.count()
    vazgecilen = Gorev.query.filter(Gorev.durum == 'vazgecildi').count()
    return render_template('dashboard.html', gorevler=gorevler, toplam=toplam,
                           gonderilen=gonderilen, vazgecilen=vazgecilen)

@app.route('/gorev/ekle', methods=['GET', 'POST'])
def gorev_ekle():
    if request.method == 'POST':
        baslik = request.form.get('baslik')
        aciklama = request.form.get('aciklama')
        onem = int(request.form.get('onem'))
        yapilma_tarihi = datetime.strptime(request.form.get('yapilma_tarihi'), '%Y-%m-%d').date()
        hedef_tarih = datetime.strptime(request.form.get('hedef_tarih'), '%Y-%m-%d').date()
        hatirlatma_gunleri = request.form.getlist('hatirlatma_gunleri')
        mailler = request.form.getlist('mailler')

        yeni_gorev = Gorev(
            baslik=baslik,
            aciklama=aciklama,
            onem=onem,
            yapilma_tarihi=yapilma_tarihi,
            hedef_tarih=hedef_tarih,
            hatirlatma_gunleri=json.dumps(hatirlatma_gunleri),
            mailler=json.dumps(mailler),
            durum='aktif'
        )
        db.session.add(yeni_gorev)
        db.session.commit()
        flash('Görev başarıyla eklendi.', 'success')
        return redirect(url_for('index'))

    tum_mailler = MailAdres.query.filter_by(aktif=True).all()
    return render_template('gorev_ekle.html', mailler=tum_mailler)

@app.route('/mailler', methods=['GET', 'POST'])
def mailler():
    if request.method == 'POST':
        yeni_mail = request.form.get('email')
        if yeni_mail:
            db.session.add(MailAdres(email=yeni_mail))
            db.session.commit()
            flash('Mail adresi eklendi.', 'success')
        return redirect(url_for('mailler'))

    liste = MailAdres.query.all()
    return render_template('mailler.html', liste=liste)

@app.route('/sil/<int:id>')
def gorev_sil(id):
    gorev = Gorev.query.get_or_404(id)
    gorev.durum = 'silindi'
    db.session.commit()
    flash('Görev silindi.', 'warning')
    return redirect(url_for('index'))

@app.route('/silinenler')
def silinenler():
    silinenler = Gorev.query.filter_by(durum='silindi').all()
    return render_template('silinenler.html', silinenler=silinenler)

@app.route('/gonderilenler')
def gonderilenler():
    loglar = MailLog.query.order_by(MailLog.gonderim_tarihi.desc()).all()
    return render_template('gonderilenler.html', loglar=loglar)


@app.route('/testmail')
def testmail():
    import smtplib
    from email.mime.text import MIMEText
    from config import Config  # bu satır önemli

    try:
        msg = MIMEText("Bu bir test mailidir.")
        msg['Subject'] = "Test Mail"
        msg['From'] = Config.SMTP_USERNAME
        msg['To'] = 'erdemak794@gmail.com'

        server = smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT)
        server.starttls()
        server.login(Config.SMTP_USERNAME, Config.SMTP_PASSWORD)
        server.sendmail(Config.SMTP_USERNAME, 'erdemak794@gmail.com', msg.as_string())
        server.quit()
        return "✅ Mail gönderildi!"
    except Exception as e:
        return f"❌ HATA: {str(e)}"



@app.route('/mail/sil/<int:id>', methods=['POST'])
def mail_sil(id):
    mail = MailAdres.query.get_or_404(id)
    db.session.delete(mail)
    db.session.commit()
    flash('Mail adresi silindi.', 'success')
    return redirect(url_for('mailler'))
