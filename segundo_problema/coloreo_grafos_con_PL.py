from pulp import LpProblem, LpVariable, LpMinimize, LpBinary, lpSum
from utilidades import *


def coloreo(cant_prendas, incompatibilidades, tiempo_lavado):
    cant_lavados = cant_prendas

    problema = LpProblem("Problema_Lavados", LpMinimize)

    # VARIABLES

    # Variables Xi,j = {1 si la prenda i se colorea con color j ; 0 sino}
    # En terminos del problema: {1 si la prenda i se lava en el lavado j ; 0 sino}
    binarias_coloreo = {(prenda, lavado): LpVariable(f"X_{prenda}_{lavado}", cat=LpBinary)
                        for lavado in range(1, cant_lavados + 1) for prenda in range(1, cant_prendas + 1)}

    # Variables Wj = {1 si se usa el color j en algún vértice ; 0 sino}
    # En terminos del problema: {1 si se usa el lavado j con alguna prenda ; 0 sino}
    binarias_colores = {lavado: LpVariable(f"W_{lavado}", lowBound=0, cat=LpBinary)
                        for lavado in range(1, cant_lavados + 1)}

    # Agregar las variables YL[i] = Tiempo del lavado i
    tiempo_lavados = {lavado: LpVariable(f"YL_{lavado}", lowBound=0, cat='Integer')
                      for lavado in range(1, cant_lavados + 1)}

    # Agregar la variable TTL = Tiempo total de lavados
    ttl = LpVariable("TTL", lowBound=0, cat='Integer')

    # problema += ttl

    # FUNCIONAL
    problema += lpSum(binarias_colores[lavado] for lavado in range(1, cant_lavados + 1))

    # RESTRICCIONES

    # Hago que todos los vertices esten pintados exactamente de un color
    # (o sea, que se laven en exactamente un lavado)
    for prenda in range(1, cant_prendas + 1):
        problema += lpSum(binarias_coloreo[(prenda, lavado)] for lavado in range(1, cant_lavados + 1)) == 1

    # Hago que, si dos vértices son adyacentes (incompatibles en este problema), no pueden tener el mismo color (lavado)
    for prenda in range(1, cant_prendas + 1):
        for prenda_incomp in incompatibilidades.get(prenda, []):
            for lavado in range(1, cant_lavados + 1):
                X_i_j = binarias_coloreo[prenda, lavado]
                X_k_j = binarias_coloreo[prenda_incomp, lavado]
                problema += X_i_j + X_k_j <= binarias_colores[lavado]

    # Eliminacion de simetría
    for lavado in range(1, cant_lavados):
        suma_j = lpSum(binarias_coloreo[(prenda, lavado)] for prenda in range(1, cant_prendas + 1))
        suma_j_1 = lpSum(binarias_coloreo[(prenda, lavado+1)] for prenda in range(1, cant_prendas + 1))
        problema += suma_j >= suma_j_1

    for lavado in range(1, cant_lavados + 1):
        problema += (tiempo_lavados[lavado] == lpSum(tiempo_lavado[prenda] * binarias_coloreo[(prenda, lavado)]
                                                     for prenda in range(1, cant_prendas + 1)))

    problema += (ttl == lpSum(tiempo_lavados[lavado] for lavado in range(1, cant_lavados + 1)))

    # RESOLUCION
    problema.solve()

    # Muestro la solucion
    lavados = {}
    for lavado in range(1, cant_lavados+1):
        if binarias_colores[lavado].value() != 0:
            lavados[lavado] = []
            for prenda in range(1, cant_prendas+1):
                if binarias_coloreo[(prenda, lavado)].value() != 0:
                    lavados[lavado] = lavados.get(lavado, []) + [prenda]
    mostrar_solucion_en_pantalla(lavados, tiempo_lavado)


if __name__ == '__main__':
    prendas, d_incompatibilidades, d_lavados = procesar_archivo_prendas()
    coloreo(prendas, d_incompatibilidades, d_lavados)
