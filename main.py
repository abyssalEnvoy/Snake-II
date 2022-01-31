import sys, time
import pygame
from snake import Snake
from food import Food
from score import Score

# Screen size
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 360
VIEW_WIDTH = 80
VIEW_HEIGHT = 45

GRAPHICS = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
TARGET = pygame.Surface((VIEW_WIDTH, VIEW_HEIGHT))

# Color
CLEAR_COLOR = ((143,70,70))

# Time
FRAMERATE = 60
main_clock = pygame.time.Clock()

# Sprites
BACKGROUND = pygame.image.load("content/SnakeBackground.png").convert()
TILESET = pygame.image.load("content/SnakeTileset.png").convert_alpha()
ICON = pygame.image.load("content/Icon.png").convert()

# Objects
snake = Snake()
food = Food()
score = Score()

def render():
    GRAPHICS.fill(CLEAR_COLOR)
    TARGET.blit(BACKGROUND, (0, 0))

    snake.render(TARGET, TILESET)
    food.render(TARGET, TILESET)
    score.render(TARGET, TILESET)

    #region Render target resizing

    window_width, window_height = GRAPHICS.get_size()
    scale = min(window_width / VIEW_WIDTH, window_height / VIEW_HEIGHT)

    bar_width = int((window_width - int(VIEW_WIDTH * scale)) / 2)
    bar_height = int((window_height - int(VIEW_HEIGHT * scale)) / 2)

    resized = pygame.transform.scale(TARGET, (int(VIEW_WIDTH * scale), int(VIEW_HEIGHT * scale)))
    GRAPHICS.blit(resized, (bar_width, bar_height))
    
    pygame.display.update()

    #endregion

def main():
    pygame.init()
    pygame.display.set_icon(ICON)
    pygame.display.set_caption("Snake")

    prev_time = time.time()
    delta_time = 0

    while True:
        main_clock.tick(FRAMERATE)
        #pygame.display.set_caption("Snake FPS: {}".format(main_clock.get_fps()))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        current_time = time.time()
        delta_time = current_time - prev_time
        prev_time = current_time

        if (snake.eaten_food(food.position)):
            food.new_food_location(snake)
        
        snake.update(food)
        score.refresh(snake)
        
        render()

if __name__ == "__main__":
    main()