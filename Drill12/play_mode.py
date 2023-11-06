import random

from pico2d import *
import game_framework

import game_world
from grass import Grass
from boy import Boy
from ball import Ball
from zombie import Zombie

# boy = None

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            boy.handle_event(event)

def init():
    global grass
    global boy

    running = True

    grass = Grass()
    game_world.add_object(grass, 0)

    boy = Boy()
    game_world.add_object(boy, 1)

    # 50개의 공을 랜덤한 x위치에 둔 뒤 월드에 추가한다.
    global balls
    balls = [Ball(random.randint(100, 1600 - 100), 60, 0) for _ in range(30)]
    game_world.add_objects(balls, 1)

    # 충돌 처리 대상 조합의 a 위치에 boy를 추가
    game_world.add_collision_pair("boy-ball", boy, None)
    # 충돌 처리 대상 조합의 b 위치에 ball을 추가
    for ball in balls:
        game_world.add_collision_pair("boy-ball", None, ball)
        
    # 5개의 좀비를 월드에 추가한다.
    zombies = [Zombie() for _ in range(5)]
    game_world.add_objects(zombies, 1)

    # 충돌 처리 대상 조합의 a 위치에 boy을 추가
    game_world.add_collision_pair("boy-zombie", boy, None)
    # 충돌 처리 대상 조합의 b 위치에 zombie를 추가
    for zombie in zombies:
        game_world.add_collision_pair("boy-zombie", None, zombie)

    # 충돌 처리 대상 조합의 a 위치에 ball_boy를 추가
    # 는 boy.py의 fire_ball() 즉 ball_boy 오브젝트를 추가하는 곳에 코드가 있다
    # 충돌 처리 대상 조합의 b 위치에 zombie를 추가
    for zombie in zombies:
        game_world.add_collision_pair("ball-zombie", None, zombie)

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

