import random
import pygame
from game import settings as s


class Bus(pygame.sprite.Sprite):
    """Bus articulado de TransMilenio que cruza por un carril."""

    def __init__(self, carril_y, velocidad):
        super().__init__()
        ancho, alto = 140, 46
        self.image = pygame.Surface((ancho, alto), pygame.SRCALPHA)
        pygame.draw.rect(self.image, s.ROJO_TRANSMILENIO, (0, 6, ancho, alto - 12), border_radius=6)
        pygame.draw.rect(self.image, s.AMARILLO, (0, 6, ancho, 6))
        # ventanas
        for i in range(6):
            pygame.draw.rect(self.image, (200, 230, 240), (10 + i * 21, 14, 14, 12))
        # ruedas
        pygame.draw.circle(self.image, s.NEGRO, (25, alto - 8), 7)
        pygame.draw.circle(self.image, s.NEGRO, (ancho - 25, alto - 8), 7)

        self.rect = self.image.get_rect(midbottom=(s.ANCHO + 150, carril_y))
        self.velocidad = velocidad

    def actualizar(self):
        self.rect.x -= self.velocidad
        if self.rect.right < -20:
            self.kill()


class Policia(pygame.sprite.Sprite):
    """Policía que persigue al jugador en el modo estación."""

    def __init__(self, carril_y, velocidad):
        super().__init__()
        ancho, alto = 30, 50
        self.image = pygame.Surface((ancho, alto), pygame.SRCALPHA)
        pygame.draw.rect(self.image, s.AZUL_POLICIA, (4, 16, ancho - 8, 26))
        pygame.draw.rect(self.image, (230, 190, 150), (8, 3, 14, 13))
        pygame.draw.rect(self.image, s.NEGRO, (6, 1, 18, 5))  # gorra policia
        pygame.draw.rect(self.image, (30, 30, 30), (5, 40, 8, 10))
        pygame.draw.rect(self.image, (30, 30, 30), (17, 40, 8, 10))

        self.rect = self.image.get_rect(midbottom=(-40, carril_y))
        self.velocidad = velocidad

    def actualizar(self):
        self.rect.x += self.velocidad
        if self.rect.left > s.ANCHO + 20:
            self.kill()


class Torniquete(pygame.sprite.Sprite):
    """Obstáculo estático que se debe saltar al inicio del modo estación."""

    def __init__(self, x, carril_y):
        super().__init__()
        ancho, alto = 26, 40
        self.image = pygame.Surface((ancho, alto), pygame.SRCALPHA)
        pygame.draw.rect(self.image, s.GRIS_CLARO, (0, 10, ancho, alto - 10))
        pygame.draw.rect(self.image, s.AMARILLO, (8, 0, 10, 14))
        self.rect = self.image.get_rect(midbottom=(x, carril_y))


def generar_carriles_y(alto_area_juego, y_inicial, num_carriles):
    """Calcula las posiciones Y (suelo) de cada carril, distribuidas en el área de juego."""
    paso = alto_area_juego // (num_carriles + 1)
    return [y_inicial + paso * (i + 1) for i in range(num_carriles)]
