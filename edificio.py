from espacio import Espacio
from material import Material
from ruido import Ruido

class Edificio:
    """
    Representa un edificio con múltiples espacios, materiales y fuentes de ruido.
    """

    def __init__(self, nombre):
        self.nombre = nombre
        self.espacios = {}
        self.materiales = {}
        self.ruidos = {}
        # Diccionario para almacenar el umbral asociado a cada espacio
        self.umbrales_habitabilidad = {}
        # Diccionario para almacenar la actividad asignada a cada espacio
        self.actividades = {}
        # (Opcional) Diccionario para almacenar la designación del espacio según el umbral
        self.designaciones = {}

    def agregar_espacio(self, espacio: Espacio):
        self.espacios[espacio.id_espacio] = espacio

    def agregar_material(self, material: Material):
        self.materiales[material.id_material] = material

    def agregar_ruido(self, ruido: Ruido):
        self.ruidos[ruido.id_ruido] = ruido

    def asignar_designacion(self, umbral):
        """
        Asigna una designación según el umbral. Puedes personalizar estas reglas.
        """
        if umbral < 40:
            return 'Espacio silencioso'
        elif umbral < 60:
            return 'Espacio moderado'
        else:
            return 'Espacio ruidoso'

    def agregar_actividad(self, espacio_id, id_actividad, umbral):
        """
        Registra o actualiza la actividad y su umbral asociado para el espacio indicado.
        """
        self.actividades[espacio_id] = id_actividad
        self.umbrales_habitabilidad[espacio_id] = umbral
        # Asigna la designación en base al umbral
        self.designaciones[espacio_id] = self.asignar_designacion(umbral)

    def intercambiar_actividad(self, espacio_id1, espacio_id2):
        """
        Intercambia la actividad, el umbral y la designación entre dos espacios.
        Luego imprime el estado actualizado de cada uno.
        """
        # Verificar que ambos espacios existan en el registro
        if espacio_id1 not in self.actividades or espacio_id2 not in self.actividades:
            print("Uno de los espacios no existe. Verifica los identificadores.")
            return

        # Intercambio de actividad y umbral
        self.actividades[espacio_id1], self.actividades[espacio_id2] = \
            self.actividades[espacio_id2], self.actividades[espacio_id1]
        self.umbrales_habitabilidad[espacio_id1], self.umbrales_habitabilidad[espacio_id2] = \
            self.umbrales_habitabilidad[espacio_id2], self.umbrales_habitabilidad[espacio_id1]

        # Actualizar designaciones para ambos espacios
        self.designaciones[espacio_id1] = self.asignar_designacion(self.umbrales_habitabilidad[espacio_id1])
        self.designaciones[espacio_id2] = self.asignar_designacion(self.umbrales_habitabilidad[espacio_id2])

        print("Intercambio realizado:")
        print(f"  - {espacio_id1}: Actividad = {self.actividades[espacio_id1]}, "
            f"Umbral = {self.umbrales_habitabilidad[espacio_id1]}, "
            f"Designación = {self.designaciones[espacio_id1]}")
        print(f"  - {espacio_id2}: Actividad = {self.actividades[espacio_id2]}, "
            f"Umbral = {self.umbrales_habitabilidad[espacio_id2]}, "
            f"Designación = {self.designaciones[espacio_id2]}")

    def calcular_habitabilidad_espacios(self, aristas):
        """
        Calcula la habitabilidad de cada espacio comparando el ruido total con el umbral asignado.
        Muestra en consola la actividad, el ruido total, el umbral y la designación.
        """
        for espacio in self.espacios.values():
            ruido_total = espacio.calcular_ruido(self.materiales, self.ruidos, aristas)
            umbral = self.umbrales_habitabilidad.get(espacio.id_espacio, float('inf'))
            actividad = self.actividades.get(espacio.id_espacio, "Sin actividad asignada")
            designacion = self.designaciones.get(espacio.id_espacio, "Sin designación")
            es_habitable = ruido_total <= umbral
            print(
                f"Espacio: {espacio.id_espacio} | Actividad: {actividad} | "
                f"Ruido: {ruido_total:.2f} dB | Umbral: {umbral} dB | "
                f"Designación: {designacion} | Habitable: {'Sí' if es_habitable else 'No'}"
            )

    def ajustar_habitabilidad(self, aristas):
        """
        Ajusta dinámicamente los valores del edificio para que todos los espacios sean habitables.
        :param aristas: Diccionario con las conexiones entre espacios y sus materiales.
        """
        cambios_realizados = False

        for espacio_id, espacio in self.espacios.items():
            # Calcular el ruido total del espacio
            ruido_total = espacio.calcular_ruido(self.materiales, self.ruidos, aristas)
            # Obtener el umbral actual
            umbral_actual = self.umbrales_habitabilidad.get(espacio_id, float('inf'))

            # Si el ruido total supera el umbral, ajustamos el umbral para que sea habitable
            if ruido_total > umbral_actual:
                # Incrementar el umbral para que sea igual o mayor al ruido
                self.umbrales_habitabilidad[espacio_id] = ruido_total + 5  # Ajuste dinámico (puedes cambiar el +5 según lo desees)
                cambios_realizados = True

        if cambios_realizados:
            print("Ajustes realizados para garantizar que todos los espacios sean habitables.")
        else:
            print("Todos los espacios ya son habitables.")