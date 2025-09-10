from Config.database import SessionLocal
from Models.agenda import Usuario, TipoMovi, Movimiento
from sqlalchemy.orm import joinedload

# -------------------------
# USUARIOS
# -------------------------
def get_all_usuarios():
    session = SessionLocal()
    usuarios = session.query(Usuario).options(joinedload(Usuario.movimientos)).all()
    result = []
    for u in usuarios:
        result.append({
            'id': u.id,
            'name': u.name,
            'telefono': u.telefono,
            'correo': u.correo,
            'movimientos': [
                {
                    'id': m.id,
                    'monto': m.monto,
                    'descripcion': m.descripcion,
                    'fecha': m.fecha.isoformat() if m.fecha else None,
                    'tipo': m.tipo.name if m.tipo else None
                }
                for m in u.movimientos
            ]
        })
    session.close()
    return result


def get_usuario_by_id(usuario_id):
    session = SessionLocal()
    u = session.query(Usuario).options(joinedload(Usuario.movimientos)).filter(Usuario.id == usuario_id).first()
    if u:
        result = {
            'id': u.id,
            'name': u.name,
            'telefono': u.telefono,
            'correo': u.correo,
            'movimientos': [
                {
                    'id': m.id,
                    'monto': m.monto,
                    'descripcion': m.descripcion,
                    'fecha': m.fecha.isoformat() if m.fecha else None,
                    'tipo': m.tipo.name if m.tipo else None
                }
                for m in u.movimientos
            ]
        }
    else:
        result = None
    session.close()
    return result


def create_usuario(data):
    session = SessionLocal()
    usuario = Usuario(
        name=data['name'],
        telefono=data.get('telefono'),
        correo=data['correo']
    )
    session.add(usuario)
    session.commit()
    result = {
        'id': usuario.id,
        'name': usuario.name,
        'telefono': usuario.telefono,
        'correo': usuario.correo,
        'movimientos': []
    }
    session.close()
    return result


def update_usuario(usuario_id, data):
    session = SessionLocal()
    usuario = session.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        session.close()
        return None
    usuario.name = data.get('name', usuario.name)
    usuario.telefono = data.get('telefono', usuario.telefono)
    usuario.correo = data.get('correo', usuario.correo)
    session.commit()
    result = {
        'id': usuario.id,
        'name': usuario.name,
        'telefono': usuario.telefono,
        'correo': usuario.correo
    }
    session.close()
    return result


def delete_usuario(usuario_id):
    session = SessionLocal()
    usuario = session.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        session.close()
        return False
    session.delete(usuario)
    session.commit()
    session.close()
    return True


# -------------------------
# TIPOS
# -------------------------
def init_default_tipos():
    session = SessionLocal()
    defaults = ["Ingreso", "Gasto"]
    for name in defaults:
        tipo = session.query(TipoMovi).filter(TipoMovi.name == name).first()
        if not tipo:
            session.add(TipoMovi(name=name))
    session.commit()
    session.close()


def get_all_tipos():
    session = SessionLocal()
    tipos = session.query(TipoMovi).options(joinedload(TipoMovi.movimientos)).all()
    result = []
    for t in tipos:
        result.append({
            'id': t.id,
            'name': t.name,
            'movimientos': [m.id for m in t.movimientos]
        })
    session.close()
    return result




# -------------------------
# MOVIMIENTOS
# -------------------------
def get_all_movimientos():
    session = SessionLocal()
    movimientos = session.query(Movimiento).options(joinedload(Movimiento.usuario), joinedload(Movimiento.tipo)).all()
    result = []
    for m in movimientos:
        result.append({
            'id': m.id,
            'monto': m.monto,
            'descripcion': m.descripcion,
            'fecha': m.fecha.isoformat() if m.fecha else None,
            'usuario': m.usuario.name if m.usuario else None,
            'tipo': m.tipo.name if m.tipo else None
        })
    session.close()
    return result


def get_movimiento_by_id(movimiento_id):
    session = SessionLocal()
    m = session.query(Movimiento).options(joinedload(Movimiento.usuario), joinedload(Movimiento.tipo)).filter(Movimiento.id == movimiento_id).first()
    if m:
        result = {
            'id': m.id,
            'monto': m.monto,
            'descripcion': m.descripcion,
            'fecha': m.fecha.isoformat() if m.fecha else None,
            'usuario': m.usuario.name if m.usuario else None,
            'tipo': m.tipo.name if m.tipo else None
        }
    else:
        result = None
    session.close()
    return result


def create_movimiento(data):
    session = SessionLocal()
    movimiento = Movimiento(
        monto=data['monto'],
        descripcion=data.get('descripcion'),
        fecha=data['fecha'],
        usuario_id=data['usuario_id'],
        tipo_id=data['tipo_id']
    )
    session.add(movimiento)
    session.commit()
    result = {
        'id': movimiento.id,
        'monto': movimiento.monto,
        'descripcion': movimiento.descripcion,
        'fecha': movimiento.fecha.isoformat() if movimiento.fecha else None,
        'usuario_id': movimiento.usuario_id,
        'tipo_id': movimiento.tipo_id
    }
    session.close()
    return result


def update_movimiento(movimiento_id, data):
    session = SessionLocal()
    movimiento = session.query(Movimiento).filter(Movimiento.id == movimiento_id).first()
    if not movimiento:
        session.close()
        return None
    movimiento.monto = data.get('monto', movimiento.monto)
    movimiento.descripcion = data.get('descripcion', movimiento.descripcion)
    movimiento.fecha = data.get('fecha', movimiento.fecha)
    movimiento.usuario_id = data.get('usuario_id', movimiento.usuario_id)
    movimiento.tipo_id = data.get('tipo_id', movimiento.tipo_id)
    session.commit()
    result = {
        'id': movimiento.id,
        'monto': movimiento.monto,
        'descripcion': movimiento.descripcion,
        'fecha': movimiento.fecha.isoformat() if movimiento.fecha else None,
        'usuario_id': movimiento.usuario_id,
        'tipo_id': movimiento.tipo_id


