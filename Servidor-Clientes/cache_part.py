from flask import Flask, jsonify
import grpc
import redis
import config_pb2
import config_pb2_grpc
import hashlib

app = Flask(__name__)

partitions = [
    redis.StrictRedis(host='localhost', port=6379, db=0, health_check_interval=30),
    redis.StrictRedis(host='localhost', port=6380, db=0, health_check_interval=30),
    redis.StrictRedis(host='localhost', port=6381, db=0, health_check_interval=30)
]

channel = grpc.insecure_channel('localhost:50051')
stub = config_pb2_grpc.ReclamosServiceStub(channel)

def calculate_partition(key, num_partitions):
    hash_value = int(hashlib.sha256(key.encode()).hexdigest(), 16)
    partition_index = hash_value % num_partitions
    return partition_index

@app.route('/get_reclamo/<int:id>', methods=['GET'])
def get_reclamo(id):
    cache_key = f"reclamo:{id}"
    partition_index = calculate_partition(cache_key, len(partitions))
    cache = partitions[partition_index]

    cached_data = cache.get(cache_key)

    if cached_data:
        response = config_pb2.ReclamoResponse()
        response.ParseFromString(cached_data)
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

    request_data = config_pb2.ReclamoRequest(id=id)
    response = stub.GetReclamoById(request_data)

    cache.set(cache_key, response.SerializeToString(), ex=3600)  # Caché de 1 hora

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
