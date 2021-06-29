from agente_v3 import *
from comida_v3 import Comida


class GrupoAgentes:
    def __init__(self, n_agentes):
        self.lista_agentes = []
        self.numero_agentes = n_agentes
        # self.crear_agentes(n_agentes, LARGO, ALTO, velocidad_bola,lista_comidas)

    def crear_agentes(self, LARGO, ALTO, velocidad_bola, lista_comidas):
        self.lista_comidas = lista_comidas
        for _ in range(self.numero_agentes):
            nuevo_agente = Person(velocidad_bola,
                                  random.randint(0, LARGO), random.randint(0, ALTO), lista_comidas,
                                  self.lista_agentes)
            self.lista_agentes.append(nuevo_agente)

    def update_agentes(self, screen):
        for _ in reversed(range(len(self.lista_agentes))):
            if self.lista_agentes[_].is_ded is False:
                self.lista_agentes[_].actual(screen)
            else:
                self.lista_agentes.pop(_)
                pass

    def all_dead(self):
        for _ in range(len(self.lista_agentes)):
            if self.lista_agentes[_].is_ded is False:
                return False
