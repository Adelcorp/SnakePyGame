import random
import time
import sys
import pygame
from pygame.math import Vector2
import pygame_menu

pygame.init()


class SNAKE:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)
        self.new_block = False
        self.score = 0

        self.head_up = pygame.image.load('snake/up_head.png').convert_alpha()
        self.head_down = pygame.image.load('snake/down_head.png').convert_alpha()
        self.head_right = pygame.image.load('snake/right_head.png').convert_alpha()
        self.head_left = pygame.image.load('snake/left_head.png').convert_alpha()

        self.tail_up = pygame.image.load('snake/up_tail.png').convert_alpha()
        self.tail_down = pygame.image.load('snake/down_tail.png').convert_alpha()
        self.tail_right = pygame.image.load('snake/right_tail.png').convert_alpha()
        self.tail_left = pygame.image.load('snake/left_tail.png').convert_alpha()

        self.body_vertical = pygame.image.load('snake/vert_body.jpg').convert_alpha()
        self.body_horizontal = pygame.image.load('snake/hor_body.jpg').convert_alpha()

        self.body_br = pygame.image.load('snake/up_right.png').convert_alpha()
        self.body_bl = pygame.image.load('snake/up_left.png').convert_alpha()
        self.body_tr = pygame.image.load('snake/down_right.png').convert_alpha()
        self.body_tl = pygame.image.load('snake/down_left.png').convert_alpha()

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index, block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl, block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl, block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr, block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br, block_rect)

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1, 0):
            self.head = self.head_left
        elif head_relation == Vector2(-1, 0):
            self.head = self.head_right
        elif head_relation == Vector2(0, 1):
            self.head = self.head_up
        elif head_relation == Vector2(0, -1):
            self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1, 0):
            self.tail = self.tail_left
        elif tail_relation == Vector2(-1, 0):
            self.tail = self.tail_right
        elif tail_relation == Vector2(0, 1):
            self.tail = self.tail_up
        elif tail_relation == Vector2(0, -1):
            self.tail = self.tail_down

    def move_snake(self):
        if self.new_block:
            body_copy = self.body[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
        body_copy.insert(0, body_copy[0] + self.direction)
        self.body = body_copy[:]

    def add_block(self):
        self.new_block = True
        self.score += 1

class FRUIT:

    def __init__(self):
        self.grape = pygame.image.load('snake/grape.png').convert_alpha()
        self.apple = pygame.image.load('snake/apple.png').convert_alpha()
        self.randomize()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(self.fruit, fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)
        if random.randint(0, 3) == 0:
            self.fruit = self.grape
        else:
            self.fruit = self.apple


class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
        self.speed = 5
        self.score = 0

    def update(self):
        self.draw_grass()
        if self.snake.direction != Vector2(0, 0):
            self.snake.move_snake()
            self.check_collision()
            self.check_fail()

    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            if self.fruit.fruit == self.fruit.apple:
                self.snake.add_block()
                self.speed += 3
            else:
                self.snake.add_block()
                self.snake.add_block()
                self.snake.add_block()
                self.speed += 6
        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        self.speed = 5
        self.reset()

    def reset(self):
        time.sleep(0.05)
        self.score = str(self.snake.score)
        self.snake.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.snake.direction = Vector2(0, 0)

        h = True
        while h is True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        h = False
                        break
                    if event.key == pygame.K_ESCAPE:
                        event.type = pygame.QUIT
                elif event.type == pygame.QUIT:
                    pygame.quit()
            self.table(int(self.score))
            self.draw_end_screen()
            pygame.display.update()

    def draw_grass(self):
        grass_color = (167, 209, 61)
        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)

    def st_grass_draw(self):
        grass = pygame.image.load('snake/grasstoppres_st.png')
        for col in range(cell_number):
            for colA1 in range(cell_number):
                rect = pygame.Rect(col * cell_size, colA1 * cell_size, cell_size, cell_size)
                screen.blit(grass, rect)

    def draw_end_screen(self):
        big_apple = pygame.image.load('snake/big_apple.png')
        wr = 'Your score:'
        wrd = self.score
        wrdd = 'Tap space to try again'
        exit_message = 'Tap esc to finish'

        font = pygame.font.Font(None, 50)

        score_sur = font.render(wr, True, (56, 74, 12))
        score_sur_d = font.render(wrd, True, (56, 74, 12))
        score_sur_dd = font.render(wrdd, True, (56, 74, 12))
        score_sur_ddd = font.render(exit_message, True, (56, 74, 12))

        rect_ = big_apple.get_rect(center=(400, 400))
        self.st_grass_draw()
        screen.blit(big_apple, rect_)
        screen.blit(score_sur, (300, 400))
        screen.blit(score_sur_d, (380, 440))
        screen.blit(score_sur_dd, (240, 480))
        screen.blit(score_sur_ddd, (280, 520))
        self.snake.score = 0
        pygame.display.update()

    def draw_score(self):
        score_text = str(self.snake.score)
        score_surface = game_font.render(score_text, True, (56, 74, 12))
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        apple_rect = apple.get_rect(midright=(score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left, apple_rect.top, apple_rect.width + score_rect.width + 6,
                              apple_rect.height)

        pygame.draw.rect(screen, (167, 209, 61), bg_rect)
        screen.blit(score_surface, score_rect)
        screen.blit(apple, apple_rect)
        pygame.draw.rect(screen, (56, 74, 12), bg_rect, 2)


    def table(self, res):
        name = user_name.get_value()
        dct = {}
        with open('records.txt') as f:
            f = f.read().split('\n')
            for e in f:
                e = e.split(':   ')
                dct[e[0]] = int(e[1])
        dct[name] = max(dct.get(name, -1), res)
        f1 = sorted(dct.keys(), key=lambda a: dct[a], reverse=True)
        with open('records.txt', 'w') as f:
            t = 0
            for e in f1[:5]:
                t += 1
                f.write(e + ':   ' + str(dct[e]))
                if t != len(dct):
                    f.write('\n')


pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
apple = pygame.image.load('snake/apple.png').convert_alpha()

game_font = pygame.font.Font(None, 30)
speed = 200

def set_difficulty(value, difficulty):
    global speed
    speed = difficulty * 50


def start_the_game():
    global speed
    clock = pygame.time.Clock()

    main_game = MAIN()

    SCREEN_UPDATE = pygame.USEREVENT
    pygame.time.set_timer(SCREEN_UPDATE, speed)

    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == SCREEN_UPDATE:
                main_game.update()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0, -1)
                elif event.key == pygame.K_DOWN and main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0, 1)
                elif event.key == pygame.K_RIGHT and main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1, 0)
                elif event.key == pygame.K_LEFT and main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1, 0)
                elif event.key == pygame.K_ESCAPE:
                    event.type = pygame.QUIT

        screen.fill((150, 202, 50))
        main_game.draw_elements()
        pygame.display.update()
        clock.tick(5 + main_game.speed)


menu = pygame_menu.Menu('Snake Game', 400, 300,
                        theme=pygame_menu.themes.THEME_SOLARIZED)

user_name = menu.add.text_input('Name :', default='Player 1')
menu.add.selector('Difficulty :', [('Easy', 5), ('Normal', 4), ('Hard', 3), ('Pro', 2), ('Seriously?', 1)],
                  onchange=set_difficulty)
menu.add.button('Start', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)
menu.mainloop(screen)
