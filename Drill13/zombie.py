from pico2d import *

import random
import math
import game_framework
import game_world
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector
import play_mode


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

animation_names = ['Walk', 'Idle']


class Zombie:
    images = None

    def load_images(self):
        if Zombie.images == None:
            Zombie.images = {}
            for name in animation_names:
                Zombie.images[name] = [load_image("./zombie/" + name + " (%d)" % i + ".png") for i in range(1, 11)]
            Zombie.font = load_font('ENCR10B.TTF', 40)
            Zombie.marker_image = load_image('hand_arrow.png')


    def __init__(self, x=None, y=None):
        self.x = x if x else random.randint(100, 1180)
        self.y = y if y else random.randint(100, 924)
        self.load_images()
        self.dir = 0.0      # radian 값으로 방향을 표시
        self.speed = 0.0
        self.frame = random.randint(0, 9)
        self.state = 'Idle'
        self.ball_count = 0

        self.tx, self.ty = 0, 0
        self.build_behavior_tree()

        self.patrol_locations = [(43, 274), (1118, 274), (1050, 494), (575, 804), (235, 991), (575, 804), (1050, 494),
                                 (1118, 274)]
        self.loc_no = 0


    def get_bb(self):
        return self.x - 50, self.y - 50, self.x + 50, self.y + 50

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        self.bt.run()

    def draw(self):
        if math.cos(self.dir) < 0:
            Zombie.images[self.state][int(self.frame)].composite_draw(0, 'h', self.x, self.y, 100, 100)
        else:
            Zombie.images[self.state][int(self.frame)].draw(self.x, self.y, 100, 100)
        self.font.draw(self.x - 10, self.y + 60, f'{self.ball_count}', (0, 0, 255))
        draw_rectangle(*self.get_bb())

    # 이벤트 받기 (없음)
    def handle_event(self, event):
        pass

    # 충돌 처리
    def handle_collision(self, group, other):
        if group == 'zombie:ball':
            self.ball_count += 1
    # 이동
    def move_slightly_to(self, tx, ty):
        self.dir = math.atan2(ty - self.y, tx - self.x)
        self.speed = RUN_SPEED_PPS
        self.x += self.speed * math.cos(self.dir) * game_framework.frame_time
        self.y += self.speed * math.sin(self.dir) * game_framework.frame_time

    # 반대편으로 이동
    def move_slightly_opposite_to(self, tx, ty):
        self.dir = math.atan2(ty - self.y, tx - self.x)
        self.speed = RUN_SPEED_PPS
        self.x -= self.speed * math.cos(self.dir) * game_framework.frame_time
        self.y -= self.speed * math.sin(self.dir) * game_framework.frame_time

    # 배회
    def wander_move(self, r=0.5):
        self.state = 'Walk'
        self.move_slightly_to(self.tx, self.ty)
        if self.distance_less_than(self.tx, self.ty, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    # 랜덤 위치 설정
    def set_random_location(self):
        self.tx, self.ty = random.randint(100, 1280 - 100), random.randint(100, 1024 - 100)
        return BehaviorTree.SUCCESS

    # 거리가 r 이내인지 판정
    def distance_less_than(self, x1, y1, x2, y2, r):
        distance2 = (x1 - x2) ** 2 + (y1 - y2) ** 2
        return distance2 < (PIXEL_PER_METER * r) ** 2

    # 소년이 r 이내에 있고 self(좀비)가 소년보다 공이 많거나 같은지 확인
    def checkIfChase(self, r):
        if self.distance_less_than(play_mode.boy.x, play_mode.boy.y, self.x, self.y, r)\
                and self.ball_count >= play_mode.boy.ball_count:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    # 소년이 r 이내에 있고 self(좀비)가 소년보다 공이 적은지 확인
    def checkIfRunaway(self, r):
        if self.distance_less_than(play_mode.boy.x, play_mode.boy.y, self.x, self.y, r)\
                and self.ball_count < play_mode.boy.ball_count:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    # 소년에게로 이동 (추격)
    def chase_boy(self, r=0.5):
        self.state = 'Walk'
        self.move_slightly_to(play_mode.boy.x, play_mode.boy.y)
        if self.distance_less_than(play_mode.boy.x, play_mode.boy.y, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    # 소년 반대편으로 이동 (도망)
    def runaway_from_boy(self, r=0.5):
        self.state = 'Walk'
        self.move_slightly_opposite_to(play_mode.boy.x, play_mode.boy.y)
        if self.distance_less_than(play_mode.boy.x, play_mode.boy.y, self.x, self.y, r):
            return BehaviorTree.RUNNING
        else:
            return BehaviorTree.SUCCESS

    # 행동 트리
    def build_behavior_tree(self):

        # 소년 추격
        con1 = Condition('소년과의 거리 <= 7km and 공 개수 >= 소년의 공 개수', self.checkIfChase, 7)
        act1 = Action('추적', self.chase_boy)
        SEQ_chase = Sequence('시퀀스', con1, act1)

        # 소년으로부터 도망
        con2 = Condition('소년과의 거리 <= 7km and 공 개수 < 소년의 공 개수', self.checkIfRunaway, 7)
        act2 = Action('도망', self.runaway_from_boy)
        SEQ_runaway = Sequence('시퀀스', con2, act2)

        # 배회
        act3 = Action('랜덤 위치 지정', self.set_random_location)
        act4 = Action('지정 위치로 이동', self.wander_move)
        SEQ_wander = Sequence('순찰', act3, act4)

        # 행동 셀렉터
        SEL_zombieActions = Selector('추적 또는 도망 또는 배회', SEQ_chase, SEQ_runaway, SEQ_wander)

        # 행동 트리 지정
        self.bt = BehaviorTree(SEL_zombieActions)

