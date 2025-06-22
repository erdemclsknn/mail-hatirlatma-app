from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Gorev(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    baslik = db.Column(db.String(255), nullable=False)
    aciklama = db.Column(db.Text, nullable=True)
    onem = db.Column(db.Integer, nullable=False)
    yapilma_tarihi = db.Column(db.Date, nullable=False)
    hedef_tarih = db.Column(db.Date, nullable=False)
    hatirlatma_gunleri = db.Column(db.String(255), nullable=False)  # JSON string: "[1,2,7,30]"
    mailler = db.Column(db.String(1000), nullable=False)  # JSON string: "[\"a@a.com\",\"b@b.com\"]"
    durum = db.Column(db.String(50), default="aktif")  # aktif, silindi, gönderildi, vazgecildi
    olusturma_tarihi = db.Column(db.DateTime, default=datetime.utcnow)

class MailAdres(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    aktif = db.Column(db.Boolean, default=True)

class MailLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gorev_id = db.Column(db.Integer, db.ForeignKey('gorev.id'), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    gonderim_tarihi = db.Column(db.DateTime, default=datetime.utcnow)
    durum = db.Column(db.String(50))  # gonderildi, basarisiz
