import csv
import random

filename = "prueba.csv"

cantidad_numeros = 5000  

probabilidad_repeticion = 0.6

numeros_generados = []

for i in range(cantidad_numeros):
        num = random.randint(1, 500)
        numeros_generados.append(num)


# CSV
with open(filename, mode="w", newline="") as file:
    writer = csv.writer(file)
    
    for _ in range(cantidad_numeros):
        # Decide si elegir un número aleatorio o uno de la lista de números 
        if random.random() < probabilidad_repeticion and numeros_generados:
            # Elige un número de la lista de números ya generados
            numero_aleatorio = random.choice(numeros_generados)
        else:
            # Genera un número aleatorio nuevo
            numero_aleatorio = random.randint(1, 206890)
        
        # Guarda el número aleatorio en la lista de números ya generados
        numeros_generados.append(numero_aleatorio)
        
        # Escribe el número aleatorio en el archivo CSV
        writer.writerow([numero_aleatorio])

print(f"Se han guardado {cantidad_numeros} números aleatorios en el archivo '{filename}'")
