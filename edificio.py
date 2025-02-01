from espacio import Espacio
from material import Material
from ruido import Ruido

class Edificio:
    """
    Representa un edificio con múltiples espacios, materiales y fuentes de ruido.
    """

    def __init__(self, nombre):
        """
        Inicializa un edificio con un nombre y contenedores de datos.

        :param nombre: Nombre del edificio.
        """
        self.nombre = nombre
        self.espacios = {}
        self.materiales = {}
        self.ruidos = {}
        self.umbrales_habitabilidad = {}

    def agregar_espacio(self, espacio: Espacio):
        self.espacios[espacio.id_espacio] = espacio

    def agregar_material(self, material: Material):
        self.materiales[material.id_material] = material

    def agregar_ruido(self, ruido: Ruido):
        self.ruidos[ruido.id_ruido] = ruido

    def agregar_actividad(self, espacio_id, id_actividad, umbral):
        self.umbrales_habitabilidad[espacio_id] = umbral

    def calcular_habitabilidad_espacios(self, aristas):
        """
        Calcula la habitabilidad de cada espacio y muestra en consola su ruido total y umbral.

        :param aristas: Diccionario con las conexiones entre espacios y sus materiales.
        """
        for espacio in self.espacios.values():
            ruido_total = espacio.calcular_ruido(self.materiales, self.ruidos, aristas)
            umbral = self.umbrales_habitabilidad.get(espacio.id_espacio, float('inf'))
            es_habitable = ruido_total <= umbral
            print(f"Espacio: {espacio.id_espacio} | Ruido: {ruido_total:.2f} dB | Umbral: {umbral} dB | Habitable: {'Sí' if es_habitable else 'No'}")
