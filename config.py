from urllib.parse import quote_plus

class Config:
    SERVER = ''
    DATABASE = ''
    PORT = ''
    USERNAME = ''
    PASSWORD = '' 
    PASSWORD_ENCODED = quote_plus(PASSWORD)  

    SQLALCHEMY_DATABASE_URI = f"postgresql://{USERNAME}:{PASSWORD_ENCODED}@{SERVER}:{PORT}/{DATABASE}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = ''