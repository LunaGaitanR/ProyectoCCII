class Ruido:
    """
    Representa una fuente de ruido con su frecuencia e intensidad.
    """

    def __init__(self, id_ruido, frecuencia, intensidad):
        """
        Inicializa una fuente de ruido con un ID, frecuencia e intensidad.

        :param id_ruido: Nombre o identificador de la fuente de ruido.
        :param frecuencia: Frecuencia del ruido en Hz.
        :param intensidad: Intensidad del ruido en decibeles (dB).
        """
        self.id_ruido = id_ruido
        self.frecuencia = frecuencia
        self.intensidad = intensidad
