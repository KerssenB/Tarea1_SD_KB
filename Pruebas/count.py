import csv
from collections import Counter

def contar_numeros_repetidos(csv_filename):
    # Diccionario para contar las ocurrencias de cada número
    contador = Counter()
    
    # Abrir el archivo CSV para lectura
    with open(csv_filename, mode='r') as file:
        # Crear un lector de CSV
        reader = csv.reader(file)
        
        # Saltar la primera fila si contiene una cabecera (opcional)
        next(reader, None)
        
        # Leer cada fila y contar los números
        for row in reader:
            # Convertir cada valor a entero
            numero = int(row[0])
            contador[numero] += 1
    
    # Contar cuántos números están repetidos
    numeros_repetidos = sum(1 for numero, count in contador.items() if count > 1)
    
    # Imprimir el número de números repetidos
    print(f"Hay {numeros_repetidos} números repetidos en el archivo '{csv_filename}'")

    # Imprimir los números y sus frecuencias
    print("\nNúmeros repetidos y sus frecuencias:")
    for numero, count in contador.items():
        if count > 1:
            print(f"Número: {numero}, Veces repetido: {count}")

# Nombre del archivo CSV que contiene los números
csv_filename = 'Pruebas/prueba.csv'

# Llamar a la función para contar los números repetidos
contar_numeros_repetidos(csv_filename)
