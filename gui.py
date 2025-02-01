import tkinter as tk
from tkinter import messagebox
from edificio import Edificio
from ruido import Ruido
from espacio import Espacio
from material import Material
from grafo import imprimir_grafo

class Aplicacion:
    """
    Interfaz gráfica para modificar los valores de ruido y generar el grafo en tiempo real.
    """

    def __init__(self, root):
        self.root = root
        self.root.title("Simulación de Habitabilidad - Configuración de Ruidos")

        # Crear el edificio
        self.edificio = self.inicializar_edificio()

        # Crear interfaz gráfica
        self.crear_interfaz()

    def inicializar_edificio(self):
        """Inicializa el edificio con espacios, materiales y ruidos predefinidos."""
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

        # Ruidos iniciales
        self.ruidos = {
            "Avión": {"frecuencia": 2000, "intensidad": 90},
            "Vía": {"frecuencia": 500, "intensidad": 70},
            "Gimnasio": {"frecuencia": 500, "intensidad": 65}
        }
        self.ruido_entries = {}

        for nombre, datos in self.ruidos.items():
            edificio.agregar_ruido(Ruido(nombre, datos["frecuencia"], datos["intensidad"]))

        # Umbrales de habitabilidad
        edificio.agregar_umbral("H1", 70)
        edificio.agregar_umbral("H2", 40)
        edificio.agregar_umbral("H3", 40)
        edificio.agregar_umbral("H4", 65)
        edificio.agregar_umbral("H5", 50)
        edificio.agregar_umbral("S", 35)
        edificio.agregar_umbral("E", 50)

        return edificio

    def crear_interfaz(self):
        """Genera la interfaz gráfica con campos para modificar ruidos."""
        tk.Label(self.root, text="Modifique los valores de ruido y genere el grafo", font=("Arial", 12, "bold")).pack(pady=10)

        frame_ruidos = tk.Frame(self.root)
        frame_ruidos.pack()

        # Crear campos de entrada para los ruidos
        for i, (nombre, datos) in enumerate(self.ruidos.items()):
            tk.Label(frame_ruidos, text=f"{nombre}:").grid(row=i, column=0, padx=10, pady=5)

            freq_entry = tk.Entry(frame_ruidos, width=10)
            freq_entry.insert(0, str(datos["frecuencia"]))
            freq_entry.grid(row=i, column=1)

            inten_entry = tk.Entry(frame_ruidos, width=10)
            inten_entry.insert(0, str(datos["intensidad"]))
            inten_entry.grid(row=i, column=2)

            self.ruido_entries[nombre] = (freq_entry, inten_entry)

        # Botón para aplicar cambios y generar grafo
        tk.Button(self.root, text="Generar Grafo", command=self.actualizar_ruidos_y_generar_grafo, font=("Arial", 12)).pack(pady=20)

    def actualizar_ruidos_y_generar_grafo(self):
        """Actualiza los valores de ruido y genera el grafo."""
        try:
            # Leer valores modificados
            for nombre, (freq_entry, inten_entry) in self.ruido_entries.items():
                nueva_frecuencia = int(freq_entry.get())
                nueva_intensidad = int(inten_entry.get())

                self.ruidos[nombre]["frecuencia"] = nueva_frecuencia
                self.ruidos[nombre]["intensidad"] = nueva_intensidad

            # Actualizar ruidos en el edificio
            self.edificio.ruidos.clear()
            for nombre, datos in self.ruidos.items():
                self.edificio.agregar_ruido(Ruido(nombre, datos["frecuencia"], datos["intensidad"]))

            # Aristas del edificio
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

            # Generar el grafo
            imprimir_grafo(self.edificio, aristas)

        except ValueError:
            messagebox.showerror("Error", "Ingrese valores numéricos válidos.")

