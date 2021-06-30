import pygame

Estados = ("Nace", "Camina", "Come", "Busca_comida",
           "Ataca", "Reproduce", "Busca_pareja", "Muere")
print(Estados)
currentEstado = Estados[0]
print(currentEstado)

pygame.init()
BLACK = (255, 255, 255)
WIDTH = 640
HEIGHT = 640
windowSurface = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
windowSurface.fill(BLACK)

print("vivo")
currentEstado = Estados[1]
while currentEstado is not Estados[7]:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if currentEstado == Estados[1]:  # Camina
                if event.key == pygame.K_a:
                    currentEstado = Estados[3]  # Busca_comida
                if event.key == pygame.K_s:
                    currentEstado = Estados[4]  # Ataca
                if event.key == pygame.K_d:
                    currentEstado = Estados[6]  # Busca_pareja
                if event.key == pygame.K_f:
                    currentEstado = Estados[7]  # Muere
            if currentEstado == Estados[2]:  # Come
                if event.key == pygame.K_q:
                    currentEstado = Estados[3]  # Busca_comida
                if event.key == pygame.K_w:
                    currentEstado = Estados[1]  # Camina
            if currentEstado == Estados[3]:  # Busca_comida
                if event.key == pygame.K_q:
                    currentEstado = Estados[2]  # Come
                if event.key == pygame.K_w:
                    currentEstado = Estados[1]  # Camina
                if event.key == pygame.K_e:
                    currentEstado = Estados[4]  # Ataca
            if currentEstado == Estados[4]:  # Ataca
                if event.key == pygame.K_q:
                    currentEstado = Estados[1]  # Camina
                if event.key == pygame.K_w:
                    currentEstado = Estados[7]  # Muere
            if currentEstado == Estados[5]:  # Reproduce
                if event.key == pygame.K_q:
                    currentEstado = Estados[1]  # Camina
                if event.key == pygame.K_w:
                    currentEstado = Estados[7]  # Muere
            if currentEstado == Estados[6]:  # Busca_pareja
                if event.key == pygame.K_q:
                    currentEstado = Estados[5]  # Reproduce
                if event.key == pygame.K_w:
                    currentEstado = Estados[7]  # Muere
            if currentEstado == Estados[7]:  # Muere
                pygame.quit()
        if event.type == pygame.QUIT:  # Cerrar el programa?
            done = True  # Si
            pygame.quit()
    print(currentEstado)
