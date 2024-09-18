#============================================================ JosCLF =================================================================
#============================================================ LIBRERIAS =================================================================

import numpy as np
import itertools  
import random
import math
#============================================================  PARAMETROS =================================================================
nombre_ciudades = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Diego", "Dallas", "San Francisco", "Austin", "Las Vegas"]
print(len(nombre_ciudades))
m = 3
Nciudades = 11
MATRIZ_de_distancias = [
    [0, 3091, 927, 1876, 2704, 94, 2999, 1641, 3471, 1838, 3013],
    [3091, 0, 2542, 1681, 375, 2994, 138, 1442, 389, 1407, 290],
    [927, 2542, 0, 1337, 2169, 930, 2464, 1100, 2935, 1168, 2465],
    [1876, 1681, 1337, 0, 1308, 1778, 1603, 240, 2075, 163, 1604],
    [2704, 375, 2169, 1308, 0, 2603, 366, 1069, 767, 1034, 296],
    [94, 2994, 930, 1778, 2603, 0, 2898, 1543, 3369, 1740, 2915],
    [2999, 138, 2464, 1603, 366, 2898, 0, 1364, 531, 1329, 338],
    [1641, 1442, 1100, 240, 1069, 1543, 1364, 0, 1836, 201, 1365],
    [3471, 389, 2935, 2075, 767, 3369, 531, 1836, 0, 1801, 607],
    [1838, 1407, 1168, 163, 1034, 1740, 1329, 201, 1801, 0, 1330],
    [3013, 290, 2465, 1604, 296, 2915, 338, 1365, 607, 1330, 0]
]
Nindividuos = 50
genMax = 50
#============================================================  GENERACION DE LA POBLACION INICIAL  =================================================================
def generar_poblacion_inicial(Nindividuos, Nciudades):
    poblacion = []
    while len(poblacion) < Nindividuos:
        individuo = list(range(1, Nciudades + 1))
        random.shuffle(individuo)
        poblacion.append(individuo)
    return poblacion
#============================================================  FUNCION DE EVALUAR LA POBLACION  =================================================================
def evaluar_poblacion(poblacion, MATRIZ_de_distancias):
    poblacion_evaluada = []
    for ruta in poblacion:
        distancia_total = 0
        num_ciudades = len(ruta)
        for i in range(num_ciudades):
            ciudad_actual = ruta[i]
            if i == num_ciudades - 1:  # Si es la última ciudad, calcular la distancia a la primera
                ciudad_siguiente = ruta[0]
            else:
                ciudad_siguiente = ruta[i + 1]
            distancia = MATRIZ_de_distancias[ciudad_actual - 1][ciudad_siguiente - 1]
            distancia_total += distancia
        poblacion_evaluada.append(distancia_total)
    return poblacion_evaluada
#============================================================  CREAR LISTA DE VECINOS  =================================================================
def crear_lista_vecinos(padre1, padre2, numCiudades):
    lista_de_ciudades = []
    for i in range(numCiudades):
        ciudad = padre1[i]
        idx1 = [i-1, i+1]
        idx2 = np.nonzero(padre2 == ciudad)[0]
        idx1 = [(idx + numCiudades) % numCiudades for idx in idx1]
        idx2 = [(idx + numCiudades) % numCiudades for idx in idx2]

        vecinos = list(itertools.product(idx1, idx2))
        lista_de_ciudades.append(vecinos)

        elementos_padre1 = [padre1[idx] for idx in idx1]
        elementos_padre2 = [padre2[idx] for idx in idx2]
        concatenados = np.concatenate((elementos_padre1, elementos_padre2))
        vecinas = np.unique(concatenados)
        
        print("Vecinos de la ciudad", ciudad, ":", vecinas)

    return lista_de_ciudades
#============================================================  PRUEBAS  =================================================================
poblacion = generar_poblacion_inicial(Nindividuos, Nciudades)
for ruta in poblacion:
    print(ruta)

print('poblacion en representacion de rutas: \n ', poblacion)
poblacion_inicial_evaluada = evaluar_poblacion(poblacion, MATRIZ_de_distancias)
print(poblacion_inicial_evaluada)
#============================================================  PRUEBAS LISTAS DE CIUDADES VECINAS  =================================================================
for i in range(len(poblacion) - 1):
    resultado = crear_lista_vecinos(poblacion[i], poblacion[i + 1], Nciudades)
    print('lista de vecinos para', poblacion[i], 'y', poblacion[i + 1], ': \n', resultado)
#============================================================  REMOCION DE ABRUPTOS  =================================================================
def remocion_de_abruptos(individuo, m, MATRIZ_de_distancias):
    n = random.choice(individuo)# seleccion de ciudad random
# escoger m ciudades aleatorias para compararse con la ciudad n que se eligio anteriormente
    ciudades_comparacion = random.sample([c for c in individuo if c != n], m)
# se calculan las distancias usando la matriz de distancias 
    distancias_n = [MATRIZ_de_distancias[n - 1][ciudad - 1] for ciudad in ciudades_comparacion]
    # encontrar la ciudad mss cercana a n
    ciudad_cercana = ciudades_comparacion[distancias_n.index(min(distancias_n))]
    # Crear dos nuevas rutas con la ciudad_cercana despues de la ciudad elegida y anttes de ella (n+1 y n-1)
    nueva_ruta1 = individuo[:individuo.index(n) + 1] + [ciudad_cercana] + individuo[individuo.index(n) + 1:]
    nueva_ruta2 = individuo[:individuo.index(n)] + [ciudad_cercana] + individuo[individuo.index(n):]

    # Verificar si la ciudad cercana ya está presente en alguna de las nuevas rutas
    if ciudad_cercana in nueva_ruta1:
        nueva_ruta1.remove(ciudad_cercana)
    if ciudad_cercana in nueva_ruta2:
        nueva_ruta2.remove(ciudad_cercana)

    # Evaluar las nuevas rutas
    distancia_nueva_ruta1 = sum(MATRIZ_de_distancias[nueva_ruta1[i] - 1][nueva_ruta1[i + 1] - 1] for i in range(len(nueva_ruta1) - 1))
    distancia_nueva_ruta2 = sum(MATRIZ_de_distancias[nueva_ruta2[i] - 1][nueva_ruta2[i + 1] - 1] for i in range(len(nueva_ruta2) - 1))

    # Utilizar la función evaluar_poblacion para calcular la distancia
    distancia_evaluada_nueva_ruta1 = evaluar_poblacion([nueva_ruta1], MATRIZ_de_distancias)[0]
    distancia_evaluada_nueva_ruta2 = evaluar_poblacion([nueva_ruta2], MATRIZ_de_distancias)[0]

    # Elegir la nueva ruta con la menor distancia
    if distancia_evaluada_nueva_ruta1 < distancia_evaluada_nueva_ruta2:
        nuevo_individuo = nueva_ruta1
    else:
        nuevo_individuo = nueva_ruta2

    return nuevo_individuo
#============================================================  PRUEBA DE REMOCION DE ABRUPTOS  =================================================================
individuo_prueba = [2, 1, 4, 3]
hijo = remocion_de_abruptos(individuo_prueba, m, MATRIZ_de_distancias)
print("Nuevo individuo después de la remoción de abruptos:", hijo)
#============================================================ APLICAR LA REMOCION DE BRUPTOS A LA POBLACION INICIAL =================================================================
poblacion_inicia_lista = []

for individuo in poblacion:
    nuevo_individuo = remocion_de_abruptos(individuo, m, MATRIZ_de_distancias)
    poblacion_inicia_lista.append(nuevo_individuo)

print("Población inicial después de la remoción de abruptos:")
for individuo in poblacion_inicia_lista:
    print(individuo)
#============================================================  SELECCION DE PADRES  =================================================================
def seleccion_de_padres(poblacion):
    padre1, padre2 = random.sample(poblacion, 2)
    return padre1, padre2
#============================================================ edge recombination =================================================================
def edge_recombination(padre1, padre2, num_ciudades):
    # Inicialización
    hijo = [0] * num_ciudades

    # Paso 1: Crear la lista de ciudades vecinas
    lista_ciudades_vecinas = creador_lista(padre1, padre2, num_ciudades)

    # Paso 2: Seleccionar la primera ciudad
    rd = round(random.random())
    ciudad_actual = padre1[0] if rd == 1 else padre2[0]
    hijo[0] = ciudad_actual

    # Paso 3: Recorrer las ciudades restantes

    for i in range(1, num_ciudades):
        # Actualizar la lista de ciudades vecinas
        for vecinos in lista_ciudades_vecinas.values():
            if ciudad_actual in vecinos:
                vecinos.remove(ciudad_actual)


        # Ciudades vecinas a la ciudad actual
        vecindario_actual = lista_ciudades_vecinas[ciudad_actual]

        if not vecindario_actual:
            # Determinar las ciudades no visitadas y elegir una aleatoria
            ciudades_no_visitadas = set(range(1, num_ciudades)) - set(hijo[:i])
            ciudad_actual = random.choice(list(ciudades_no_visitadas))
        else:
            # Num de conexiones de ciudades vecinas
            n_conex = [len(lista_ciudades_vecinas[vecino]) for vecino in vecindario_actual]

            # Encuentra los índices de los valores mínimos
            min_conex = min(n_conex)
            min_indices = [i for i, conexiones in enumerate(n_conex) if conexiones == min_conex]

            # Selecciona aleatoriamente uno de los índices mínimos
            idx_min = random.choice(min_indices)
            ciudad_actual = vecindario_actual[idx_min]

        hijo[i] = ciudad_actual

    return hijo
#============================================================ FUNCION DE CREACION DE LISTA =================================================================

def creador_lista(padre1, padre2, num_ciudades):
    lista_ciudades_vecinas = {}

    # Construir diccionarios de vecinos para cada ciudad en ambos padres
    for ciudad in range(1, num_ciudades + 1):
        vecinos = set()
        idx_padre1 = padre1.index(ciudad)
        idx_padre2 = padre2.index(ciudad)
        
        # Vecino anterior
        vecino_anterior1 = padre1[idx_padre1 - 1]
        vecino_anterior2 = padre2[idx_padre2 - 1]
        vecinos.add(vecino_anterior1)
        vecinos.add(vecino_anterior2)

        # Vecino posterior
        vecino_posterior1 = padre1[(idx_padre1 + 1) % num_ciudades]
        vecino_posterior2 = padre2[(idx_padre2 + 1) % num_ciudades]
        vecinos.add(vecino_posterior1)
        vecinos.add(vecino_posterior2)

        lista_ciudades_vecinas[ciudad] = list(vecinos)

    return lista_ciudades_vecinas

#============================================================ PRUEBAS EDGE RECOMBINATION =================================================================
padre1 = [2, 1, 4, 3, 5]
padre2 = [5, 4, 3, 2, 1]
num_ciudades = 5

hijo = edge_recombination(padre1, padre2, num_ciudades)
print("Hijo después de edge recombination:", hijo)
#============================================================ PASO 5 MUTACION =================================================================
def mutacion(probabilidad_mutacion, poblacion, num_ciudades):
    nueva_poblacion = [poblacion.copy()]
    for individuo in nueva_poblacion:
        if random.random() < probabilidad_mutacion:
            individuo = individuo.copy()
        else:
          individuo = list(range(1, Nciudades + 1))
          individuo = random.shuffle(individuo)

    return nueva_poblacion      
# ================================================================= BUCLE GEMERALL =================================================================
genActual = 0
while genMax > genActual:
    print(f"Generación {genActual + 1}:")
    
    # Paso 3: Selección de padres aleatoriamente
    padre1, padre2 = seleccion_de_padres(poblacion)

    # Aplicar el cruce por "Edge Recombination (ER)" entre los padres y generar un descendiente
    hijo = edge_recombination(padre1, padre2, Nciudades)  # Pass Nciudades as the num_ciudades argument

    # Evaluar la aptitud del descendiente
    aptitud_hijo = evaluar_poblacion([hijo], MATRIZ_de_distancias)[0]

    # Aplicar la heurística "Remoción de Abruptos" al descendiente
    hijo = remocion_de_abruptos(hijo, m, MATRIZ_de_distancias)

    # Paso 4: Ordenar los padres y el descendiente de acuerdo a su aptitud (Familia), y pasan a conformar la siguiente generación los dos mejores individuos
    poblacion.extend([padre1, padre2, hijo])
    poblacion.sort(key=lambda x: evaluar_poblacion([x], MATRIZ_de_distancias)[0])
    poblacion = poblacion[:Nindividuos]  # Mantener solo a los Nindividuos mejores
    
    # Imprimir la población actual
    print("Población:\n")
    for individuo in poblacion:
        print(individuo)
    
    # Aplicar la remoción de abruptos a la población
    poblacion_con_remocion = [remocion_de_abruptos(individuo, m, MATRIZ_de_distancias) for individuo in poblacion]
    
    # Imprimir la población después de la remoción de abruptos
    print("Población con remoción de abruptos: \n ")
    for individuo in poblacion_con_remocion:
        print(individuo)

    # Evaluar la población actual
    evaluacion_poblacion = evaluar_poblacion(poblacion_con_remocion, MATRIZ_de_distancias)
    print("Evaluación de la población: \n")
    print(evaluacion_poblacion)
    print("mejor individuo de la generacion de la generacion: \n")
    print(min(evaluacion_poblacion))
    # Incrementar el número de generación actual
    genActual += 1
