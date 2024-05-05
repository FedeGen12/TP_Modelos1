from utilidades import *

def obtener_tiempo_lavado(lavado, tiempo_lavado_prendas):
    tiempo_lavado = 0
    for prenda in lavado:
        tiempo_lavado_prenda = tiempo_lavado_prendas[prenda]
        tiempo_lavado = max(tiempo_lavado_prenda, tiempo_lavado)
    return tiempo_lavado


def es_compatible(nueva_prenda, lavados, num_lavado, incompatibilidades, lavados_por_prenda):
    lavado = lavados[num_lavado]
    removes_a_realizar = []

    for prenda in lavado:
        if nueva_prenda in incompatibilidades[prenda]:
            cant_lavados_de_prenda = len(lavados_por_prenda[prenda])
            if cant_lavados_de_prenda > 1:
                removes_a_realizar.append((prenda, num_lavado))
                continue
            return False

    for remove in removes_a_realizar:
        prenda, num_lavado = remove
        lavado.remove(prenda)
        lavados_por_prenda[prenda].remove(num_lavado)
    return True


def intentar_redistribucion(lavados, prendas_con_lavados, incompatibilidades):
    for prenda in prendas_con_lavados:
        for lavado in lavados:
            if lavado not in prendas_con_lavados[prenda]:
                if es_compatible(prenda, lavados, lavado, incompatibilidades, prendas_con_lavados):
                        lavados[lavado].append(prenda)
                        prendas_con_lavados[prenda].append(lavado)


def problema_lavados(num_prendas, incompatibilidades, tiempos_lavado):
    prendas_ordenadas = sorted(range(1, num_prendas + 1), key=lambda prenda1: tiempos_lavado[prenda1], reverse=True)

    lavados, nuevo_lavado, prendas_con_lavados = {}, 1, {}

    for prenda in prendas_ordenadas:
        intentar_redistribucion(lavados, prendas_con_lavados, incompatibilidades)

        mejor_tiempo = float('inf')
        mejores_lavados = []

        for num_lavado in lavados:
            lavado = lavados[num_lavado]

            tiempo_lavado = obtener_tiempo_lavado(lavado, tiempos_lavado)

            if es_compatible(prenda, lavados, num_lavado, incompatibilidades, prendas_con_lavados):
                nuevo_tiempo = max(tiempo_lavado, tiempos_lavado[prenda])
                if nuevo_tiempo <= mejor_tiempo:
                    mejor_tiempo = nuevo_tiempo
                    mejores_lavados.append(num_lavado)

        if not mejores_lavados:
            lavados[nuevo_lavado] = [prenda]
            prendas_con_lavados[prenda] = [nuevo_lavado]
            nuevo_lavado += 1
        else:
            for num_lavado in mejores_lavados:
                lavados[num_lavado].append(prenda)
                prendas_con_lavados[prenda] = prendas_con_lavados.get(prenda, []) + [num_lavado]

    for prenda in prendas_con_lavados:
        lavados_prenda = prendas_con_lavados[prenda].copy()

        if len(lavados_prenda) > 1:
            lavado_elegido = 0
            tiempo_sin_prenda = float('inf')

            for num_lavado in lavados_prenda:
                lavados[num_lavado].remove(prenda)
                prendas_con_lavados[prenda].remove(num_lavado)
                tiempo_sin_prenda_act = obtener_tiempo_lavado(lavados[num_lavado], tiempos_lavado)
                if tiempo_sin_prenda_act < tiempo_sin_prenda:
                    lavado_elegido = num_lavado
                    tiempo_sin_prenda = tiempo_sin_prenda_act

            lavados[lavado_elegido].append(prenda)
            prendas_con_lavados[prenda].append(lavado_elegido)

    tiempo_total_lavado = sum([obtener_tiempo_lavado(lavado, tiempos_lavado) for lavado in lavados.values()])

    return lavados, tiempo_total_lavado


def solucion_valida(sol, incompatibilidades):
    for lavado in sol:
        prendas_en_lavado = sol[lavado]
        cant_prendas = len(prendas_en_lavado)
        for i in range(cant_prendas):
            for j in range(i+1, cant_prendas):
                prenda1, prenda2 = prendas_en_lavado[i], prendas_en_lavado[j]
                if prenda2 in incompatibilidades[prenda1] or prenda1 in incompatibilidades[prenda2]:
                    return 'La solución es inválida'
    return 'La solución es válida'


if __name__ == "__main__":
    cantidad_prendas, dic_incompatibilidades, dic_lav_prendas = procesar_archivo_prendas(2)

    solucion, tiempo_total = problema_lavados(cantidad_prendas, dic_incompatibilidades, dic_lav_prendas)
    print(solucion_valida(solucion, dic_incompatibilidades))
    mostrar_solucion_en_pantalla(solucion, dic_lav_prendas)
    escribir_solucion(solucion)
