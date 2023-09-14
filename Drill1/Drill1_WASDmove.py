import turtle

movelength = 50 # 한 번에 이동하는 거리

# 각 위치 이동 함수

def move_up():
    turtle.setheading(90) # 위쪽 바라보기
    turtle.forward(movelength) # 바라보는 방향으로 이동
    turtle.stamp() # 도장을 찍는다

def move_down():
    turtle.setheading(270) # 아래쪽 바라보기
    turtle.forward(movelength) # 바라보는 방향으로 이동
    turtle.stamp() # 도장을 찍는다

def move_left():
    turtle.setheading(180) # 왼쪽 바라보기
    turtle.forward(movelength) # 바라보는 방향으로 이동
    turtle.stamp() # 도장을 찍는다

def move_right():
    turtle.setheading(0) # 오른쪽 바라보기
    turtle.forward(movelength) # 바라보는 방향으로 이동
    turtle.stamp() # 도장을 찍는다

# --- 여기서부터 코드 실행됨 ---

# turtle의 모양을 "turtle"로 설정한다
turtle.shape("turtle")

# 키 입력에 따라 동작(함수)을 수행한다
turtle.onkey(move_up, 'w')
turtle.onkey(move_left, 'a')
turtle.onkey(move_down, 's')
turtle.onkey(move_right, 'd')

# 키 입력을 인식한다
turtle.listen()
