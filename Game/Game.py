import pygame
import socket
import sys
from Constants import WIDTH, HEIGHT
from Renderer import render, display_winner
from Resources import load_images
from TurtleGame import Turtle
import ipaddress

def is_valid_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

if len(sys.argv) != 2:
    exit('-1 не указан адрес сервера')

ip_server = sys.argv[1]

if not is_valid_ip(ip_server):
    exit('-1 неверный формат ip')

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Черепашья гонка - Клиент")

red_turtle_img, blue_turtle_img, yellow_turtle_img, sea_img = load_images()
red_turtle = Turtle(red_turtle_img, (100, 50))
blue_turtle = Turtle(blue_turtle_img, (100, 150))
yellow_turtle = Turtle(yellow_turtle_img, (100, 250))
turtles = [red_turtle, blue_turtle, yellow_turtle]

start_line = pygame.Rect(100, 0, 2, HEIGHT)
finish_line = pygame.Rect(WIDTH - 100, 0, 2, HEIGHT)

font = pygame.font.Font(None, 36)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = (ip_server, 12345)  # Используем переданный IP-адрес
client_socket.settimeout(5)

client_socket.sendto("CONNECT".encode('utf-8'), server_address)

try:
    # Ожидание ответа от сервера
    data, _ = client_socket.recvfrom(1024)
    response = data.decode('utf-8')

    # Проверка ответа от сервера
    if not response.startswith("SELECT :"):
        print("Неверный IP сервера или сервер недоступен.")
        exit('-1 неверный IP сервера')

    turtle_color = response.split(":")[1].strip()
    print(f"Ваша черепашка: {turtle_color}")

except socket.timeout:
    print("Не удалось подключиться к серверу. Проверьте IP и доступность сервера.")
    exit('-1 неверный IP сервера')

def display_message(screen, font, message):
    text = font.render(message, True, (255, 255, 255))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()

running = True
game_started = False
show_start_message = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Отправка команды "MOVE" серверу
                client_socket.sendto("MOVE".encode('utf-8'), server_address)
                show_start_message = False  # Скрыть сообщение после первого движения

    # Получение обновленного состояния игры от сервера
    client_socket.settimeout(0.1)  # Таймаут для неблокирующего получения данных
    try:
        data, _ = client_socket.recvfrom(1024)
        game_status = data.decode('utf-8')
        print(game_status)

        if "Два игрока подключились! Игра начинается." in game_status:
            game_started = True

        # Обновление позиций черепашек на основе данных от сервера
        for line in game_status.split('\n'):
            if ':' in line:
                color, pos = line.split(':')
                color = color.strip()
                if pos.strip():  # Проверяем, что pos не пустой
                    pos = int(pos.strip())
                    if color == 'red':
                        red_turtle.rect.x = pos
                    elif color == 'blue':
                        blue_turtle.rect.x = pos
                    elif color == 'yellow':
                        yellow_turtle.rect.x = pos

        for turtle in turtles:
            if turtle.rect.x >= WIDTH - 100:
                winner = 'красная' if turtle == red_turtle \
                    else 'синяя' if turtle == blue_turtle \
                    else 'желтая'
                display_winner(screen, font, winner)
                pygame.time.delay(5000)
                running = False
                break

        render(screen, sea_img, turtles, start_line, finish_line, font)

        # Отображение уведомления о готовности игры
        if not game_started:
            display_message(screen, font, "Ожидание второго игрока...")
        elif game_started and show_start_message:
            display_message(screen, font, "Игра начинается!")

    except socket.timeout:
        pass

    pygame.time.delay(30)

client_socket.close()
pygame.quit()