import math
from random import randint, random

import tkinter as tk

from gamelib import Sprite, GameApp, Text

from consts import *


class SlowFruit(Sprite):
    fruit_type = 'slow'

    def __init__(self, app, x, y):
        super().__init__(app, 'images/apple.png', x, y)

        self.app = app

    def update(self):
        self.y += FRUIT_SLOW_SPEED

        if self.y > CANVAS_WIDTH + 30:
            self.to_be_deleted = True

    def is_out_of_screen_left(self):
        if self.x < 20:
            return True
        return False

    def is_out_of_screen_right(self):
        if self.x > CANVAS_WIDTH - 20:
            return True
        return False

    def reappear_1(self):
        self.x = CANVAS_WIDTH - 20

    def reappear_2(self):
        self.x = 20


class FastFruit(Sprite):
    fruit_type = 'fast'

    def __init__(self, app, x, y):
        super().__init__(app, 'images/banana.png', x, y)

        self.app = app

    def update(self):
        self.y += FRUIT_FAST_SPEED

        if self.y > CANVAS_WIDTH + 30:
            self.to_be_deleted = True

    def is_out_of_screen_left(self):
        if self.x < 20:
            return True
        return False

    def is_out_of_screen_right(self):
        if self.x > CANVAS_WIDTH - 20:
            return True
        return False

    def reappear_1(self):
        self.x = CANVAS_WIDTH - 20

    def reappear_2(self):
        self.x = 20


class SlideFruit(Sprite):
    fruit_type = 'slide'

    def __init__(self, app, x, y):
        super().__init__(app, 'images/cherry.png', x, y)

        self.app = app
        self.direction = randint(0, 1)*2 - 1

    def update(self):
        self.y += FRUIT_FAST_SPEED
        self.x += self.direction * 5

        if self.y > CANVAS_WIDTH + 30:
            self.to_be_deleted = True

    def is_out_of_screen_left(self):
        if self.x < 20:
            return True
        return False

    def is_out_of_screen_right(self):
        if self.x > CANVAS_WIDTH - 20:
            return True
        return False

    def reappear_1(self):
        self.x = CANVAS_WIDTH - 20

    def reappear_2(self):
        self.x = 20


class CurvyFruit(Sprite):
    fruit_type = 'curvy'

    def __init__(self, app, x, y):
        super().__init__(app, 'images/pear.png', x, y)

        self.app = app
        self.t = randint(0,360) * 2 * math.pi / 360

    def update(self):
        self.y += FRUIT_SLOW_SPEED * 1.2
        self.t += 1
        self.x += math.sin(self.t*0.08)*10

        if self.y > CANVAS_WIDTH + 30:
            self.to_be_deleted = True

    def is_out_of_screen_left(self):
        if self.x < 20:
            return True
        return False

    def is_out_of_screen_right(self):
        if self.x > CANVAS_WIDTH - 20:
            return True
        return False

    def reappear_1(self):
        self.x = CANVAS_WIDTH - 20

    def reappear_2(self):
        self.x = 20


class Basket(Sprite):
    def __init__(self, app, x, y):
        super().__init__(app, 'images/basket.png', x, y)

        self.app = app
        self.direction = None

    def update(self):
        if self.direction == BASKET_LEFT:
            if self.x >= BASKET_MARGIN:
                self.x -= BASKET_SPEED
        elif self.direction == BASKET_RIGHT:
            if self.x <= CANVAS_WIDTH - BASKET_MARGIN:
                self.x += BASKET_SPEED

    def check_collision(self, fruit):
        if self.distance_to(fruit) <= BASKET_CATCH_DISTANCE:
            if fruit.fruit_type == 'slow':
                fruit.to_be_deleted = True
                self.app.score += 1
                self.app.update_score()
            elif fruit.fruit_type == 'fast' or fruit.fruit_type == 'slide':
                fruit.to_be_deleted = True
                self.app.score += 2
                self.app.update_score()
            elif fruit.fruit_type == 'curvy':
                fruit.to_be_deleted = True
                self.app.score += 3
                self.app.update_score()

    def is_out_of_screen_left(self):
        if self.x < 25:
            return True
        return False

    def is_out_of_screen_right(self):
        if self.x > CANVAS_WIDTH - 25:
            return True
        return False

    def reappear_1(self):
        self.x = CANVAS_WIDTH - 25

    def reappear_2(self):
        self.x = 25

    def set_next_direction(self, direction):
        self.next_direction = direction


class BasketGame(GameApp):
    def init_game(self):
        self.basket = Basket(self, CANVAS_WIDTH // 2, CANVAS_HEIGHT - 50)
        self.elements.append(self.basket)

        self.score = 0
        self.score_text = Text(self, 'Score: 0', 100, 40)
        self.fruits = []

        self.command = {'Left': self.get_next_direction_function(self.basket, BASKET_LEFT),
                        'Right': self.get_next_direction_function(self.basket, BASKET_RIGHT)
                        }

    def update_score(self):
        self.score_text.set_text('Score: ' + str(self.score))

    def random_fruits(self):
        if random() > 0.95:
            p = random()
            x = randint(50, CANVAS_WIDTH - 50)
            if p <= 0.3:
                new_fruit = SlowFruit(self, x, 0)
            elif p <= 0.6:
                new_fruit = FastFruit(self, x, 0)
            elif p <= 0.8:
                new_fruit = SlideFruit(self, x, 0)
            else:
                new_fruit = CurvyFruit(self, x, 0)

            self.fruits.append(new_fruit)

    def process_collisions(self):
        for f in self.fruits:
            self.basket.check_collision(f)

    def update_and_filter_deleted(self, elements):
        new_list = []
        for e in elements:
            e.update()
            e.render()
            if e.to_be_deleted:
                e.delete()
            else:
                new_list.append(e)

        for fruit in self.fruits:
            if fruit.is_out_of_screen_left():
                fruit.reappear_1()
            if fruit.is_out_of_screen_right():
                fruit.reappear_2()

        return new_list

    def post_update(self):
        self.process_collisions()
        if self.basket.is_out_of_screen_left():
            self.basket.reappear_1()
        if self.basket.is_out_of_screen_right():
            self.basket.reappear_2()

        self.random_fruits()

        self.fruits = self.update_and_filter_deleted(self.fruits)

    def on_key_pressed(self, event):
        ch = event.char.upper()
        if ch in self.command:
            self.command[ch]()

    def get_next_direction_function(self, basket, next_direction):
        def f():
            basket.set_next_direction(next_direction)
        return f
    

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Basket Fighter")
 
    # do not allow window resizing
    root.resizable(False, False)
    app = BasketGame(root, CANVAS_WIDTH, CANVAS_HEIGHT, UPDATE_DELAY)
    app.start()
    root.mainloop()
