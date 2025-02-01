import random
import tkinter as tk
from tkinter import messagebox
from edificio import Edificio
from ruido import Ruido
from espacio import Espacio
from material import Material
from grafo import imprimir_grafo, imprimir_grafo_coloreado, imprimir_grafo_coloreado_vecinos


class Aplicacion:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulación de Habitabilidad - Configuración de Ruidos y Actividades")

        # Crear el edificio
        self.edificio = self.inicializar_edificio()

        # Guardar los datos originales
        self.actividades_originales = self.edificio.actividades.copy()
        self.umbrales_originales = self.edificio.umbrales_habitabilidad.copy()

        # Crear la interfaz gráfica
        self.crear_interfaz()

    def inicializar_edificio(self):
        """Inicializa el edificio con espacios, materiales, ruidos y actividades predefinidos."""
        edificio = Edificio("Mi Edificio")

        # Materiales
        edificio.agregar_material(Material("Ladrillo", 0.02, 0.04))
        edificio.agregar_material(Material("Loseta", 0.06, 0.04))
        edificio.agregar_material(Material("Espuma", 0.55, 0.65))
        # Materiales adicionales
        edificio.agregar_material(Material("Aislante Fuerte", 0.70, 0.80))
        edificio.agregar_material(Material("Vidrio Doble", 0.50, 0.60))

        # Espacios
        edificio.agregar_espacio(Espacio("H1", 4, 2, 0))
        edificio.agregar_espacio(Espacio("H2", 4, 4, 0))
        edificio.agregar_espacio(Espacio("S", 3, 3, 0))
        edificio.agregar_espacio(Espacio("H3", 4, 4, 4))
        edificio.agregar_espacio(Espacio("H4", 3, 2, 4))
        edificio.agregar_espacio(Espacio("H5", 4, 2, 4))
        edificio.agregar_espacio(Espacio("E", 3, 3, 4))

        # Ruidos iniciales
        self.ruidos = {
            "Avión": {"frecuencia": 2000, "intensidad": 90},
            "Vía": {"frecuencia": 500, "intensidad": 70},
            "Gimnasio": {"frecuencia": 500, "intensidad": 65}
        }
        self.ruido_entries = {}

        for nombre, datos in self.ruidos.items():
            edificio.agregar_ruido(Ruido(nombre, datos["frecuencia"], datos["intensidad"]))

        # Umbrales de habitabilidad asociados a las actividades de cada espacio.
        edificio.agregar_actividad("H1", 'Tienda', 70)
        edificio.agregar_actividad("H2", 'Dormitorio', 40)
        edificio.agregar_actividad("H3", 'Dormitorio', 40)
        edificio.agregar_actividad("H4", 'Gimnasio', 65)
        edificio.agregar_actividad("H5", 'Varios', 50)
        edificio.agregar_actividad("S", 'Estudio', 35)
        edificio.agregar_actividad("E", 'Varios', 50)

        return edificio

    def crear_interfaz(self):
        """Genera la interfaz gráfica con campos para modificar solo la intensidad de los ruidos."""
        tk.Label(self.root, text="Modifique la intensidad de los ruidos y genere el grafo", font=("Arial", 12, "bold")).pack(pady=10)

        frame_ruidos = tk.Frame(self.root)
        frame_ruidos.pack()

        # Crear campos de entrada solo para la intensidad
        for i, (nombre, datos) in enumerate(self.ruidos.items()):
            tk.Label(frame_ruidos, text=f"{nombre} (Frecuencia: {datos['frecuencia']} Hz):").grid(row=i, column=0, padx=10, pady=5)

            inten_entry = tk.Entry(frame_ruidos, width=10)
            inten_entry.insert(0, str(datos["intensidad"]))
            inten_entry.grid(row=i, column=1)

            self.ruido_entries[nombre] = inten_entry  # Solo guardamos la intensidad

        # Botón para aplicar cambios y generar grafo
        tk.Button(self.root, text="Generar Grafo", command=self.actualizar_ruidos_y_generar_grafo, font=("Arial", 12)).pack(pady=10)

        # Botón para generar grafo con coloreado gradual
        tk.Button(self.root, text="Coloreado del Grafo", command=self.generar_grafo_coloreado, font=("Arial", 12)).pack(pady=10)

        # Botón para coloración restringida de vecinos
        tk.Button(self.root, text="Coloración por Vecinos", command=self.generar_grafo_coloreado_vecinos, font=("Arial", 12)).pack(pady=10)

        # Sección para ajustar
        frame_automatico = tk.Frame(self.root)
        frame_automatico.pack(pady=10)

        tk.Label(frame_automatico, text="Ajustar actividades", font=("Arial", 12, "bold")).pack(pady=5)
        tk.Button(frame_automatico, text="Ajustar", command=self.ajustar_espacios, font=("Arial", 12)).pack(pady=10)

        # Botón para restablecer el grafo
        frame_reset = tk.Frame(self.root)
        frame_reset.pack(pady=10)

        tk.Label(frame_reset, text="Restablecer grafo a su versión original", font=("Arial", 12, "bold")).pack(pady=5)
        tk.Button(frame_reset, text="Restablecer", command=self.restablecer_grafo, font=("Arial", 12)).pack(pady=10)

    def ajustar_espacios(self):
        """Primero intenta ajustar el material del espacio con materiales adicionales; si no funciona, intercambia actividades."""
        aristas = {
            ('H2', 'H3'): 'Ladrillo',
            ('H1', 'S'): 'Loseta',
            ('H1', 'H5'): 'Ladrillo',
            ('S', 'H4'): 'Ladrillo',
            ('S', 'E'): 'Ladrillo',
            ('H4', 'E'): 'Loseta',
            ('H5', 'E'): 'Loseta',
            ('H3', 'E'): 'Loseta',
        }

        # Mapeo explícito del material actual por nodo
        materiales_por_nodo = {
            'H1': 'Ladrillo',
            'H2': 'Loseta',
            'H3': 'Ladrillo',
            'H4': 'Espuma',
            'H5': 'Ladrillo',
            'S': 'Loseta',
            'E': 'Ladrillo',
        }

        # Identificar nodos habitables y no habitables
        nodos_no_habitables = []
        nodos_habitables = []

        for espacio_id, espacio in self.edificio.espacios.items():
            ruido_total = espacio.calcular_ruido(self.edificio.materiales, self.edificio.ruidos, aristas)
            umbral = self.edificio.umbrales_habitabilidad.get(espacio_id, float('inf'))
            if ruido_total > umbral:
                nodos_no_habitables.append(espacio_id)
            else:
                nodos_habitables.append(espacio_id)

        # Si no hay nodos no habitables, no es necesario hacer ajustes
        if not nodos_no_habitables:
            messagebox.showinfo("Info", "Todos los nodos ya son habitables.")
            return

        # Materiales adicionales priorizados
        materiales_prioritarios = ["Aislante Fuerte", "Vidrio Doble"]

        # Intentar ajustar materiales primero
        for nodo in nodos_no_habitables:
            material_actual = materiales_por_nodo.get(nodo, "Desconocido")  # Obtener material actual del nodo
            material_cambiado = False  # Flag para rastrear si el material fue cambiado

            # Intentar usar materiales adicionales primero
            for material_id in materiales_prioritarios:
                if material_id != material_actual:  # Evitar cambiar por el mismo material
                    ruido_total = self.edificio.espacios[nodo].calcular_ruido(self.edificio.materiales, self.edificio.ruidos, aristas)
                    if ruido_total <= self.edificio.umbrales_habitabilidad.get(nodo, float('inf')):
                        print(f"Recomendación de ajuste: Cambiar el material de {material_actual} a {material_id} en el nodo {nodo}")
                        materiales_por_nodo[nodo] = material_id  # Actualizar material del nodo
                        material_cambiado = True
                        break

            # Si los materiales adicionales no funcionan, probar otros materiales
            if not material_cambiado:
                for material_id, material in self.edificio.materiales.items():
                    if material_id != material_actual:  # Evitar cambiar por el mismo material
                        ruido_total = self.edificio.espacios[nodo].calcular_ruido(self.edificio.materiales, self.edificio.ruidos, aristas)
                        if ruido_total <= self.edificio.umbrales_habitabilidad.get(nodo, float('inf')):
                            print(f"Recomendación de ajuste: Cambiar el material de {material_actual} a {material_id} en el nodo {nodo}")
                            materiales_por_nodo[nodo] = material_id  # Actualizar material del nodo
                            break
                else:
                    # Si ningún material resuelve el problema, pasar a intercambiar actividades
                    actividades_no_habitables = [self.edificio.actividades[nodo] for nodo in nodos_no_habitables]
                    actividades_permutadas = actividades_no_habitables[:]
                    random.shuffle(actividades_permutadas)

                    # Asignar las actividades permutadas a los nodos no habitables
                    for nodo, actividad in zip(nodos_no_habitables, actividades_permutadas):
                        ruido_total = self.edificio.espacios[nodo].calcular_ruido(self.edificio.materiales, self.edificio.ruidos, aristas)
                        umbral_ajustado = max(ruido_total, 40) + 5  # Margen de 5 dB
                        self.edificio.agregar_actividad(nodo, actividad, umbral_ajustado)

        # Recalcular habitabilidad
        self.edificio.ajustar_habitabilidad(aristas)

        # Actualizar el grafo
        self.refrescar_grafo()




    def restablecer_grafo(self):
        """Restaura las actividades y umbrales originales."""
        self.edificio.actividades = self.actividades_originales.copy()
        self.edificio.umbrales_habitabilidad = self.umbrales_originales.copy()
        self.refrescar_grafo()

    def generar_grafo_coloreado(self):
        """Genera el grafo con coloreado gradual basado en el ruido."""
        aristas = {
            ('H2', 'H3'): 'Ladrillo',
            ('H1', 'S'): 'Loseta',
            ('H1', 'H5'): 'Ladrillo',
            ('S', 'H4'): 'Ladrillo',
            ('S', 'E'): 'Ladrillo',
            ('H4', 'E'): 'Loseta',
            ('H5', 'E'): 'Loseta',
            ('H3', 'E'): 'Loseta',
        }

        # Calcular habitabilidad
        print("\nResumen de ruido por espacio:")
        self.edificio.calcular_habitabilidad_espacios(aristas)

        # Generar el grafo con gradiente de colores
        imprimir_grafo_coloreado(self.edificio, aristas)

    def generar_grafo_coloreado_vecinos(self):
        """Genera el grafo con nodos coloreados sin que vecinos compartan color."""
        aristas = {
            ('H2', 'H3'): 'Ladrillo',
            ('H1', 'S'): 'Loseta',
            ('H1', 'H5'): 'Ladrillo',
            ('S', 'H4'): 'Ladrillo',
            ('S', 'E'): 'Ladrillo',
            ('H4', 'E'): 'Loseta',
            ('H5', 'E'): 'Loseta',
            ('H3', 'E'): 'Loseta',
        }

        # Generar el grafo con coloración restringida
        imprimir_grafo_coloreado_vecinos(self.edificio, aristas)


    def actualizar_ruidos_y_generar_grafo(self):
        """Actualiza los valores de ruido, recalcula la habitabilidad y genera el grafo."""
        try:
            # Leer valores modificados
            for nombre, inten_entry in self.ruido_entries.items():
                nueva_intensidad = int(inten_entry.get())

                self.ruidos[nombre]["intensidad"] = nueva_intensidad

            self.edificio.ruidos.clear()
            for nombre, datos in self.ruidos.items():
                self.edificio.agregar_ruido(Ruido(nombre, datos["frecuencia"], datos["intensidad"]))

            aristas = {
                ('H2', 'H3'): 'Ladrillo',
                ('H1', 'S'): 'Loseta',
                ('H1', 'H5'): 'Ladrillo',
                ('S', 'H4'): 'Ladrillo',
                ('S', 'E'): 'Ladrillo',
                ('H4', 'E'): 'Loseta',
                ('H5', 'E'): 'Loseta',
                ('H3', 'E'): 'Loseta',
            }

            print("\nResumen de ruido por espacio:")
            self.edificio.calcular_habitabilidad_espacios(aristas)
            imprimir_grafo(self.edificio, aristas)

        except ValueError:
            messagebox.showerror("Error", "Ingrese valores numéricos válidos.")

    def refrescar_grafo(self):
        """Refresca el grafo basado en el estado actual del edificio."""
        aristas = {
            ('H2', 'H3'): 'Ladrillo',
            ('H1', 'S'): 'Loseta',
            ('H1', 'H5'): 'Ladrillo',
            ('S', 'H4'): 'Ladrillo',
            ('S', 'E'): 'Ladrillo',
            ('H4', 'E'): 'Loseta',
            ('H5', 'E'): 'Loseta',
            ('H3', 'E'): 'Loseta',
        }
        imprimir_grafo(self.edificio, aristas)
