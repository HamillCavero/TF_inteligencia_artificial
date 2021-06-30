from agente_v3 import pygame
import colors


class Comida:
    # color = colors.GREEN

    def __init__(self, _posX, _posY, _alimentacion=40, color=colors.BLACK,radius=4):
        self.iseaten = False
        self.posicion = pygame.Vector2(_posX, _posY)
        self.color = color
        self.alimento=_alimentacion
        self.radio=radius

    def graficar_comida(self, screen):
        if self.iseaten is False:
            pygame.draw.circle(screen, self.color, self.posicion, self.radio)

    def get_pos(self):
        return self.posicion

    def self(self):
        return self

    def is_eaten(self):
        return self.iseaten

    def eaten(self):
        self.iseaten = True
