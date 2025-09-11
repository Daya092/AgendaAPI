# Importamos lo necesario de SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

# Base principal para declarar los modelos
Base = declarative_base()

# Modelo para la tabla de usuarios
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)      # ID único del usuario
    name = Column(String(255), nullable=False)              # Nombre del usuario
    telefono = Column(String(50), nullable=True)            # Teléfono (opcional)
    correo = Column(String(255), nullable=False, unique=True) # Correo (obligatorio y único)

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

