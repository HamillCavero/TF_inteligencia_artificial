from controlador_agente_v3 import *
from controlador_comida_v3 import GrupoComidas
from colors import *
import matplotlib.pyplot as plt

# Iniciar pygame
pygame.init()

# Establecemos las dimenciones de la aplicacion
ALTO = 720
LARGO = 720
WINDOW_SIZE = [LARGO, ALTO]
screen = pygame.display.set_mode(WINDOW_SIZE)
# Titulo
pygame.display.set_caption("Proyecto Final Intelicencia Artificial")
myfont = pygame.font.SysFont('Comic Sans MS', 30)
# screen = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE)

# Terminó?
done = False

# Medir el tiempo de renderizado
clock = pygame.time.Clock()
x_tiempo = []
y_poblacion = []




text = "Integrantes del grupo:\n" \
       "-Cavero Beraún, Edgar Hamill               - U201821775\n" \
       "-Gómez Lozano, Aldo Jhair                   - U201822450\n" \
       "-Morales Montero, Christopher Elvis     - U201820751\n\n" \
       "Cómo funciona:\n"\
       "La simulación trabaja creando un número aleatorio de personajes iniciales, estos empiezan con un color, velocidad, rango de visión" \
       "y energía máxima diferente\n"


font = pygame.font.SysFont('Arial', 64)


class Juego:
    def dibujar_fondo(self):
        screen.fill(WHITE)

    def blit_text(surface, text, pos, font, color=pygame.Color('black')):
        words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
        space = font.size(' ')[0]  # The width of a space.
        max_width, max_height = screen.get_size()
        x, y = pos
        for line in words:
            for word in line:
                word_surface = font.render(word, 0, color)
                word_width, word_height = word_surface.get_size()
                if x + word_width >= max_width:
                    x = pos[0]  # Reset the x.
                    y += word_height  # Start on new row.
                screen.blit(word_surface, (x, y))
                x += word_width + space
            x = pos[0]  # Reset the x.
            y += word_height  # Start on new row.

    def dibujar_destino(self, pos):
        pygame.draw.circle(screen, GREEN, pos, 5)

    def creditos(self):
        done = False
        button = pygame.Rect(100, 100, 50, 50)
        while done is not True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos  # gets mouse position
                    if button.collidepoint(mouse_pos):
                        done = True

            screen.fill(WHITE)

            pygame.draw.rect(screen, [255, 0, 0], button)  # draw button

            # screen.fill(WHITE)
            font = pygame.font.SysFont('Arial', 24)
            img = font.render('Regresar al menú', True, BLUE)
            self.blit_text(text, (100, 220), font)
            screen.blit(img, (160, 120))
            pygame.display.flip()
            for event in pygame.event.get():  # Registra eventos variados
                if event.type == pygame.QUIT:  # Cerrar el programa?
                    done = True  # Si

            pygame.display.update()
            clock.tick(30)


    def menu(self):
        done = False
        button = pygame.Rect(100, 200, 50, 50)
        button2 = pygame.Rect(100, 300, 50, 50)
        while done is not True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos  # gets mouse position

                    # checks if mouse position is over the button

                    if button.collidepoint(mouse_pos):
                        # prints current location of mouse
                        print('button was pressed at {0}'.format(mouse_pos))
                        done = True

                    if button2.collidepoint(mouse_pos):
                        # prints current location of mouse
                        print('button 2 was pressed at {0}'.format(mouse_pos))
                        self.creditos()

            screen.fill(WHITE)

            pygame.draw.rect(screen, [255, 0, 0], button)  # draw button
            pygame.draw.rect(screen, [0, 255, 0], button2)  # draw button
            font = pygame.font.SysFont('Arial', 24)
            img = font.render('Iniciar simulación', True, BLUE)
            screen.blit(img, (160, 220))
            img = font.render('Créditos', True, BLUE)
            screen.blit(img, (160, 320))
            img = font.render('Trabajo Final inteligencia Articifial', True, BLUE)
            screen.blit(img, (20, 20))
            pygame.display.flip()
            for event in pygame.event.get():  # Registra eventos variados
                if event.type == pygame.QUIT:  # Cerrar el programa?
                    done = True  # Si

            pygame.display.update()
            clock.tick(30)

    def iniciar_simulacion(self):
        done = False
        while done is not True:
            pos = pygame.mouse.get_pos()
            self.dibujar_fondo()
            if not self.GrupoAgentes.all_dead():
                self.GrupoAgentes.update_agentes(screen)
            self.lista_comidas.update_comidas(screen)
            if pygame.time.get_ticks() % 5 == 0:
                self.lista_comidas.agrega_comida(WINDOW_SIZE, self.GrupoAgentes.lista_agentes)

            for event in pygame.event.get():  # Registra eventos variados
                if event.type == pygame.QUIT:  # Cerrar el programa?
                    done = True  # Si
                    plt.plot(x_tiempo, y_poblacion, color='blue', linestyle='--', label="")
                    plt.tick_params(axis='both',width='0')

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    print(pygame.mouse.get_pos())

            if pygame.time.get_ticks() % 10 == 0:
                self.print_plot()
            # self.dibujar_destino(pos)
            clock.tick(120)
            pygame.display.flip()
        pygame.quit()  # no borrar

    def print_plot(self):
        if len(self.GrupoAgentes.lista_agentes) > 0:
            print(len(self.GrupoAgentes.lista_agentes))
            y_poblacion.append(len(self.GrupoAgentes.lista_agentes))
            x_tiempo.append(pygame.time.get_ticks())
            # plt.plot(x_tiempo, y_poblacion, color='blue', linestyle='--', label="")
            # plt.pause(0.01)

    def __init__(self, PP, _velocidad_bola, _Num_comidas_ini):
        self.lista_comidas = GrupoComidas(_Num_comidas_ini)
        self.GrupoAgentes = GrupoAgentes(PP)
        self.lista_comidas.crear_comidas(ALTO, LARGO, self.GrupoAgentes.lista_agentes)
        self.GrupoAgentes.crear_agentes(ALTO, LARGO, _velocidad_bola, self.lista_comidas.lista_comidas)


Velocidad_bola = 4
Num_comidas_ini = 15
Population = 4

juego = Juego(Population, Velocidad_bola, Num_comidas_ini)
juego.menu()
juego.iniciar_simulacion()
plt.title("Variación de la población con respecto al tiempo", fontdict={'family': 'serif',
            'color': 'black',
            'weight': 'normal',
            'size': 16,
            })
plt.show()
print("a")
