from pico2d import * # pico2d 모듈 import
import random # random 모듈 import

BG_WIDTH, BG_HEIGHT = 800, 600 # 배경 크기
open_canvas(BG_WIDTH, BG_HEIGHT) # 화면 열기

# 이미지 불러오기
img_bg = load_image('TUK_GROUND.png')
img_boy = load_image('animation_sheet.png')
img_handarrow = load_image('hand_arrow.png')

# 변수들
boy_frame = 0 # 현재 소년 프레임
nowplayerx, nowplayery = BG_WIDTH // 2, BG_HEIGHT // 2 # 현재 소년 위치
nowhandx, nowhandy = BG_WIDTH // 2, BG_HEIGHT // 2     # 현재 손 위치

startx, starty = 0, 0 # 이동 시작점 (그 순간의 플레이어 위치)
endx, endy = 0, 0     # 이동 끝점   (그 순간의 손 화살표 위치)

nowmovepercent = 0 # 현재 이동한 정도

nowlookingdir = "right" # 현재 바라보는 방향 - "right" / "left"
nowplayerstate = "standing" # 현재 플레이어 상태 - "standing" <-> "moving"

# nowstate(현재 상태)는 "newhand" -> "following" -> "arrive" -> 반복
# 각각 새로운 손화살표를 표시한다 / 소년이 손을 향하여 간다 / 소년이 손에 도착한다
nowstate = "newhand"

running = True # 실행 여부

# 함수들

# 새로운 손 화살표 표시
def show_newhand():
    global nowhandx, nowhandy
    nowhandx = random.randint(20, BG_WIDTH - 20)
    nowhandy = random.randint(20, BG_HEIGHT - 20)

# 소년 애니메이션 그리기
def boy_animation_draw():
    global boy_frame # 현재 소년 프레임
    global nowplayerx, nowplayery # 현재 소년 위치
    global nowlookingdir, nowplayerstate # 현재 바라보는 방향, 플레이어 상태

    frameline = 0 # Animation Sheet에서 표시할 프레임 선
    if nowplayerstate == "standing":
        frameline = 3
    elif nowplayerstate == "running":
        frameline = 1

    boy_frame = (boy_frame + 1) % 8 # 프레임 이동
    delay(0.1)  # 동작 사이의 지연 시간

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
    img_handarrow.draw(nowhandx, nowhandy)  # 현재 손 위치에 따라 손 그리기
    boy_animation_draw()  # 소년 애니메이션 그리기

# 상태에 따른 동작 수행

def state_manager_function():
    global startx, starty, endx, endy # 이동 시작점, 이동 끝점
    global nowlookingdir, nowplayerstate  # 현재 바라보는 방향 / 현재 플레이어 상태
    global nowmovepercent # 현재 이동한 정도(%)
    global nowstate # 현재 상태
    global nowplayerx, nowplayery # 현재 플레이어 위치
    global nowhandx, nowhandy # 현재 손 화살표 위치

    # 상태에 따른 동작 수행 "newhand" -> "following" -> "arrive" -> 반복

    # 손 바꾸기 상태
    if nowstate == "newhand":
        show_newhand() # 새로운 손 화살표 표시

        startx, starty = nowplayerx, nowplayery # 이동 시작점 (그 순간의 플레이어 위치)
        endx, endy = nowhandx, nowhandy         # 이동 끝점   (그 순간의 손 화살표 위치)

        # 플레이어 위치와 손 화살표 위치를 비교하여 바라보는 위치 지정
        if nowplayerx < nowhandx:
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

        # 다음 상태로 변경
        nowstate = "newhand"
        pass

# ---------------- 프로그램 실행 ----------------

# 실행중일 경우
while running:

    # 상태에 따른 동작 수행
    state_manager_function()

    # 화면 그리기
    clear_canvas() # 화면 초기화
    draw_objects() # 오브젝트 그리기
    update_canvas() # 화면 업데이트

    # handle_events() # 동작 확인하는 함수

# 화면을 닫는다
close_canvas()





