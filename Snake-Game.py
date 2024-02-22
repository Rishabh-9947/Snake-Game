import pygame
import random

# Initialize Pygame
pygame.init()

# Game variables
window_width, window_height = 640, 480
cell_size = 20
snake_pos = [pygame.Vector2(window_width/2, window_height/2)]
snake_direction = pygame.Vector2(cell_size, 0)
food_pos = pygame.Vector2(random.randint(0, (window_width-cell_size)//cell_size) * cell_size, random.randint(0, (window_height-cell_size)//cell_size) * cell_size)
snake_speed = cell_size
score = 0
mouth_open = True  # Variable to track the mouth animation state

# Set up the display
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()

# Set up the font for the scoreboard
font = pygame.font.Font(None, 36)

def place_food():
    while True:
        new_food_pos = pygame.Vector2(random.randint(0, (window_width-cell_size)//cell_size) * cell_size, random.randint(0, (window_height-cell_size)//cell_size) * cell_size)
        if new_food_pos not in snake_pos:
            return new_food_pos

def draw_scoreboard():
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    window.blit(score_text, (10, 10))

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake_direction != pygame.Vector2(0, snake_speed):
                snake_direction = pygame.Vector2(0, -snake_speed)
            elif event.key == pygame.K_DOWN and snake_direction != pygame.Vector2(0, -snake_speed):
                snake_direction = pygame.Vector2(0, snake_speed)
            elif event.key == pygame.K_LEFT and snake_direction != pygame.Vector2(snake_speed, 0):
                snake_direction = pygame.Vector2(-snake_speed, 0)
            elif event.key == pygame.K_RIGHT and snake_direction != pygame.Vector2(-snake_speed, 0):
                snake_direction = pygame.Vector2(snake_speed, 0)

    # Update snake position
    new_head = snake_pos[0] + snake_direction
    new_head.x = new_head.x % window_width
    new_head.y = new_head.y % window_height
    snake_pos.insert(0, new_head)
    if snake_pos[0] == food_pos:
        score += 1
        food_pos = place_food()
    else:
        snake_pos.pop()

    # Check for self collision
    if snake_pos[0] in snake_pos[1:]:
        running = False

    # Drawing the game
    window.fill((0, 0, 0))  # Clear the screen

    # Draw the snake
    for i, pos in enumerate(snake_pos):
        if i == 0:  # Draw the head with mouth animation
            if mouth_open:
                pygame.draw.rect(window, (0, 255, 0), pygame.Rect(pos.x, pos.y, cell_size, cell_size))
            else:
                pygame.draw.circle(window, (0, 255, 0), (int(pos.x + cell_size/2), int(pos.y + cell_size/2)), cell_size//2)
        else:  # Draw the body
            pygame.draw.rect(window, (0, 255, 0), pygame.Rect(pos.x, pos.y, cell_size, cell_size))

    # Toggle the mouth open/close state
    mouth_open = not mouth_open

    # Draw the food
    pygame.draw.rect(window, (255, 0, 0), pygame.Rect(food_pos.x, food_pos.y, cell_size, cell_size))

    # Draw the scoreboard
    draw_scoreboard()

    # Update the display
    pygame.display.flip()

    # Frame rate
    clock.tick(10)

# Game over
print(f"Game Over! Your score was: {score}")

# Clean up
pygame.quit()