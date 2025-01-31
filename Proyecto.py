import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class Material:
    def __init__(self, id_material, resistencia_500hz, resistencia_2000hz):
        self.id_material = id_material
        self.resistencias = {'500hz': resistencia_500hz, '2000hz': resistencia_2000hz}

class Espacio:
    def __init__(self, id_espacio, x, y, z, actividad=None, fuente=None):
        self.id_espacio = id_espacio
        self.x = x
        self.y = y
        self.z = z
        self.actividad = actividad
        self.fuente = fuente

    def calcular_habitabilidad(self, materiales, ruidos, umbrales, aristas):
        #Calcula si el espacio es habitable según los umbrales de ruido
        ruido_total = 0
        for arista, material_id in aristas.items():
            if self.id_espacio in arista:
                material = materiales.get(material_id)
                if material:
                    for fuente_id, ruido in ruidos.items():  # Itera sobre los ruidos
                        frecuencia = ruido.frecuencia
                        intensidad = ruido.intensidad
                        absorcion = material.resistencias.get(str(frecuencia) + 'hz')
                        if absorcion is not None:
                            ruido_total += intensidad * absorcion
                        else:
                            print(f"Advertencia: No se encontró absorción para {material_id} a {frecuencia} Hz.")
                else:
                    print(f"Advertencia: No se encontró el material con ID {material_id}.")
        return ruido_total <= umbrales.get(self.id_espacio, float('inf'))

class Ruido:
    def __init__(self, id_ruido, frecuencia, intensidad):
        self.id_ruido = id_ruido
        self.frecuencia = frecuencia
        self.intensidad = intensidad

class Edificio:
    def __init__(self, nombre):
        self.nombre = nombre
        self.espacios = {}  # Diccionario para almacenar los espacios del edificio
        self.materiales = {}  # Diccionario para almacenar los materiales del edificio
        self.ruidos = {}  # Diccionario para almacenar los ruidos del edificio
        self.umbrales_habitabilidad = {}  # Diccionario para almacenar los umbrales de habitabilidad

    def agregar_espacio(self, espacio):
        self.espacios[espacio.id_espacio] = espacio

    def agregar_material(self, material):
        self.materiales[material.id_material] = material

    def agregar_ruido(self, ruido):
        self.ruidos[ruido.id_ruido] = ruido

    def agregar_umbral(self, espacio_id, umbral):
        self.umbrales_habitabilidad[espacio_id] = umbral

    def calcular_habitabilidad_espacios(self, aristas):
        #Calcula la habitabilidad de todos los espacios del edificio
        for espacio in self.espacios.values():
            es_habitable = espacio.calcular_habitabilidad(self.materiales, self.ruidos, self.umbrales_habitabilidad, aristas)
            print(f"El espacio {espacio.id_espacio} es habitable: {es_habitable}")

    def imprimir_grafo(self, aristas):
        #Imprime el grafo del edificio y sus espacios, coloreando según habitabilidad.
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        for espacio in self.espacios.values():
            es_habitable = espacio.calcular_habitabilidad(self.materiales, self.ruidos, self.umbrales_habitabilidad, aristas)
            color = 'green' if es_habitable else 'red'
            ax.scatter(espacio.x, espacio.y, espacio.z, c=color, marker='o', s=100)
            ax.text(espacio.x, espacio.y, espacio.z, espacio.id_espacio, fontsize=12)

        for arista in aristas:
            nodo1, nodo2 = arista
            x1, y1, z1 = self.espacios[nodo1].x, self.espacios[nodo1].y, self.espacios[nodo1].z
            x2, y2, z2 = self.espacios[nodo2].x, self.espacios[nodo2].y, self.espacios[nodo2].z
            ax.plot([x1, x2], [y1, y2], [z1, z2], c='cyan')

        ax.set_xlabel('Eje X')
        ax.set_ylabel('Eje Y')
        ax.set_zlabel('Eje Z')
        plt.show()

class Main:
    # --- Inicialización de datos ---
    edificio = Edificio("Mi Edificio")

    # Materiales
    edificio.agregar_material(Material("Ladrillo", 0.02, 0.04))
    edificio.agregar_material(Material("Loseta", 0.06, 0.04))
    edificio.agregar_material(Material("Espuma", 0.55, 0.65))

    # Espacios
    edificio.agregar_espacio(Espacio("H1", 4, 2, 0))
    edificio.agregar_espacio(Espacio("H2", 4, 4, 0))
    edificio.agregar_espacio(Espacio("S", 3, 3, 0))
    edificio.agregar_espacio(Espacio("H3", 4, 4, 4))
    edificio.agregar_espacio(Espacio("H4", 3, 2, 4))
    edificio.agregar_espacio(Espacio("H5", 4, 2, 4))
    edificio.agregar_espacio(Espacio("E", 3, 3, 4))

    # Ruidos
    edificio.agregar_ruido(Ruido("Avión", 2000, 90))
    edificio.agregar_ruido(Ruido("Vía", 500, 70))
    edificio.agregar_ruido(Ruido("Gimnasio", 500, 65))

    # Umbrales de habitabilidad, estos están dados por las actividades que se hace por espacio
    edificio.agregar_umbral("H1", 70) #Tienda
    edificio.agregar_umbral("H2", 40) #Dormitorio
    edificio.agregar_umbral("H3", 40) #Dormitorio
    edificio.agregar_umbral("H4", 65) #Gimnasio
    edificio.agregar_umbral("H5", 50) #Varios
    edificio.agregar_umbral("S", 35) #Estudio
    edificio.agregar_umbral("E", 50) #Varios

    aristas = {
        ('H2', 'H3'): 'Ladrillo',  # Usa 'Ladrillo' (el ID) y no el objeto Material
        ('H1', 'S'): 'Loseta',
        ('H1', 'H5'): 'Ladrillo',
        ('S', 'H4'): 'Ladrillo',
        ('S', 'E'): 'Ladrillo',
        ('H4', 'E'): 'Loseta',
        ('H5', 'E'): 'Loseta',
        ('H3', 'E'): 'Loseta',
    }

    # --- Ejecución ---
    edificio.imprimir_grafo(aristas)
    edificio.calcular_habitabilidad_espacios(aristas)
    
