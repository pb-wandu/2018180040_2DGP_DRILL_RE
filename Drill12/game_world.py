objects = [[] for _ in range(4)]

# fill here

def add_object(o, depth = 0):
    objects[depth].append(o)

def add_objects(ol, depth = 0):
    objects[depth] += ol


def update():
    for layer in objects:
        for o in layer:
            o.update()


def render():
    for layer in objects:
        for o in layer:
            o.draw()

# 두 오브젝트간 충돌을 판정하는 함수
def collide(a, b):
    # 각 오브젝트의 바운딩 박스 가져오기
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    # 충돌하지 않은 경우 False 값을 return
    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    # 충돌한 경우 True 값을 return
    return True

def remove_object(o):
    for layer in objects:
        if o in layer:
            layer.remove(o) # 레이어에서 지우기
            remove_collision_object(o) # 충돌 처리 대상에서 지우기
            del o # 오브젝트 지우기
            return
    raise ValueError('Cannot delete non existing object')


def clear():
    for layer in objects:
        layer.clear()

# 충돌 처리를 최대한 적게 하도록

# 충돌 처리 대상 조합(a, b) 등록

collision_pairs = {}

# 충돌 처리 대상 조합(a, b) 추가
def add_collision_pair(group, a, b):
    # a와 b 사이 충돌 검사가 필요하다

    # 새로운 group인 경우
    if group not in collision_pairs:
        print(f"새로운 그룹 ({group})을 추가했습니다")
        # collision_pairs에서 새로운 group을 초기화한다
        collision_pairs[group] = [ [], [] ]

    # 각 충돌 대상 오브젝트를 그룹에 추가한다
    if a:
        collision_pairs[group][0].append(a)
    if b:
        collision_pairs[group][1].append(b)

# 충돌 오브젝트 제거
def remove_collision_object(obj):
    for pairs in collision_pairs.values():
        # 충돌 조합에서 오브젝트를 지우기
        if obj in pairs[0]:
            pairs[0].remove(obj)
        if obj in pairs[1]:
            pairs[1].remove(obj)


# 충돌 처리
def handle_collisions():
    # group과 조합 정보를 가져온다
    for group, pairs in collision_pairs.items():
        # a와 b 각각에 대하여
        for a in pairs[0]:
            for b in pairs[1]:
                # a와 b가 충돌했다면
                if collide(a, b):
                    # 각 오브젝트에 대하여 상대 오브젝트와 충돌 처리
                    a.handle_collision(group, b) # a가 b에 대하여
                    b.handle_collision(group, a) # b가 a에 대하여
