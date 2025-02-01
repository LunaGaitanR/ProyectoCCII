import networkx as nx
import matplotlib.pyplot as plt

def colorear_grafo_welch_powell(nodos, aristas):
    """
    Aplica el algoritmo de Welch-Powell para colorear nodos sin que vecinos tengan el mismo color.

    :param nodos: Lista de nodos del grafo.
    :param aristas: Diccionario de conexiones entre nodos.
    :return: Diccionario {nodo: color}.
    """
    # Crear grafo con NetworkX
    G = nx.Graph()
    G.add_nodes_from(nodos)
    G.add_edges_from(aristas.keys())

    # Ordenamos los nodos por el grado en orden descendente
    nodos_ordenados = sorted(G.nodes, key=lambda x: G.degree[x], reverse=True)

    colores_disponibles = ["red", "blue", "green", "yellow", "purple", "orange"]
    asignacion_colores = {}

    for nodo in nodos_ordenados:
        vecinos = set(G.neighbors(nodo))
        colores_usados = {asignacion_colores[vec] for vec in vecinos if vec in asignacion_colores}

        # Asigna el primer color disponible que no esté en los vecinos
        for color in colores_disponibles:
            if color not in colores_usados:
                asignacion_colores[nodo] = color
                break

    return asignacion_colores

def obtener_colores_vecinos(edificio, aristas):
    """
    Aplica la coloración de Welch-Powell y retorna un diccionario con los colores asignados a cada nodo.
    """
    nodos = list(edificio.espacios.keys())
    colores = colorear_grafo_welch_powell(nodos, aristas)  # Diccionario {nodo: color}
    return colores  # Retornamos los colores sin dibujar el grafo aquí
