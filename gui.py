import random
import tkinter as tk
from tkinter import messagebox
from edificio import Edificio
from ruido import Ruido
from espacio import Espacio
from material import Material
from grafo import imprimir_grafo


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
        """Genera la interfaz gráfica con campos para modificar ruidos y ajustar actividades."""
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
        tk.Button(self.root, text="Generar Grafo", command=self.actualizar_ruidos_y_generar_grafo, font=("Arial", 12)).pack(pady=10)

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
        """Ajusta las actividades y umbrales para que todos los espacios sean habitables."""
        # Obtener las actividades únicas disponibles
        actividades = list(set(self.edificio.actividades.values()))
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

        # Asignar actividades al azar y ajustar umbrales
        for espacio_id in self.edificio.espacios:
            actividad_aleatoria = random.choice(actividades)
            ruido_total = self.edificio.espacios[espacio_id].calcular_ruido(self.edificio.materiales, self.edificio.ruidos, aristas)
            umbral_ajustado = max(ruido_total, 40) + 5  # Margen de 5 dB
            self.edificio.agregar_actividad(espacio_id, actividad_aleatoria, umbral_ajustado)

        # Recalcular habitabilidad
        self.edificio.ajustar_habitabilidad(aristas)

        # Actualizar el grafo
        self.refrescar_grafo()

    def restablecer_grafo(self):
        """Restaura las actividades y umbrales originales."""
        self.edificio.actividades = self.actividades_originales.copy()
        self.edificio.umbrales_habitabilidad = self.umbrales_originales.copy()
        self.refrescar_grafo()

    def actualizar_ruidos_y_generar_grafo(self):
        """Actualiza los valores de ruido, recalcula la habitabilidad y genera el grafo."""
        try:
            for nombre, (freq_entry, inten_entry) in self.ruido_entries.items():
                nueva_frecuencia = int(freq_entry.get())
                nueva_intensidad = int(inten_entry.get())
                self.ruidos[nombre]["frecuencia"] = nueva_frecuencia
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


if __name__ == "__main__":
    root = tk.Tk()
    app = Aplicacion(root)
    root.mainloop()
