import random
import pygame
from random import *
from pygame import mixer
import math


# Inicializar Pygame
pygame.init()

# Crear una pantalla de Paygame    (Su tamaño)
pantalla = pygame.display.set_mode((800, 700))

# Titulo & icono y fondo
pygame.display.set_caption("Invasión Espacial")
icono = pygame.image.load("icono_juego.png")
pygame.display.set_icon(icono)
fondo = pygame.image.load("fondito.jpg")

# Musica de Fondo
mixer.music.load("music.mp3")
mixer.music.set_volume(0.3)
mixer.music.play(-1)

# Jugador & sus valores
player_img = pygame.image.load("nave.png")
jugador_x = 363
jugador_y = 590
moviento_jugador = 0


# Bomba & sus valores
bomba_img = pygame.image.load("bomba.png")
bomba_x = 379
bomba_y = 575
moviento_bomba = 0
moviento_y_bomba = 0
bomba_visible = False


# Enemigos y sus variables
enemigo_img = []
enemigo_x = []
enemigo_Y = []
enemigo_x_cambio = []
enemigo_y_cambio = []

cantidad_de_enemigos = 8
for e in range(cantidad_de_enemigos):
    # Varible de los enemigos
    enemigo_img.append(pygame.image.load("Enemigo.png"))
    enemigo_x.append(randint(0, 736))
    enemigo_Y.append(randint(11, 250))
    enemigo_x_cambio.append(0.5)
    enemigo_y_cambio.append(35)

# Puntaje y sus valores
puntaje = 0
fuente = pygame.font.Font('freesansbold.ttf', 32)
puntaje_x = 10
puntaje_y = 10

# texto final del juego
fuente_f = pygame.font.Font('freesansbold.ttf', 64)
texto_f_x = 200
texto_f_y = 250
# Funcion para mostrar el texto final
def texto_final(x, y):
    texto_f = fuente_f.render(f"Game Over", True, (255, 255, 255))
    pantalla.blit(texto_f, (x, y))


# Linea final
linea = pygame.font.Font('freesansbold.ttf', 12)
linea_x = 0
linea_y = 530
def linea_final(x, y):
    linea_F = linea.render("_" * 800, True, (255, 255, 255))
    pantalla.blit(linea_F, (x, y))

# funcion para medir distancias
def distancias(x1, y1, x2, y2):
    distancia = math.sqrt(math.pow(x1 - x2, 2) + math.pow(y2 - y1, 2))

    if distancia < 27:
        return True
    else:
        return False

# Funcion mostrar puntaje
def mostrar_puntaje(x, y):
    texto = fuente.render(f"Puntaje: {puntaje}", True, (255, 255, 255))
    pantalla.blit(texto, (x, y))

# Funciones para mostrar en pantalla la bomba, nave, enemigos
def bomba(x, y):
    global bomba_visible
    bomba_visible = True
    pantalla.blit(bomba_img, (x, y))

def jugador(x, y):
    pantalla.blit(player_img, (x, y))

def enemigo(x, y, ene):
    pantalla.blit(enemigo_img[ene], (x, y))


# Ciclo While para que la pantalla no se cierre
se_ejecuta = True
while se_ejecuta:
    # Validación de un evento de pygame (Quit evento de undir en la x)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            se_ejecuta = False

        # moviento de la nave & bomba
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_d:
                moviento_jugador = 1
            if evento.key == pygame.K_a:
                moviento_jugador = -1
            # Salida de la Bomba
            if evento.key == pygame.K_w:
                if not bomba_visible:
                    moviento_bomba = jugador_x
                    moviento_y_bomba = -3
                    bomba(moviento_bomba, bomba_y)
                    sonido_bala = mixer.Sound("disparo.mp3")
                    sonido_bala.play()
        # Freno de la nave y bomba
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_d or evento.key == pygame.K_a:
                moviento_jugador = 0

    # Color de Fondo
    pantalla.blit(fondo, (0, 0))
    # Codigo del Juego

    # Controladores de movimiento
    jugador_x += moviento_jugador

    # Limites del jugador y Bomba
    if jugador_x <= 0:
        jugador_x = 0
        bomba_x = 16
    elif jugador_x >= 736:
        jugador_x = 736
        bomba_x = 752

    # Invocación de la bala
    if bomba_visible:
        bomba(moviento_bomba + 16, bomba_y)
        bomba_y += moviento_y_bomba
    # Bomba regresa al inicio
    if bomba_y == -1:
        bomba_y = 575
        moviento_y_bomba = 0
        bomba_visible = False

    # Enemigos
    for e in range(cantidad_de_enemigos):
        # Fin del juego
        if enemigo_Y[e] > 500:
            for k in range(cantidad_de_enemigos):
                enemigo_Y[k] = 1000
            # Fin del Juego
            texto_final(texto_f_x, texto_f_y)
            break

        # Moviento del enemigo
        enemigo_x[e] += enemigo_x_cambio[e]
        # Limites del enemigo derecha
        if enemigo_x[e] <= 0:
            enemigo_x_cambio[e] = 0.5
            enemigo_Y[e] += enemigo_y_cambio[e]
            # Aunmento de dificultad
            if puntaje > 20:
                enemigo_x_cambio[e] = 0.8
                cantidad_de_enemigos = 7
            # mas dificultad
            if puntaje > 40:
                enemigo_x_cambio[e] = 1
                cantidad_de_enemigos = 6
        # limites izquierda
        elif enemigo_x[e] >= 736:
            enemigo_x_cambio[e] = -0.5
            enemigo_Y[e] += enemigo_y_cambio[e]
            # aumento de dificultad
            if puntaje > 20:
                enemigo_x_cambio[e] = -0.8
            # mas dificultad
            if puntaje > 40:
                enemigo_x_cambio[e] = -1

        # Colision
        colision = distancias(enemigo_x[e], enemigo_Y[e], moviento_bomba, bomba_y)
        if colision:
            sonido_colision = mixer.Sound("explosion.mp3")
            sonido_colision.play()
            bomba_y = 575
            moviento_y_bomba = 0
            bomba_visible = False
            puntaje += 1
            enemigo_x[e] = randint(0, 736)
            enemigo_Y[e] = randint(11, 250)

        # invocador de enemigos
        enemigo(enemigo_x[e], enemigo_Y[e], e)

    # Invocadores
    jugador(jugador_x, jugador_y)
    linea_final(linea_x, linea_y)
    mostrar_puntaje(puntaje_x, puntaje_y)

    # Actualización de pantalla
    pygame.display.update()