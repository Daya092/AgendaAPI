# 1. Obtener todos los usuarios
curl -i http://localhost:5000/usuarios

# 2. Obtener un usuario por ID (ejemplo: 1)
curl -i http://localhost:5000/usuarios/1

# 3. Obtener un usuario inexistente (ejemplo: 99)
curl -i http://localhost:5000/usuarios/99

# 4. Crear un nuevo usuario
curl -i -X POST http://localhost:5000/usuarios \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Daya", "email": "daya@email.com"}'

# 5. Crear un usuario con datos incompletos
curl -i -X POST http://localhost:5000/usuarios \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Juan"}'

# 6. Actualizar un usuario existente (ejemplo: 1)
curl -i -X PUT http://localhost:5000/usuarios/1 \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Dayana", "email": "dayana@email.com"}'

# 7. Actualizar un usuario inexistente (ejemplo: 99)
curl -i -X PUT http://localhost:5000/usuarios/99 \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Desconocido", "email": "none@email.com"}'

# 8. Eliminar un usuario existente (ejemplo: 1)
curl -i -X DELETE http://localhost:5000/usuarios/1

# 9. Eliminar un usuario inexistente (ejemplo: 99)
curl -i -X DELETE http://localhost:5000/usuarios/99


# 10. verificar tipos de gasto
curl -i http://localhost:5000/tipos

#11. crear un movimiento
curl -i -X POST http://localhost:5000/movimientos \
  -H "Content-Type: application/json" \
  -d '{"tipo_id": 1, "usuario_id": 1, "monto": 1500, "descripcion": "Pago de proyecto"}'

#12. verificar movimientos creados
curl -i http://localhost:5000/movimientos

#13.obtener movimiento por id
curl -i http://localhost:5000/movimientos/1

#14. Actualizar un movimiento
curl -i -X PUT http://localhost:5000/movimientos/1 \
  -H "Content-Type: application/json" \
  -d '{"monto": 2000, "descripcion": "Pago actualizado"}'

#15. Eliminar un movimiento
curl -i -X DELETE http://localhost:5000/movimientos/1

