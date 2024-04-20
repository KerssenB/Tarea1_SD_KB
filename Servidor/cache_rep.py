from flask import Flask, jsonify
import grpc
import redis
import config_pb2
import config_pb2_grpc

app = Flask(__name__)

# Configura el caché replicado con Redis Sentinel
# Define los servidores Sentinel. Utiliza las instancias de Redis Sentinel especificadas en el archivo docker-compose.
sentinel_servers = [('localhost', 26379), ('localhost', 26380), ('localhost', 26381)]

# Crea un objeto de Sentinel
sentinel = redis.Sentinel(sentinel_servers, socket_timeout=0.1)

# Conéctate al servidor maestro de Redis supervisado por Sentinel
# 'mymaster' es el nombre del grupo maestro configurado en Redis Sentinel
cache = sentinel.master_for('mymaster', password=None, db=0)

# Configura la conexión gRPC
channel = grpc.insecure_channel('localhost:50051')
stub = config_pb2_grpc.ReclamosServiceStub(channel)

@app.route('/get_reclamo/<int:id>', methods=['GET'])
def get_reclamo(id):
    # Genera la clave de caché
    cache_key = f"reclamo:{id}"

    # Consulta el caché replicado
    cached_data = cache.get(cache_key)

    if cached_data:
        # Si los datos están en caché, deserialízalos y devuélvelos como respuesta JSON
        response = config_pb2.ReclamoResponse()
        response.FromString(cached_data)
        return jsonify({
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
        })

    # Si los datos no están en caché, realiza la solicitud gRPC
    request_data = config_pb2.ReclamoRequest(id=id)
    response = stub.GetReclamoById(request_data)

    # Almacena los datos en caché replicado
    cache.set(cache_key, response.SerializeToString(), ex=3600)  # Caché de 1 hora

    # Devuelve la respuesta como JSON
    return jsonify({
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
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
