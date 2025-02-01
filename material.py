class Material:
    """
    Representa un material con sus coeficientes de absorción a diferentes frecuencias.
    """

    def __init__(self, id_material, resistencia_500hz, resistencia_2000hz):
        """
        Inicializa un material con su ID y coeficientes de absorción para 500 Hz y 2000 Hz.

        :param id_material: Nombre o identificador del material.
        :param resistencia_500hz: Coeficiente de absorción a 500 Hz.
        :param resistencia_2000hz: Coeficiente de absorción a 2000 Hz.
        """
        self.id_material = id_material
        self.resistencias = {
            '500hz': resistencia_500hz,
            '2000hz': resistencia_2000hz
        }
