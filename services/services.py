# -----------------------
# Usuarios en memoria
# -----------------------
usuarios = []
next_usuario_id = 1

def get_all_usuarios():
    return usuarios

def get_usuario_by_id(usuario_id):
    return next((u for u in usuarios if u["id"] == usuario_id), None)

def create_usuario(data):
    global next_usuario_id
    usuario = {
        "id": next_usuario_id,
        "nombre": data.get("nombre"),
        "email": data.get("email")
    }
    usuarios.append(usuario)
    next_usuario_id += 1
    return usuario

def update_usuario(usuario_id, data):
    for u in usuarios:
        if u["id"] == usuario_id:
            u["nombre"] = data.get("nombre", u["nombre"])
            u["email"] = data.get("email", u["email"])
            return u
    return None

def delete_usuario(usuario_id):
    global usuarios
    if any(u["id"] == usuario_id for u in usuarios):
        usuarios = [u for u in usuarios if u["id"] != usuario_id]
        return True
    return False

# -----------------------
# Tipos fijos
# -----------------------
tipos = [
    {"id": 1, "nombre": "Ingresos"},
    {"id": 2, "nombre": "Gastos"},
    {"id": 3, "nombre": "Total"}
]

def get_all_tipos():
    return tipos

def get_tipo_by_id(tipo_id):
    return next((t for t in tipos if t["id"] == tipo_id), None)

# -----------------------
# Movimientos en memoria
# -----------------------
movimientos = []
next_movimiento_id = 1

def get_all_movimientos():
    return movimientos

def get_movimiento_by_id(movimiento_id):
    return next((m for m in movimientos if m["id"] == movimiento_id), None)

def create_movimiento(data):
    global next_movimiento_id
    movimiento = {
        "id": next_movimiento_id,
        "tipo_id": data.get("tipo_id"),
        "usuario_id": data.get("usuario_id"),
        "monto": data.get("monto"),
        "descripcion": data.get("descripcion")
    }
    movimientos.append(movimiento)
    next_movimiento_id += 1
    return movimiento

def update_movimiento(movimiento_id, data):
    for m in movimientos:
        if m["id"] == movimiento_id:
            m["tipo_id"] = data.get("tipo_id", m["tipo_id"])
            m["usuario_id"] = data.get("usuario_id", m["usuario_id"])
            m["monto"] = data.get("monto", m["monto"])
            m["descripcion"] = data.get("descripcion", m["descripcion"])
            return m
    return None

def delete_movimiento(movimiento_id):
    global movimientos
    if any(m["id"] == movimiento_id for m in movimientos):
        movimientos = [m for m in movimientos if m["id"] != movimiento_id]
        return True
    return False

