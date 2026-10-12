from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from config import settings
import os

#1. Definimos la URL de la base de datos SQLite (se creará un archivo llamado biblioteca.db
DATABASE_URL= settings.database_url

#2. Creamos el motor de conexión engine
if DATABASE_URL.startswith('sqlite'):
    engine=create_engine(
        DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    engine=create_engine(DATABASE_URL)

#3. Creamos la fábrica de sesiones para interactuar con la BD
SessionLocal= sessionmaker(autocommit= False, autoflush=False, bind=engine)

#4. Clase para definir nuestros modelos de base de datos
Base= declarative_base()

def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()