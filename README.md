# TOMBO TU LLAVE 🚌

Juego retro sobre correr a coger el TransMilenio en Bogotá, hecho en
Python con [Pygame](https://www.pygame.org/).

## Estructura del proyecto

```
tombo_tu_llave/
├── main.py                # Loop principal, menús y las dos rutas jugables
├── requirements.txt
├── game/
│   ├── __init__.py
│   ├── settings.py         # Colores, tamaños, velocidades (aquí ajustas dificultad)
│   ├── player.py           # Clase del jugador
│   └── obstaculos.py       # Buses, policías y torniquete
```

## 1. Instalación (una sola vez)

Abre una terminal en VSCode (Ctrl + `) dentro de la carpeta del proyecto:

```bash
cd tombo_tu_llave

# Crear entorno virtual (recomendado para no ensuciar tu Python global)
python3 -m venv venv
source venv/bin/activate     # en Linux/Ubuntu

# Instalar dependencias
pip install -r requirements.txt
```

Si en Ubuntu te da error de librerías del sistema al instalar pygame, corre:

```bash
sudo apt update
sudo apt install python3-dev python3-setuptools libsdl2-dev libsdl2-image-dev \
    libsdl2-mixer-dev libsdl2-ttf-dev
```

## 2. Correrlo como ventana normal (la forma más rápida de probar)

```bash
python3 main.py
```

Se abre una ventana nativa. Úsala mientras programas — es el ciclo de
prueba más rápido (cada `python3 main.py` reinicia todo en segundos).

## 3. Correrlo en el navegador vía localhost

Como pediste probarlo en localhost, usamos **pygbag**, que compila el
juego a WebAssembly y lo sirve en un servidor local:

```bash
pygbag main.py
```

Esto va a:
1. Compilar el proyecto (la primera vez tarda un poco más).
2. Levantar un servidor en `http://localhost:8000`.
3. Ábrelo en tu navegador y ahí verás el juego corriendo dentro del `<canvas>`.

Para detenerlo: `Ctrl + C` en la terminal.

> Nota: `pygbag` necesita que el punto de entrada (`main.py`) tenga una
> función `async def main()` y uses `await asyncio.sleep(0)` dentro del
> loop — **ya está así en el código** que hicimos, no necesitas tocar nada.

## Controles

| Tecla | Acción |
|---|---|
| ↑ / ↓ | Cambiar de carril |
| ESPACIO | Saltar (esquivar bus / saltar el torniquete) |
| ENTER | Confirmar en menús / reintentar |
| 1 | Elegir modo Calle |
| 2 | Elegir modo Estación |

## Cómo está armado el juego (para que lo puedas modificar)

- **Modo Calle** (`JUGANDO_CALLE`): el jugador se mueve entre 4 carriles
  horizontales. Buses de TransMilenio aparecen desde la derecha y cruzan
  hacia la izquierda; hay que cambiar de carril o saltar para esquivarlos.
- **Modo Estación** (`JUGANDO_ESTACION`): al empezar hay un torniquete
  (`Torniquete`) que hay que saltar con ESPACIO. Una vez lo saltas,
  empiezan a aparecer policías que vienen desde la izquierda persiguiéndote.
- Ambos modos comparten: vidas (3), distancia acumulada, y una meta
  (`DISTANCIA_META` en `settings.py`) que si alcanzas, ganas.
- La dificultad sube solita con el tiempo (`INCREMENTO_VELOCIDAD`).

## Próximos pasos sugeridos (para ir mejorando poco a poco)

1. Reemplazar los rectángulos por sprites/pixel-art reales (imágenes .png).
2. Agregar sonido (silbato de policía, bus pasando, salto).
3. Animación de correr (piernas moviéndose) en vez de sprite estático.
4. Un modo "historia" que una las dos rutas en una sola partida.
5. Guardar el mejor puntaje (distancia máxima) en un archivo local.
6. Pantalla de "cómo jugar" antes de la selección de modo.

Dime cuál de estos quieres atacar primero y seguimos construyendo. 🚀
