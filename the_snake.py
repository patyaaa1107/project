from random import randint
import pygame

# Инициализация PyGame:
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
CENTER_POSITION = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки:
BORDER_COLOR = (93, 216, 228)

# Цвет яблока, фальшивого яблока и камня:
APPLE_COLOR = (255, 0, 0)
FALSE_APPLE_COLOR = (255, 51, 255)
STONE_COLOR = (128, 128, 128)
# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

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


class GameObject:
    """Создаем основной класс, от которого будут наследоваться все дочерные классы."""

    def __init__(self, position=(int, int), body_color=(int, int, int)):
        """Создаемв нем конструктор с основными атрибутами."""
        self.body_color = body_color
        self.position = position

    def draw(self, surface):
        """Заглушка для отрисовывания объектов."""
        pass


class Apple(GameObject):
    """Создаем дочерный класс, от основого класса GameOject."""

    def __init__(self, position=CENTER_POSITION, body_color=APPLE_COLOR):
        """Конструктор создаем для яблока."""
        super().__init__(position, body_color)
        self.randomize_position()

    def draw(self, surface):
        """Отрисовываем яблоко на поле."""
        rect = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

    def randomize_position(self):
        """Функция для обновления позиции яблока случайным образом"""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE)


class FalseApple(Apple):
    """Наследуем дочерный класс от дочерного класса для фальшивого яблока"""

    def __init__(self, position=CENTER_POSITION, body_color=FALSE_APPLE_COLOR):
        super().__init__(position, body_color)
        self.position = position
        self.body_color = body_color


class Stone(Apple):
    """Снова создаем субкласс от яблока для создания препятствия для змейки"""

    def __init__(self, position=CENTER_POSITION, body_color=STONE_COLOR):
        super().__init__(position, body_color)
        self.position = position
        self.body_color = body_color


class Snake(GameObject):
    """наследуем класс змейки от основного класса"""

    def __init__(self):
        self.body_color = SNAKE_COLOR
        self.position = CENTER_POSITION
        self.length = 1
        self.positions = [self.position] * self.length
        self.direction = RIGHT
        self.next_direction = None

    def draw(self, surface):
        """метод для отрисовывания змейки"""
        for position in self.positions[:-1]:
            rect = (
                pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

            head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.body_color, head_rect)
            pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1)

    def get_head_position(self):
        """возвращаем положение головы змейки"""
        return self.positions[0]

    def move(self):
        """Функция, инициализирующяя движение змейки."""
        axis_x, axis_y = self.get_head_position()
        direction_1 = self.direction[0] * 20
        direction_2 = self.direction[-1] * 20
        self.new_head = ((axis_x + (direction_1)) % SCREEN_WIDTH,
                         (axis_y + (direction_2)) % SCREEN_HEIGHT)
        if self.new_head in self.positions:
            self.reset()
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.positions.insert(0, self.new_head)

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def reset(self):
        """Метод для обновление змейки"""
        self.position = CENTER_POSITION
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None


def main():
    """Описываем основную логику игры"""
    apple = Apple(APPLE_COLOR)
    snake = Snake()
    falseapple = FalseApple()
    stone = Stone()

    while True:

        clock.tick(SPEED)
        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw(screen)
        snake.draw(screen)
        falseapple.draw(screen)
        stone.draw(screen)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.positions[0] == apple.position:
            apple.randomize_position()
            snake.length += 1

        if snake.positions[0] == falseapple.position:
            falseapple.randomize_position()
            snake.length -= 1

        if snake.positions[0] == stone.position:
            snake.reset()
            stone.randomize_position()

        if apple.position == snake.positions:
            apple.randomize_position()

        pygame.display.update()


if __name__ == '__main__':
    main()
