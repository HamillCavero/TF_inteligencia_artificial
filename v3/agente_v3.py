import pygame
# import random
# from comida_v3 import Comida
from controlador_comida_v3 import *


# La clase persona, que será la que llevará la máquina de estados finito dentro de si
class Person():
    choque = False
    mutacion = 0.15
    Estados = ("Nace", "Camina", "Come", "Busca_comida",
               "Ataca", "Reproduce", "Busca_pareja", "Muere")
    currentEstado = Estados[0]

    # Inicio de la clase
    def __init__(self, v, px, py, _lista_comidas, _lista_agentes, c=None):
        self.is_ded = False
        self.posicion = pygame.Vector2(px, py)
        self.velocidad = v
        if c is None:
            self.color = colors.Colors[random.randint(0, len(colors.Colors) - 1)]
        else:
            self.color = c
        if self.color[1] >= 255: self.color = (self.color[0], 255, self.color[2])
        self.score = 0
        self.radio = 5
        self.currentEstado = self.Estados[1]
        self.energia = 150
        self.my_fud = None
        self.my_partner = None
        self.willing = None
        self.best = 300
        self.distance_search_partner = 600
        self.id_comida = int
        self.lista_comidas = _lista_comidas
        self.lista_agentes = _lista_agentes
        self.id_partner = int
        self.comidas_comidas = 0
        # print(self.comidas_comidas)

    def actual(self, screen):
        # Camina
        if self.currentEstado == self.Estados[1]:
            if self.energia <= 0:
                # print("dead")
                self.currentEstado = self.Estados[7]  # Muere
                pass
            self.mover_A([random.randint(0, screen.get_width()),
                          random.randint(0, screen.get_height())])
            if self.energia >= 200:
                self.currentEstado = self.Estados[6]  # Busca_pareja
            elif 0 < self.energia < 200:
                self.currentEstado = self.Estados[3]  # Busca_comida
            self.energia -= 1
            print(self.energia)
        # Come
        if self.currentEstado == self.Estados[2]:
            # print(self.my_fud, "mio")
            # print(self.energia)
            if self.my_fud is not None:
                if self.objetivo(self.my_fud.get_pos(), 3.5):
                    if self.my_fud.is_eaten() is False:
                        self.energia += 30
                        self.comidas_comidas += 1
                        self.my_fud.eaten()
                        self.my_fud = None
                        self.best = 300
                        self.currentEstado = self.Estados[1]
                    else:
                        self.currentEstado = self.Estados[3]
                else:
                    self.currentEstado = self.Estados[3]
            else:
                self.currentEstado = self.Estados[3]
            self.energia -= 0.5
            if self.energia <= 50:
                self.currentEstado = self.Estados[3]  # Busca_comida
            if self.energia > 50:
                self.currentEstado = self.Estados[1]  # Camina
        # Busca_comida
        if self.currentEstado == self.Estados[3]:
            # print("hm")
            if self.my_fud is not None:
                if self.my_fud.is_eaten() is False:
                    self.mover_A(self.my_fud.get_pos())
                    if self.objetivo(self.my_fud.get_pos(), 2.5):
                        self.currentEstado = self.Estados[2]
                else:
                    self.my_fud = None
                    self.currentEstado = self.Estados[1]
            else:
                # self.currentEstado = self.Estados[3]
                self.best = 300
                self.buscar_comida()
                if self.my_fud is None:
                    self.currentEstado = self.Estados[1]
                if self.buscar_comida() is False:
                    self.currentEstado = self.Estados[1]
            self.energia -= 0.5
        # Reproduce
        if self.currentEstado == self.Estados[5]:
            print("AAAA")
            if self.is_willing() and self.my_partner.is_willing():
                if self.objetivo(self.my_partner.get_pos(), 3.5):
                    nuevo_agente = Person(float(self.velocidad),
                                          float(self.posicion.x + 20),
                                          float(self.posicion.y), self.lista_comidas, self.lista_agentes,
                                          (self.color[0], self.color[1] + 10, 0)
                                          )
                    self.lista_agentes.append(nuevo_agente)
                    self.energia -= 20
                    self.my_partner.energia -= 20
                    self.willing = False
                    self.my_partner.willing = False
                    self.distance_search_partner = 600
                    self.my_partner.distance_search_partner = 600
                    self.my_partner.currentEstado = self.Estados[1]
                    self.currentEstado = self.Estados[1]
                    self.id_partner = None
                    self.my_partner = None

                    # print("boom un hijo", self.energia, self.currentEstado)
                elif self.energia >= 100:
                    self.mover_A(self.my_partner.get_pos())
                else:
                    self.currentEstado = self.Estados[1]
                    # self.my_partner=None
            elif self.energia >= 200:
                self.currentEstado = self.Estados[6]
            else:
                self.currentEstado = self.Estados[1]
            self.energia -= 1
        # if self.currentEstado == self.Estados[5]:
        #     if self.energia >= 200:
        #         nuevo_agente = Person(float(self.velocidad),
        #                               float(self.posicion.x + 20),
        #                               float(self.posicion.y), self.lista_comidas, self.lista_agentes,
        #                               (self.color[0], self.color[1] + 10, 0)
        #                               )
        #         self.lista_agentes.append(nuevo_agente)
        #         self.energia -= 20
        #         self.currentEstado = self.Estados[1]
        #         # print("boom un hijo", self.energia, self.currentEstado)
        #     self.currentEstado = self.Estados[1]
        # Busca_pareja
        if self.currentEstado == self.Estados[6]:
            print("ojo")
            self.willing = True
            if self.my_partner is not None:
                if self.my_partner.is_willing() is True:
                    self.mover_A(self.my_partner.get_pos())
                    if self.objetivo(self.my_partner.get_pos(), 2.5):
                        self.currentEstado = self.Estados[5]
                else:
                    self.my_partner = None
                    self.currentEstado = self.Estados[1]
            else:
                self.distance_search_partner = 600
                self.buscar_pareja()
                if self.my_partner is None:
                    if self.energia <= 100:
                        self.willing = False
                        self.currentEstado = self.Estados[1]
                    else:
                        self.currentEstado = self.Estados[1]

                # if self.my_partner is None or self.energia <= 100:
                #     self.willing=False
                #     self.currentEstado = self.Estados[1]
                elif self.buscar_pareja() is False:
                    self.currentEstado = self.Estados[1]
            self.energia -= 0.5
        # Muere
        if self.currentEstado == self.Estados[7]:
            self.is_ded = True
            comida = Comida(self.posicion.x, self.posicion.y, 2, 2, self.lista_comidas, self.lista_agentes,
                            color=colors.BLACK)
            self.lista_comidas.append(comida)
            # print("ded")
        # print(self.energia)
        # print(self.currentEstado)
        pygame.draw.circle(screen, self.color, self.posicion, self.radio)

    # Acá calcula que tan lejos esta del objetivo al que está yendo
    def objetivo(self, _objetivo, _dis):
        return pygame.Vector2.length(self.posicion - _objetivo) <= _dis

    def buscar_comida(self):
        if self.lista_comidas:
            for _ in range(len(self.lista_comidas)):
                temp_comida = self.lista_comidas[_].get_pos()
                dist = pygame.Vector2.length(temp_comida - self.posicion)
                if dist <= self.best:
                    self.my_fud = self.lista_comidas[_]
                    self.best = dist
                    self.id_comida = self.lista_comidas.index(self.lista_comidas[_])
        else:
            return False
            # print(self.lista_comidas[self.id_comida], "mundo")
            # print(self.lista_comidas[self.id_comida] is self.my_fud, "es?")

    def buscar_pareja(self):
        if self.lista_agentes:
            for _ in range(len(self.lista_agentes)):
                if self.lista_agentes[_] is not self:
                    temp_agente = self.lista_agentes[_].get_pos()
                    dist = pygame.Vector2.length(temp_agente - self.posicion)
                    if dist <= self.best and self.lista_agentes[_].my_partner is None \
                            and self.lista_agentes[_].is_willing():
                        self.my_partner = self.lista_agentes[_]
                        self.distance_search_partner = dist
                        self.lista_agentes[_].my_partner = self
                        self.id_partner = self.lista_agentes.index(self.lista_agentes[_])
        else:
            return False
            # print(self.lista_comidas[self.id_comida], "mundo")
            # print(self.lista_comidas[self.id_comida] is self.my_fud, "es?")

    def mover_A(self, _objetivo):
        delta = pygame.Vector2.normalize(self.posicion - _objetivo)
        if not self.is_ded:
            if self.objetivo(_objetivo=_objetivo, _dis=2.5):
                pass
            elif self.posicion.y >= 0 and self.posicion.x >= 0:
                self.posicion -= delta * self.velocidad
            else:
                self.is_ded = True

    def get_pos(self):
        return self.posicion

    def is_willing(self):
        return self.willing
