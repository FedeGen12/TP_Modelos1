import csv

RUTA_ARCHIVO = '../tercera_parte/tercera_parte/tercer_problema.txt'
RUTA_SOLUCION = "solucion_segundo_problema.txt"

COMANDO = 0
PRENDA_1 = 1
PRENDA_2 = 2
TIEMPO_LAVADO = 2
CANT_PRENDAS = 2

COMENTARIO = 'c'
DEFINICION_PROBLEMA = 'p'
INCOMPATIBILIDAD = 'e'
TIEMPO_LAVADOS = 'n'

DELIMITER = " "
LINE_TERMINATOR = '\n'


def procesar_archivo_prendas(version=1):
    incompatibilidades = {}
    lavados = {}
    cant_prendas = 0

    with (open(RUTA_ARCHIVO) as archivo_prendas):
        for linea in archivo_prendas:
            contenido = linea.split()
            comando = contenido[COMANDO]

            if comando == COMENTARIO:
                continue

            elif comando == DEFINICION_PROBLEMA:
                cant_prendas = int(contenido[CANT_PRENDAS])

            elif comando == INCOMPATIBILIDAD:
                if version == 1:
                    manejar_incompatibilidades1(int(contenido[PRENDA_1]), int(contenido[PRENDA_2]), incompatibilidades)
                else:
                    manejar_incompatibilidades2(int(contenido[PRENDA_1]), int(contenido[PRENDA_2]), incompatibilidades)

            elif comando == TIEMPO_LAVADOS:
                prenda1 = int(contenido[PRENDA_1])
                lavados[prenda1] = lavados.get(prenda1, 0) + int(contenido[TIEMPO_LAVADO])

    return cant_prendas, incompatibilidades, lavados


def manejar_incompatibilidades1(prenda1, prenda2, incompatibilidades):
    # Para evitar redundancias --> si p1 es incompatible con p2, evito decir que p2 es incompatible con p1
    if prenda1 not in incompatibilidades.get(prenda2, []):
        incompatibilidades[prenda1] = incompatibilidades.get(prenda1, []) + [prenda2]


def manejar_incompatibilidades2(prenda1, prenda2, incompatibilidades):
    if prenda1 not in incompatibilidades.get(prenda2, []):
        incompatibilidades[prenda2] = incompatibilidades.get(prenda2, []) + [prenda1]
    if prenda2 not in incompatibilidades.get(prenda1, []):
        incompatibilidades[prenda1] = incompatibilidades.get(prenda1, []) + [prenda2]


def mostrar_solucion_en_pantalla(lavados, tiempo_de_lavado):
    tiempo_total_de_lavado = 0
    for lavado in lavados:
        tiempo_lavado_actual = 0
        for prenda in lavados[lavado]:
            tiempo_lavado_actual = max(tiempo_lavado_actual, tiempo_de_lavado[prenda])
        print(f"Prendas lavadas en Lavado {lavado}: {lavados[lavado]} en {tiempo_lavado_actual} unidades de tiempo")
        tiempo_total_de_lavado += tiempo_lavado_actual
    print(f"Tiempo total de lavado: {tiempo_total_de_lavado}")


def escribir_solucion(lavados):
    with open(RUTA_SOLUCION, 'w') as arc_solucion:
        csv_writer = csv.writer(arc_solucion, delimiter=DELIMITER, lineterminator=LINE_TERMINATOR)
        for lavado in lavados:
            for prenda in lavados[lavado]:
                csv_writer.writerow([prenda, lavado])
