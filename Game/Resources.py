import pygame
import os
from Constants import WIDTH, HEIGHT

# Функция для обработки изображения
def load_images():
    base_path = os.path.join(os.path.dirname(__file__), 'images')

    red_turtle_img = pygame.image.load(os.path.join(base_path, 'red.png')).convert_alpha()
    blue_turtle_img = pygame.image.load(os.path.join(base_path, 'blue.png')).convert_alpha()
    yellow_turtle_img = pygame.image.load(os.path.join(base_path, 'yellow.png')).convert_alpha()
    sea_img = pygame.image.load(os.path.join(base_path, 'sea.jpg'))

    turtle_size = (50, 50)
    red_turtle_img = pygame.transform.scale(red_turtle_img, turtle_size)
    blue_turtle_img = pygame.transform.scale(blue_turtle_img, turtle_size)
    yellow_turtle_img = pygame.transform.scale(yellow_turtle_img, turtle_size)
    sea_img = pygame.transform.scale(sea_img, (WIDTH, HEIGHT))

    return red_turtle_img, blue_turtle_img, yellow_turtle_img, sea_img
