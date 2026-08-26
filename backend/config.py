import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()

class Config:
    DB_USER=os.getenv("DB_USER","root")
    DB_PASSWORD=os.getenv("DB_PASSWORD","")
    DB_HOST=os.getenv("DB_HOST","localhost")
    DB_PORT=os.getenv("DB_PORT","3306")
    DB_NAME=os.getenv("DB_NAME","libelli")
    DATABASE_URL=os.getenv("DATABASE_URL")
    if DATABASE_URL:
        SQLALCHEMY_DATABASE_URI=DATABASE_URL
    elif os.getenv("USE_MYSQL","false").lower()=="true":
        SQLALCHEMY_DATABASE_URI=f"mysql+pymysql://{quote_plus(DB_USER)}:{quote_plus(DB_PASSWORD)}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"
    else:
        SQLALCHEMY_DATABASE_URI="sqlite:///libelli.db"
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SECRET_KEY=os.getenv("SECRET_KEY","dev")
