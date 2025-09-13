
# AgendaAPI

API REST para gestión de usuarios, movimientos y tipos de gasto/ingreso.

## Instalación y ejecución

1. Instala las dependencias necesarias:
	 - Python 3.12+
	 - Flask
	 - SQLAlchemy
	 - python-dotenv

2. Ejecuta la aplicación:
	 ```bash
	 python src/app.py
	 ```

## Estructura de la base de datos

- **Usuario**: id, name, correo, telefono
- **TipoMovi**: id, name
- **Movimiento**: id, monto, descripcion, fecha, usuario_id, tipo_id

## Endpoints principales

### Usuarios

- `GET /usuarios` — Lista todos los usuarios
- `GET /usuarios/<id>` — Obtiene usuario por ID
- `POST /usuarios` — Crea usuario
	- Body: `{ "name": "Daya", "correo": "daya@email.com", "telefono": "3001234567" }`
- `PUT /usuarios/<id>` — Actualiza usuario
	- Body: `{ "name": "Dayana", "correo": "dayana@email.com", "telefono": "3009876543" }`
- `DELETE /usuarios/<id>` — Elimina usuario

### Tipos de movimiento

- `GET /tipos` — Lista todos los tipos

### Movimientos

- `GET /movimientos` — Lista todos los movimientos
- `GET /movimientos/<id>` — Obtiene movimiento por ID
- `POST /movimientos` — Crea movimiento
	- Body: `{ "tipo_id": 1, "usuario_id": 1, "monto": 1500, "descripcion": "Pago de proyecto", "fecha": "2025-09-11" }`
- `PUT /movimientos/<id>` — Actualiza movimiento
	- Body: `{ "monto": 2000, "descripcion": "Pago actualizado" }`
- `DELETE /movimientos/<id>` — Elimina movimiento

## Ejemplos de uso (curl)

```bash
# Obtener todos los usuarios
curl -i http://localhost:5000/usuarios

# Crear usuario
curl -i -X POST http://localhost:5000/usuarios \
	-H "Content-Type: application/json" \
	-d '{"name": "Daya", "correo": "daya@email.com", "telefono": "3001234567"}'

# Crear movimiento
curl -i -X POST http://localhost:5000/movimientos \
	-H "Content-Type: application/json" \
	-d '{"tipo_id": 1, "usuario_id": 1, "monto": 1500, "descripcion": "Pago de proyecto", "fecha": "2025-09-11"}'

# Ver tipos
curl -i http://localhost:5000/tipos
```

## Notas

- Si no existe conexión MySQL, se usará SQLite local (`agenda_local.db`).
- Los tipos por defecto son: Ingreso, Gasto, Transferencia.
