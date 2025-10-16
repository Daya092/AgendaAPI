import sys
import os

# Asegurar que el directorio padre (workspace) esté en sys.path para poder importar "config"
_root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _root_dir not in sys.path:
    sys.path.insert(0, _root_dir)

from datetime import datetime
import logging
from typing import Optional, Dict, List
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import Session
from config.database import SessionLocal
from models.agenda import Usuario, Movimiento, TipoMovi  # importa modelos reales que uses

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def _usuario_to_dict(u: Usuario) -> Dict:
    return {
        "id": u.id,
        "name": getattr(u, "name", None),
        "correo": getattr(u, "correo", None),
        "telefono": getattr(u, "telefono", None),
    }

def get_all_usuarios() -> List[Dict]:
    db: Session = SessionLocal()
    try:
        usuarios = db.query(Usuario).all()
        return [_usuario_to_dict(u) for u in usuarios]
    finally:
        db.close()

def get_usuario_by_id(usuario_id: int) -> Optional[Dict]:
    db: Session = SessionLocal()
    try:
        u = db.query(Usuario).filter(Usuario.id == usuario_id).first()
        return _usuario_to_dict(u) if u else None
    finally:
        db.close()

def create_usuario(data: Dict) -> Dict:
    """
    data esperado: {'name','correo','password', 'telefono'(opcional)}
    """
    db: Session = SessionLocal()
    try:
        if db.query(Usuario).filter(Usuario.correo == data.get("correo")).first():
            raise ValueError("El correo ya está registrado")

        hashed = generate_password_hash(data["password"])
        nuevo = Usuario(
            name=data.get("name"),
            correo=data.get("correo"),
            telefono=data.get("telefono", ""),
            password=hashed,
        )
        db.add(nuevo)
        db.commit()
        db.refresh(nuevo)
        logger.info(f"Usuario creado: {nuevo.correo}")
        return _usuario_to_dict(nuevo)
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def update_usuario(usuario_id: int, updates: Dict) -> Optional[Dict]:
    db: Session = SessionLocal()
    try:
        u = db.query(Usuario).filter(Usuario.id == usuario_id).first()
        if not u:
            return None
        if "name" in updates:
            u.name = updates["name"]
        if "correo" in updates:
            u.correo = updates["correo"]
        if "telefono" in updates:
            u.telefono = updates["telefono"]
        if "password" in updates and updates["password"]:
            u.password = generate_password_hash(updates["password"])
        db.commit()
        db.refresh(u)
        return _usuario_to_dict(u)
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def delete_usuario(usuario_id: int) -> Optional[Dict]:
    db: Session = SessionLocal()
    try:
        u = db.query(Usuario).filter(Usuario.id == usuario_id).first()
        if not u:
            return None
        db.delete(u)
        db.commit()
        return _usuario_to_dict(u)
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def authenticate_user(identifier: str, password: str) -> Optional[Usuario]:
    """
    identifier puede ser nombre (name) o correo.
    Devuelve la instancia Usuario si las credenciales son válidas, o None.
    """
    db: Session = SessionLocal()
    try:
        # primero por correo
        user = db.query(Usuario).filter(Usuario.correo == identifier).first()
        if not user:
            # luego por name
            user = db.query(Usuario).filter(Usuario.name == identifier).first()
        if not user:
            return None
        if not check_password_hash(user.password, password):
            return None
        return user
    finally:
        db.close()

def get_all_movimientos():
    session = SessionLocal()
    movimientos = session.query(Movimiento).all()
    result = []
    for m in movimientos:
        result.append({
            "id": m.id,
            "monto": m.monto,
            "descripcion": m.descripcion,
            "fecha": str(m.fecha),
            "usuario_id": m.usuario_id,
            "tipo_id": m.tipo_id
        })
    session.close()
    return result


def get_movimiento_by_id(mov_id):
    session = SessionLocal()
    m = session.query(Movimiento).filter(Movimiento.id == mov_id).first()
    if m:
        result = {
            "id": m.id,
            "monto": m.monto,
            "descripcion": m.descripcion,
            "fecha": str(m.fecha),
            "usuario_id": m.usuario_id,
            "tipo_id": m.tipo_id
        }
    else:
        result = None
    session.close()
    return result


def create_movimiento(data):
    session = SessionLocal()

    fecha_str = data.get("fecha")
    if fecha_str:
        fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
    else:
        fecha = datetime.utcnow().date()

    m = Movimiento(
        monto=data["monto"],
        descripcion=data.get("descripcion"),
        fecha=fecha,
        usuario_id=data["usuario_id"],
        tipo_id=data["tipo_id"]
    )
    session.add(m)
    session.commit()
    session.refresh(m)
    session.close()
    return {
        "id": m.id,
        "monto": m.monto,
        "descripcion": m.descripcion,
        "fecha": str(m.fecha),
        "usuario_id": m.usuario_id,
        "tipo_id": m.tipo_id
    }


def update_movimiento(mov_id, data):
    session = SessionLocal()
    m = session.query(Movimiento).filter(Movimiento.id == mov_id).first()
    if not m:
        session.close()
        return None
    m.monto = data.get("monto", m.monto)
    m.descripcion = data.get("descripcion", m.descripcion)
    m.fecha = data.get("fecha", m.fecha)
    m.usuario_id = data.get("usuario_id", m.usuario_id)
    m.tipo_id = data.get("tipo_id", m.tipo_id)
    session.commit()
    result = {
        "id": m.id,
        "monto": m.monto,
        "descripcion": m.descripcion,
        "fecha": str(m.fecha),
        "usuario_id": m.usuario_id,
        "tipo_id": m.tipo_id
    }
    session.close()
    return result


def delete_movimiento(mov_id):
    session = SessionLocal()
    m = session.query(Movimiento).filter(Movimiento.id == mov_id).first()
    if not m:
        session.close()
        return False
    session.delete(m)
    session.commit()
    session.close()
    return True

# ------------------- TIPOS -------------------

def get_all_tipos():
    session = SessionLocal()
    tipos = session.query(TipoMovi).all()
    session.close()
    return [{"id": t.id, "name": t.name} for t in tipos]


def init_default_tipos():
    session = SessionLocal()
    defaults = ["Ingreso", "Gasto", "Transferencia"]
    for name in defaults:
        existe = session.query(TipoMovi).filter(TipoMovi.name == name).first()
        if not existe:
            session.add(TipoMovi(name=name))
    session.commit()
    session.close()
