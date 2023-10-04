# Drill #8. 공들의 자유 낙하 구현

from pico2d import *
import random

# ------ 사용자 정의 클래스 ------

# 잔디 클래스
class Grass:

    # 생성자 - 모든 클래스 안에 기본적으로 들어감
    # 객체가 생성될 때 처음으로 호출되는 함수 (초기 상태 설정)
    # self : 클래스 안에서 함수를 정의할 때의 1번째 인수 - 생성된 객체 그 자신
    def __init__(self):
        # 자기 자신의 image를 설정한다
        self.image = load_image('grass.png')

    # Grass를 화면에 표시한다(그린다)
    def draw(self):
        # 자기 자신의 image를 그리다
        self.image.draw(400, 30)

    # Grass의 상태를 갱신한다
    # Grass는 늘 그대로이므로 의미가 없지만 통일성을 위해 둔 함수
    def update(self): pass

# 소년 클래스
class Boy:
    def __init__(self):
        self.x, self.y = random.randint(100, 700), 90
        self.frame = random.randint(0, 7)
        self.image = load_image("run_animation.png")

    def update(self):
        self.frame = (self.frame + 1) % 8
        self.x += 5

    def draw(self):
        self.image.clip_draw(self.frame*100, 0, 100, 100, self.x, self.y)

# 공 클래스
class Ball:
    def __init__(self):

        # x, y좌표와 낙하속도 지정
        self.x, self.y = random.randint(100, 700), 599
        self.spd = random.randint(5, 12)

        # 종류에 따라 공 이미지 지정
        self.type = random.randint(1, 2)
        if self.type == 1:
            self.image = load_image("ball41x41.png")
        elif self.type == 2:
            self.image = load_image("ball21x21.png")

    def update(self):
        # 속도에 맞춰 y좌표를 아래로 이동(낙하)
        self.y -= self.spd
        # 땅에 닿았다면 땅에 멈추고 속도를 0으로 한다
        # 공의 종류에 따른 좌표 보정
        if self.type == 1 and self.y <= 68:
            self.y = 68
            self.spd = 0
        elif self.type == 2 and self.y <= 58:
            self.y = 58
            self.spd = 0

    def draw(self):
        # 공 이미지 그리기
        self.image.draw(self.x, self.y)

# ------ 사용자 정의 함수 ------

# 사용자 입력 받기
def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False

# world 초기화
def reset_world():
    global running
    global world

    global grass
    global team
    global balls

    running = True # 게임 실행중 여부
    world = [] # 오브젝트들을 담는 list

    # Grass 객체 grass를 생성하고 world에 더한다
    grass = Grass()
    world.append(grass)

    # Boy 11개가 있는 list를 생성하고 world에 더한다
    team = [Boy() for i in range(11)]
    world += team

    # Ball 20개가 있는 list를 생성하고 world에 더한다
    balls = [Ball() for i in range(20)]
    world += balls

# world 업데이트
def update_world():
    # world 안에 있는 객체들을 update한다
    for obj in world:
        obj.update()

# world 그리기
def render_world():
    clear_canvas()
    # world 안에 있는 객체들을 draw한다
    for obj in world:
        obj.draw()
    update_canvas()

# ------ 프로그램 실행 ------

# 화면 열기
open_canvas()

# world 초기화
reset_world()

# 게임 실행
while running:
    handle_events() # 사용자 입력 받기
    update_world()  # world 업데이트
    render_world()  # world 그리기
    delay(0.05)

# 화면 닫기
close_canvas()
