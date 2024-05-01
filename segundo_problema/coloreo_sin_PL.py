import networkx as nx
from utilidades import *


def es_compatible(grafo, colores, v):
    for w in grafo.neighbors(v):
        if w in colores and colores[w] == colores[v]:
            return False
    return True


def usa_mas_colores(pintados, cant_minima):
    colores_usados = {}
    for v in pintados:
        colores_usados[pintados[v]] = colores_usados.get(pintados[v], 0) + 1
    return len(colores_usados) > cant_minima


def usa_mas_tiempo_lavado(v_pintados, min_tiempo, tiempo_lavados):
    return obtener_tiempo_lavado(v_pintados, tiempo_lavados) > min_tiempo


def obtener_tiempo_lavado(prendas_lavados, tiempo_lavado):
    tiempo_por_lavado = {}
    for prenda in prendas_lavados:
        lavado = prendas_lavados[prenda]
        tiempo_por_lavado[lavado] = max(tiempo_por_lavado.get(lavado, 0), tiempo_lavado[prenda])
    return sum(tiempo_por_lavado.values())


def crear_grafo(cant_prendas, incompatibilidades):
    grafo = nx.Graph()
    for nodo_prenda in range(1, cant_prendas + 1):
        grafo.add_node(nodo_prenda)

    for prenda1 in range(1, cant_prendas + 1):
        for prenda2 in range(prenda1 + 1, cant_prendas + 1):
            if prenda2 in incompatibilidades.get(prenda1, []):  # Hago una arista por cada par de prendas incompatibles
                grafo.add_edge(prenda1, prenda2)
    return grafo


def solucion_por_coloreo(tiempo_de_lavado):
    min_colores_ant, min_sol_ant, min_tiempo_ant = prendas + 1, {}, sum(d_lavados.values())

    mejor_ind_cromatico, mejor_sol, mejor_tiempo = min_colores_ant, min_sol_ant, min_tiempo_ant

    for prenda_act in range(1, prendas + 1):

        min_colores_act, min_sol_act, min_tiempo_act, _ = coloreo_rec(grafo_prendas, prendas,
                                                                      {}, prenda_act,
                                                                      min_colores_ant, min_sol_ant,
                                                                      min_tiempo_ant, d_lavados)

        # Agrego esto para los vertices (prendas) aislados
        for prenda in range(1, prendas + 1):
            if prenda not in min_sol_act:
                min_colores_completo, min_sol_completo, min_tiempo_completo, _ = coloreo_rec(grafo_prendas, prendas,
                                                                                             min_sol_act, prenda,
                                                                                             min_colores_ant,
                                                                                             min_sol_ant,
                                                                                             min_tiempo_ant, d_lavados)

                min_colores_act, min_sol_act, min_tiempo_act = min_colores_completo, min_sol_completo, min_tiempo_completo

        if min_tiempo_act < mejor_tiempo:
            mejor_ind_cromatico, mejor_sol, mejor_tiempo = min_colores_act, min_sol_act, min_tiempo_act

    lavados = {}
    for prenda_ in mejor_sol:
        lavado_actual = mejor_sol[prenda_]
        lavados[lavado_actual] = lavados.get(lavado_actual, []) + [prenda_]

    mostrar_solucion_en_pantalla(lavados, tiempo_de_lavado)


def coloreo_rec(grafo, k, v_pintados, v, min_colores, min_sol, min_tiempo, tiempo_lavados):
    for color in range(1, k + 1):
        v_pintados[v] = color  # Pinto al vertice v del color `color`

        if not es_compatible(grafo, v_pintados, v):
            continue

        if usa_mas_colores(v_pintados, min_colores):
            continue

        if usa_mas_tiempo_lavado(v_pintados, min_tiempo, tiempo_lavados):
            continue

        correcto = True
        for w in grafo.neighbors(v):
            if w in v_pintados:
                continue

            min_colores, min_sol, min_tiempo, correcto = coloreo_rec(grafo, k,
                                                                     v_pintados, w,
                                                                     min_colores, min_sol,
                                                                     min_tiempo, tiempo_lavados)
            if not correcto:
                break

        if correcto:
            if len(v_pintados) > len(min_sol):
                min_sol = v_pintados
            if len(v_pintados) == grafo.number_of_nodes() and not usa_mas_colores(v_pintados, min_colores):
                return len(v_pintados), v_pintados, obtener_tiempo_lavado(v_pintados, tiempo_lavados), True
            return min_colores, min_sol, min_tiempo, True

    del v_pintados[v]
    return min_colores, min_sol, min_tiempo, False


if __name__ == "__main__":
    prendas, d_incompatibilidades, d_lavados = procesar_archivo_prendas()
    grafo_prendas = crear_grafo(prendas, d_incompatibilidades)
    solucion_por_coloreo(d_lavados)
