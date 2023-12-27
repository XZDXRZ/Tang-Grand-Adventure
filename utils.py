import numpy

size = {
    "width": 1000,
    "height": 650
}

bg_color = (255, 255, 255)
game_tick = 10
player_shoot_CD = 15
player_max_hp = 5
kit_cd = {
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
    else:
        return -1
