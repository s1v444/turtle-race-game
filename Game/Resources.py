import pygame
from Constants import WIDTH, HEIGHT

#Функция для обработки изображения
def load_images():
    red_turtle_img = pygame.image.load('images/red.jpg')
    blue_turtle_img = pygame.image.load('images/blue.jpg')
    yellow_turtle_img = pygame.image.load('images/yellow.jpg')
    sea_img = pygame.image.load('images/sea.jpg')

    turtle_size = (50, 50) #Аргумент изображение, кортеж
    red_turtle_img = pygame.transform.scale(red_turtle_img, turtle_size)
    blue_turtle_img = pygame.transform.scale(blue_turtle_img, turtle_size)
    yellow_turtle_img = pygame.transform.scale(yellow_turtle_img, turtle_size)
    sea_img = pygame.transform.scale(sea_img, (WIDTH, HEIGHT))

    return red_turtle_img, blue_turtle_img, yellow_turtle_img, sea_img #Возвращает готовых черепашек для игры