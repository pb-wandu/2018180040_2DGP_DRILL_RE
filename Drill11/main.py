from pico2d import open_canvas, delay, close_canvas
import game_framework

import play_mode as start_mode

open_canvas(800, 600, sync=True)
game_framework.run(start_mode)
close_canvas()

# 코드 설명

"""

def getPixelPerSecond(km):
    PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
    mph = (km * 1000.0) # 시간당 미터
    mpm = (mph / 60.0) # 분당 미터
    mps = (mpm / 60.0) # 초당 미터
    pps = (mps * PIXEL_PER_METER) # 초당 픽셀
    return pps

# bird의 초당 픽셀 속도는 '시간당 5~60미터'를 '초당 픽셀'로 변환하는 함수를 사용하여 랜덤 지정
bird.pps = getPixelPerSecond(random.uniform(5, 60))

TIME_PER_ACTION = 0.1
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 14

# 동작당 프레임은 14개 있으며, 날갯짓 동작당 0.1초의 시간을 사용한다

if obj.movedir == RIGHT:
    obj.image.clip_draw(182 * framex, 170 * framey, 180, 160, obj.x, obj.y, 100, 80)
elif obj.movedir == LEFT:
    obj.image.clip_composite_draw(182 * framex, 170 * framey, 180, 160, 0, 'h', obj.x, obj.y, 100, 80)
    
# 새의 크기는 (100, 80) 으로 그렸으며 위치에 따라 맞는 방향을 바라보게 했다

"""