from random import choice, randint
import pygame

# Инициализация PyGame:
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption("Змейка")

# Настройка времени:
clock = pygame.time.Clock()


def handle_keys(game_object):
    """Метод для управления змейкой через нажатие клавиш"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


# Тут опишите все классы игры.ы
class GameObject:
    """Создаем основной класс, от которого будут происходить все дочерные классы."""

    def __init__(self, position=(int, int), body_color=(int, int, int)):
        """Создаемв нем конструктор с основными атрибутами."""
        self.body_color = body_color
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.position = position

    def draw(self):
        """Заглушка для отрисовывания объектов."""
        pass


class Apple(GameObject):
    """Создаем дочерный класс, от основого класса GameOject."""

    def __init__(self, position=(int, int), body_color=(int, int, int)):
        """Конструктор создаем для яблока."""
        super().__init__(position, body_color)
        self.position = position
        self.position = self.randomize_position()
        self.body_color = APPLE_COLOR

    def draw(self, surface):
        """Отрисовываем яблоко на поле."""
        rect = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

    def randomize_position(self):
        """Функция для рисования яблока на рандомной позиции на поле."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )
        return self.position


class Snake(GameObject):
    """Создаем класс змейки."""

    def __init__(self, position=tuple[int, int], body_color=(int, int, int)):
        """Создаем конструктор для змеюги. Позиция - это список координат."""
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None

        super().__init__(position, body_color)
        self.body_color = SNAKE_COLOR
        self.position = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.positions = [position] * self.length
        self.last = None

    def update_direction(self):
        """Функция для передачи движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

# Метод draw класса Snake
    def draw(self, surface):
        """Метод для отрисовывания змейки."""
        # for position in self.positions[:-1]:
        rect = (pygame.Rect(
            self.position[0], (GRID_SIZE, GRID_SIZE)))
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

        # for position in self.positions[1:]:
        #   segment_rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        #    pygame.draw.rect(surface, self.body_color, segment_rect)
        #    pygame.draw.rect(surface, BORDER_COLOR, segment_rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(
            (self.position[0], self.position[1]), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Создаем функцию, передающее новое положение головы змейки."""
        return self.position[0]

    def move(self):
        """Функция инициализируещее движение змейки."""
        self.head_position = self.get_head_position()
        # self.head_position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.new_head = ((self.head_position[0] + self.direction[0] * GRID_SIZE)
                         % SCREEN_WIDTH,
                         (self.head_position[1]
                          + self.direction[1] * GRID_SIZE)
                         % SCREEN_WIDTH)
        if self.new_head in self.position[1:]:
            self.reset()
        if len(self.positions) > self.length:
            self.last = self.position.pop()
        else:
            self.position.insert(0, self.new_head)

    def reset(self):
        """
        Функция, которая при столкновении змейки с самой собой
        возвращает ее в первоначальное положение.
        """
        self.length = 1
        self.position = [self.position]
        self.direction = choice(((UP, DOWN, LEFT, RIGHT)))


def main():
    """Описываем основную логику игры и создаем экземпляры класса."""
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()

    while True:

        clock.tick(SPEED)
        handle_keys(snake)

        if snake.get_head_position() == apple.position:
            apple.randomize_position()
            snake.length += 1
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.move()
        apple.draw(screen)
        snake.draw(screen)
        snake.update_direction()

        pygame.display.update()


if __name__ == "__main__":
    main()
