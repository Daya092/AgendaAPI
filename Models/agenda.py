from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    telefono = Column(String(255), nullable=False)
    correo = Column(String(255), nullable=False)
    albums = relationship('Album', back_populates='band', cascade='all, delete-orphan')

class TipoMovi(Base):
    __tablename__ = 'tipomovis'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    albums = relationship('Album', back_populates='band', cascade='all, delete-orphan')

class Movimiento(Base):
    __tablename__ = 'movimientos'
    id = Column(Integer, primary_key=True, index=True)
    monto = Column(String(255), nullable=False)
    fecha = Column(Date(255), nullable=False)
    fecha = Column(Integer, ForeignKey('bands.id'))
    band_id = Column(Integer, ForeignKey('bands.id'))
    band = relationship('Band', back_populates='albums')
    
