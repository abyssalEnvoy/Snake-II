import time
import copy
import pygame

class Snake:

    #region Sprites

    # Head
    SPRITE_RIGHT_HEAD = pygame.Rect(0, 8, 4, 4)
    SPRITE_LEFT_HEAD = pygame.Rect(4, 8, 4, 4)
    SPRITE_UP_HEAD = pygame.Rect(8, 8, 4, 4)
    SPRITE_DOWN_HEAD = pygame.Rect(12, 8, 4, 4)

    SPRITE_RIGHT_OPEN_HEAD = pygame.Rect(0, 12, 4, 4)
    SPRITE_LEFT_OPEN_HEAD = pygame.Rect(4, 12, 4, 4)
    SPRITE_UP_OPEN_HEAD = pygame.Rect(8, 12, 4, 4)
    SPRITE_DOWN_OPEN_HEAD = pygame.Rect(12, 12, 4, 4)

    # Body
    SPRITE_VERTICAL_BODY = pygame.Rect(0, 0, 4, 4)
    SPRITE_HORIZONTAL_BODY = pygame.Rect(0, 4, 4, 4)
    SPRITE_EATEN_BODY = pygame.Rect(4, 4, 4, 4)

    # Tail
    SPRITE_RIGHT_TAIL = pygame.Rect(8, 0, 4, 4)
    SPRITE_LEFT_TAIL = pygame.Rect(12, 0, 4, 4)
    SPRITE_UP_TAIL = pygame.Rect(12, 4, 4, 4)
    SPRITE_DOWN_TAIL = pygame.Rect(8, 4, 4, 4)

    # Corners
    SPRITE_RIGHT_UP_CORNER = pygame.Rect(8, 20, 4, 4)
    SPRITE_LEFT_UP_CORNER = pygame.Rect(12, 20, 4, 4)
    SPRITE_RIGHT_DOWN_CORNER = pygame.Rect(0, 20, 4, 4)
    SPRITE_LEFT_DOWN_CORNER = pygame.Rect(4, 20, 4, 4)
    
    SPRITE_RIGHT_UP_EATEN_CORNER = pygame.Rect(8, 16, 4, 4)
    SPRITE_LEFT_UP_EATEN_CORNER = pygame.Rect(12, 16, 4, 4)
    SPRITE_RIGHT_DOWN_EATEN_CORNER = pygame.Rect(0, 16, 4, 4)
    SPRITE_LEFT_DOWN_EATEN_CORNER = pygame.Rect(4, 16, 4, 4)

    # Debug
    SPRITE_BODY = pygame.Rect(20, 24, 4, 4)
    SPRITE_HEAD = pygame.Rect(16, 28, 4, 4)
    SPRITE_TAIL = pygame.Rect(16, 24, 4, 4)

    #endregion

    class SnakeBody:
        def __init__(self, x, y, sprite, eaten):
            self.position = pygame.Vector2(x, y)
            self.sprite = sprite
            self.eaten = eaten
    
    # Utils
    body = [
        SnakeBody(28, 24, SPRITE_RIGHT_TAIL, False), 
        SnakeBody(32, 24, SPRITE_HORIZONTAL_BODY, False),
        SnakeBody(36, 24, SPRITE_RIGHT_HEAD, False)]

    dead_body = body

    x_dir = 0
    y_dir = 0
    alive = True
    visible = True

    speed = 4
    total = 3

    # Time
    DELAY = 0.18
    remaining_delay = DELAY

    GAME_OVER_DELAY = 1.2
    remaining_game_over_delay = GAME_OVER_DELAY

    BLINK_AMOUNT = 0.18
    remaining_blink_amount = BLINK_AMOUNT 

    prev_time = time.time()

    def update(self, food):

        current_time = time.time()
        delta_time = current_time - self.prev_time
        self.prev_time = current_time

        self.set_dir()
        self.remaining_delay -= delta_time

        if self.alive:
            if self.remaining_delay <= 0:
                head = self.body[len(self.body) - 1].position

                if not self.x_dir + self.y_dir == 0:
                    self.dead_body = copy.deepcopy(self.body)

                    if self.total == len(self.body):
                        self.body.pop(0)
                    else:
                        self.body[len(self.body) - 1].eaten = True

                    head = pygame.Vector2(head.x + self.x_dir, head.y + self.y_dir)
                    self.body.append(self.SnakeBody(head.x, head.y, self.SPRITE_RIGHT_HEAD, False))

                    self.push_inbounds()
                    self.update_anims(food)

                self.remaining_delay = self.DELAY
        else:
            self.is_dead(delta_time, food)
        
        self.game_over()

    def render(self, target, tilset):
        if self.visible:
            for piece in self.body:
                sprite = tilset.subsurface(piece.sprite)
                target.blit(sprite, piece.position)

    def out_of_bounds(self, position):
        if position.x < 4:
            position = pygame.Vector2(72, position.y)

        elif position.x > 72:
            position = pygame.Vector2(4, position.y)

        elif position.y < 12:
            position = pygame.Vector2(position.x, 36)

        elif position.y > 36:
            position = pygame.Vector2(position.x, 12)

        return position
        
    def is_dead(self, delta, food):
        self.remaining_game_over_delay -= delta
        self.remaining_blink_amount -= delta

        if self.remaining_blink_amount <= 0:
            self.visible = not self.visible
            self.remaining_blink_amount = self.BLINK_AMOUNT

        if self.remaining_game_over_delay <= 0:
            self.remaining_game_over_delay = self.GAME_OVER_DELAY

            self.total = 3
            self.alive = True
            self.visible = True
            self.x_dir = 0
            self.y_dir = 0

            self.body = [
                self.SnakeBody(28, 24, self.SPRITE_RIGHT_TAIL, False), 
                self.SnakeBody(32, 24, self.SPRITE_HORIZONTAL_BODY, False),
                self.SnakeBody(36, 24, self.SPRITE_RIGHT_HEAD, False)]
                
            food.reset_food_location()

    def game_over(self):
        head = self.body[len(self.body) - 1].position

        i = 0
        while i < len(self.body) - 1:
            if head == self.body[i].position:
                self.body = copy.deepcopy(self.dead_body)
                self.alive = False        
            
            i += 1

    def set_dir(self):
        keys_pressed = pygame.key.get_pressed()
        
        head = self.body[len(self.body) - 1].position
        second_part = self.body[len(self.body) - 2].position

        if (keys_pressed[pygame.K_w] or keys_pressed[pygame.K_UP]):
            if not (self.out_of_bounds(head - pygame.Vector2(0, self.speed)).y == second_part.y):
                self.x_dir = 0
                self.y_dir = -self.speed

        elif (keys_pressed[pygame.K_s] or keys_pressed[pygame.K_DOWN]):
            if not (self.out_of_bounds(head + pygame.Vector2(0, self.speed)).y == second_part.y):
                self.x_dir = 0
                self.y_dir = self.speed

        if (keys_pressed[pygame.K_d] or keys_pressed[pygame.K_RIGHT]):
            if not (self.out_of_bounds(head + pygame.Vector2(self.speed, 0)).x == second_part.x):
                self.x_dir = self.speed
                self.y_dir = 0

        elif (keys_pressed[pygame.K_a] or keys_pressed[pygame.K_LEFT]):
            if not (self.out_of_bounds(head - pygame.Vector2(self.speed, 0)).x == second_part.x):
                self.x_dir = -self.speed
                self.y_dir = 0

    def push_inbounds(self):
        for piece in self.body:
            piece.position = self.out_of_bounds(piece.position)

    def eaten_food(self, position):
        head = self.body[len(self.body) - 1].position
        if head == position:
            self.total += 1
            return True
        return False

    def update_anims(self, food):

        #region Tail

        tail = self.body[0]

        if self.out_of_bounds(tail.position + pygame.Vector2(self.speed, 0)) == self.body[1].position:
            tail.sprite = self.SPRITE_RIGHT_TAIL
        elif self.out_of_bounds(tail.position + pygame.Vector2(-self.speed, 0)) == self.body[1].position:
            tail.sprite = self.SPRITE_LEFT_TAIL
        elif self.out_of_bounds(tail.position + pygame.Vector2(0, self.speed)) == self.body[1].position:
            tail.sprite = self.SPRITE_DOWN_TAIL
        elif self.out_of_bounds(tail.position + pygame.Vector2(0, -self.speed)) == self.body[1].position:
            tail.sprite = self.SPRITE_UP_TAIL

        #endregion

        #region Body

        i = 1
        while i < len(self.body) - 1:
            piece = self.body[i]

            # Horizontal
            if (self.out_of_bounds(piece.position + pygame.Vector2(self.speed, 0)) == self.body[i + 1].position) and (
                self.out_of_bounds(piece.position + pygame.Vector2(-self.speed, 0)) == self.body[i - 1].position
                ) or (
                self.out_of_bounds(piece.position + pygame.Vector2(-self.speed, 0)) == self.body[i + 1].position) and (
                self.out_of_bounds(piece.position + pygame.Vector2(self.speed, 0)) == self.body[i - 1].position):

                piece.sprite = self.SPRITE_HORIZONTAL_BODY
            
            # Vertical
            if (self.out_of_bounds(piece.position + pygame.Vector2(0, self.speed)) == self.body[i + 1].position) and (
                self.out_of_bounds(piece.position + pygame.Vector2(0, -self.speed)) == self.body[i - 1].position
                ) or (
                self.out_of_bounds(piece.position + pygame.Vector2(0, -self.speed)) == self.body[i + 1].position) and (
                self.out_of_bounds(piece.position + pygame.Vector2(0, self.speed)) == self.body[i - 1].position):

                piece.sprite = self.SPRITE_VERTICAL_BODY

            # Eaten
            if piece.eaten:
                piece.sprite = self.SPRITE_EATEN_BODY

            i += 1

        #endregion

        #region Corners

        i = 1
        while i < len(self.body) - 1:
            piece = self.body[i]

            if not self.body[i].eaten:

                # Right-Up
                if (self.out_of_bounds(piece.position + pygame.Vector2(self.speed, 0)) == self.body[i + 1].position) and (
                    self.out_of_bounds(piece.position + pygame.Vector2(0, -self.speed)) == self.body[i - 1].position
                    ) or (
                    self.out_of_bounds(piece.position + pygame.Vector2(0, -self.speed)) == self.body[i + 1].position) and (
                    self.out_of_bounds(piece.position + pygame.Vector2(self.speed, 0)) == self.body[i - 1].position):

                    piece.sprite = self.SPRITE_RIGHT_UP_CORNER
                
                # Left-Up
                if (self.out_of_bounds(piece.position + pygame.Vector2(-self.speed, 0)) == self.body[i + 1].position) and (
                    self.out_of_bounds(piece.position + pygame.Vector2(0, -self.speed)) == self.body[i - 1].position
                    ) or (
                    self.out_of_bounds(piece.position + pygame.Vector2(0, -self.speed)) == self.body[i + 1].position) and (
                    self.out_of_bounds(piece.position + pygame.Vector2(-self.speed, 0)) == self.body[i - 1].position):

                    piece.sprite = self.SPRITE_LEFT_UP_CORNER

                # Right-Down
                if (self.out_of_bounds(piece.position + pygame.Vector2(self.speed, 0)) == self.body[i + 1].position) and (
                    self.out_of_bounds(piece.position + pygame.Vector2(0, self.speed)) == self.body[i - 1].position
                    ) or (
                    self.out_of_bounds(piece.position + pygame.Vector2(0, self.speed)) == self.body[i + 1].position) and (
                    self.out_of_bounds(piece.position + pygame.Vector2(self.speed, 0)) == self.body[i - 1].position):

                    piece.sprite = self.SPRITE_RIGHT_DOWN_CORNER

                # Left-Down
                if (self.out_of_bounds(piece.position + pygame.Vector2(-self.speed, 0)) == self.body[i + 1].position) and (
                    self.out_of_bounds(piece.position + pygame.Vector2(0, self.speed)) == self.body[i - 1].position
                    ) or (
                    self.out_of_bounds(piece.position + pygame.Vector2(0, self.speed)) == self.body[i + 1].position) and (
                    self.out_of_bounds(piece.position + pygame.Vector2(-self.speed, 0)) == self.body[i - 1].position):

                    piece.sprite = self.SPRITE_LEFT_DOWN_CORNER
            else:
                # Right-Up Eaten
                if (self.out_of_bounds(piece.position + pygame.Vector2(self.speed, 0)) == self.body[i + 1].position) and (
                    self.out_of_bounds(piece.position + pygame.Vector2(0, -self.speed)) == self.body[i - 1].position
                    ) or (
                    self.out_of_bounds(piece.position + pygame.Vector2(0, -self.speed)) == self.body[i + 1].position) and (
                    self.out_of_bounds(piece.position + pygame.Vector2(self.speed, 0)) == self.body[i - 1].position):

                    piece.sprite = self.SPRITE_RIGHT_UP_EATEN_CORNER
                
                # Left-Up Eaten
                if (self.out_of_bounds(piece.position + pygame.Vector2(-self.speed, 0)) == self.body[i + 1].position) and (
                    self.out_of_bounds(piece.position + pygame.Vector2(0, -self.speed)) == self.body[i - 1].position
                    ) or (
                    self.out_of_bounds(piece.position + pygame.Vector2(0, -self.speed)) == self.body[i + 1].position) and (
                    self.out_of_bounds(piece.position + pygame.Vector2(-self.speed, 0)) == self.body[i - 1].position):

                    piece.sprite = self.SPRITE_LEFT_UP_EATEN_CORNER

                # Right-Down Eaten
                if (self.out_of_bounds(piece.position + pygame.Vector2(self.speed, 0)) == self.body[i + 1].position) and (
                    self.out_of_bounds(piece.position + pygame.Vector2(0, self.speed)) == self.body[i - 1].position
                    ) or (
                    self.out_of_bounds(piece.position + pygame.Vector2(0, self.speed)) == self.body[i + 1].position) and (
                    self.out_of_bounds(piece.position + pygame.Vector2(self.speed, 0)) == self.body[i - 1].position):

                    piece.sprite = self.SPRITE_RIGHT_DOWN_EATEN_CORNER

                # Left-Down Eaten
                if (self.out_of_bounds(piece.position + pygame.Vector2(-self.speed, 0)) == self.body[i + 1].position) and (
                    self.out_of_bounds(piece.position + pygame.Vector2(0, self.speed)) == self.body[i - 1].position
                    ) or (
                    self.out_of_bounds(piece.position + pygame.Vector2(0, self.speed)) == self.body[i + 1].position) and (
                    self.out_of_bounds(piece.position + pygame.Vector2(-self.speed, 0)) == self.body[i - 1].position):

                    piece.sprite = self.SPRITE_LEFT_DOWN_EATEN_CORNER
            i += 1

        #endregion

        #region Head

        head = self.body[len(self.body) - 1]

        # Closed Mouth

        if self.x_dir == self.speed:
            head.sprite = self.SPRITE_RIGHT_HEAD

        elif self.x_dir == -self.speed:
            head.sprite = self.SPRITE_LEFT_HEAD

        elif self.y_dir == self.speed:
            head.sprite = self.SPRITE_DOWN_HEAD

        elif self.y_dir == -self.speed:
            head.sprite = self.SPRITE_UP_HEAD

        # Open Mouth

        if self.out_of_bounds(head.position + pygame.Vector2(self.speed, 0)) == food.position and self.x_dir == self.speed:
            head.sprite = self.SPRITE_RIGHT_OPEN_HEAD

        elif self.out_of_bounds(head.position + pygame.Vector2(-self.speed, 0)) == food.position and self.x_dir == -self.speed:
            head.sprite = self.SPRITE_LEFT_OPEN_HEAD

        elif self.out_of_bounds(head.position + pygame.Vector2(0, self.speed)) == food.position and self.y_dir == self.speed:
            head.sprite = self.SPRITE_DOWN_OPEN_HEAD

        elif self.out_of_bounds(head.position + pygame.Vector2(0, -self.speed)) == food.position and self.y_dir == -self.speed:
            head.sprite = self.SPRITE_UP_OPEN_HEAD

        #endregion