import random
import math
import game_framework

from pico2d import *
import game_world

# zombie Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# zombie Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 10.0

animation_names = ['Walk']

class Zombie:
    images = None

    def load_images(self):
        if Zombie.images == None:
            Zombie.images = {}
            for name in animation_names:
                Zombie.images[name] = [load_image("./zombie/"+ name + " (%d)" % i + ".png") for i in range(1, 11)]

    def __init__(self):
        self.x, self.y = random.randint(1600-800, 1600), 150
        self.load_images()
        self.frame = random.randint(0, 9)
        self.dir = random.choice([-1, 1])

        self.hp = 2 # 좀비의 체력

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        self.x += RUN_SPEED_PPS * self.dir * game_framework.frame_time
        if self.x > 1600:
            self.dir = -1
        elif self.x < 800:
            self.dir = 1
        self.x = clamp(800, self.x, 1600)
        pass


    def draw(self):
        HP2SIZE, HP1SIZE = 200, 100
        
        # 방향에 따라 방향을 다르게 draw한다
        # 현재 hp에 따라 크기를 다르게 draw한다
        
        if self.dir < 0:
            if self.hp == 2:
                Zombie.images['Walk'][int(self.frame)].composite_draw(0, 'h', self.x, self.y, HP2SIZE, HP2SIZE)
            elif self.hp == 1:
                Zombie.images['Walk'][int(self.frame)].composite_draw(0, 'h', self.x, self.y - HP1SIZE/2, HP1SIZE, HP1SIZE)
        else:
            if self.hp == 2:
                Zombie.images['Walk'][int(self.frame)].draw(self.x, self.y, HP2SIZE, HP2SIZE)
            elif self.hp == 1:
                Zombie.images['Walk'][int(self.frame)].draw(self.x, self.y - HP1SIZE/2, HP1SIZE, HP1SIZE)

        # 디버그용 - 바운딩 박스 그리기
        draw_rectangle(*self.get_bb())

    # 바운딩 박스 가져오기
    def get_bb(self):
        HP2SIZE, HP1SIZE = 100, 50

        if self.hp == 2:
            return self.x - HP2SIZE, self.y - HP2SIZE, self.x + HP2SIZE, self.y + HP2SIZE
        elif self.hp == 1:
            return self.x - HP1SIZE, self.y - HP1SIZE * 2, self.x + HP1SIZE, self.y

    def handle_collision(self, group, other):
        # zombie와 ball이 충돌한 경우
        if group == 'ball-zombie':
            self.hp -= 1  # 체력이 1 줄어든다

            # 체력이 0이 된 경우
            if self.hp == 0:
                # 월드에서 해당 오브젝트를 제거한다
                game_world.remove_object(self)

    def handle_event(self, event):
        pass

