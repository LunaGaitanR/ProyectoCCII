class Espacio:
    """
    Representa un espacio dentro del edificio con su posición en 3D y su evaluación de habitabilidad.
    """

    def __init__(self, id_espacio, x, y, z):
        """
        Inicializa un espacio con su ID y posición en el espacio 3D.

        :param id_espacio: Identificador del espacio.
        :param x: Coordenada en el eje X.
        :param y: Coordenada en el eje Y.
        :param z: Coordenada en el eje Z.
        """
        self.id_espacio = id_espacio
        self.x = x
        self.y = y
        self.z = z

    def calcular_ruido(self, materiales, ruidos, aristas):
        """
        Calcula el ruido total en el espacio basado en las conexiones con otros espacios y los materiales.

        :param materiales: Diccionario con los materiales disponibles.
        :param ruidos: Diccionario con las fuentes de ruido.
        :param aristas: Diccionario con las conexiones entre espacios y sus materiales.
        :return: Nivel total de ruido en el espacio.
        """
        ruido_total = 0

        for arista, material_id in aristas.items():
            if self.id_espacio in arista:
                material = materiales.get(material_id)
                if material:
                    for ruido in ruidos.values():
                        absorcion = material.resistencias.get(str(ruido.frecuencia) + 'hz', 0)
                        ruido_total += ruido.intensidad * absorcion * 2  # Multiplicamos por 2 para simular ambos lados

        return ruido_total
