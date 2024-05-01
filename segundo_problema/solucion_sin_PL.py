import csv
from utilidades import *

RUTA_ARCHIVO = 'segundo_problema.txt'
RUTA_SOLUCION = "solucion_segundo_problema.txt"

COMANDO = 0
PRENDA_1 = 1
PRENDA_2 = 2
TIEMPO_LAVADO = 2
CANT_PRENDAS = 2

DEFINICION_PROBLEMA = 'p'
INCOMPATIBILIDAD = 'e'
TIEMPO_LAVADOS = 'n'

DELIMITER = " "
LINE_TERMINATOR = '\n'


def procesar_archivo_prendas():
    incompatibilidades = {}
    lavados = {}
    cant_prendas = 0

    with open(RUTA_ARCHIVO) as archivo_prendas:
        for linea in archivo_prendas:
            contenido = linea.split()
            comando = contenido[COMANDO]

            if comando == DEFINICION_PROBLEMA:
                cant_prendas = int(contenido[CANT_PRENDAS])

            elif comando == INCOMPATIBILIDAD:
                # Para evitar redundancias --> si p1 es incompatible con p2, evito decir que p2 es incompatible con p1
                prenda1 = int(contenido[PRENDA_1])
                prenda2 = int(contenido[PRENDA_2])
                if prenda1 not in incompatibilidades.get(prenda2, []):
                    incompatibilidades[prenda1] = incompatibilidades.get(prenda1, []) + [prenda2]

            elif comando == TIEMPO_LAVADOS:
                prenda1 = int(contenido[PRENDA_1])
                lavados[prenda1] = lavados.get(prenda1, 0) + int(contenido[TIEMPO_LAVADO])

    return cant_prendas, incompatibilidades, lavados


def algoritmo_solucion(cant_prendas, incompatibilidades, tiempo_de_lavado):
    lavados = {0: []}

    for prenda in range(1, cant_prendas + 1):
        fue_colocada = False
        for lavado in lavados:
            if prenda_es_compatible_en(lavados[lavado], prenda, incompatibilidades):
                lavados[lavado] = lavados.get(lavado, []) + [prenda]
                fue_colocada = True
                break
        if not fue_colocada:
            nuevo_lavado = [prenda]
            lavados[len(lavados)] = nuevo_lavado

    mostrar_solucion_en_pantalla(lavados, tiempo_de_lavado)
    escribir_solucion(lavados)


def prenda_es_compatible_en(lavado, prenda, incompatibilidades):
    for prenda_actual in lavado:
        if prenda in incompatibilidades.get(prenda_actual, []):
            return False
    return True


def escribir_solucion(lavados):
    with open(RUTA_SOLUCION, 'w') as arc_solucion:
        csv_writer = csv.writer(arc_solucion, delimiter=DELIMITER, lineterminator=LINE_TERMINATOR)
        for lavado in lavados:
            for prenda in lavados[lavado]:
                csv_writer.writerow([prenda, lavado])


if __name__ == '__main__':
    prendas, d_incompatibilidades, d_lavados = procesar_archivo_prendas()
    algoritmo_solucion(prendas, d_incompatibilidades, d_lavados)
