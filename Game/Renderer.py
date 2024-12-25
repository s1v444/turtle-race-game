import pygame

from Constants import WIDTH, HEIGHT, WHITE


def render(screen, sea_img, turtles, start_line, finish_line, font):
    screen.blit(sea_img, (0, 0))

    pygame.draw.rect(screen, WHITE, start_line)
    pygame.draw.rect(screen, WHITE, finish_line)

    start_text = font.render("Старт", True, WHITE)
    finish_text = font.render("Финиш", True, WHITE)
    screen.blit(start_text, (10, 10))  # Сдвиг старт
    screen.blit(finish_text, (WIDTH - 90, 10))  # Сдвиг финиш

    for turtle in turtles:
        screen.blit(turtle.image, turtle.rect)

    # Обновление экрана
    pygame.display.flip()


def display_winner(screen, font, winner):
    winner_text = font.render(f"Победителем стала {winner} черепашка!", True, WHITE)
    screen.blit(winner_text, (WIDTH // 2 - 250, HEIGHT // 2))
    pygame.display.flip()
