from pico2d import *
import game_framework

import game_world
from grass import Grass
from bird import Bird

def handle_events():
    # events = get_events()
    pass

def init():
    global grass
    global bird

    grass = Grass()
    game_world.add_object(grass, 0)

    birds = [Bird() for i in range(10)]
    game_world.add_objects(birds, 1)


def finish():
    game_world.clear()
    pass

def update():
    game_world.update()
    delay(0.1)

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass

