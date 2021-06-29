import copy
import os
from controlador_agente_v3 import *
from controlador_comida_v3 import GrupoComidas
from colors import *
import matplotlib

matplotlib.use("TkAgg")

import matplotlib.pyplot as plt

# Iniciar pygame
pygame.init()

# Establecemos las dimenciones de la aplicacion
ALTO = 640
LARGO = 640
WINDOW_SIZE = [ALTO, LARGO]
screen = pygame.display.set_mode(WINDOW_SIZE)
# Titulo
pygame.display.set_caption("Proyecto Final Intelicencia Artificial")

# Terminó?
done = False

# Medir el tiempo de renderizado
clock = pygame.time.Clock()
x_tiempo = []
y_poblacion = []
print(plt.get_backend())
pcm = plt.get_current_fig_manager()
pcm.window.resizable(False, False)


class Juego:
    def dibujar_fondo(self):
        screen.fill(WHITE)

    def dibujar_destino(self, pos):
        pygame.draw.circle(screen, GREEN, pos, 5)

    def iniciar_simulacion(self):
        done = False
        while done is not True:
            pos = pygame.mouse.get_pos()
            self.dibujar_fondo()
            if not self.GrupoAgentes.all_dead():
                self.GrupoAgentes.update_agentes(screen)
            self.lista_comidas.update_comidas(screen)
            if pygame.time.get_ticks() % 10 == 0:
                self.lista_comidas.agrega_comida(WINDOW_SIZE, self.GrupoAgentes.lista_agentes)

            for event in pygame.event.get():  # Registra eventos variados
                if event.type == pygame.QUIT:  # Cerrar el programa?
                    done = True  # Si
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    print(pygame.mouse.get_pos())

            if pygame.time.get_ticks() % 90 == 0:
                self.print_plot()
            self.dibujar_destino(pos)
            clock.tick(30)
            pygame.display.flip()
        pygame.quit()  # no borrar
        # plt.plot(x_tiempo, y_poblacion, color='blue', linestyle='-', label="")

    def print_plot(self):
        if len(self.GrupoAgentes.lista_agentes) > 0:
            print(len(self.GrupoAgentes.lista_agentes))
            y_poblacion.append(len(self.GrupoAgentes.lista_agentes))
            x_tiempo.append(pygame.time.get_ticks())
            plt.plot(x_tiempo, y_poblacion, color='blue', linestyle='--', label="")
            plt.pause(0.1)

    def __init__(self, PP, _velocidad_bola, _Num_comidas_ini):

        self.lista_comidas = GrupoComidas(_Num_comidas_ini)
        self.GrupoAgentes = GrupoAgentes(PP)
        self.lista_comidas.crear_comidas(ALTO, LARGO, self.GrupoAgentes.lista_agentes)
        self.GrupoAgentes.crear_agentes(ALTO, LARGO, _velocidad_bola, self.lista_comidas.lista_comidas)


Velocidad_bola = 4
Num_comidas_ini = 15
Population = 2

juego = Juego(Population, Velocidad_bola, Num_comidas_ini)
juego.iniciar_simulacion()
plt.show()
print("a")
