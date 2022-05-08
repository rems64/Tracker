import math
import numpy as np

import tracker.cameraProjection as cproj

# def func(x):
#     return math.exp(x)-2

# res = utils.newtonSolve(func, lambda x: math.exp(x), 1, 0.00001)
# print("The root is at", res)

invMat = cproj.constructInverseIntrinsicMatrix([1500, 1000], 4.75, 50)

u=1291
v=556
coords = np.matrix([[u], [v], [1]])

# Get direction

direction = invMat * coords
direction /= direction[2] #Project on image plane, which is kind of a non-sense

print(direction)