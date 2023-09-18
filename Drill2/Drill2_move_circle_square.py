from pico2d import * # Pico2d 모듈 import
import math          # Math 모듈 import

open_canvas() # 화면 열기

# 이미지 가져오기
grass = load_image('img_grass.png')
character = load_image('img_character.png')

STARTX, STARTY = 400, 90 # 시작시 x, y좌표
RIGHT, UP, LEFT, DOWN = 11, 12, 13, 14 # 이동 방향
CIRCLESIZE = 200 # 원 크기

movex, movey = 0, 0 # x, y 이동거리
movedir = RIGHT # 이동 방향
nowangle = 0  # 현재 각도

movetype = "circle" # 이동 종류 : rect <-> circle

# 무한히 실행된다
while True:
    
    clear_canvas() # 화면 초기화

    # 이동 종류가 "사각형 이동"일 경우
    if movetype == "rect":

        # 오른쪽 이동
        if movedir == RIGHT:
            movex += 10
            
            if movex == 300:
                # 위쪽 방향으로 이동 방향 변경
                movedir = UP
                
            # 출발지점으로 돌아왔다면 "원형 이동"으로 전환
            elif movex == 0:
                movetype = "circle"
                nowangle = 0  # 현재 각도 초기화

        # 위쪽 이동
        elif movedir == UP:
            movey += 10
            
            if movey == 400:
                # 왼쪽 방향으로 이동 방향 변경
                movedir = LEFT
                
        # 왼쪽 이동
        if movedir == LEFT:
            movex -= 10
            
            if movex == -300:
                # 위쪽 방향으로 이동 방향 변경
                movedir = DOWN
                
        # 아래쪽 이동
        elif movedir == DOWN:
            movey -= 10
            
            if movey == 0:
                # 왼쪽 방향으로 이동 방향 변경
                movedir = RIGHT

    # 이동 종류가 "원형 이동"일 경우
    elif movetype == "circle":

        # 각도에 따른 x, y 이동거리
        movex = CIRCLESIZE * math.sin(nowangle % 360 / 360 * 2 * math.pi)
        movey = CIRCLESIZE + 200 * math.cos((180 + nowangle) % 360 / 360 * 2 * math.pi)

        # 각도를 5도씩 반시계 방향으로 돌린다
        nowangle += 5 

        # 한 바퀴 다 돌았을 경우 "사각형 이동"으로 전환
        if nowangle > 360:  
            movex, movey = 0, 0 # 이동길이 초기화 (<-오차 수정)
            movetype = 'rect'

    # 풀의 위치는 변하지 않는다
    grass.draw(400, 30)
    # 캐릭터의 위치 (시작지점을 기준으로)
    character.draw(STARTX + movex, STARTY + movey)

    update_canvas() # 화면 그리기
    delay(0.01) # 다음 동작까지의 대기시간
    get_events()
    
close_canvas() # 화면 닫기
