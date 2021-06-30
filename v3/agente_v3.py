import pygame
from controlador_comida_v3 import *


# La clase persona, que será la que llevará la máquina de estados finito dentro de si
class Person:
    choque = False
    mutacion = 0.15
    Estados = ("Nace", "Camina", "Come", "Busca_comida",
               "Ataca", "Reproduce", "Busca_pareja", "Muere")
    currentEstado = Estados[0]

    def cargar_datos(self, _adn=None):
        if _adn is None:
            self.velocidad = random.uniform(3, 5)
            self.color = colors.Colors[random.randint(1, len(colors.Colors) - 2)]
            self.radio = 5 + random.uniform(-2, 2)
            self.energia_max = 150 + random.uniform(-50, 50)
            self.best_max = 300 + random.uniform(-100, 100)
            self.distance_search_partner_max = 300 + random.uniform(-100, 100)
        else:
            self.velocidad = _adn[0]
            self.color = _adn[1]
            self.radio = _adn[2]
            self.energia_max = _adn[3]
            self.best_max = _adn[4]
            self.distance_search_partner_max = _adn[5]
        self.energia = float(self.energia_max)
        self.best = float(self.best_max)
        self.distance_search_partner = float(self.distance_search_partner_max)
        self.currentEstado = self.Estados[1]

    def __init__(self, px, py, _lista_comidas, _lista_agentes, _adn=None):
        self.is_ded = False
        self.posicion = pygame.Vector2(px, py)
        self.cargar_datos(_adn)
        self.score = 0
        self.my_fud = None
        self.my_partner = None
        self.willing = None
        self.id_comida = int
        self.lista_comidas = _lista_comidas
        self.lista_agentes = _lista_agentes
        self.id_partner = int
        self.comidas_comidas = 0
        # print(self.comidas_comidas)

    def actual(self, screen):
        # Camina
        if self.currentEstado == self.Estados[1]:
            if self.energia > 0:
                self.mover_A([random.randint(0, screen.get_width()),random.randint(0, screen.get_height())])
                if self.energia >= 200:
                    self.currentEstado = self.Estados[6]  # Busca_pareja
                elif 0 < self.energia < 200:
                    self.currentEstado = self.Estados[3]  # Busca_comida
                self.energia -= 1
            else:
                self.currentEstado = self.Estados[7]

        # Come
        if self.currentEstado == self.Estados[2]:
            # print(self.my_fud, "mio")
            # print(self.energia)
            if self.my_fud is not None:
                # if self.objetivo(self.my_fud.get_pos(), 3.5):
                if self.objetivo2(self.my_fud):
                    if self.my_fud.is_eaten() is False:
                        self.energia += self.my_fud.alimento
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
                    # self.mover_A(self.my_fud.get_pos())
                    self.mover_A_entidad(self.my_fud)
                    # if self.objetivo(self.my_fud.get_pos(), 2.5):
                    if self.objetivo2(self.my_fud):
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
            # print("AAAA")
            if self.is_willing() and self.my_partner.is_willing():
                # if self.objetivo(self.my_partner.get_pos(), 3.5):
                if self.objetivo2(self.my_partner):
                    self.crear_hijo()
                    # print("boom un hijo", self.energia, self.currentEstado)
                elif self.energia >= 100:
                    # self.mover_A(self.my_partner.get_pos())
                    self.mover_A_entidad(self.my_partner)
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
            # print("ojo")
            self.willing = True
            if self.my_partner is not None:
                if self.my_partner.is_willing() is True:
                    # self.mover_A(self.my_partner.get_pos())
                    self.mover_A_entidad(self.my_partner)
                    # if self.objetivo(self.my_partner.get_pos(), 2.5):
                    if self.objetivo2(self.my_partner):
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
            comida = Comida(self.posicion.x, self.posicion.y, 40, color=colors.BLACK)
            self.lista_comidas.append(comida)
            # print("ded")
        # print(self.energia)
        # print(self.currentEstado)
        pygame.draw.circle(screen, self.color, self.posicion, self.radio)

    # Acá calcula que tan lejos esta del objetivo al que está yendo
    def objetivo(self, _objetivo, _dis):
        return pygame.Vector2.length(self.posicion - _objetivo) <= _dis

    def objetivo2(self, _objetivo):
        return pygame.Vector2.length(self.posicion - _objetivo.posicion) <= abs(self.radio-_objetivo.radio)

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
        dist = self.posicion - _objetivo
        if not dist.length()<=0:
            delta = pygame.Vector2.normalize(dist)
            if not self.is_ded:
                if not self.objetivo(_objetivo=_objetivo, _dis=2.5):
                # if not self.objetivo2(_objetivo=_objetivo):
                    if not dist.length() < self.velocidad:
                        self.posicion -= delta * self.velocidad
                    else:
                        self.posicion -= delta * dist.length()
            else: self.currentEstado = self.Estados[7]
        else: self.currentEstado=self.Estados[2]

    def mover_A_entidad(self, _objetivo):
        dist = self.posicion - _objetivo.posicion
        if not dist.length()<=0:
            delta = pygame.Vector2.normalize(dist)
            if not self.is_ded:
                if not self.objetivo2(_objetivo=_objetivo):
                    if not dist.length() < self.velocidad:
                        self.posicion -= delta * self.velocidad
                    else:
                        self.posicion -= delta * dist.length()
            else: self.currentEstado=self.Estados[7]

    def get_pos(self):
        return self.posicion

    def is_willing(self):
        return self.willing

    def crear_hijo(self):
        #### posicion
        temp_pos = pygame.Vector2((self.posicion.x + self.my_partner.get_pos().x) / 2,
                                  (self.posicion.y + self.my_partner.get_pos().y) / 2)
        #### velocidad
        if 1 - self.mutacion > random.random() > 0.5:
            temp_speed = float(self.velocidad)
        elif self.mutacion < random.random() <= 0.5:
            temp_speed = float(self.my_partner.velocidad)
        else:
            temp_speed = (float(self.velocidad) + float(self.my_partner.velocidad)) / 2
        if random.random() < self.mutacion:
            if random.random() < 0.5: temp_speed += random.uniform(-0.5, 0.5)
            if temp_speed <= 0: temp_speed = 0.1
        #### color
        temp_color = [0, 0, 0]
        if 1 - self.mutacion > random.random() > 0.5:
            temp_color = [self.color[0], self.color[1], self.color[2]]
        elif self.mutacion < random.random() <= 0.5:
            temp_color = [self.my_partner.color[0], self.my_partner.color[1], self.my_partner.color[2]]
        else:
            for _ in range(len(temp_color)):
                temp_color[_] = round((self.color[_] + self.my_partner.color[_]) / 2)
        if random.random() < self.mutacion:
            for _ in range(len(temp_color)):
                if random.random() < 0.5:
                    temp_color[_] += random.randint(-10, 10)
                if temp_color[_] > 255:
                    temp_color[_] = 255
                elif temp_color[_] < 0:
                    temp_color[_] = 0
        #### radio
        if 1 - self.mutacion > random.random() > 0.5:
            temp_radius = float(self.radio)
        elif self.mutacion < random.random() <= 0.5:
            temp_radius = float(self.my_partner.radio)
        else:
            temp_radius = (float(self.radio) + float(self.my_partner.radio)) / 2
        if random.random() < self.mutacion:
            if random.random() < 0.5:
                temp_radius += random.uniform(-0.5, 0.5)
            if temp_radius > 10:
                temp_radius = 10
            elif temp_radius < 1:
                temp_radius = 1
        #### energia_max
        if 1 - self.mutacion > random.random() > 0.5:
            temp_energia = float(self.energia_max)
        elif self.mutacion < random.random() <= 0.5:
            temp_energia = float(self.my_partner.energia_max)
        else:
            temp_energia = (float(self.energia_max) + float(self.my_partner.energia_max)) / 2
        if random.random() < self.mutacion:
            if random.random() < 0.5:
                temp_energia += 0.1
            else:
                temp_energia -= 0.1
            if temp_energia > 8:
                temp_energia = 8
            elif temp_energia < 1:
                temp_energia = 1
        #### best_max
        if 1 - self.mutacion > random.random() > 0.5:
            temp_best = float(self.best_max)
        elif self.mutacion < random.random() <= 0.5:
            temp_best = float(self.my_partner.best_max)
        else:
            temp_best = (float(self.best_max) + float(self.my_partner.best_max)) / 2
        if random.random() < self.mutacion:
            if random.random() < 0.5:
                temp_best += 0.1
            else:
                temp_best -= 0.1
            if temp_best > 8:
                temp_best = 8
            elif temp_best < 1:
                temp_best = 1
        #### distance_search_partner_max
        if 1 - self.mutacion > random.random() > 0.5:
            temp_partner_max = float(self.distance_search_partner_max)
        elif self.mutacion < random.random() <= 0.5:
            temp_partner_max = float(self.my_partner.distance_search_partner_max)
        else:
            temp_partner_max = (float(self.distance_search_partner_max) + float(
                self.my_partner.distance_search_partner_max)) / 2
        if random.random() < self.mutacion:
            if random.random() < 0.5:
                temp_partner_max += 0.1
            else:
                temp_partner_max -= 0.1
            if temp_partner_max > 8:
                temp_partner_max = 8
            elif temp_partner_max < 1:
                temp_partner_max = 1
        adn_ = [temp_speed, temp_color, temp_radius, temp_energia, temp_best, temp_partner_max]
        adn_string = ''.join([str(item) for item in adn_])
        print(adn_string)
        print(adn_string[0])

        # nuevo_agente = Person(temp_pos.x, temp_pos.y,
        #                       self.lista_comidas, self.lista_agentes,
        #                       temp_speed, temp_color
        #                       )
        nuevo_agente = Person(temp_pos.x, temp_pos.y, self.lista_comidas,
                              self.lista_agentes, adn_
                              )
        self.lista_agentes.append(nuevo_agente)
        self.energia -= 75
        self.my_partner.energia -= 75
        self.willing = False
        self.my_partner.willing = False
        self.distance_search_partner = 600
        self.my_partner.distance_search_partner = 600
        self.my_partner.currentEstado = self.Estados[1]
        self.currentEstado = self.Estados[1]
        self.id_partner = None
        self.my_partner = None
