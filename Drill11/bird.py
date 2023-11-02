# 이것은 각 상태들을 객체로 구현한 것임.
import random

from pico2d import get_time, load_image, load_font, clamp,  SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT
import game_world
import game_framework

def getPixelPerSecond(km):
    PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
    mph = (km * 1000.0) # 시간당 미터
    mpm = (mph / 60.0) # 분당 미터
    mps = (mpm / 60.0) # 초당 미터
    pps = (mps * PIXEL_PER_METER) # 초당 픽셀

    return pps


# Bird 동작 시간
TIME_PER_ACTION = 0.2
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 14

# 새 방향
LEFT, RIGHT = -1, 1

class Fly:

    @staticmethod
    def enter(obj, e):
        pass

    @staticmethod
    def exit(obj, e):
        pass

    @staticmethod
    def do(obj):
        # 0~13
        obj.frame = (obj.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 14

        # RIGHT == 1 / LEFT == -1
        # pps는 해당 오브젝트의 초당 픽셀 속도
        obj.x += obj.movedir * obj.pps * game_framework.frame_time

        if obj.x < 0:
            obj.x = 0 + 5
            obj.movedir = -1 * obj.movedir
        elif obj.x > 800:
            obj.x = 800 - 5
            obj.movedir = -1 * obj.movedir


    @staticmethod
    def draw(obj):
        framex = int(obj.frame % 5)
        framey = 2 - int(obj.frame / 5)

        if obj.movedir == RIGHT:
            obj.image.clip_draw(182 * framex, 170 * framey, 180, 160, obj.x, obj.y, 100, 80)
        elif obj.movedir == LEFT:
            obj.image.clip_composite_draw(182 * framex, 170 * framey, 180, 160, 0, 'h', obj.x, obj.y, 100, 80)

class StateMachine:
    def __init__(self, obj):
        self.obj = obj
        self.cur_state = Fly

    def start(self):
        self.cur_state.enter(self.obj, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.obj)

    def handle_event(self, e):
        """
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.boy, e)
                self.cur_state = next_state
                self.cur_state.enter(self.boy, e)
                return True
        """
        return False

    def draw(self):
        self.cur_state.draw(self.obj)

# 새 클래스

class Bird:
    def __init__(self):
        self.x, self.y = 400, 300
        self.frame = 0
        self.movedir = random.choice([LEFT, RIGHT])
        self.image = load_image('bird_animation.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()

        # 초당 픽셀 속도
        self.pps = getPixelPerSecond(random.uniform(5, 60))

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
