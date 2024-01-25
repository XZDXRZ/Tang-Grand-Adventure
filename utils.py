import numpy

SIZE = {
    "width": 1000,
    "height": 650
}

BG_COLOR = (255, 255, 255)
GAME_TICK = 10

PLAYER_SHOOT_CD = 15
PLAYER_MAX_HP = 5

KIT_CD = {
    "mean": 300,
    "sd": 5
}

def abs(x):
    if x < 0:
        return -x
    return x

def random_sign() -> int:
    x = numpy.random.random()
    if x > 0.5:
        return 1
    return -1
