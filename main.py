from p5 import *
import numpy as np
from boid import Boid

flock = []
height = 1000
width = 2000
for _ in range(10):
    pos = np.random.rand(2) * 1000
    flock.append(Boid(*pos, width, height))

def setup():
    size(width, height)
    no_stroke()

def draw():
    background(255)
    for boid in flock:
        boid.show()
        boid.apply_behaviour(flock)
        boid.update()
        boid.edges()

run()