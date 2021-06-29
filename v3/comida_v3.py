from agente_v3 import pygame
import  colors

class Comida:
    # color = colors.GREEN

    def __init__(self, _posX, _posY, _alto, _ancho,_lista_comidas,_lista_agentes,color=colors.GREEN):
        self.iseaten = False
        self.posicion = pygame.Vector2(_posX, _posY)
        self.valor = 10
        self.color=color
        lista_comidas = _lista_comidas
        lista_agentes = _lista_agentes

    def graficar_comida(self, screen):
        if self.iseaten is False:        pygame.draw.circle(screen, self.color, self.posicion, 5)

    def get_pos(self):
        return self.posicion

    def self(self):
        return self

    def is_eaten(self):
        return self.iseaten

    def eaten(self):
        self.iseaten=True
    # def is_eaten(self):
    #     if self.iseaten is False:
    #         self.iseaten = True
    #     else:
    #         return True
