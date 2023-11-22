from pico2d import *
import game_world
import game_framework
import random

import server

class Ball:
    image = None

    def __init__(self, x = None, y = None):
        if Ball.image == None:
            Ball.image = load_image('ball21x21.png')
        self.x = x if x else random.randint(100, 1180)
        self.y = y if y else random.randint(100, 924)

    def draw(self):

        self.image.draw(self.x - server.boy.bg.window_left, self.y - server.boy.bg.window_bottom)
        draw_rectangle(*self.get_bb())

    def update(self):
        pass

    def get_bb(self):
        return (self.x - server.boy.bg.window_left - 10, self.y - server.boy.bg.window_bottom - 10,
                self.x - server.boy.bg.window_left + 10, self.y - server.boy.bg.window_bottom + 10)

    def handle_collision(self, group, other):
        # 소년과 충돌시
        if group == 'boy-ball':
            # 공 오브젝트를 제거한다
            game_world.remove_object(self)
