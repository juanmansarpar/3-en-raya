import pygame
import sys
import random

pygame.init()

ANCHO, ALTO = 600, 600
screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption('3 en Raya')

BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL = (0, 0, 255)

turno = 0
tablero = [['', '', ''],
           ['', '', ''],
           ['', '', '']]

estado_juego = 'inicio'

fuente = pygame.font.SysFont(None, 50)

def dibujar_tablero():
    screen.fill(BLANCO)
    pygame.draw.line(screen, NEGRO, (200, 0), (200, 600), 5)
    pygame.draw.line(screen, NEGRO, (400, 0), (400, 600), 5)
    pygame.draw.line(screen, NEGRO, (0, 200), (600, 200), 5)
    pygame.draw.line(screen, NEGRO, (0, 400), (600, 400), 5)

    for fila in range(3):
        for columna in range(3):
            if tablero[fila][columna] == 'X':
                pygame.draw.line(screen, NEGRO, (columna * 200 + 50, fila * 200 + 50), (columna * 200 + 150, fila * 200 + 150), 5)
                pygame.draw.line(screen, NEGRO, (columna * 200 + 150, fila * 200 + 50), (columna * 200 + 50, fila * 200 + 150), 5)
            elif tablero[fila][columna] == 'O':
                pygame.draw.circle(screen, AZUL, (columna * 200 + 100, fila * 200 + 100), 50, 5)

def verificar_ganador():
    for i in range(3):
        if tablero[i][0] == tablero[i][1] == tablero[i][2] != '':
            return tablero[i][0]
        if tablero[0][i] == tablero[1][i] == tablero[2][i] != '':
            return tablero[0][i]
    if tablero[0][0] == tablero[1][1] == tablero[2][2] != '':
        return tablero[0][0]
    if tablero[0][2] == tablero[1][1] == tablero[2][0] != '':
        return tablero[0][2]
    return None

def movimiento_IA():
    disponibles = []
    for fila in range(3):
        for columna in range(3):
            if tablero[fila][columna] == '':
                disponibles.append((fila, columna))
    if disponibles:
        fila, columna = random.choice(disponibles)
        tablero[fila][columna] = 'O'

def mostrar_menu():
    screen.fill(BLANCO)

    titulo = fuente.render('3 en Raya', True, NEGRO)
    titulo_rect = titulo.get_rect(center=(ANCHO // 2, ALTO // 3))
    screen.blit(titulo, titulo_rect)

    jugar_texto = fuente.render('Jugar', True, NEGRO)
    jugar_rect = jugar_texto.get_rect(center=(ANCHO // 2, ALTO // 2))
    pygame.draw.rect(screen, BLANCO, jugar_rect)
    screen.blit(jugar_texto, jugar_rect)

    salir_texto = fuente.render('Salir', True, NEGRO)
    salir_rect = salir_texto.get_rect(center=(ANCHO // 2, ALTO // 2 + 100))
    pygame.draw.rect(screen, BLANCO, salir_rect)
    screen.blit(salir_texto, salir_rect)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = pygame.mouse.get_pos()

                if jugar_rect.collidepoint(x, y):
                    return 'jugando'
                elif salir_rect.collidepoint(x, y):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

def mostrar_resultado(mensaje):
    screen.fill(BLANCO)

    resultado_texto = fuente.render(mensaje, True, NEGRO)
    resultado_rect = resultado_texto.get_rect(center=(ANCHO // 2, ALTO // 2))
    screen.blit(resultado_texto, resultado_rect)

    volver_texto = fuente.render('Volver al Menú', True, NEGRO)
    volver_rect = volver_texto.get_rect(center=(ANCHO // 2, ALTO // 2 + 100))
    pygame.draw.rect(screen, BLANCO, volver_rect)
    screen.blit(volver_texto, volver_rect)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = pygame.mouse.get_pos()

                if volver_rect.collidepoint(x, y):
                    return 'inicio'

        pygame.display.update()

while True:
    if estado_juego == 'inicio':
        estado_juego = mostrar_menu()
        tablero = [['', '', ''],
                   ['', '', ''],
                   ['', '', '']]
        turno = 0
        pygame.display.set_caption('3 en Raya')

    elif estado_juego == 'jugando':
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and turno == 0:
                x, y = pygame.mouse.get_pos()
                fila = y // 200
                columna = x // 200

                if tablero[fila][columna] == '':
                    tablero[fila][columna] = 'X'
                    turno = 1

        if turno == 1:
            movimiento_IA()
            turno = 0

        dibujar_tablero()

        ganador = verificar_ganador()
        if ganador:
            estado_juego = 'ganador'
        elif all(tablero[i][j] != '' for i in range(3) for j in range(3)):
            estado_juego = 'perdedor'

        pygame.display.flip()

    elif estado_juego == 'ganador':
        mensaje = f'¡Ha ganado el jugador {ganador}!'
        estado_juego = mostrar_resultado(mensaje)

    elif estado_juego == 'perdedor':
        mensaje = '¡Has perdido!'
        estado_juego = mostrar_resultado(mensaje)
