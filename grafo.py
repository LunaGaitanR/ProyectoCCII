import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

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
        color = 'green' if ruido_total <= umbral else 'red'

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
    ax.set_title("Grafo del Edificio")

    plt.show()
