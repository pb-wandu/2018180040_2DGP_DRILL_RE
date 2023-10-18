from pico2d import load_image

class Grass:
    def __init__(self, position):
        self.image = load_image('grass.png')
        self.position = position # 풀 위치

    def draw(self):
        if self.position == "back":
            self.image.draw(400, 60)
        elif self.position == "front":
            self.image.draw(400, 30)

    def update(self):
        pass
