import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from coloracion import obtener_color_gradual
from coloracion_vecinos import obtener_colores_vecinos

def imprimir_grafo(edificio, aristas):
    """
    Grafica el edificio en 3D, coloreando los nodos según su habitabilidad.

    :param edificio: Objeto de tipo Edificio con los espacios, umbrales y actividades.
    :param aristas: Diccionario con las conexiones entre espacios y sus materiales.
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Graficar nodos
    for espacio in edificio.espacios.values():
        # Calcular el ruido total del espacio
        ruido_total = espacio.calcular_ruido(edificio.materiales, edificio.ruidos, aristas)
        # Obtener el umbral asociado al espacio
        umbral = edificio.umbrales_habitabilidad.get(espacio.id_espacio, float('inf'))
        # Determinar el color según la habitabilidad
        color = 'green' if ruido_total <= umbral else 'red' # Colores fijos

        # Dibujar nodo
        ax.scatter(espacio.x, espacio.y, espacio.z, c=color, marker='o', s=100)
        # Mostrar el ID del espacio y la actividad asignada
        actividad = edificio.actividades.get(espacio.id_espacio, "Sin actividad")
        ax.text(espacio.x, espacio.y, espacio.z, f"{espacio.id_espacio}\n({actividad})", fontsize=9)

    # Graficar aristas
    for nodo1, nodo2 in aristas.keys():
        x1, y1, z1 = edificio.espacios[nodo1].x, edificio.espacios[nodo1].y, edificio.espacios[nodo1].z
        x2, y2, z2 = edificio.espacios[nodo2].x, edificio.espacios[nodo2].y, edificio.espacios[nodo2].z
        ax.plot([x1, x2], [y1, y2], [z1, z2], c='cyan', alpha=0.7)

    # Configurar los ejes
    ax.set_xlabel('Eje X')
    ax.set_ylabel('Eje Y')
    ax.set_zlabel('Eje Z')
    plt.title("Grafo de Habitabilidad")
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
    plt.title("Propagación del Ruido")
    plt.show()

def imprimir_grafo_coloreado_vecinos(edificio, aristas):
    """
    Genera el grafo en 3D con la coloración de Welch-Powell, donde nodos vecinos tienen diferentes colores.
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Obtener los colores de cada nodo
    colores_nodos = obtener_colores_vecinos(edificio, aristas)

    for espacio in edificio.espacios.values():
        color = colores_nodos.get(espacio.id_espacio, 'gray')  # Color según el algoritmo
        ax.scatter(espacio.x, espacio.y, espacio.z, c=color, marker='o', s=100)
        ax.text(espacio.x, espacio.y, espacio.z, espacio.id_espacio, fontsize=12)

    for nodo1, nodo2 in aristas.keys():
        x1, y1, z1 = edificio.espacios[nodo1].x, edificio.espacios[nodo1].y, edificio.espacios[nodo1].z
        x2, y2, z2 = edificio.espacios[nodo2].x, edificio.espacios[nodo2].y, edificio.espacios[nodo2].z
        ax.plot([x1, x2], [y1, y2], [z1, z2], c='cyan')

    ax.set_xlabel('Eje X')
    ax.set_ylabel('Eje Y')
    ax.set_zlabel('Eje Z')
    plt.title("Coloración por Vecinos")
    plt.show()
