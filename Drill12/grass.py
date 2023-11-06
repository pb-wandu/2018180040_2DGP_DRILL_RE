from pico2d import *

class Grass:
    def __init__(self):
        self.image = load_image('grass.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(400, 30)
        self.image.draw(1200, 30)

        # 디버그용 - 바운딩 박스 그리기
        draw_rectangle(*self.get_bb())

    # 바운딩 박스 가져오기
    def get_bb(self):
        return 0, 0, 1600 - 1, 50


