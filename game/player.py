import os
import pygame

from game import settings as s


class Jugador(pygame.sprite.Sprite):

    def __init__(self, x, suelo_y):

        super().__init__()

        # ========================================================
        # POSICIÓN
        # ========================================================

        self.suelo_y = suelo_y

        # 0 = izquierda, 1 = centro, 2 = derecha
        self.carril = 1

        self.target_y = suelo_y

        # Movimiento suave entre carriles
        self.velocidad_carril = 18

        # ========================================================
        # SALTO
        # ========================================================

        self.saltando = False
        self.vel_y = 0

        self.fuerza_salto = -17
        self.gravedad = 0.85

        # ========================================================
        # ANIMACIÓN
        # ========================================================

        self.estado_animacion = "corriendo_lateral"

        self.frame_animacion = 0
        self.timer_animacion = 0

        # Menor número = animación más rápida
        self.velocidad_animacion = 6

        # ========================================================
        # INVULNERABILIDAD
        # ========================================================

        self.invulnerable = False
        self.invulnerable_timer = 0

        # ========================================================
        # CARGAR SPRITES
        # ========================================================

        base_dir = os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        )

        carpeta_player = os.path.join(
            base_dir,
            "assets",
            "player"
        )

        # --------------------------------------------------------
        # CARRERA LATERAL
        # --------------------------------------------------------

        self.frames_lateral = []

        for i in range(1, 5):

            ruta = os.path.join(
                carpeta_player,
                f"run_{i:02d}.png"
            )

            if os.path.isfile(ruta):

                imagen = pygame.image.load(
                    ruta
                ).convert_alpha()

                imagen = self._escalar_sprite(
                    imagen,
                    0.65
                )

                self.frames_lateral.append(
                    imagen
                )

        # --------------------------------------------------------
        # CARRERA DE ESPALDA
        # --------------------------------------------------------

        self.frames_espalda = []

        for i in range(1, 4):

            ruta = os.path.join(
                carpeta_player,
                f"back_run_{i:02d}.png"
            )

            if os.path.isfile(ruta):

                imagen = pygame.image.load(
                    ruta
                ).convert_alpha()

                imagen = self._escalar_sprite(
                    imagen,
                    0.42
                )

                self.frames_espalda.append(
                    imagen
                )

        # ========================================================
        # SPRITE INICIAL
        # ========================================================

        if self.frames_lateral:
            self.image = self.frames_lateral[0]

        elif self.frames_espalda:
            self.image = self.frames_espalda[0]

        else:
            # Fallback para detectar fácilmente si faltan sprites.
            self.image = pygame.Surface(
                (60, 90),
                pygame.SRCALPHA
            )

            pygame.draw.rect(
                self.image,
                (30, 100, 200),
                (15, 15, 30, 50)
            )

        self.rect = self.image.get_rect()

        self.rect.centerx = x
        self.rect.bottom = suelo_y

        # X inicial; durante la partida la cámara mantiene
        # al personaje abajo y centrado.
        self.x_fijo = x

    # ============================================================
    # ESCALAR SPRITE
    # ============================================================

    def _escalar_sprite(self, imagen, factor):

        ancho = max(
            1,
            int(imagen.get_width() * factor)
        )

        alto = max(
            1,
            int(imagen.get_height() * factor)
        )

        return pygame.transform.smoothscale(
            imagen,
            (ancho, alto)
        )

    # ============================================================
    # CAMBIAR CARRIL
    # ============================================================

    def mover_carril(self, direccion, carriles_y):

        nuevo_carril = self.carril + direccion

        if nuevo_carril < 0:
            return

        if nuevo_carril >= len(carriles_y):
            return

        self.carril = nuevo_carril

        self.target_y = carriles_y[
            nuevo_carril
        ]

    # ============================================================
    # SALTAR
    # ============================================================

    def saltar(self):

        if self.saltando:
            return

        self.saltando = True
        self.vel_y = self.fuerza_salto

    # ============================================================
    # ACTUALIZAR
    # ============================================================

    def actualizar(self):

        # --------------------------------------------------------
        # MOVIMIENTO SUAVE ENTRE CARRILES
        # --------------------------------------------------------

        diferencia = (
            self.target_y -
            self.rect.bottom
        )

        if abs(diferencia) > 2:

            paso = min(
                self.velocidad_carril,
                abs(diferencia)
            )

            if diferencia > 0:
                self.rect.bottom += paso
            else:
                self.rect.bottom -= paso

        else:
            self.rect.bottom = self.target_y

        # --------------------------------------------------------
        # SALTO
        # --------------------------------------------------------

        if self.saltando:

            self.rect.y += self.vel_y
            self.vel_y += self.gravedad

            if self.rect.bottom >= self.suelo_y:

                self.rect.bottom = self.suelo_y
                self.vel_y = 0
                self.saltando = False

        else:

            self.suelo_y = self.target_y

        # --------------------------------------------------------
        # ANIMACIÓN
        # --------------------------------------------------------

        self.timer_animacion += 1

        if self.timer_animacion >= self.velocidad_animacion:

            self.timer_animacion = 0
            self.frame_animacion += 1

        # --------------------------------------------------------
        # INVULNERABILIDAD
        # --------------------------------------------------------

        if self.invulnerable:

            self.invulnerable_timer -= 1

            if self.invulnerable_timer <= 0:
                self.invulnerable = False

    # ============================================================
    # INVULNERABILIDAD
    # ============================================================

    def hacer_invulnerable(self, duracion=90):

        self.invulnerable = True
        self.invulnerable_timer = duracion

    # ============================================================
    # OBTENER FRAME
    # ============================================================

    def _obtener_frame(self):

        if self.estado_animacion == "corriendo_lateral":

            frames = self.frames_lateral

        elif self.estado_animacion == "corriendo_espalda":

            frames = self.frames_espalda

        else:

            # Si llega otro estado, usamos la animación
            # de espalda durante la partida.
            frames = self.frames_espalda

        if not frames:

            return self.image

        indice = (
            self.frame_animacion
            % len(frames)
        )

        return frames[indice]

    # ============================================================
    # DIBUJAR
    # ============================================================

    def dibujar(self, pantalla):

        # Parpadeo mientras es invulnerable.
        if self.invulnerable:

            if (
                (self.invulnerable_timer // 5)
                % 2
                == 0
            ):
                return

        frame = self._obtener_frame()

        # Conservamos la posición de los pies.
        posicion_pies = self.rect.midbottom

        self.image = frame

        self.rect = self.image.get_rect(
            midbottom=posicion_pies
        )

        pantalla.blit(
            self.image,
            self.rect
        )
        