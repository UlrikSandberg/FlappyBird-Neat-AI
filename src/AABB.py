class AABB:

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

class AABBPoint:
    def __init__(self, x, y, width, height, pipeNr):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.pipeNr = pipeNr

def aabbCollision(box1, box2):
    if box1.x < box2.x + box2.width and box1.x + box1.width > box2.x and box1.y < box2.y + box2.height and box1.y + box1.height > box2.y:
        return True

    return False