from pico2d import *
import math

open_canvas()

grass=load_image('grass.png')
character=load_image('character.png')
x=0
y=90

def render_all(x,y):
    clear_canvas_now()
    grass.draw_now(400, 30)
    character.draw_now(x, y)
    delay(0.02)

def run_rectagle():
    
    print("rectagle")

    #오른쪽 이동
    for x in range(400, 780+1, 10):
        render_all(x, 90)
        
    #위쪽 이동
    for y in range(90, 550+1, 10):
        render_all(780, y)
        
    #왼쪽 이동
    for x in range(750, 20-1, -10):
        render_all(x, 550)
        
    #아래쪽 이동
    for y in range(550, 90-1, -10):
        render_all(20, y)
        
    #원 운동 시작점까지 이동
    for x in range(20, 400+1, 10):
        render_all(x, 90)
    pass

def run_circle():

    print("circle")
        
    cx, cy, r = 400, 300, 200
    for deg in range(-90, 270, 5):
        x = cx + r * math.cos(deg/360 * 2 * math.pi)
        y = cy + r * math.sin(deg/360 * 2 * math.pi)
        render_all(x,y)

while (True):
    run_rectagle()
    run_circle()
    # break
    

close_canvas()
