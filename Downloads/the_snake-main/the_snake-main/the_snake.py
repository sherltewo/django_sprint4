import pygame
import random

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)

BORDER_COLOR = (93, 216, 228)

APPLE_COLOR = (255, 0, 0)

SNAKE_COLOR = (0, 255, 0)

SPEED = 20

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

pygame.display.set_caption('Змейка')

clock = pygame.time.Clock()



class GameObject:
    """Базовый класс для всех игровых объектов."""

    def __init__(self, position=None):
        """
        Инициализирует игровой объект.

        Args:
            position (tuple, optional): Начальная позиция объекта в формате (x, y).
                                      Если None, устанавливается в центр экрана.
        """
        if position is None:
            self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        else:
            self.position = position
        self.body_color = None

    def draw(self, screen):
        """
        Отрисовывает объект на поверхности.

        Этот метод должен быть переопределен в дочерних классах.
        """
        pass


class Apple(GameObject):
    """Класс, представляющий яблоко в игре."""

    def __init__(self):
        """Инициализирует яблоко."""
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайное положение яблока в пределах игрового поля."""
        grid_x = random.randint(0, GRID_WIDTH - 1)
        grid_y = random.randint(0, GRID_HEIGHT - 1)
        self.position = (grid_x * GRID_SIZE, grid_y * GRID_SIZE)

    def draw(self, screen):
        """
        Отрисовывает яблоко на поверхности.

        Args:
            screen (pygame.Surface): Поверхность для отрисовки.
        """
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс, представляющий змейку в игре."""

    def __init__(self):
        """Инициализирует змейку."""
        start_position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        super().__init__(start_position)

        self.body_color = SNAKE_COLOR
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Обновляет направление движения змейки после нажатия на кнопку."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """
        Перемещает змейку в текущем направлении.

        Description:
            Добавляет новую голову в направлении движения и удаляет хвост,
            если длина змейки не увеличилась. Обрабатывает телепортацию через границы.
        """
        self.update_direction()

        head_x, head_y = self.positions[0]
        dx, dy = self.direction
        new_head_x = head_x + dx * GRID_SIZE
        new_head_y = head_y + dy * GRID_SIZE

        if new_head_x >= SCREEN_WIDTH:
            new_head_x = 0
        elif new_head_x < 0:
            new_head_x = SCREEN_WIDTH - GRID_SIZE

        if new_head_y >= SCREEN_HEIGHT:
            new_head_y = 0
        elif new_head_y < 0:
            new_head_y = SCREEN_HEIGHT - GRID_SIZE

        new_head = (new_head_x, new_head_y)
        self.last = self.positions[-1] if len(self.positions) > 1 else None
        self.positions.insert(0, new_head)
        self.position = new_head

        if len(self.positions) > self.length:
            self.positions.pop()

    def grow(self):
        """Увеличивает длину змейки на один сегмент."""
        self.length += 1

    def draw(self, screen):
        """
        Отрисовывает змейку на поверхности.

        Args:
            screen (pygame.Surface): Поверхность для отрисовки.
        """
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def check_self_collision(self):
        """
        Проверяет столкновение головы змейки с её телом.

        Returns:
            bool: True если произошло столкновение, иначе False.
        """
        head_pos = self.get_head_position()
        return head_pos in self.positions[1:]

    def get_head_position(self):
        """
        Возвращает позицию головы змейки.

        Returns:
            tuple: Позиция головы в формате (x, y).
        """
        return self.positions[0] if self.positions else self.position

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        start_position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.position = start_position
        self.positions = [start_position]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.last = None


def handle_keys(game_object):
    """
    Обрабатывает нажатия клавиш для управления змейкой.

    Args:
        game_object (Snake): Объект змейки, направление которой нужно изменить.
    """
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


def main():
    """Основная функция игры, содержащая главный игровой цикл."""
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)

        handle_keys(snake)

        snake.move()

        if snake.get_head_position() == apple.position:
            snake.grow()
            apple.randomize_position()
            while apple.position in snake.positions:
                apple.randomize_position()

        if snake.check_self_collision():
            snake.reset()

        screen.fill(BOARD_BACKGROUND_COLOR)

        snake.draw(screen)
        apple.draw(screen)

        pygame.display.update()


if __name__ == "__main__":
    main()
