import sys
import os

_root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _root_dir not in sys.path:
    sys.path.insert(0, _root_dir)

from datetime import datetime
import logging
from typing import Optional, Dict, List
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import Session
from config.database import SessionLocal
from models.agenda import Usuario, Movimiento, TipoMovi

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# ==================== FUNCIONES DE USUARIOS ====================

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

def delete_usuario(usuario_id: int) -> bool:
    db: Session = SessionLocal()
    try:
        u = db.query(Usuario).filter(Usuario.id == usuario_id).first()
        if not u:
            return False
        db.delete(u)
        db.commit()
        return True
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def authenticate_user(identifier: str, password: str) -> Optional[Usuario]:
    db: Session = SessionLocal()
    try:
        user = db.query(Usuario).filter(Usuario.correo == identifier).first()
        if not user:
            user = db.query(Usuario).filter(Usuario.name == identifier).first()
        if not user:
            return None
        if not check_password_hash(user.password, password):
            return None
        return user
    finally:
        db.close()

# ==================== FUNCIONES DE MOVIMIENTOS ====================

def _movimiento_to_dict(m: Movimiento) -> Dict:
    return {
        "id": m.id,
        "monto": m.monto,
        "descripcion": m.descripcion,
        "fecha": str(m.fecha),
        "usuario_id": m.usuario_id,
        "tipo_id": m.tipo_id,
        "usuario_nombre": m.usuario.name if m.usuario else None,
        "tipo_nombre": m.tipo.name if m.tipo else None
    }

def get_all_movimientos(usuario_id: Optional[int] = None) -> List[Dict]:
    """Obtiene movimientos, opcionalmente filtrados por usuario"""
    db: Session = SessionLocal()
    try:
        query = db.query(Movimiento)
        if usuario_id:
            query = query.filter(Movimiento.usuario_id == usuario_id)
        movimientos = query.all()
        return [_movimiento_to_dict(m) for m in movimientos]
    finally:
        db.close()

def get_movimientos_usuario_actual(usuario_id: int) -> List[Dict]:
    """Obtiene solo los movimientos del usuario autenticado"""
    return get_all_movimientos(usuario_id=usuario_id)

def get_movimiento_by_id(mov_id: int, usuario_id: Optional[int] = None) -> Optional[Dict]:
    """Obtiene un movimiento, con opción de verificar propiedad"""
    db: Session = SessionLocal()
    try:
        query = db.query(Movimiento).filter(Movimiento.id == mov_id)
        if usuario_id:
            query = query.filter(Movimiento.usuario_id == usuario_id)
        m = query.first()
        return _movimiento_to_dict(m) if m else None
    finally:
        db.close()

def create_movimiento(data: Dict) -> Dict:
    """Crea un nuevo movimiento"""
    db: Session = SessionLocal()
    try:
        fecha_str = data.get("fecha")
        if fecha_str:
            fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
        else:
            fecha = datetime.utcnow().date()

        movimiento = Movimiento(
            monto=data["monto"],
            descripcion=data.get("descripcion", ""),
            fecha=fecha,
            usuario_id=data["usuario_id"],
            tipo_id=data["tipo_id"]
        )
        db.add(movimiento)
        db.commit()
        db.refresh(movimiento)
        logger.info(f"Movimiento creado: {movimiento.id} para usuario {movimiento.usuario_id}")
        return _movimiento_to_dict(movimiento)
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def update_movimiento(mov_id: int, data: Dict, usuario_id: Optional[int] = None) -> Optional[Dict]:
    """Actualiza movimiento, con verificación de propiedad opcional"""
    db: Session = SessionLocal()
    try:
        query = db.query(Movimiento).filter(Movimiento.id == mov_id)
        if usuario_id:
            query = query.filter(Movimiento.usuario_id == usuario_id)
        
        movimiento = query.first()
        if not movimiento:
            return None

        if "monto" in data:
            movimiento.monto = data["monto"]
        if "descripcion" in data:
            movimiento.descripcion = data["descripcion"]
        if "fecha" in data:
            fecha_str = data["fecha"]
            movimiento.fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
        if "tipo_id" in data:
            movimiento.tipo_id = data["tipo_id"]

        db.commit()
        db.refresh(movimiento)
        return _movimiento_to_dict(movimiento)
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def delete_movimiento(mov_id: int, usuario_id: Optional[int] = None) -> bool:
    """Elimina movimiento, con verificación de propiedad opcional"""
    db: Session = SessionLocal()
    try:
        query = db.query(Movimiento).filter(Movimiento.id == mov_id)
        if usuario_id:
            query = query.filter(Movimiento.usuario_id == usuario_id)
        
        movimiento = query.first()
        if not movimiento:
            return False

        db.delete(movimiento)
        db.commit()
        return True
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

# ==================== FUNCIONES DE TIPOS ====================

def _tipo_to_dict(t: TipoMovi) -> Dict:
    return {"id": t.id, "name": t.name}

def get_all_tipos() -> List[Dict]:
    db: Session = SessionLocal()
    try:
        tipos = db.query(TipoMovi).all()
        return [_tipo_to_dict(t) for t in tipos]
    finally:
        db.close()

def get_tipo_by_id(tipo_id: int) -> Optional[Dict]:
    db: Session = SessionLocal()
    try:
        t = db.query(TipoMovi).filter(TipoMovi.id == tipo_id).first()
        return _tipo_to_dict(t) if t else None
    finally:
        db.close()

def create_tipo(data: Dict) -> Dict:
    db: Session = SessionLocal()
    try:
        tipo = TipoMovi(name=data["name"])
        db.add(tipo)
        db.commit()
        db.refresh(tipo)
        return _tipo_to_dict(tipo)
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def init_default_tipos():
    """Inicializa tipos por defecto si no existen"""
    db: Session = SessionLocal()
    try:
        defaults = ["Ingreso", "Gasto", "Transferencia"]
        for name in defaults:
            existe = db.query(TipoMovi).filter(TipoMovi.name == name).first()
            if not existe:
                db.add(TipoMovi(name=name))
        db.commit()
        logger.info("Tipos por defecto inicializados")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

# ==================== FUNCIONES DE REPORTES ====================

def get_resumen_usuario(usuario_id: int) -> Dict:
    """Obtiene resumen financiero del usuario"""
    db: Session = SessionLocal()
    try:
        movimientos = db.query(Movimiento).filter(Movimiento.usuario_id == usuario_id).all()
        
        total_ingresos = sum(m.monto for m in movimientos if m.tipo_id == 1)  # ID 1 = Ingreso
        total_gastos = sum(m.monto for m in movimientos if m.tipo_id == 2)    # ID 2 = Gasto
        balance = total_ingresos - total_gastos
        
        return {
            "total_ingresos": total_ingresos,
            "total_gastos": total_gastos,
            "balance": balance,
            "total_movimientos": len(movimientos)
        }
    finally:
        db.close()