"""
TOMBO TU LLAVE
Juego endless-runner ambientado en una estación de TransMilenio.

FASE 2:
- Intro animada.
- Personaje corre de izquierda a derecha.
- El personaje salta el torniquete.
- Continúa corriendo hacia la estación.
- Después comienza la partida.

Controles durante el juego:
    ← / →       Cambiar de carril
    ESPACIO     Saltar
"""

import asyncio
import random
import sys
import os

import pygame

from game import settings as s
from game.player import Jugador
from game.obstaculos import (
    Bus,
    Policia,
    Torniquete,
    generar_carriles_y,
)


# ============================================================
# ESTADOS DEL JUEGO
# ============================================================

MENU = "menu"
INTRO = "intro"
JUGANDO = "jugando"
GAME_OVER = "game_over"
VICTORIA = "victoria"


class Juego:

    def __init__(self):

        pygame.init()

        pygame.display.set_caption(
            s.TITULO
        )

        self.pantalla = pygame.display.set_mode(
            (s.ANCHO, s.ALTO)
        )

        self.reloj = pygame.time.Clock()

        # ----------------------------------------------------
        # PORTADA
        # ----------------------------------------------------

        # La portada está dentro de la carpeta del proyecto:
        # tombo_tu_llave/assets/ui/portada.png
        base_dir = os.path.dirname(os.path.abspath(__file__))
        ruta_portada = os.path.join(
            base_dir,
            "assets",
            "ui",
            "portada.png"
        )

        print("Buscando portada en:")
        print(ruta_portada)

        if not os.path.isfile(ruta_portada):
            archivos_ui = []
            carpeta_ui = os.path.join(base_dir, "assets", "ui")
            if os.path.isdir(carpeta_ui):
                archivos_ui = os.listdir(carpeta_ui)

            raise FileNotFoundError(
                "No se encontró la portada.\n"
                f"Ruta buscada: {ruta_portada}\n"
                f"Archivos encontrados en assets/ui: {archivos_ui}"
            )

        self.portada = pygame.image.load(ruta_portada).convert()
        self.portada = pygame.transform.smoothscale(
            self.portada,
            (s.ANCHO, s.ALTO)
        )
        # ----------------------------------------------------
        # FUENTES
        # ----------------------------------------------------

        self.fuente_grande = pygame.font.SysFont(
            "consolas",
            48,
            bold=True
        )

        self.fuente_media = pygame.font.SysFont(
            "consolas",
            26,
            bold=True
        )

        self.fuente_chica = pygame.font.SysFont(
            "consolas",
            18
        )

        # ----------------------------------------------------
        # ESTADO
        # ----------------------------------------------------

        self.estado = MENU

        self.reiniciar_partida()


    # ========================================================
    # PREPARAR PARTIDA
    # ========================================================

    def reiniciar_partida(self):

        # ----------------------------------------------------
        # CARRILES
        # ----------------------------------------------------

        area_top = 110

        area_bottom = s.ALTO - 40

        self.carriles_y = generar_carriles_y(
            area_bottom - area_top,
            area_top,
            s.NUM_CARRILES
        )

        # El personaje empieza en el segundo carril.
        carril_inicial = self.carriles_y[1]

        self.jugador = Jugador(
            120,
            carril_inicial
        )

        # ----------------------------------------------------
        # OBSTÁCULOS
        # ----------------------------------------------------

        self.obstaculos = pygame.sprite.Group()

        # ----------------------------------------------------
        # PARTIDA
        # ----------------------------------------------------

        self.vidas = 3

        self.distancia = 0

        self.velocidad = (
            s.VELOCIDAD_INICIAL
        )

        self.timer_spawn = 0

        # ----------------------------------------------------
        # TORNIQUETE
        # ----------------------------------------------------

        self.torniquete = Torniquete(
            330,
            carril_inicial
        )

        self.torniquete_saltado = False

        # ----------------------------------------------------
        # VARIABLES DE INTRO
        # ----------------------------------------------------

        self.intro_timer = 0

        self.intro_fase = "entrada"

        # Posición inicial del personaje durante la intro
        self.intro_x = 120

        # Velocidad del personaje durante la intro
        self.intro_velocidad = 3.5

        # Cuando termina la intro, empieza el juego.
        self.intro_duracion_maxima = (
            s.FPS * 7
        )

        # ----------------------------------------------------
        # ELEMENTOS VISUALES DE LA ESTACIÓN
        # ----------------------------------------------------

        self.offset_fondo = 0

        self.lineas_fondo = []

        self.crear_elementos_fondo()


    # ========================================================
    # ELEMENTOS DECORATIVOS
    # ========================================================

    def crear_elementos_fondo(self):

        self.lineas_fondo.clear()

        # Columnas de la estación
        for x in range(
            40,
            s.ANCHO,
            180
        ):

            self.lineas_fondo.append(
                {
                    "x": x,
                    "alto": random.randint(
                        160,
                        260
                    )
                }
            )


    # ========================================================
    # LOOP PRINCIPAL
    # ========================================================

    async def correr(self):

        corriendo = True

        while corriendo:

            # ------------------------------------------------
            # EVENTOS
            # ------------------------------------------------

            for evento in pygame.event.get():

                if evento.type == pygame.QUIT:

                    corriendo = False

                elif evento.type == pygame.KEYDOWN:

                    self.manejar_tecla(
                        evento.key
                    )

            # ------------------------------------------------
            # ACTUALIZAR
            # ------------------------------------------------

            self.actualizar()

            # ------------------------------------------------
            # DIBUJAR
            # ------------------------------------------------

            self.dibujar()

            pygame.display.flip()

            self.reloj.tick(
                s.FPS
            )

            # Necesario para pygbag
            await asyncio.sleep(0)

        pygame.quit()

        sys.exit()


    # ========================================================
    # TECLADO
    # ========================================================

    def manejar_tecla(self, key):

        # ----------------------------------------------------
        # MENÚ
        # ----------------------------------------------------

        if self.estado == MENU:

            if key == pygame.K_RETURN:

                self.reiniciar_partida()

                self.estado = INTRO


        # ----------------------------------------------------
        # INTRO
        # ----------------------------------------------------

        elif self.estado == INTRO:

            # ENTER permite saltar la intro.
            if key == pygame.K_RETURN:

                self.terminar_intro()


        # ----------------------------------------------------
        # JUEGO
        # ----------------------------------------------------

        elif self.estado == JUGANDO:

            if key == pygame.K_LEFT:

                self.jugador.mover_carril(
                    -1,
                    self.carriles_y
                )

            elif key == pygame.K_RIGHT:

                self.jugador.mover_carril(
                    1,
                    self.carriles_y
                )

            elif key == pygame.K_SPACE:

                self.jugador.saltar()

        # ----------------------------------------------------
        # FIN DE PARTIDA
        # ----------------------------------------------------

        elif self.estado in (
            GAME_OVER,
            VICTORIA
        ):

            if key == pygame.K_RETURN:

                self.reiniciar_partida()

                self.estado = INTRO


    # ========================================================
    # ACTUALIZACIÓN GENERAL
    # ========================================================

    def actualizar(self):

        # ----------------------------------------------------
        # INTRO
        # ----------------------------------------------------

        if self.estado == INTRO:

            self.actualizar_intro()

            return


        # ----------------------------------------------------
        # SOLO JUGANDO
        # ----------------------------------------------------

        if self.estado != JUGANDO:

            return


        # ----------------------------------------------------
        # JUGADOR
        # ----------------------------------------------------

        self.jugador.actualizar()


        # ----------------------------------------------------
        # DIFICULTAD
        # ----------------------------------------------------

        if self.velocidad < s.VELOCIDAD_MAX:

            self.velocidad += (
                s.INCREMENTO_VELOCIDAD
            )


        # ----------------------------------------------------
        # DISTANCIA
        # ----------------------------------------------------

        self.distancia += (
            self.velocidad * 0.1
        )


        # ----------------------------------------------------
        # TORNIQUETE
        # ----------------------------------------------------

        if (
            self.torniquete
            and
            not self.torniquete_saltado
        ):

            if self.jugador.rect.colliderect(
                self.torniquete.rect
            ):

                if self.jugador.saltando:

                    self.torniquete_saltado = True

                    self.torniquete.kill()

                    self.torniquete = None

                else:

                    self.jugador.rect.right = (
                        self.torniquete.rect.left
                    )


        # ----------------------------------------------------
        # OBSTÁCULOS
        # ----------------------------------------------------

        self.spawnear_obstaculos()

        self.obstaculos.update()

        self.chequear_colisiones()


        # ----------------------------------------------------
        # META
        # ----------------------------------------------------

        if (
            self.distancia
            >= s.DISTANCIA_META
        ):

            self.estado = VICTORIA


    # ========================================================
    # INTRO ANIMADA
    # ========================================================

    def actualizar_intro(self):

        self.intro_timer += 1


        # ====================================================
        # FASE 1
        # EL PERSONAJE ENTRA CORRIENDO
        # ====================================================

        if self.intro_fase == "entrada":

            self.intro_x += (
                self.intro_velocidad
            )

            self.jugador.rect.centerx = (
                int(self.intro_x)
            )

            # Animación lateral durante la intro.
            self.jugador.estado_animacion = (
                "corriendo_lateral"
            )

            # Cuando se acerca al torniquete
            if self.intro_x >= 225:

                self.intro_fase = "pre_salto"

                self.jugador.saltar()


        # ====================================================
        # FASE 2
        # SALTO DEL TORNIQUETE
        # ====================================================

        elif self.intro_fase == "pre_salto":

            # Continuamos avanzando horizontalmente.
            self.intro_x += (
                self.intro_velocidad
            )

            self.jugador.rect.centerx = (
                int(self.intro_x)
            )

            # Física del salto
            self.jugador.actualizar()

            # Cuando ya pasó el torniquete
            if (
                self.intro_x
                > self.torniquete.rect.centerx + 70
            ):

                if not self.torniquete_saltado:

                    self.torniquete_saltado = True

                    self.torniquete.kill()

                    self.torniquete = None

                self.intro_fase = "salida"


        # ====================================================
        # FASE 3
        # CONTINÚA CORRIENDO
        # ====================================================

        elif self.intro_fase == "salida":

            self.intro_x += (
                self.intro_velocidad + 1
            )

            self.jugador.rect.centerx = (
                int(self.intro_x)
            )

            self.jugador.actualizar()

            # Cuando sale de la zona derecha
            if self.intro_x >= 570:

                self.terminar_intro()


        # ----------------------------------------------------
        # Movimiento visual del fondo
        # ----------------------------------------------------

        self.offset_fondo += 1

        if (
            self.intro_timer
            >= self.intro_duracion_maxima
        ):

            self.terminar_intro()


    # ========================================================
    # TERMINAR INTRO
    # ========================================================

    def terminar_intro(self):

        self.torniquete_saltado = True

        if self.torniquete:

            self.torniquete.kill()

            self.torniquete = None

        # El personaje empieza abajo, centrado en la pantalla.
        self.jugador.rect.centerx = (
            s.ANCHO // 2
        )

        self.jugador.rect.bottom = (
            self.carriles_y[1]
        )

        self.jugador.suelo_y = (
            self.carriles_y[1]
        )

        self.jugador.saltando = False

        self.jugador.vel_y = 0

        # Durante la partida vemos al personaje desde atrás.
        self.jugador.estado_animacion = (
            "corriendo_espalda"
        )

        self.estado = JUGANDO


    # ========================================================
    # GENERAR OBSTÁCULOS
    # ========================================================

    def spawnear_obstaculos(self):

        self.timer_spawn -= 1

        if self.timer_spawn > 0:

            return


        carril_y = random.choice(
            self.carriles_y
        )


        # Por ahora mantenemos los obstáculos
        # existentes.
        #
        # Más adelante:
        #
        # ESTACIÓN -> POLICÍAS
        # CALLE    -> TRANSMILENIOS

        if self.torniquete_saltado:

            self.obstaculos.add(
                Policia(
                    carril_y,
                    self.velocidad
                    + random.uniform(1, 3)
                )
            )


        self.timer_spawn = random.randint(
            50,
            90
        )


    # ========================================================
    # COLISIONES
    # ========================================================

    def chequear_colisiones(self):

        if self.jugador.invulnerable:

            return


        for obstaculo in self.obstaculos:

            if self.jugador.rect.colliderect(
                obstaculo.rect
            ):

                obstaculo.kill()

                self.vidas -= 1

                self.jugador.hacer_invulnerable()


                if self.vidas <= 0:

                    self.estado = GAME_OVER

                break


    # ========================================================
    # DIBUJADO
    # ========================================================

    def dibujar(self):

        if self.estado == MENU:

            self.dibujar_menu()


        elif self.estado == INTRO:

            self.dibujar_intro()


        elif self.estado == JUGANDO:

            self.dibujar_juego()


        elif self.estado == GAME_OVER:

            self.dibujar_fin(
                "¡TE COGIERON!",
                s.ROJO_TRANSMILENIO,
                "Presiona ENTER para reintentar"
            )


        elif self.estado == VICTORIA:

            self.dibujar_fin(
                "¡COGISTE EL TRANSMILENIO!",
                s.VERDE,
                "Presiona ENTER para jugar de nuevo"
            )


    # ========================================================
    # FONDO GENERAL
    # ========================================================

    def dibujar_fondo(self):

        # Fondo
        self.pantalla.fill(
            (210, 220, 225)
        )

        # Techo
        pygame.draw.rect(
            self.pantalla,
            (45, 48, 55),
            (
                0,
                0,
                s.ANCHO,
                75
            )
        )

        # Franja superior de estación
        pygame.draw.rect(
            self.pantalla,
            s.ROJO_TRANSMILENIO,
            (
                0,
                75,
                s.ANCHO,
                12
            )
        )

        # Piso
        pygame.draw.rect(
            self.pantalla,
            (105, 108, 112),
            (
                0,
                390,
                s.ANCHO,
                110
            )
        )

        # Línea amarilla del andén
        pygame.draw.rect(
            self.pantalla,
            s.AMARILLO,
            (
                0,
                380,
                s.ANCHO,
                8
            )
        )


    # ========================================================
    # FONDO DE ESTACIÓN
    # ========================================================

    def dibujar_estacion(self):

        self.dibujar_fondo()


        # ----------------------------------------------------
        # Columnas
        # ----------------------------------------------------

        for elemento in self.lineas_fondo:

            x = elemento["x"]

            alto = elemento["alto"]

            pygame.draw.rect(
                self.pantalla,
                (80, 84, 90),
                (
                    x,
                    90,
                    35,
                    alto
                )
            )


        # ----------------------------------------------------
        # Ventanales
        # ----------------------------------------------------

        for x in range(
            90,
            s.ANCHO,
            180
        ):

            pygame.draw.rect(
                self.pantalla,
                (165, 205, 220),
                (
                    x,
                    100,
                    120,
                    150
                )
            )

            pygame.draw.rect(
                self.pantalla,
                (70, 75, 82),
                (
                    x,
                    100,
                    120,
                    150
                ),
                4
            )


        # ----------------------------------------------------
        # Parte inferior del andén
        # ----------------------------------------------------

        pygame.draw.rect(
            self.pantalla,
            (145, 148, 150),
            (
                0,
                250,
                s.ANCHO,
                130
            )
        )


        # ----------------------------------------------------
        # Líneas del piso
        # ----------------------------------------------------

        for x in range(
            -100,
            s.ANCHO + 200,
            100
        ):

            desplazamiento = (
                self.offset_fondo % 100
            )

            pygame.draw.line(
                self.pantalla,
                (125, 128, 130),
                (
                    x - desplazamiento,
                    250
                ),
                (
                    x + 40 - desplazamiento,
                    380
                ),
                2
            )


        # ----------------------------------------------------
        # Señal de estación
        # ----------------------------------------------------

        pygame.draw.rect(
            self.pantalla,
            s.ROJO_TRANSMILENIO,
            (
                30,
                105,
                180,
                48
            ),
            border_radius=6
        )

        texto = self.fuente_media.render(
            "TRANSMILENIO",
            True,
            s.BLANCO
        )

        self.pantalla.blit(
            texto,
            (
                43,
                115
            )
        )


    # ========================================================
    # MENÚ
    # ========================================================

    def dibujar_menu(self):

        # La portada ya contiene el título y el texto
        # "PRESIONE ENTER PARA EMPEZAR".
        # No dibujamos ningún menú encima.
        self.pantalla.blit(
            self.portada,
            (0, 0)
        )


    # ========================================================
    # INTRO
    # ========================================================

    def dibujar_intro(self):

        self.dibujar_estacion()


        # ----------------------------------------------------
        # Título
        # ----------------------------------------------------

        titulo = self.fuente_media.render(
            "¡CORRE!",
            True,
            s.BLANCO
        )

        self.pantalla.blit(
            titulo,
            titulo.get_rect(
                center=(
                    s.ANCHO // 2,
                    105
                )
            )
        )


        # ----------------------------------------------------
        # Torniquete
        # ----------------------------------------------------

        if self.torniquete:

            self.pantalla.blit(
                self.torniquete.image,
                self.torniquete.rect
            )


        # ----------------------------------------------------
        # Jugador
        # ----------------------------------------------------

        self.jugador.dibujar(
            self.pantalla
        )


        # ----------------------------------------------------
        # Texto según la fase
        # ----------------------------------------------------

        if self.intro_fase == "entrada":

            mensaje = "¡Rápido! Vas a perder el TransMilenio..."

        elif self.intro_fase == "pre_salto":

            mensaje = "¡SALTA EL TORNIQUETE!"

        else:

            mensaje = "¡ENTRA A LA ESTACIÓN!"


        texto = self.fuente_chica.render(
            mensaje,
            True,
            s.BLANCO
        )

        # Fondo para que el texto sea legible
        fondo_texto = pygame.Surface(
            (
                texto.get_width() + 30,
                texto.get_height() + 14
            ),
            pygame.SRCALPHA
        )

        fondo_texto.fill(
            (0, 0, 0, 130)
        )

        rect_texto = fondo_texto.get_rect(
            center=(
                s.ANCHO // 2,
                s.ALTO - 55
            )
        )

        self.pantalla.blit(
            fondo_texto,
            rect_texto
        )

        self.pantalla.blit(
            texto,
            texto.get_rect(
                center=rect_texto.center
            )
        )


        # ----------------------------------------------------
        # Indicador para saltar intro
        # ----------------------------------------------------

        skip = self.fuente_chica.render(
            "ENTER = saltar intro",
            True,
            s.GRIS_CLARO
        )

        self.pantalla.blit(
            skip,
            (
                20,
                20
            )
        )


    # ========================================================
    # JUEGO
    # ========================================================

    def dibujar_juego(self):

        self.dibujar_estacion()


        # ----------------------------------------------------
        # Carriles
        # ----------------------------------------------------

        for y in self.carriles_y:

            pygame.draw.line(
                self.pantalla,
                (220, 220, 220),
                (0, y),
                (s.ANCHO, y),
                1
            )


        # ----------------------------------------------------
        # Torniquete
        # ----------------------------------------------------

        if self.torniquete:

            self.pantalla.blit(
                self.torniquete.image,
                self.torniquete.rect
            )


        # ----------------------------------------------------
        # Obstáculos
        # ----------------------------------------------------

        for obstaculo in self.obstaculos:

            self.pantalla.blit(
                obstaculo.image,
                obstaculo.rect
            )


        # ----------------------------------------------------
        # Jugador
        # ----------------------------------------------------

        self.jugador.dibujar(
            self.pantalla
        )


        # ----------------------------------------------------
        # VIDAS
        # ----------------------------------------------------

        vidas_txt = self.fuente_chica.render(
            f"Vidas: {'♥ ' * self.vidas}",
            True,
            s.ROJO_TRANSMILENIO
        )

        self.pantalla.blit(
            vidas_txt,
            (
                20,
                20
            )
        )


        # ----------------------------------------------------
        # DISTANCIA
        # ----------------------------------------------------

        progreso = min(
            self.distancia
            / s.DISTANCIA_META,
            1.0
        )


        pygame.draw.rect(
            self.pantalla,
            s.GRIS_CLARO,
            (
                s.ANCHO - 220,
                20,
                200,
                18
            )
        )


        pygame.draw.rect(
            self.pantalla,
            s.VERDE,
            (
                s.ANCHO - 220,
                20,
                int(
                    200 * progreso
                ),
                18
            )
        )


        # ----------------------------------------------------
        # OBJETIVO
        # ----------------------------------------------------

        objetivo = self.fuente_chica.render(
            "META: G43 → SAN MATEO",
            True,
            s.BLANCO
        )

        self.pantalla.blit(
            objetivo,
            (
                s.ANCHO // 2 - 100,
                20
            )
        )


    # ========================================================
    # FINAL
    # ========================================================

    def dibujar_fin(
        self,
        mensaje,
        color,
        submensaje
    ):

        self.dibujar_estacion()


        # Oscurecer fondo
        overlay = pygame.Surface(
            (s.ANCHO, s.ALTO),
            pygame.SRCALPHA
        )

        overlay.fill(
            (0, 0, 0, 150)
        )

        self.pantalla.blit(
            overlay,
            (0, 0)
        )


        txt = self.fuente_grande.render(
            mensaje,
            True,
            color
        )

        self.pantalla.blit(
            txt,
            txt.get_rect(
                center=(
                    s.ANCHO // 2,
                    220
                )
            )
        )


        sub = self.fuente_chica.render(
            submensaje,
            True,
            s.BLANCO
        )

        self.pantalla.blit(
            sub,
            sub.get_rect(
                center=(
                    s.ANCHO // 2,
                    280
                )
            )
        )


# ============================================================
# MAIN
# ============================================================

async def main():

    juego = Juego()

    await juego.correr()


if __name__ == "__main__":

    asyncio.run(main())