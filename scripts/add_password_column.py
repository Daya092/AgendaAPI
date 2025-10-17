import sys
import os

_root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _root_dir not in sys.path:
    sys.path.insert(0, _root_dir)

import logging
from sqlalchemy import inspect, text
from config.database import engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    inspector = inspect(engine)
    cols = [c["name"] for c in inspector.get_columns("usuarios")]
    if "password" in cols:
        logger.info("La columna 'password' ya existe en 'usuarios'")
        return

    logger.info("Añadiendo columna 'password' a la tabla 'usuarios'...")
    with engine.connect() as conn:
        conn.execute(text('ALTER TABLE usuarios ADD COLUMN password TEXT'))
        conn.commit()
    logger.info("Columna añadida. Reinicia la app y prueba de nuevo.")

if __name__ == "__main__":
    main()