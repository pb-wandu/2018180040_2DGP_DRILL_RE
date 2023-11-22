import random
import json
import os

from pico2d import *
import game_framework
import game_world

import server
from boy import Boy
from ball import Ball

from background import FixedBackground as Background

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            server.boy.handle_event(event)



def init():
    server.background = Background()
    game_world.add_object(server.background, 0)
    server.boy = Boy()
    game_world.add_object(server.boy, 1)
    server.boy.set_background(server.background)

    # 100개의 공을 랜덤한 위치에 둔 뒤 월드에 추가한다.
    server.balls = [Ball(
        # 끝에서 40 떨어진 범위까지의 가운데 내에서 랜덤
        random.randint(40, 1800-40), random.randint(40, 1100-40)
        ) for _ in range(100)]
    game_world.add_objects(server.balls, 1)

    # 충돌 처리 대상 조합에 boy-ball을 추가
    game_world.add_collision_pair("boy-ball", server.boy, None)

    for ball in server.balls:
        game_world.add_collision_pair("boy-ball", None, ball)

    pass

def finish():
    game_world.clear()
    pass


def update():
    game_world.update()
    game_world.handle_collisions()

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass



