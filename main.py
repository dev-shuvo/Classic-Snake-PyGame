import pygame, sys, random
from pygame.math import Vector2

# Initialize pygame and screen
pygame.init()
cell_size = 24
number_of_cells = 20
offset = 55
screen = pygame.display.set_mode(
    (2 * offset + cell_size * number_of_cells, 2 * offset + cell_size * number_of_cells)
)
clock = pygame.time.Clock()
favicon = pygame.image.load("graphics/favicon.png")
pygame.display.set_icon(favicon)
pygame.display.set_caption("Snake")

# Load game assets
font = pygame.font.Font("font/ka1.ttf", 28)
eat_sound = pygame.mixer.Sound("sounds/eat.mp3")
game_over_sound = pygame.mixer.Sound("sounds/game_over.mp3")


# Game colors
dark_green = (38, 60, 0)
light_green = (142, 163, 44)


# Snake's food
class Food:
    def __init__(self, snake_body):
        self.position = self.generate_random_position(snake_body)

    def draw(self):
        food_image = pygame.image.load("graphics/food.png")
        food_rect = pygame.Rect(
            offset + self.position.x * cell_size,
            offset + self.position.y * cell_size,
            cell_size,
            cell_size,
        )

        screen.blit(food_image, food_rect)

    # Generate random cell position for the food
    def generate_random_cell(self):
        x = random.randint(0, number_of_cells - 1)
        y = random.randint(0, number_of_cells - 1)

        return Vector2(x, y)

    def generate_random_position(self, snake_body):
        position = self.generate_random_cell()

        # Checks if the food's position already blocked by snake's body
        while position in snake_body:
            position = self.generate_random_cell()

        return position


# Snake
class Snake:
    def __init__(self):
        self.body = [Vector2(6, 9), Vector2(5, 9), Vector2(4, 9)]
        self.direction = Vector2(1, 0)
        self.add_segment = False

    def draw(self):
        for segment in self.body:
            segment_rect = (
                offset + segment.x * cell_size + 2,
                offset + segment.y * cell_size + 2,
                cell_size - 4,
                cell_size - 4,
            )
            pygame.draw.rect(screen, dark_green, segment_rect, 8, 0)

    def update(self):
        # Add a new segment in the x direction
        self.body.insert(0, self.body[0] + self.direction)

        if self.add_segment:
            self.add_segment = False
        else:
            # Remove the last segment of snake's body to move forward
            self.body = self.body[:-1]

    def reset(self):
        self.body = [Vector2(6, 9), Vector2(5, 9), Vector2(4, 9)]
        self.direction = Vector2(1, 0)


# Main game class
class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food(self.snake.body)
        self.state = True
        self.score = 0

    def draw(self):
        self.food.draw()
        self.snake.draw()

    def update(self):
        if self.state:
            self.snake.update()
            self.check_collision_with_food()
            self.check_collision_with_edges()
            self.check_collision_with_tail()

    def check_collision_with_food(self):
        if self.snake.body[0] == self.food.position:
            self.food.position = self.food.generate_random_position(self.snake.body)
            self.snake.add_segment = True
            self.score += 1
            eat_sound.play()

    def check_collision_with_edges(self):
        if self.snake.body[0].x == number_of_cells or self.snake.body[0].x == -1:
            self.game_over()
            game_over_sound.play()
        if self.snake.body[0].y == number_of_cells or self.snake.body[0].y == -1:
            self.game_over()
            game_over_sound.play()

    def check_collision_with_tail(self):
        headless_body = self.snake.body[1:]

        if self.snake.body[0] in headless_body:
            self.game_over()
            game_over_sound.play()

    def game_over(self):
        self.snake.reset()
        self.food.position = self.food.generate_random_position(self.snake.body)
        self.state = False


# Calling main game object
game = Game()

# Custom game event
snake_update = pygame.USEREVENT
pygame.time.set_timer(snake_update, 200)

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == snake_update:
            game.update()

        # Snake controls (Up, Down, Left, Right)
        if event.type == pygame.KEYDOWN:
            if not game.state:
                game.state = True
                game.score = 0

            if event.key == pygame.K_UP and game.snake.direction != Vector2(0, 1):
                game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN and game.snake.direction != Vector2(0, -1):
                game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT and game.snake.direction != Vector2(1, 0):
                game.snake.direction = Vector2(-1, 0)
            if event.key == pygame.K_RIGHT and game.snake.direction != Vector2(-1, 0):
                game.snake.direction = Vector2(1, 0)

    # Drawing objects on the display
    screen.fill(light_green)

    pygame.draw.rect(
        screen,
        dark_green,
        (
            offset - 5,
            offset - 5,
            cell_size * number_of_cells + 10,
            cell_size * number_of_cells + 10,
        ),
        5,
    )

    # Drawing display grid
    for x in range(number_of_cells):
        for y in range(number_of_cells):
            pygame.draw.rect(
                screen,
                dark_green,
                (
                    offset + x * cell_size,
                    offset + y * cell_size,
                    cell_size,
                    cell_size,
                ),
                1,
            )

    game.draw()

    game_title_surface = font.render("Snake", True, dark_green)
    score_surface = font.render(str(game.score), True, dark_green)
    game_over_surface = font.render("Game over", True, dark_green)

    screen.blit(
        game_title_surface,
        (
            (
                1.1 * offset
                + cell_size * number_of_cells
                - game_title_surface.get_width()
            ),
            10,
        ),
    )
    screen.blit(score_surface, (offset - 5, 10))

    if not game.state:
        screen.blit(
            game_over_surface, (offset - 5, offset + cell_size * number_of_cells + 10)
        )

    # Updating the display
    pygame.display.update()
    clock.tick(60)
