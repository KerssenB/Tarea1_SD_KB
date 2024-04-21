# Script para ver si el caché funciona correctamente

import redis

sentinel_servers = [('localhost', 26379), ('localhost', 26380), ('localhost', 26381)]

sentinel = redis.Sentinel(sentinel_servers, socket_timeout=0.1)

r = sentinel.master_for('mymaster', password=None, db=0)


# Consulta todas las claves
keys = r.keys('reclamo:*')
print("Claves en caché:", keys)

# Ver los datos asociados a una clave específica
for key in keys:
    data = {
            "id": response.id,
            "comuna_consumidor": response.comuna_consumidor,
            "region_consumidor": response.region_consumidor,
            "nombre_region_consumidor": response.nombre_region_consumidor,
            "nombre_mercado": response.nombre_mercado,
            "nombre_categoria_mercado": response.nombre_categoria_mercado,
            "tipo_prod": response.tipo_prod,
            "motivo_legal": response.motivo_legal,
            "categoria_ml": response.categoria_ml,
            "resultado": response.resultado
        }
    
    
    