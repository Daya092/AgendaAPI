import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_DB = os.getenv('MYSQL_DB')

# Intentar construir URL si hay variables de entorno
DATABASE_URL = None
if MYSQL_USER and MYSQL_PASSWORD and MYSQL_HOST and MYSQL_DB:
    DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"
else:
    DATABASE_URL = os.getenv('DATABASE_URI')

# Solo crear engine si hay URL válida
engine = create_engine(DATABASE_URL, echo=True) if DATABASE_URL else None
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) if engine else None
Base = declarative_base()
