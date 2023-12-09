import numpy

size = (1000, 650)
bg_color = (255, 255, 255)
tick = 10
player_shoot_CD = 15

def abs(x):
    if x > 0:
        return x
    return -x

def normal_random(mean, sd):
    x = numpy.random.normal(mean, sd)
    if abs(x) < 0.01:
        x = 0.01
    return x
