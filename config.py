class Config:
    DEBUG = True
    SECRET_KEY = "minha-chave-secreta"
    SQLALCHEMY_DATABASE_URI = "sqlite:///banco.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
