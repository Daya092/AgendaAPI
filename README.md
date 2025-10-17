# AgendaAPI

Resumen
- API REST para gestión de usuarios (registro, login con JWT, CRUD).
- Stack: Flask + SQLAlchemy + Flask-JWT-Extended + SQLite (por defecto).
- Tests: pytest (tests en `tests/`).
- Colección Postman: `postman_collection.json`.

Requisitos
- Python 3.10+ (el contenedor usa Python 3.12).
- pip
- (Opcional) jq para extraer tokens en scripts curl.
- (Opcional) Node + newman para ejecutar colección Postman desde CLI.

Instalación (rápida)
```bash
# desde la raíz del repo (/workspaces/AgendaAPI)
python -m pip install --upgrade pip
pip install -r requirements.txt
# si no existe requirements.txt:
pip install flask flask-jwt-extended sqlalchemy werkzeug pytest
```

Variables de entorno importantes
- JWT_SECRET_KEY — clave secreta para firmar JWT. Requerida para arrancar la app y para los tests.
Ejemplo:
```bash
export JWT_SECRET_KEY="clave_secreta_local"
```
Nota: los tests ya establecen `JWT_SECRET_KEY` internamente, pero al ejecutar la app manualmente se recomienda exportarla.

Configuración de la base de datos
- Revisa `config/database.py` para la URL de la BD (por defecto puede ser sqlite).
- Si la BD ya existe y se creó con un esquema antiguo, puedes:
  - Opción no destructiva: añadir columna `password`:
    ```bash
    python3 scripts/add_password_column.py
    python3 scripts/fill_missing_passwords.py   # opcional: setear contraseñas por defecto hasheadas
    ```
  - Opción destructiva (dev): borrar el archivo sqlite y reiniciar la app para que cree las tablas:
    ```bash
    # ejemplo
    rm path/to/db.sqlite
    python3 src/app.py
    ```

Cómo ejecutar la API (desarrollo)
```bash
# desde la raíz del repo
export JWT_SECRET_KEY="clave_secreta_local"
python3 src/app.py
# la app escucha en: http://0.0.0.0:5000
```

Endpoints principales
- POST /api/usuarios
  - Crear usuario
  - Body JSON: { "name", "correo", "password", "telefono" (opcional) }
- POST /api/login
  - Login devuelve `access_token`
  - Body JSON: { "name" } o { "correo" } + "password"
- POST /api/refresh
  - (si está implementado) Refresh token (envía refresh token)
- POST /api/logout
  - Revocar token actual (si está implementado)
- GET /api/usuarios
  - Listar usuarios (protegido)
- GET /api/usuarios/<id>
  - Obtener usuario por id (protegido)
- PUT /api/usuarios/<id>
  - Actualizar usuario (protegido)
- DELETE /api/usuarios/<id>
  - Eliminar usuario (protegido)

Autenticación (resumen)
- Registro guarda contraseña hasheada (werkzeug.security.generate_password_hash).
- Login crea JWT (Flask-JWT-Extended). Usar header:
  Authorization: Bearer <ACCESS_TOKEN>
- Ejemplo obtener token (requiere jq):
```bash
TOKEN=$(curl -s -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"name":"user1","password":"pass1"}' | jq -r .access_token)
curl -H "Authorization: Bearer $TOKEN" http://localhost:5000/api/usuarios
```

Tests automatizados (pytest)
- Ubicación: `tests/test_auth.py`
- Ejecutar:
```bash
# desde la raíz del repo
# (export JWT_SECRET_KEY si prefieres)
pytest -q
```
- El test recrea las tablas antes de cada ejecución para evitar contaminación entre pruebas.
- Si pytest falla con errores SQLite sobre columnas faltantes, ejecutar:
```bash
python3 scripts/add_password_column.py
python3 scripts/fill_missing_passwords.py
```

Colección Postman / Newman
- Archivo: `postman_collection.json` (importar en Postman).
- Ejecutar con newman (opcional):
```bash
# instalar newman (si corresponde)
sudo apt update && sudo apt install -y nodejs npm
sudo npm install -g newman
newman run postman_collection.json --env-var "baseUrl=http://localhost:5000"
```

Scripts útiles incluidos
- `scripts/add_password_column.py` — añade columna `password` a la tabla `usuarios` (no destructivo).
- `scripts/fill_missing_passwords.py` — rellena contraseñas faltantes con una por defecto hasheada.
- `scripts/run_collection.sh` — (opcional) script que crea usuarios, hace login y lista usuarios con curl/jq.

Buenas prácticas Git
- Ramas: `main` y `develop` mínimas; usar `feature/*` para cambios.
- Commits: >= 5 commits descriptivos.
- `.gitignore` recomendado: `__pycache__/`, `*.pyc`, `.env`, `*.sqlite`, `db.sqlite`, `.vscode/`, `.pytest_cache/`.

Problemas comunes y solución rápida
- 404 en rutas `/api/...`: comprobar que la app está corriendo y que el blueprint `usuario_bp` está registrado (`src/app.py`).
- `ModuleNotFoundError: No module named 'config'`: ejecutar comandos desde la raíz del repo y asegurarse que la raíz está en `sys.path` (los módulos del proyecto ya realizan esto).
- `sqlite3.OperationalError: no such column: usuarios.password`: ejecutar `python3 scripts/add_password_column.py` y reiniciar la app.

Contacto / desarrollo
- Añadir más tests y OpenAPI/Swagger mejora la calidad.
- Para añadir refresh tokens o revocación persistente, sustituir la blocklist en memoria por almacenamiento persistente (Redis/BD).

Licencia
- Proyecto sin licencia especificada (añadir `LICENSE` si se requiere).
