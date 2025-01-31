import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


#Materiales
materiales={#Resistencias a 500 y 2000 Hz
            'Ladrillo': {'500hz': 0.02, '2000hz': 0.04},#Ladrillo, muro con enlucido de yeso 
            'Loseta': {'500hz': 0.06, '2000hz': 0.04},#Losetas de yeso seco
            'Espuma': {'500hz': 0.55, '2000hz': 0.65}#La espuma de poliuretano
}

#Espacios
espacios = {'H1': (4, 2, 0),
        'H2': (4, 4, 0),
        'S': (3, 3, 0),
        'H3': (4, 4, 4),
        'H4':(3,2,4),
        'H5':(4,2,4),
        'E': (3, 3, 4),}


# Aristas
aristas = {('H2', 'H3'):'Ladrillo',
            ('H1', 'S'):'Loseta', 
            ('H1', 'H5'):'Ladrillo', 
            ('S', 'H4'):'Ladrillo',
            ('S', 'E'): 'Ladrillo',
            ('H4', 'E'):'Loseta',
            ('H5', 'E'):'Loseta',
            ('H3','E'):'Loseta',}

#Ruidos
ruidos={'Avión': {'intensidad': 90, 'frecuencia': 2000},
    'Vía': {'intensidad': 70, 'frecuencia': 500},
    'Gimnasio': {'intensidad': 65, 'frecuencia': 500}}

umbrales_habitabilidad = {
    'H1': 70,
    'H2': 40,
    'H3':40,
    'H4':65,
    'H5': 50,
    'S':35,
    'E':50,
}

def calcular_ruido_espacio(espacio, aristas, materiales, ruidos, umbrales):
    ruido_total = 0
    for arista, material in aristas.items():
        if espacio in arista:
            for fuente, datos_ruido in ruidos.items():
                frecuencia = datos_ruido['frecuencia']
                intensidad = datos_ruido['intensidad']
                absorcion = materiales[material][str(frecuencia) + 'hz']
                ruido_total += intensidad * absorcion*2
    
    # Comparar con el umbral específico del espacio
    umbral = umbrales[espacio]
    return ruido_total <= umbral


def imprimirGrafo():
    # Crear la figura y los ejes 3D
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Graficar los nodos con color según habitabilidad
    for nodo, coordenadas in espacios.items():
        x, y, z = coordenadas
        es_habitable = calcular_ruido_espacio(nodo, aristas, materiales, ruidos, umbrales_habitabilidad)
        color = 'green' if es_habitable else 'red'
        ax.scatter(x, y, z, c=color, marker='o', s=100)
        ax.text(x, y, z, nodo, fontsize=12)

    # Graficar las aristas
    for arista in aristas:
        nodo1, nodo2 = arista
        x1, y1, z1 = espacios[nodo1]
        x2, y2, z2 = espacios[nodo2]
        ax.plot([x1, x2], [y1, y2], [z1, z2], c='cyan')

        
    # Etiquetas de los ejes
    ax.set_xlabel('Eje X')
    ax.set_ylabel('Eje Y')
    ax.set_zlabel('Eje Z')

    # Mostrar el gráfico
    plt.show()
    


imprimirGrafo()
# Calcular la habitabilidad de cada espacio
for espacio in espacios:
    es_habitable = calcular_ruido_espacio(espacio, aristas, materiales, ruidos, umbrales_habitabilidad)
    print(f"El espacio {espacio} es habitable: {es_habitable}")
