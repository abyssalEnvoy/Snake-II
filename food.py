import random
import pygame

class Food:

    # Sprites
    SPRITE_FOOD = pygame.Rect(4, 0, 4, 4)

    # Utils
    position = pygame.Vector2(60, 24)

    COLOUMS = 18
    ROWS = 7

    def new_food_location(self, snake):
        x = random.randint(1, self.COLOUMS) * 4
        y = random.randint(3, self.ROWS + 2) * 4

        i = 0
        while i < len(snake.body):
            if len(snake.body) >= self.COLOUMS * self.ROWS:
                break

            part = snake.body[i].position

            if part.x == x and part.y == y:
                x = random.randint(1, self.COLOUMS) * 4
                y = random.randint(3, self.ROWS + 2) * 4
                i = 0
            
            i += 1
        
        self.position = pygame.Vector2(x, y)

    def reset_food_location(self):
        self.position = pygame.Vector2(60, 24)

    def render(self, target, tileset):
        sprite = tileset.subsurface(self.SPRITE_FOOD)
        target.blit(sprite, self.position)