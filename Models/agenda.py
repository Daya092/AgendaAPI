from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    telefono = Column(String(50), nullable=True)
    correo = Column(String(255), nullable=False, unique=True)

    movimientos = relationship("Movimiento", back_populates="usuario")


class TipoMovi(Base):
    __tablename__ = "tipomovis"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)

    movimientos = relationship("Movimiento", back_populates="tipo")


class Movimiento(Base):
    __tablename__ = "movimientos"

    id = Column(Integer, primary_key=True, index=True)
    monto = Column(Float, nullable=False)
    descripcion = Column(String(255), nullable=True)
    fecha = Column(Date, nullable=False)

    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    tipo_id = Column(Integer, ForeignKey("tipomovis.id"))

    usuario = relationship("Usuario", back_populates="movimientos")
    tipo = relationship("TipoMovi", back_populates="movimientos")

