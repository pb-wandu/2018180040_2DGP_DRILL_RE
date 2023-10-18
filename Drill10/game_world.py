objects = [ [ ], [ ], [ ] ]
# depth 0 : 플레이어 뒤 grass
# depth 1 : 플레이어
# depth 2 : 플레이어 앞 grass

def add_object(o, depth):
    objects[depth].append(o)

def add_objects(ol, depth):
    objects[depth] += ol

def remove_object(o):
    # objects에 있는 레이어에 대하여
    for layer in objects:
        # 레이어 안에 오브젝트가 있다면
        if o in layer:
            print("removed : " + str(type(o)))
            layer.remove(o)
            return

    # 오류 발생시 오류 메시지 출력
    raise ValueError('존재하지 않는 object는 지울 수 없습니다')

def update():
    for layer in objects:
        for o in layer:
            o.update()


def render():
    for layer in objects:
        for o in layer:
            o.draw()


