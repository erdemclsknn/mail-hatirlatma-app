import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'gizli-anahtar'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'instance', 'hatirlatma.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SMTP_SERVER = 'mail.kebirsut.com.tr'
    SMTP_PORT = 587
    SMTP_USERNAME = 'hatirlatma@kebirsut.com.tr'
    SMTP_PASSWORD = 'Erdem61'
