from comida_v3 import *
import random


class GrupoComidas:
    def __init__(self, comidas_iniciales):
        self.lista_comidas = []
        self.cantidad = comidas_iniciales
        # self.crear_comidas(self.cantidad, LARGO, ALTO)

    def update_comidas(self, screen):
        for _ in reversed(range(len(self.lista_comidas))):
            self.lista_comidas[_].graficar_comida(screen)
        self.limpiar_comidas()

    def limpiar_comidas(self):
        self.cantidad = len(self.lista_comidas)
        for _ in reversed(range(self.cantidad)):
            if self.lista_comidas[_].iseaten:
                self.lista_comidas.pop(_)

    def agrega_comida(self, dimension, _grupo_agentes):
        comida = Comida(random.randint(0, dimension[0]), random.randint(0, dimension[1]), 40)
        # print("bloop")
        self.lista_comidas.append(comida)
        self.cantidad = len(self.lista_comidas)

    def crear_comidas(self, LARGO, ALTO, _grupo_agentes):
        for _ in range(self.cantidad):
            comida = Comida(random.randint(0, LARGO), random.randint(0, ALTO), 40)
            self.lista_comidas.append(comida)
