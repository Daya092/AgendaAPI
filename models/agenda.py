import sys
import os

# Asegurar que la raíz del workspace esté en sys.path para poder importar config.*
_root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _root_dir not in sys.path:
    sys.path.insert(0, _root_dir)

from sqlalchemy import Column, Integer, String, DateTime, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base  # ← Usar la misma Base de database.py

# ELIMINA esta línea - ya existe en database.py
# Base = declarative_base()

# Modelo para la tabla de usuarios
class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    correo = Column(String, unique=True, nullable=False)
    telefono = Column(String, nullable=True)
    password = Column(String, nullable=True)  # <- asegurar que exista

    # Relación con movimientos (un usuario puede tener muchos movimientos)
    movimientos = relationship("Movimiento", back_populates="usuario")


# Modelo para la tabla de tipos de movimiento
class TipoMovi(Base):
    __tablename__ = "tipomovis"

    id = Column(Integer, primary_key=True, index=True)      # ID único del tipo
    name = Column(String(100), nullable=False)              # Nombre del tipo (ej: ingreso, gasto)

    # Relación con movimientos (un tipo puede estar en muchos movimientos)
    movimientos = relationship("Movimiento", back_populates="tipo")


# Modelo para la tabla de movimientos
class Movimiento(Base):
    __tablename__ = "movimientos"

    id = Column(Integer, primary_key=True, index=True)      # ID único del movimiento
    monto = Column(Float, nullable=False)                   # Valor del movimiento
    descripcion = Column(String(255), nullable=True)        # Texto descriptivo (opcional)
    fecha = Column(Date, nullable=False)                    # Fecha del movimiento

    # Claves foráneas para enlazar con usuario y tipo
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    tipo_id = Column(Integer, ForeignKey("tipomovis.id"))

    # Relaciones hacia Usuario y TipoMovi
    usuario = relationship("Usuario", back_populates="movimientos")
    tipo = relationship("TipoMovi", back_populates="movimientos")