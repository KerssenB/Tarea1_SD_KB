import grpc
from concurrent import futures
import config_pb2
import config_pb2_grpc
import psycopg2

# Implementar el servicio ReclamosService
class ReclamosService(config_pb2_grpc.ReclamosServiceServicer):
    def __init__(self, db_connection_string):
        # Establecer la conexión a PostgreSQL
        try:
            self.connection = psycopg2.connect("dbname=reclamos_sernac user=python password=py123 host=localhost port=5432")
            print("Conexión a PostgreSQL exitosa")
        except Exception as e:
            print(f"Error al conectar a PostgreSQL: {e}")

    def GetReclamoById(self, request, context):
        """Obtiene un reclamo de la base de datos por ID."""
        cursor = self.connection.cursor()
        try:
        # Consulta SQL para obtener el reclamo por ID
            cursor.execute("SELECT * FROM reclamos_2010 WHERE id = %s", (request.id,))
            row = cursor.fetchone()

        # Si se encuentra un registro, devuelve una respuesta con los datos
            if row:
                return config_pb2.ReclamoResponse(
                    id=row[0],
                    comuna_consumidor=row[1],
                    region_consumidor=row[2],
                    nombre_region_consumidor=row[3],
                    nombre_mercado=row[4],
                    nombre_categoria_mercado=row[5],
                    tipo_prod=row[6],
                    motivo_legal=row[7],
                    categoria_ml=row[8],
                    resultado=row[9]
                )
            else:
                # Si no se encuentra un reclamo con ese ID
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details('Reclamo no encontrado')
                return config_pb2.ReclamoResponse()
        
        except Exception as e:
            # Maneja cualquier error que pueda ocurrir
            context.set_code(grpc.StatusCode.UNKNOWN)
            context.set_details(str(e))
            return config_pb2.ReclamoResponse()
       
        finally:
            # Cierra el cursor de la base de datos
            cursor.close()


def serve():
    # Iniciar el servidor gRPC
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # Agregar el servicio implementado al servidor
    config_pb2_grpc.add_ReclamosServiceServicer_to_server(ReclamosService("dbname=reclamos_sernac user=python password=py123"), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
