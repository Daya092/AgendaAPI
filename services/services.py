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
from models.agenda import Usuario, Movimiento, TipoMovi, ClaseGym, HorarioClase, InscripcionClase

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


#--------------Clases de gym definidas------------

# ==================== CLASES DE GYM ====================

CLASES_PREDEFINIDAS = [
    {
        "nombre": "Yoga Matutino",
        "descripcion": "Clase de yoga para comenzar el día con energía",
        "instructor": "Ana Martínez",
        "capacidad_maxima": 15,
        "duracion": 60,
        "horarios": [
            {"dia_semana": "Lunes", "hora_inicio": "07:00", "hora_fin": "08:00"},
            {"dia_semana": "Miércoles", "hora_inicio": "07:00", "hora_fin": "08:00"},
            {"dia_semana": "Viernes", "hora_inicio": "07:00", "hora_fin": "08:00"}
        ]
    },
    {
        "nombre": "Spinning Intenso", 
        "descripcion": "Entrenamiento cardiovascular en bicicleta estática",
        "instructor": "Carlos Rodríguez",
        "capacidad_maxima": 20,
        "duracion": 45,
        "horarios": [
            {"dia_semana": "Lunes", "hora_inicio": "18:00", "hora_fin": "18:45"},
            {"dia_semana": "Martes", "hora_inicio": "19:00", "hora_fin": "19:45"},
            {"dia_semana": "Jueves", "hora_inicio": "18:00", "hora_fin": "18:45"}
        ]
    },
    {
        "nombre": "CrossFit",
        "descripcion": "Entrenamiento funcional de alta intensidad",
        "instructor": "María González", 
        "capacidad_maxima": 12,
        "duracion": 50,
        "horarios": [
            {"dia_semana": "Lunes", "hora_inicio": "17:00", "hora_fin": "17:50"},
            {"dia_semana": "Miércoles", "hora_inicio": "17:00", "hora_fin": "17:50"},
            {"dia_semana": "Viernes", "hora_inicio": "17:00", "hora_fin": "17:50"}
        ]
    },
    {
        "nombre": "Pilates",
        "descripcion": "Ejercicios de control corporal y respiración",
        "instructor": "Laura Sánchez",
        "capacidad_maxima": 10,
        "duracion": 55,
        "horarios": [
            {"dia_semana": "Martes", "hora_inicio": "09:00", "hora_fin": "09:55"},
            {"dia_semana": "Jueves", "hora_inicio": "09:00", "hora_fin": "09:55"},
            {"dia_semana": "Sábado", "hora_inicio": "10:00", "hora_fin": "10:55"}
        ]
    },
    {
        "nombre": "Zumba",
        "descripcion": "Baile fitness divertido y energético",
        "instructor": "David López",
        "capacidad_maxima": 25,
        "duracion": 60,
        "horarios": [
            {"dia_semana": "Lunes", "hora_inicio": "19:00", "hora_fin": "20:00"},
            {"dia_semana": "Miércoles", "hora_inicio": "19:00", "hora_fin": "20:00"},
            {"dia_semana": "Viernes", "hora_inicio": "19:00", "hora_fin": "20:00"}
        ]
    }
]

def inicializar_clases_gym():
    """Crea las clases predefinidas si no existen"""
    db: Session = SessionLocal()
    try:
        for clase_data in CLASES_PREDEFINIDAS:
            existe = db.query(ClaseGym).filter(ClaseGym.nombre == clase_data["nombre"]).first()
            if not existe:
                clase = ClaseGym(
                    nombre=clase_data["nombre"],
                    descripcion=clase_data["descripcion"],
                    instructor=clase_data["instructor"],
                    capacidad_maxima=clase_data["capacidad_maxima"],
                    duracion=clase_data["duracion"]
                )
                db.add(clase)
                db.commit()
                db.refresh(clase)
                
                # Crear horarios
                for horario_data in clase_data["horarios"]:
                    horario = HorarioClase(
                        clase_id=clase.id,
                        dia_semana=horario_data["dia_semana"],
                        hora_inicio=horario_data["hora_inicio"],
                        hora_fin=horario_data["hora_fin"]
                    )
                    db.add(horario)
                
                db.commit()
                logger.info(f"Clase creada: {clase_data['nombre']}")
                
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

# ==================== FUNCIONES DE CLASES ====================

def get_todas_clases() -> List[Dict]:
    """Obtiene todas las clases disponibles"""
    db: Session = SessionLocal()
    try:
        clases = db.query(ClaseGym).all()
        resultado = []
        for clase in clases:
            clase_dict = {
                "id": clase.id,
                "nombre": clase.nombre,
                "descripcion": clase.descripcion,
                "instructor": clase.instructor,
                "capacidad_maxima": clase.capacidad_maxima,
                "duracion": clase.duracion,
                "horarios": []
            }
            
            for horario in clase.horarios:
                # Calcular disponibilidad para este horario
                inscritos_count = db.query(InscripcionClase).filter(
                    InscripcionClase.horario_id == horario.id,
                    InscripcionClase.fecha_clase >= datetime.utcnow().date()
                ).count()
                
                disponibilidad = clase.capacidad_maxima - inscritos_count
                
                clase_dict["horarios"].append({
                    "id": horario.id,
                    "dia_semana": horario.dia_semana,
                    "hora_inicio": horario.hora_inicio,
                    "hora_fin": horario.hora_fin,
                    "disponibilidad": max(0, disponibilidad),
                    "lleno": disponibilidad <= 0
                })
            
            resultado.append(clase_dict)
        return resultado
    finally:
        db.close()

def get_horarios_disponibles(clase_id: int) -> List[Dict]:
    """Obtiene horarios disponibles para una clase específica"""
    db: Session = SessionLocal()
    try:
        clase = db.query(ClaseGym).filter(ClaseGym.id == clase_id).first()
        if not clase:
            return []
        
        horarios_disponibles = []
        for horario in clase.horarios:
            # Contar inscripciones futuras para este horario
            inscritos_count = db.query(InscripcionClase).filter(
                InscripcionClase.horario_id == horario.id,
                InscripcionClase.fecha_clase >= datetime.utcnow().date()
            ).count()
            
            disponibilidad = clase.capacidad_maxima - inscritos_count
            
            if disponibilidad > 0:
                horarios_disponibles.append({
                    "id": horario.id,
                    "dia_semana": horario.dia_semana,
                    "hora_inicio": horario.hora_inicio,
                    "hora_fin": horario.hora_fin,
                    "disponibilidad": disponibilidad
                })
        
        return horarios_disponibles
    finally:
        db.close()

def inscribir_en_clase(usuario_id: int, horario_id: int, fecha_clase: str) -> Dict:
    """Inscribe un usuario en una clase"""
    db: Session = SessionLocal()
    try:
        # Verificar disponibilidad
        horario = db.query(HorarioClase).filter(HorarioClase.id == horario_id).first()
        if not horario:
            return {"error": "Horario no encontrado"}
        
        # Contar inscripciones para esa fecha y horario
        inscritos_count = db.query(InscripcionClase).filter(
            InscripcionClase.horario_id == horario_id,
            InscripcionClase.fecha_clase == fecha_clase
        ).count()
        
        if inscritos_count >= horario.clase.capacidad_maxima:
            return {"error": "Clase llena para esta fecha"}
        
        # Verificar si ya está inscrito
        ya_inscrito = db.query(InscripcionClase).filter(
            InscripcionClase.usuario_id == usuario_id,
            InscripcionClase.horario_id == horario_id,
            InscripcionClase.fecha_clase == fecha_clase
        ).first()
        
        if ya_inscrito:
            return {"error": "Ya estás inscrito en esta clase"}
        
        # Crear inscripción
        inscripcion = InscripcionClase(
            usuario_id=usuario_id,
            horario_id=horario_id,
            fecha_clase=fecha_clase
        )
        db.add(inscripcion)
        db.commit()
        
        logger.info(f"Usuario {usuario_id} inscrito en clase {horario.clase.nombre}")
        
        return {
            "success": True,
            "mensaje": f"¡Inscrito exitosamente en {horario.clase.nombre}!",
            "clase": horario.clase.nombre,
            "dia": horario.dia_semana,
            "hora": horario.hora_inicio,
            "fecha": fecha_clase
        }
        
    except Exception:
        db.rollback()
        return {"error": "Error al inscribirse en la clase"}
    finally:
        db.close()

def get_mis_clases(usuario_id: int) -> List[Dict]:
    """Obtiene las clases en las que está inscrito el usuario"""
    db: Session = SessionLocal()
    try:
        inscripciones = db.query(InscripcionClase).filter(
            InscripcionClase.usuario_id == usuario_id,
            InscripcionClase.fecha_clase >= datetime.utcnow().date()
        ).all()
        
        resultado = []
        for inscripcion in inscripciones:
            resultado.append({
                "id": inscripcion.id,
                "clase_nombre": inscripcion.horario.clase.nombre,
                "instructor": inscripcion.horario.clase.instructor,
                "dia_semana": inscripcion.horario.dia_semana,
                "hora": inscripcion.horario.hora_inicio,
                "fecha_clase": inscripcion.fecha_clase.isoformat() if inscripcion.fecha_clase else None,
                "fecha_inscripcion": inscripcion.fecha_inscripcion.isoformat() if inscripcion.fecha_inscripcion else None
            })
        
        return resultado
    finally:
        db.close()
