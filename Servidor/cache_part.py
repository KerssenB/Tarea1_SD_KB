from flask import Flask, jsonify
import grpc
import redis
import config_pb2
import config_pb2_grpc
import hashlib

app = Flask(__name__)

# Configura el cliente Redis con particionamiento (hash sharding)
# Supón que tienes 3 particiones de Redis
partitions = [
    redis.StrictRedis(host='localhost', port=6379, db=0, health_check_interval=30),
    redis.StrictRedis(host='localhost', port=6380, db=0, health_check_interval=30),
    redis.StrictRedis(host='localhost', port=6381, db=0, health_check_interval=30)
]

# Configura la conexión gRPC
channel = grpc.insecure_channel('localhost:50051')
stub = config_pb2_grpc.ReclamosServiceStub(channel)

# Función para calcular la partición
def calculate_partition(key, num_partitions):
    # Usa una función de hash para calcular la partición a partir de la clave
    hash_value = int(hashlib.sha256(key.encode()).hexdigest(), 16)
    partition_index = hash_value % num_partitions
    return partition_index

@app.route('/get_reclamo/<int:id>', methods=['GET'])
def get_reclamo(id):
    # Calcula la clave y la partición del caché
    cache_key = f"reclamo:{id}"
    partition_index = calculate_partition(cache_key, len(partitions))
    cache = partitions[partition_index]

    # Consulta el caché
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

    # Almacena los datos en caché particionado
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
