import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from material import Material
from ruido import Ruido
from espacio import Espacio
from edificio import Edificio
from grafo import imprimir_grafo 

def main():
    # --- Inicialización de datos ---
    edificio = Edificio("Mi Edificio")

    # Materiales con sus coeficientes de absorción
    edificio.agregar_material(Material("Ladrillo", 0.02, 0.04))
    edificio.agregar_material(Material("Loseta", 0.06, 0.04))
    edificio.agregar_material(Material("Espuma", 0.55, 0.65))

    # Espacios y sus coordenadas
    edificio.agregar_espacio(Espacio("H1", 4, 2, 0))
    edificio.agregar_espacio(Espacio("H2", 4, 4, 0))
    edificio.agregar_espacio(Espacio("S", 3, 3, 0))
    edificio.agregar_espacio(Espacio("H3", 4, 4, 4))
    edificio.agregar_espacio(Espacio("H4", 3, 2, 4))
    edificio.agregar_espacio(Espacio("H5", 4, 2, 4))
    edificio.agregar_espacio(Espacio("E", 3, 3, 4))

    # Ruidos presentes en el entorno
    edificio.agregar_ruido(Ruido("Avión", 2000, 90))
    edificio.agregar_ruido(Ruido("Vía", 500, 70))
    edificio.agregar_ruido(Ruido("Gimnasio", 500, 65))

    # Umbrales de habitabilidad
    edificio.agregar_umbral("H1", 70)
    edificio.agregar_umbral("H2", 40)
    edificio.agregar_umbral("H3", 40)
    edificio.agregar_umbral("H4", 65)
    edificio.agregar_umbral("H5", 50)
    edificio.agregar_umbral("S", 35)
    edificio.agregar_umbral("E", 50)

    # Definición de conexiones entre espacios y los materiales usados en las paredes
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

    # --- Ejecución ---
    imprimir_grafo(edificio, aristas)  # Se grafica
    edificio.calcular_habitabilidad_espacios(aristas)

    # Mostrar los niveles de ruido por consola
    print("\nResumen de ruido por espacio:")
    for espacio in edificio.espacios.values():
        ruido_total = espacio.calcular_ruido(edificio.materiales, edificio.ruidos, aristas)
        umbral = edificio.umbrales_habitabilidad.get(espacio.id_espacio, float('inf'))
        print(f"Espacio {espacio.id_espacio}: Ruido = {ruido_total:.2f}, Umbral = {umbral}, Habitable: {'Sí' if ruido_total <= umbral else 'No'}")

if __name__ == "__main__":
    main()
