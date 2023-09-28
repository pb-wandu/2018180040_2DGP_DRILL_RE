# (전체적인 코드 컨셉은 Drill #5와 동일)

# Drill 5와 다른 점
# "newhand" 대신 "waiting" 상태에서 시작한다 ("newhand"에 있던 동작은 클릭시 수행으로 변경)
# 다수의 손 화살표 위치 데이터를 받는 배열을 만들어 표시한다
# nowstate == "waiting"에서 남은 화살표가 없다면 대기한다
# h_a는 hand_arrow (손 화살표) 줄임말

from pico2d import * # pico2d 모듈 import
import random # random 모듈 import

BG_WIDTH, BG_HEIGHT = 800, 600 # 배경 크기
open_canvas(BG_WIDTH, BG_HEIGHT) # 화면 열기

UNDEF = -100 # 지정되지 않음

# 이미지 불러오기
img_bg = load_image('TUK_GROUND.png')
img_boy = load_image('animation_sheet.png')
img_handarrow = load_image('hand_arrow.png')

# ---------------- 변수들 ----------------

boy_frame = 0 # 현재 소년 프레임
nowplayerx, nowplayery = BG_WIDTH // 2, BG_HEIGHT // 2 # 현재 소년 위치
nowhandx, nowhandy = BG_WIDTH // 2, BG_HEIGHT // 2     # 현재 손 위치

startx, starty = 0, 0 # 이동 시작점 (그 순간의 플레이어 위치)
endx, endy = 0, 0     # 이동 끝점   (그 순간의 손 화살표 위치)

nowmovepercent = 0 # 현재 이동한 정도

nowlookingdir = "right" # 현재 바라보는 방향 - "right" / "left"
nowplayerstate = "standing" # 현재 플레이어 상태 - "standing" <-> "moving"

# nowstate(현재 상태)는 "waiting" -> "following" -> "arrive" -> 반복
# 각각 새로운 손화살표를 표시한다 / 소년이 손을 향하여 간다 / 소년이 손에 도착한다
nowstate = "waiting"

running = True # 실행 여부

# 손 화살표 위치들을 저장하는 리스트
h_a_place_list = [[UNDEF, UNDEF] for n in range(100)]
now_target_h_a = 0 # 현재 캐릭터(소년)가 목표로 하는 손 화살표의 리스트에서의 위치 (0~99)
now_addplace_h_a = 0 # 현재 (사용자가) 손 화살표를 더할 리스트에서의 위치 (0~99)

clickedx, clickedy = 0, 0 # 클릭한 좌표

# ---------------- 함수들 ----------------

# 새로운 손 화살표 표시
def show_newhand(x, y):
    global h_a_place_list # 손 화살표 위치들을 저장하는 리스트
    global now_addplace_h_a # 현재 (사용자가) 손 화살표를 더할 리스트에서의 위치 (0~99)

    # 해당 리스트 위치에 새로운 손 화살표(의 좌표)를 추가한다
    h_a_place_list[now_addplace_h_a][0] = x
    h_a_place_list[now_addplace_h_a][1] = y

    # 리스트 위치를 옆으로 이동 (끝까지 이동했다면 가장 앞으로 이동)
    now_addplace_h_a += 1
    if now_addplace_h_a == 100:
        now_addplace_h_a = 0

# 손 화살표들 그리기

def hand_arrows_draw():
    global h_a_place_list  # 손 화살표 위치들을 저장하는 리스트

    # 저장된 좌표들에 대하여
    for [x, y] in h_a_place_list:
        # 좌표값이 UNDEF가 아닐 경우
        if x != UNDEF:
            img_handarrow.draw(x, y)  # 현재 손 위치에 따라 손 그리기

# 소년 애니메이션 그리기
def boy_animation_draw():
    global boy_frame # 현재 소년 프레임
    global nowplayerx, nowplayery # 현재 소년 위치
    global nowlookingdir, nowplayerstate # 현재 바라보는 방향, 플레이어 상태

    frameline = 0 # Animation Sheet에서 표시할 프레임 (y방향 기준 순서)
    if nowplayerstate == "standing":
        frameline = 3
    elif nowplayerstate == "running":
        frameline = 1

    boy_frame = (boy_frame + 1) % 8 # 프레임 이동
    delay(0.07)  # 동작 사이의 지연 시간

    # 캐릭터 그리기용 디폴트값들
    st_x, st_y = boy_frame * 100, frameline * 100 # 자르기 시작하는 지점
    cutsizex, cutsizey = 100, 100  # 자르는 크기
    showsizex, showsizey = 80, 60  # 보여주는 크기

    # 오른쪽을 보고 있으면 그대로 표시
    if nowlookingdir == "right":
        img_boy.clip_draw(st_x, st_y, cutsizex, cutsizey, nowplayerx, nowplayery, showsizex, showsizey)
    # 왼쪽을 보고 있으면 좌우반전 표시
    elif nowlookingdir == "left":
        img_boy.clip_composite_draw(st_x, st_y, cutsizex, cutsizey, 0, 'h', nowplayerx, nowplayery, showsizex, showsizey)

# 이미지 그리기

def draw_objects():
    img_bg.draw(BG_WIDTH // 2, BG_HEIGHT // 2)  # 배경 그리기
    hand_arrows_draw()   # 손 화살표들 그리기
    boy_animation_draw() # 소년 애니메이션 그리기

# 상태에 따른 동작 수행

def state_manager_function():
    global startx, starty, endx, endy # 이동 시작점, 이동 끝점
    global nowlookingdir, nowplayerstate  # 현재 바라보는 방향 / 현재 플레이어 상태
    global nowmovepercent # 현재 이동한 정도(%)
    global nowstate # 현재 상태
    global nowplayerx, nowplayery # 현재 플레이어 위치
    global nowhandx, nowhandy # 현재 손 화살표 위치
    global now_target_h_a # 현재 목표로 한 손 화살표의 리스트에서의 위치

    # 상태에 따른 동작 수행 "waiting" -> "following" -> "arrive" -> 반복

    # 손 바꾸기 상태
    if nowstate == "waiting":

        # 다음 목표 손 화살표의 x, y 좌표
        next_target_h_a_x = h_a_place_list[now_target_h_a][0]
        next_target_h_a_y = h_a_place_list[now_target_h_a][1]

        # 다음에 이동할 손 화살표(의 좌표)가 존재한다면 (UNDEF가 아니라면)
        if next_target_h_a_x != UNDEF:

            startx, starty = nowplayerx, nowplayery           # 이동 시작점 (그 순간의 플레이어 위치)
            endx, endy = next_target_h_a_x, next_target_h_a_y # 이동 끝점   (그 순간의 손 화살표 위치)

            # 플레이어 위치와 손 화살표 위치를 비교하여 바라보는 위치 지정
            if nowplayerx < next_target_h_a_x:
                nowlookingdir = "right"
            else:
                nowlookingdir = "left"

            nowmovepercent = 0  # 현재 이동한 정도(%) 초기화

            # 다음 상태로 변경
            nowstate = "following"
        pass

    # 소년이 손을 따라가는 상태
    elif nowstate == "following":
        nowplayerstate = "running" # 달려감 상태로 변경

        nowmovepercent += 5 # 현재 이동한 정도(%) 증가

        # 이동한 정도에 따른 플레이어 위치
        nowplayerx = (1 - nowmovepercent / 100) * startx + nowmovepercent / 100 * endx
        nowplayery = (1 - nowmovepercent / 100) * starty + nowmovepercent / 100 * endy

        # 이동한 %가 100%에 도달하면 - 다음 상태로 변경
        if nowmovepercent == 100:
            nowstate = "arrive"
        pass

    # 소년이 손에 도착한 상태
    elif nowstate == "arrive":
        nowplayerstate = "standing" # 서있음 상태로 변경

        # 현재 목표로 한 손 화살표 지우고 다음 목표로 변경
        h_a_place_list[now_target_h_a] = [UNDEF, UNDEF]
        now_target_h_a += 1

        # 다음 상태로 변경
        nowstate = "waiting"
        pass

# 이벤트에 따른 동작 수행

def handle_events():
    global running
    global clickedx, clickedy # 클릭한 좌표 위치

    events = get_events()
    for event in events:

        # 종료시 running 종료
        if event.type == SDL_QUIT:
            running = False

        # 마우스 이동
        elif event.type == SDL_MOUSEMOTION:

            # 윈도우 좌표계 -> pico2d 좌표계 변환
            clickedx, clickedy = event.x, BG_HEIGHT - 1 - event.y

        # 마우스 클릭 떼는 순간
        elif event.type == SDL_MOUSEBUTTONUP:

            # 새로운 손 화살표를 만든다
            show_newhand(clickedx, clickedy)

        # esc키 클릭시 running 종료
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False

# ---------------- 프로그램 실행 ----------------

# 실행중일 경우
while running:

    # 상태에 따른 동작 수행
    state_manager_function()

    # 이벤트에 따른 동작 수행
    handle_events()

    # 화면 그리기
    clear_canvas() # 화면 초기화
    draw_objects() # 오브젝트 그리기
    update_canvas() # 화면 업데이트

# 화면을 닫는다
close_canvas()





