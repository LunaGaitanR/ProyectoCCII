import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from coloracion import obtener_color_gradual

def imprimir_grafo(edificio, aristas):
    """
    Grafica el edificio en 3D, coloreando los nodos según su habitabilidad.

    :param edificio: Objeto de tipo Edificio con los espacios y umbrales de habitabilidad.
    :param aristas: Diccionario con las conexiones entre espacios y sus materiales.
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for espacio in edificio.espacios.values():
        ruido_total = espacio.calcular_ruido(edificio.materiales, edificio.ruidos, aristas)
        umbral = edificio.umbrales_habitabilidad.get(espacio.id_espacio, float('inf'))
        color = 'green' if ruido_total <= umbral else 'red' # Colores fijos

        ax.scatter(espacio.x, espacio.y, espacio.z, c=color, marker='o', s=100)
        ax.text(espacio.x, espacio.y, espacio.z, espacio.id_espacio, fontsize=12)

    for nodo1, nodo2 in aristas.keys():
        x1, y1, z1 = edificio.espacios[nodo1].x, edificio.espacios[nodo1].y, edificio.espacios[nodo1].z
        x2, y2, z2 = edificio.espacios[nodo2].x, edificio.espacios[nodo2].y, edificio.espacios[nodo2].z
        ax.plot([x1, x2], [y1, y2], [z1, z2], c='cyan')

    ax.set_xlabel('Eje X')
    ax.set_ylabel('Eje Y')
    ax.set_zlabel('Eje Z')
    plt.show()

def imprimir_grafo_coloreado(edificio, aristas):
    """
    Genera el grafo con un gradiente de colores basado en el ruido.
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for espacio in edificio.espacios.values():
        ruido_total = espacio.calcular_ruido(edificio.materiales, edificio.ruidos, aristas)
        umbral = edificio.umbrales_habitabilidad.get(espacio.id_espacio, float('inf'))
        color = obtener_color_gradual(ruido_total, umbral)  # Colores graduales

        ax.scatter(espacio.x, espacio.y, espacio.z, c=color, marker='o', s=100)
        ax.text(espacio.x, espacio.y, espacio.z, espacio.id_espacio, fontsize=12)

    for nodo1, nodo2 in aristas.keys():
        x1, y1, z1 = edificio.espacios[nodo1].x, edificio.espacios[nodo1].y, edificio.espacios[nodo1].z
        x2, y2, z2 = edificio.espacios[nodo2].x, edificio.espacios[nodo2].y, edificio.espacios[nodo2].z
        ax.plot([x1, x2], [y1, y2], [z1, z2], c='cyan')

    ax.set_xlabel('Eje X')
    ax.set_ylabel('Eje Y')
    ax.set_zlabel('Eje Z')
    plt.show()