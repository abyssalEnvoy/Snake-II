import pygame

class Score:
    SPRITE_ZERO = pygame.Rect(16, 0, 4, 8)
    SPRITE_ONE = pygame.Rect(20, 0, 4, 8)
    SPRITE_TWO = pygame.Rect(24, 0, 4, 8)
    SPRITE_THREE = pygame.Rect(28, 0, 4, 8)
    SPRITE_FOUR = pygame.Rect(16, 8, 4, 8)
    SPRITE_FIVE = pygame.Rect(20, 8, 4, 8)
    SPRITE_SIX = pygame.Rect(24, 8, 4, 8)
    SPRITE_SEVEN = pygame.Rect(28, 8, 4, 8)
    SPRITE_EIGHT = pygame.Rect(16, 16, 4, 8)
    SPRITE_NINE = pygame.Rect(20, 16, 4, 8)

    POINTS = 7

    sprite = [ SPRITE_ZERO, SPRITE_ZERO, SPRITE_ZERO, SPRITE_ZERO ]
    text = ""
    position = [pygame.Vector2(4, 0), pygame.Vector2(8, 0), pygame.Vector2(12, 0), pygame.Vector2(16, 0)]

    def refresh(self, snake):
        text = str((len(snake.body) - 3) * self.POINTS)

        if (len(snake.body) - 3) * self.POINTS < 10000:
            if len(text) == 1:
                text = "000" + text
            elif len(text) == 2:
                text = "00" + text
            elif len(text) == 3:
                text = "0" + text
        else:
            text = "9999"

        i = 0
        while i < 4:
            if text[i] == '0':
                self.sprite[i] = self.SPRITE_ZERO

            elif text[i] == '1':
                self.sprite[i] = self.SPRITE_ONE

            elif text[i] == '2':
                self.sprite[i] = self.SPRITE_TWO

            elif text[i] == '3':
                self.sprite[i] = self.SPRITE_THREE

            elif text[i] == '4':
                self.sprite[i] = self.SPRITE_FOUR

            elif text[i] == '5':
                self.sprite[i] = self.SPRITE_FIVE

            elif text[i] == '6':
                self.sprite[i] = self.SPRITE_SIX

            elif text[i] == '7':
                self.sprite[i] = self.SPRITE_SEVEN

            elif text[i] == '8':
                self.sprite[i] = self.SPRITE_EIGHT

            elif text[i] == '9':
                self.sprite[i] = self.SPRITE_NINE

            i += 1

    def render(self, target, tileset):
        i = 0
        while i < 4:
            sprite = tileset.subsurface(self.sprite[i])
            target.blit(sprite, self.position[i])
            i += 1