"""
Configuración global de 'Tombo Tu Llave'.
Aquí se centralizan colores, tamaños y constantes para
poder ajustar el juego fácilmente sin buscar en todo el código.
"""

# --- Ventana ---
ANCHO = 900
ALTO = 500
FPS = 60
TITULO = "TOMBO TU LLAVE"

# --- Colores (estilo retro / paleta pixel-art) ---
NEGRO = (10, 10, 10)
BLANCO = (245, 245, 245)
GRIS_OSCURO = (40, 40, 45)
GRIS_CLARO = (150, 150, 155)
ROJO_TRANSMILENIO = (200, 30, 30)
AMARILLO = (255, 200, 30)
NARANJA = (255, 140, 0)
VERDE = (60, 180, 90)
AZUL_POLICIA = (40, 60, 160)
CAFE_JUGADOR = (90, 60, 40)
VERDE_JUGADOR = (60, 90, 60)
CIELO = (135, 190, 220)

# --- Jugador ---
JUGADOR_ANCHO = 34
JUGADOR_ALTO = 54
JUGADOR_VEL = 5
JUGADOR_VEL_SALTO = -11
GRAVEDAD = 0.6

# --- Carriles (para movimiento vertical tipo "lanes") ---
NUM_CARRILES = 4

# --- Dificultad progresiva ---
VELOCIDAD_INICIAL = 5
VELOCIDAD_MAX = 12
INCREMENTO_VELOCIDAD = 0.0015  # por frame

# --- Meta ---
DISTANCIA_META = 3000  # "metros" ficticios que hay que recorrer para ganar
