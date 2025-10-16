from config.database import SessionLocal
from models.agenda import Usuario, Movimiento, TipoMovi
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# ------------------- USUARIOS -------------------

def get_all_usuarios():
    session = SessionLocal()
    usuarios = session.query(Usuario).all()
    result = []
    for u in usuarios:
        result.append({
            "id": u.id,
            "name": u.name,
            "telefono": u.telefono,
            "correo": u.correo
        })
    session.close()
    return result


def get_usuario_by_id(usuario_id):
    session = SessionLocal()
    u = session.query(Usuario).filter(Usuario.id == usuario_id).first()
    if u:
        result = {
            "id": u.id,
            "name": u.name,
            "telefono": u.telefono,
            "correo": u.correo
        }
    else:
        result = None
    session.close()
    return result


def authenticate_user(username, password):
    """Verifica si el usuario y contraseña son válidos."""
    session = SessionLocal()
    user = session.query(Usuario).filter(Usuario.name == username).first()
    if user and check_password_hash(user.password, password):
        session.close()
        return user
    session.close()
    return None


def create_usuario(data):
    """Crea un usuario nuevo con contraseña cifrada."""
    session = SessionLocal()
    hashed_pw = generate_password_hash(data["password"])  # 🔒 cifrado seguro
    u = Usuario(
        name=data["name"],
        correo=data["correo"],
        telefono=data.get("telefono"),
        password=hashed_pw
    )
    session.add(u)
    session.commit()
    session.refresh(u)
    result = {
        "id": u.id,
        "name": u.name,
        "telefono": u.telefono,
        "correo": u.correo
    }
    session.close()
    return result


def update_usuario(usuario_id, data):
    session = SessionLocal()
    u = session.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not u:
        session.close()
        return None
    u.name = data.get("name", u.name)
    u.correo = data.get("correo", u.correo)
    u.telefono = data.get("telefono", u.telefono)
    if "password" in data:  # Si desea actualizar contraseña
        u.password = generate_password_hash(data["password"])
    session.commit()
    result = {
        "id": u.id,
        "name": u.name,
        "telefono": u.telefono,
        "correo": u.correo
    }
    session.close()
    return result


def delete_usuario(usuario_id):
    session = SessionLocal()
    u = session.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not u:
        session.close()
        return False
    session.delete(u)
    session.commit()
    session.close()
    return True

# ------------------- MOVIMIENTOS -------------------

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
