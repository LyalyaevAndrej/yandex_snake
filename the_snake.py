import pygame
from random import randint


# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
CENTER_X = SCREEN_WIDTH // 2
CENTER_Y = SCREEN_HEIGHT // 2
# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (100, 100, 100)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (255, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс, от которого наследуются другие игровые объекты."""

    def __init__(self):
        self.position = (CENTER_X, CENTER_Y)
        self.body_color = None

    def draw(self):
        """
        Этот метод должен определять,
        как объект будет отрисовываться на экране.
        """
        pass


class Apple(GameObject):
    """
    Класс, унаследованный от GameObject,
    описывающий яблоко и действия с ним.
    """

    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайное положение яблока на игровом поле."""
        x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (x, y)

    def draw(self, screen):
        """
        Это абстрактный метод,
        который предназначен для переопределения в дочерних классах.
        """
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """
    Класс, унаследованный от GameObject,
    описывающий змейку и её поведение.
    """

    def __init__(self):
        super().__init__()
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновляет позицию змейки."""
        head_x, head_y = self.get_head_position()

        # Вычисляем новую позицию головы
        new_head = (
            head_x + self.direction[0] * GRID_SIZE,
            head_y + self.direction[1] * GRID_SIZE
        )

        # Обработка выхода за границы экрана
        new_head = (
            new_head[0] % SCREEN_WIDTH,
            new_head[1] % SCREEN_HEIGHT
        )

        # Добавляем новую голову в начало списка
        self.positions.insert(0, new_head)

        # Если длина змейки не увеличилась, удаляем хвост
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self, screen):
        """Отрисовывает змейку на экране, затирая след."""
        for segment in self.positions:
            rect = pygame.Rect(segment, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """
        Сбрасывает змейку в начальное состояние
        после столкновения с собой.
        """
        self.length = 1
        self.position = (CENTER_X, CENTER_Y)
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None


def handle_keys(game_object):
    """
    Обрабатывает нажатия клавиш,
    чтобы изменить направление движения змейки.
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
    return True


def main():
    """Основной цикл игры."""
    pygame.init()
    # Создание экземпляров игровых объектов
    snake = Snake()
    apple = Apple()

    # Переменные игры
    running = True
    score = 0

    # Счет
    font = pygame.font.SysFont('Arial', 25)

    # Главный игровой цикл
    while running:
        # 1. Обработка событий клавиш
        running = handle_keys(snake)
        if not running:
            break

        # 2. Обновление направления движения змейки
        snake.update_direction()

        # 3. Движение змейки
        snake.move()

        # 4. Проверка поедания яблока
        if snake.get_head_position() == apple.position:
            snake.length += 1
            score += 10
            apple.randomize_position()

        # 5. Проверка столкновения с собой
        head = snake.get_head_position()
        if head in snake.positions[1:]:
            snake.reset()
            score = 0

        # 6. Отрисовка объектов
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()
        score_text = font.render(f'Счёт: {score}', True, (255, 255, 255))
        screen.blit(score_text, (5, 5))

        # 7. Вывод счета
        pygame.display.flip()

        # 8. Контроль FPS
        clock.tick(SPEED)


if __name__ == '__main__':
    main()
