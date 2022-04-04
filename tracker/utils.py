import cv2
import numpy as np
import bson
import colorit

# colorit.init_colorit()

class logTypes:
    """
    Log types
    """
    info = colorit.Colors.green
    timer = colorit.Colors.blue
    warning = colorit.Colors.yellow
    error = colorit.Colors.red

def open_video(video_file):
    """
    Open video file
    """
    cap = cv2.VideoCapture(video_file)
    return cap

def save_json(data, file_name):
    """
    Save the data in a json file
    """
    with open(file_name, "wb") as f:
        f.write(bson.dumps(data))

def log(msg, type=logTypes.info):
    """
    Log the data
    """
    pretext = "[WARN]" if type==logTypes.warning else "[INFO]" if type==logTypes.info else "[TIME]" if type==logTypes.timer else "[ERRO]"
    print(colorit.color(pretext+" {}".format(msg), type))


def permutations(n):
    """
    Get all permutations of n
    """
    if n == 1:
        return [[1]]
    else:
        perm = permutations(n-1)
        return [p + [n] for p in perm]


class QuadTreeMedian:
    def __init__(self, points, begin, end, depth=0):
        self.points = points
        self.begin = begin
        self.end = end
        self.subdivisions = []
        self.depth = depth
        self.build()

    def build(self):
        if len(self.points) <= 1:
            return
        x_m = np.median([p[0] for p in self.points])
        y_m = np.median([p[1] for p in self.points])
        self.subdivisions.append(QuadTreeMedian([p for p in self.points if p[0] < x_m and p[1] < y_m], self.begin, (self.begin[0], y_m), self.depth+1))
        self.subdivisions.append(QuadTreeMedian([p for p in self.points if p[0] >= x_m and p[1] < y_m], (x_m, self.begin[1]), (self.end[0], y_m), self.depth+1))
        self.subdivisions.append(QuadTreeMedian([p for p in self.points if p[0] < x_m and p[1] >= y_m], (self.begin[0], y_m), (x_m, self.end[1]), self.depth+1))
        self.subdivisions.append(QuadTreeMedian([p for p in self.points if p[0] >= x_m and p[1] >= y_m], (x_m, y_m), self.end, self.depth+1))
    
    def isEmpty(self):
        return len(self.points)<=0

    def getPoints(self):
        return self.points

    def getSubdivisions(self):
        return self.subdivisions
    
    def getPoints(self):
        return self.points
    
    def getDepth(self):
        return self.depth


def getSubAfterN(quadtree, n):
    if n<=0:
        return [quadtree]
    subdivs = quadtree.getSubdivisions()
    output = []
    for i in range(4):
        if not subdivs[i].isEmpty():
            output += getSubAfterN(subdivs[i], n-1)
    return output