from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

# Leer variables por separado (defínelas en .env o en el entorno)
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")

# Validar que las credenciales esenciales estén presentes
if not (MYSQL_USER and MYSQL_PASSWORD and MYSQL_DATABASE):
    raise RuntimeError("Faltan credenciales DB. Define MYSQL_USER, MYSQL_PASSWORD y MYSQL_DATABASE en .env o variables de entorno.")

# Permitir override con DATABASE_URL si ya lo tienes
DATABASE_URL = os.getenv("DATABASE_URL") or f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
