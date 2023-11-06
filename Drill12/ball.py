from pico2d import *
import game_world
import game_framework

class Ball:
    image = None

    def __init__(self, x = 400, y = 300, velocity = 1):
        if Ball.image == None:
            Ball.image = load_image('ball21x21.png')
        self.x, self.y, self.velocity = x, y, velocity

    def draw(self):
        self.image.draw(self.x, self.y)

        # 디버그용 - 바운딩 박스 그리기
        draw_rectangle(*self.get_bb())

    def update(self):
        self.x += self.velocity * 100 * game_framework.frame_time

        if self.x < 25 or self.x > 1600 - 25:
            game_world.remove_object(self)

    # 바운딩 박스 가져오기
    def get_bb(self):
        return self.x - 10, self.y - 10, self.x + 10, self.y + 10

    # 충돌시 처리
    def handle_collision(self, group, other):
        # boy와 ball이 충돌한 경우
        if group == 'boy-ball':
            # 월드에서 지운다
            game_world.remove_object(self)

        # ball과 zombie가 충돌한 경우
        elif group == 'ball-zombie':
            # 월드에서 지운다
            game_world.remove_object(self)


