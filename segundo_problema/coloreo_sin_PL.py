import networkx as nx
from utilidades import *

GRAFO = 0
T_LAV_PRENDAS = 1

MEJOR_IND_CROMATICO = 0
MEJOR_SOL = 1
MEJOR_TIEMPO = 2

PINTADOS = 0
T_LAVADOS = 1
CORRECTO = 2
T_TOTAL_LAVADOS = 3


def es_compatible(grafo, colores, v):
    for w in grafo.neighbors(v):
        if w in colores and colores[w] == colores[v]:
            return False
    return True


def usa_mas_tiempo_lavado(tiempo_lavados, min_tiempo):
    return obtener_tiempo_lavado(tiempo_lavados) > min_tiempo


def obtener_tiempo_lavado(tiempo_lavados):
    return sum(tiempo_lavados.values())


def crear_grafo(cant_prendas, incompatibilidades):
    grafo = nx.Graph()
    for nodo_prenda in range(1, cant_prendas + 1):
        grafo.add_node(nodo_prenda)

    for prenda1 in range(1, cant_prendas + 1):
        for prenda2 in range(prenda1 + 1, cant_prendas + 1):
            if prenda2 in incompatibilidades.get(prenda1, []):  # Hago una arista por cada par de prendas incompatibles
                grafo.add_edge(prenda1, prenda2)
    return grafo


def armado_lavados(mejor_sol):
    lavados = {}
    for p in mejor_sol:
        lavado_actual = mejor_sol[p]
        lavados[lavado_actual] = lavados.get(lavado_actual, []) + [p]
    return lavados


def solucion_por_coloreo(cant_prendas, t_lavado_prendas):
    prendas, cant_colores_inicial = range(1, cant_prendas + 1), cant_prendas + 1

    mejor_ind_cromatico, mejor_sol, mejor_tiempo = cant_colores_inicial, {}, sum(t_lavado_prendas.values())

    dominio = [grafo_prendas, t_lavado_prendas]
    sol_optima = [mejor_ind_cromatico, mejor_sol, mejor_tiempo]

    for prenda_act in prendas:
        vertice_inicial = prenda_act
        sol_parcial = [{}, {}, True, 0]

        sol_parcial = coloreo_rec(dominio, sol_parcial, vertice_inicial, sol_optima)

        if not sol_parcial[CORRECTO]:
            continue

        # Agrego esto para los vertices (prendas) aislados
        for prenda in prendas:
            if prenda not in sol_parcial[PINTADOS]:
                vertice_inicial = prenda
                sol_parcial = coloreo_rec(dominio, sol_parcial, vertice_inicial, sol_optima)

        if sol_parcial[T_TOTAL_LAVADOS] < sol_optima[MEJOR_TIEMPO]:
            sol_optima[MEJOR_IND_CROMATICO] = len(sol_parcial[T_LAVADOS])
            sol_optima[MEJOR_SOL] = sol_parcial[PINTADOS].copy()
            sol_optima[MEJOR_TIEMPO] = sol_parcial[T_TOTAL_LAVADOS]

    return sol_optima


def coloreo_rec(dominio, sol_parcial, v, sol_optima):
    # Para cada color, pinto el vertice de ese color, y, si es compatible, me fijo si me da menor tiempo que antes
    for color in range(1, sol_optima[MEJOR_IND_CROMATICO] + 1):
        sol_parcial[PINTADOS][v] = color                        # Pinto al vertice v del color `color`

        if not es_compatible(dominio[GRAFO], sol_parcial[PINTADOS], v):
            continue

        t_lav_ant = sol_parcial[T_LAVADOS].get(color, 0)
        sol_parcial[T_LAVADOS][color] = max(t_lav_ant, dominio[T_LAV_PRENDAS][v])
        diferencia = dominio[T_LAV_PRENDAS][v] - t_lav_ant
        if diferencia > 0:
            sol_parcial[T_TOTAL_LAVADOS] += diferencia

        if sol_parcial[T_TOTAL_LAVADOS] > sol_optima[MEJOR_TIEMPO]:
            # Vuelvo a poner los tiempos de lavado como estaban antes
            sol_parcial[T_LAVADOS][color] = t_lav_ant
            sol_parcial[T_TOTAL_LAVADOS] -= diferencia
            continue

        sol_parcial[CORRECTO] = True
        for w in dominio[GRAFO].neighbors(v):
            if w in sol_parcial[PINTADOS]:
                continue

            sol_parcial = coloreo_rec(dominio, sol_parcial, w, sol_optima)

            if not sol_parcial[CORRECTO] or len(sol_parcial[PINTADOS]) == len(sol_optima[MEJOR_SOL]):
                break

        if sol_parcial[CORRECTO]:
            # if (len(sol_parcial[PINTADOS]) >= len(sol_optima[MEJOR_SOL]) and
            # sol_parcial[PINTADOS] != sol_optima[MEJOR_SOL] and
            if(
                    sol_parcial[T_TOTAL_LAVADOS] < sol_optima[MEJOR_TIEMPO]):
                return sol_parcial

        # Vuelvo a poner los tiempos de lavado como estaban antes
        sol_parcial[T_LAVADOS][color] = t_lav_ant
        sol_parcial[T_TOTAL_LAVADOS] -= diferencia

    del sol_parcial[PINTADOS][v]
    sol_parcial[CORRECTO] = False
    return sol_parcial


if __name__ == "__main__":
    cantidad_prendas, dic_incompatibilidades, dic_lav_prendas = procesar_archivo_prendas()
    grafo_prendas = crear_grafo(cantidad_prendas, dic_incompatibilidades)
    solucion = solucion_por_coloreo(cantidad_prendas, dic_lav_prendas)

    lavados_solucion = armado_lavados(solucion[MEJOR_SOL])
    mostrar_solucion_en_pantalla(lavados_solucion, dic_lav_prendas)
    escribir_solucion(lavados_solucion)
