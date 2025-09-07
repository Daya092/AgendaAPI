# services/services.py

# Datos en memoria
usuarios = []
next_id = 1

# ----------------- GET ALL -----------------
def get_all_usuarios():
    return usuarios

# ----------------- GET BY ID -----------------
def get_usuario_by_id(usuario_id):
    usuario = next((u for u in usuarios if u["id"] == usuario_id), None)
    return usuario

# ----------------- CREATE -----------------
def create_usuario(data):
    global next_id
    usuario = {
        "id": next_id,
        "nombre": data.get("nombre"),
        "email": data.get("email")
    }
    usuarios.append(usuario)
    next_id += 1
    return usuario

# ----------------- UPDATE -----------------
def update_usuario(usuario_id, data):
    for u in usuarios:
        if u["id"] == usuario_id:
            u["nombre"] = data.get("nombre", u["nombre"])
            u["email"] = data.get("email", u["email"])
            return u
    return None

# ----------------- DELETE -----------------
def delete_usuario(usuario_id):
    global usuarios
    if any(u["id"] == usuario_id for u in usuarios):
        usuarios = [u for u in usuarios if u["id"] != usuario_id]
        return True
    return False
