import pygame

def handle_events(turtles):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:  # Обработка нажатых клавиш и сдвиг на 50 пикселей
            if event.key == pygame.K_r:
                turtles[0].move(50)
            elif event.key == pygame.K_b:
                turtles[1].move(50)
            elif event.key == pygame.K_y:
                turtles[2].move(50)
    return True
