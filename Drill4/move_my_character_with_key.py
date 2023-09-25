from pico2d import * # pico2d 전체를 import


CANVASWIDTH, CANVASHEIGHT = 800, 600 # 화면 너비, 높이
LEFT, STOP, RIGHT, UP, DOWN = -1, 0, 1, 10, -10 # 방향

PLAYERSIZEX, PLAYERSIZEY = 60, 120 # 플레이어 크기

running = True # 실행중 여부를 확인하는 변수
nowmovedir = STOP # 현재 이동하는 방향
nowlookdir = RIGHT # 현재 바라보는 방향
nowplx, nowply = CANVASWIDTH//2, CANVASHEIGHT//2 # 현재 플레이어 위치

MOVEAMOUNT = 12 # 이동 거리

MOVING, CROUCHING, JUMPING, NOTHING = 2, 1, 0, -1 # 프레임 종류 (위치에 따름)

nowplayingtype = NOTHING # 현재 동작 종류
nowframe = 0 # 현재 프레임 x위치 번호

# 화면을 연다
open_canvas(CANVASWIDTH, CANVASHEIGHT)

# 이미지 불러오기

img_bg = load_image('TUK_GROUND.png')
img_character = load_image('img_spritesheet.png')


# 화면 업데이트 함수
def canvasupdate():

    global nowmovedir, nowlookdir # 현재 이동방향, 현재 바라보는 방향
    global nowplayingtype, nowframe # 현재 프레임 y위치 번호, x위치 번호
    global nowplx, nowply # 현재 플레이어 위치

    # 화면 초기화
    clear_canvas()

    # 배경 그리기
    img_bg.draw(CANVASWIDTH // 2, CANVASHEIGHT // 2)
            
    # 이동하는 방향별 동작

    startxlist = [0, 0, 0, 0, 0, 0] # 프레임별 자르기 시작하는 x좌표
    
    if nowmovedir == LEFT:
        nowplx -= MOVEAMOUNT
        if nowplx < PLAYERSIZEX/2:
            nowplx = PLAYERSIZEX/2

        nowplayingtype = MOVING
        startxlist = [0, 1000, 1800, 2500, 3300, 4200]
        
    elif nowmovedir == RIGHT:
        nowplx += MOVEAMOUNT
        if nowplx > CANVASWIDTH - PLAYERSIZEX/2:
            nowplx = CANVASWIDTH - PLAYERSIZEX/2

        nowplayingtype = MOVING
        startxlist = [0, 1000, 1800, 2500, 3300, 4200]

    elif nowmovedir == UP:
        nowply += MOVEAMOUNT
        if nowply > CANVASHEIGHT - PLAYERSIZEY/2:
            nowply = CANVASHEIGHT - PLAYERSIZEY/2
            
        nowplayingtype = JUMPING
        startxlist = [0, 900, 1700, 2500, 3300, 4100]
        
    elif nowmovedir == DOWN:
        nowply -= MOVEAMOUNT
        if nowply < PLAYERSIZEY/2:
            nowply = PLAYERSIZEY/2
            
        nowplayingtype = CROUCHING
        startxlist = [0, 800, 1550, 2250, 3400, 4200]

    elif nowmovedir == STOP:
        nowplayingtype = NOTHING

    # 멈춰있는 상태
    if nowplayingtype == NOTHING:

        # 프레임 변경
        if nowframe < 1:
            nowframe += 1
        else:
            nowframe = 0
        
        # (점프 1,2번째 프레임과 동일한 이미지)
        startx, starty = nowframe * 900, 0 # 자르기 시작하는 지점
        cutsizex, cutsizey = 800, 1600 # 자르는 크기
        showsizex, showsizey = 60, 120 # 보여주는 크기

        delay(0.3) # 동작 사이의 지연 시간
        
        pass

    # 동작중인 상태
    else:

        # 프레임 변경
        if nowframe < 5:
            nowframe += 1
        else:
            nowframe = 0

        # 캐릭터 그리기용 디폴트값들
        startx = startxlist[nowframe] # 자르기 시작하는 지점
        starty = nowplayingtype * 1600 # 자르기 시작하는 지점
        cutsizex, cutsizey = 800, 1600 # 자르는 크기
        showsizex, showsizey = PLAYERSIZEX, PLAYERSIZEY # 보여주는 크기

        # 예외 처리 - 이외에는 디폴트값
        if nowplayingtype == CROUCHING and nowframe == 0:
            cutsizex, showsizex = 750, 55
        elif nowplayingtype == CROUCHING and nowframe == 1:
            cutsizex, showsizex = 650, 50
        elif nowplayingtype == CROUCHING and nowframe == 2:
            cutsizex, showsizex = 600, 45
        elif nowplayingtype == CROUCHING and nowframe == 3:
            cutsizex, showsizex = 1000, 75
            cutsizey, showsizey = 1500, 105
            starty = 1680
        elif nowplayingtype == JUMPING and nowframe == 3:
            cutsizey, showsizey = 1700, 123

        delay(0.06) # 동작 사이의 지연 시간

        pass
        
    # 오른쪽을 보고 있으면 그대로 표시
    if nowlookdir == RIGHT:
        img_character.clip_draw(startx, starty, cutsizex, cutsizey, nowplx, nowply, showsizex, showsizey)

    # 왼쪽을 보고 있으면 좌우반전 표시
    elif nowlookdir == LEFT:
        img_character.clip_composite_draw(startx, starty, cutsizex, cutsizey, 0, 'h', nowplx, nowply, showsizex, showsizey)
        
    # 화면 업데이트
    update_canvas()
    
    pass

# 동작 확인하는 함수
def handle_events():

    global running # 실행중 여부 변수
    global nowmovedir, nowlookdir # 현재 이동방향, 현재 바라보는 방향
    global nowplx, nowply # 현재 플레이어 위치
    global nowframe # 현재 프레임

    events = get_events()

    # 이벤트에 따른 동작 수행
    for event in events:
        
        # 종료인 경우
        if event.type == SDL_QUIT:
            running = False

        # 키가 눌렸을 때
        elif event.type == SDL_KEYDOWN:

            # 오른쪽 화살표키 : 오른쪽 방향
            if event.key == SDLK_RIGHT:
                nowmovedir = RIGHT
                nowlookdir = RIGHT

            # 왼쪽 화살표키 : 왼쪽 방향
            elif event.key == SDLK_LEFT:
                nowmovedir = LEFT
                nowlookdir = LEFT

            # 위쪽 화살표키 : 점프 동작
            elif event.key == SDLK_UP:
                nowmovedir = UP

            # 아래쪽 화살표키 : 웅크리기 동작
            elif event.key == SDLK_DOWN:
                nowmovedir = DOWN

            # esc키 누를시 종료
            elif event.key == SDLK_ESCAPE:
                running = False

        # 키가 떼어졌을 때
        elif event.type == SDL_KEYUP:

            # 프레임 초기화

            nowframe = 0

            # 이동하는 방향을 STOP으로 한다
            # 동작을 NOTHING (아무것도 안 함)으로 한다
            # 바라보는 방향은 유지
            
            if event.key == SDLK_RIGHT:
                nowmovedir = STOP
                nowplayingtype = NOTHING
                
            elif event.key == SDLK_LEFT:
                nowmovedir = STOP
                nowplayingtype = NOTHING

            elif event.key == SDLK_UP:
                nowmovedir = STOP
                nowplayingtype = NOTHING
                
            elif event.key == SDLK_DOWN:
                nowmovedir = STOP
                nowplayingtype = NOTHING

    pass

# 실행중일 경우
while running:

    canvasupdate() # 화면 업데이트 함수
    handle_events() # 동작 확인하는 함수

# 화면을 닫는다
close_canvas()
