from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class LibroDB(Base):
    __tablename__ = "libros"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True)
    autor = Column(String, index=True)
    prestado = Column(Boolean, default=False)
    
    # Debe ser "usuarios.id" en plural
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    
    propietario = relationship("UsuarioDB", back_populates="libros")


class UsuarioDB(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    libros = relationship("LibroDB", back_populates="propietario")