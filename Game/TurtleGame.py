class Turtle:
    def __init__(self, image, start_pos):
        self.image = image
        self.rect = self.image.get_rect(topleft=start_pos)  # Нач.позиция для квадрата изображения

    def move(self, distance):
        self.rect.x += distance  # По координате х вперед
