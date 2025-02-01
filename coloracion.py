import matplotlib.cm as cm
import matplotlib.colors as mcolors

def obtener_color_gradual(ruido, umbral):
    """
    Devuelve un color basado en el nivel de ruido relativo al umbral.
    Verde -> Habitabilidad alta, Amarillo -> Límite, Rojo -> Ruido excesivo.
    
    :param ruido: Nivel de ruido en el espacio.
    :param umbral: Umbral de ruido permitido para el espacio.
    :return: Color en formato hexadecimal.
    """
    ratio = min(ruido / umbral, 1)  # Normalizamos (máximo 1)
    return mcolors.to_hex(cm.RdYlGn(1 - ratio))  # `RdYlGn` -> Rojo - Amarillo - Verde
