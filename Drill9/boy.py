# 이것은 각 상태들을 객체로 구현한 것임.

from pico2d import *
import math

LEFT, RIGHT = 2, 3

# ----------- 이벤트 확인 함수들 -----------
def space_down(e):
    return e[0] == "INPUT" and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

def a_down(e):
    return e[0] == "INPUT" and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT
def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT
def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT
def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT

def time_out(e):
    return e[0] == "TIME_OUT"

# ----------- 상태들 -----------

# Idle 상태
class Idle:
    @staticmethod
    def enter(boy, e):
        print("Idle enter")

        # 바라보는 방향에 따른 action(세로줄) 지정
        if boy.action == 0:
            boy.action = LEFT
        elif boy.action == 1:
            boy.action = RIGHT

        # 방향, 프레임 초기화 및 대기시간 현재로 지정
        boy.dir = 0
        boy.frame = 0
        boy.wait_time = get_time()
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8

        if get_time() - boy.wait_time > 2:
            boy.state_machine.handle_event(('TIME_OUT', 0))

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)

    @staticmethod
    def exit(boy, e):
        print("Idle exit")
        pass


# Sleep 상태
class Sleep:
    @staticmethod
    def enter(boy, e):
        print("Sleep enter")
        boy.frame = 0

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8

    @staticmethod
    def draw(boy):
        if boy.action == 2:
            boy.image.clip_composite_draw(boy.frame * 100, 200, 100, 100,
                                          -3.141592 / 2, '', boy.x + 25, boy.y - 25, 100, 100)
        else:
            boy.image.clip_composite_draw(boy.frame * 100, 300, 100, 100,
                                          3.141592 / 2, '', boy.x - 25, boy.y - 25, 100, 100)

    @staticmethod
    def exit(boy, e):
        print("Sleep exit")
        pass


# Run 상태
class Run:

    @staticmethod
    def enter(boy, e):
        print("Run enter")

        # 동작에 따른 dir(방향) 및 action(sprite sheet 세로줄) 지정
        if right_down(e) or left_up(e):  # 오른쪽으로 RUN
            boy.dir, boy.action = 1, 1
        elif left_down(e) or right_up(e):  # 왼쪽으로 RUN
            boy.dir, boy.action = -1, 0

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        boy.x += boy.dir * 5
        pass

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y, boy.sizex, boy.sizey)

    @staticmethod
    def exit(boy, e):
        print("Run exit")
        pass

# AutoRun 상태
class Autorun:

    @staticmethod
    def enter(boy, e):
        print("Autorun enter")

        # 현재 action에 따른 dir(방향) 및 action(sprite sheet 세로줄) 지정
        if boy.action == LEFT:
            boy.action = 0
            boy.dir = -1
        elif boy.action == RIGHT:
            boy.action = 1
            boy.dir = 1

        # 소년 y위치 보정
        boy.y = 100

        # 프레임 초기화 및 현재 시간부터 측정 시작
        boy.frame = 0
        boy.start_time = get_time() # 측정 시작 시간
        boy.now_time = 0            # 현재 시간
        boy.check_time = 0          # 시간 확인용

        pass

    @staticmethod
    def do(boy):

        # 프레임 변경 및 이동
        boy.frame = (boy.frame + 1) % 8
        boy.x += boy.dir * 11

        # 이동범위
        if boy.x > 800: boy.x = 0
        elif boy.x < 0: boy.x = 800

        boy.now_time = get_time() # 실시간 시간 확인

        # 1초가 지날 때마다 남은 초 출력
        ### 남은 시간이 얼만지는 확인해야 할 것 같아 추가로 넣은 코드
        if boy.now_time - boy.start_time >= 1:
            boy.check_time += 1 # 확인 시간 1(초) 증가
            print(f"Autorun 시간 {5 - boy.check_time}초 남음")
            boy.start_time = get_time() # 시작 시간 갱신

        # 5초가 지나면 TIME_OUT
        if boy.check_time >= 5:
            boy.state_machine.handle_event(('TIME_OUT', 0))

    @staticmethod
    def draw(boy):
        # 그리기 (Autorun 중에만 확대하여 표시)
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y, boy.sizex * 1.4, boy.sizey * 1.4)

    @staticmethod
    def exit(boy, e):

        boy.y = 90 # 소년 y위치 원래대로

        print("Autorun exit")
        pass

# 상태 확인
class StateMachine:

    # 초기 상태로
    def __init__(self, boy):
        # boy를 지정하고 현재 상태를 Sleep로 한다
        self.boy = boy
        self.cur_state = Sleep

        # 각 상태에서의 동작 전환
        self.transitions = {
            Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run, time_out: Sleep, a_down: Autorun},
            Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle},
            Sleep: {right_down: Run, left_down: Run, right_up: Run, left_up: Run, space_down: Idle},
            Autorun: {time_out: Idle}
        }

    def start(self):
        self.cur_state.enter(self.boy, ('NONE', 0))

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.boy, e)
                self.cur_state = next_state
                self.cur_state.enter(self.boy, e)
                return True
        return False

    def update(self):
        self.cur_state.do(self.boy)

    def draw(self):
        self.cur_state.draw(self.boy)

class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.sizex, self.sizey = 100, 100
        self.frame = 0
        self.action = 3
        self.image = load_image('animation_sheet.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
