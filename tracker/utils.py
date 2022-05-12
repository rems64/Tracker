from email import message
import cv2
import numpy as np
import bson
import json
import colorit
import progress.bar

# colorit.init_colorit()

class logTypes:
    """
    Log types
    """
    info = colorit.Colors.green
    timer = colorit.Colors.blue
    warning = colorit.Colors.yellow
    error = colorit.Colors.red
    trace = colorit.Colors.white

def log(msg, type:logTypes=logTypes.info) -> None:
    """
    Log the data
    """
    pretext = "[WARN]" if type==logTypes.warning else "[INFO]" if type==logTypes.info or type==logTypes.trace else "[TIME]" if type==logTypes.timer else "[ERRO]"
    print(colorit.color(pretext+" {}".format(msg), type))

def log_newline() -> None:
    """
    Log a new line
    """
    print("")

def logf(frame: int, target_frame: int, *args, **kwargs) -> None:
    """
    Log if target_frame matches frame
    """
    if frame==target_frame:
        log(*args, **kwargs)

class ProgressBar(progress.bar.IncrementalBar):
    message = "Progress: "
    suffix = "%(percent)d%%"
    def __init__(self, *args, **kwargs):
        super(progress.bar.IncrementalBar, self).__init__(*args, **kwargs)
        self.start()

def open_video(video_file: str) -> cv2.VideoCapture:
    """
    Open video file
    """
    cap = cv2.VideoCapture(video_file)
    return cap

def save_bson(data, file_name: str) -> None:
    """
    Save the data in a json file
    """
    with open(file_name, "wb") as f:
        f.write(bson.dumps(data))

def open_bson(file_name: str) -> dict:
    """
    Open the json file
    """
    with open(file_name, "rb") as f:
        return bson.loads(f.read())

def open_json(file_name: str):
    """
    Open the json file
    """
    with open(file_name, "r") as f:
        return json.loads(f.read())


def permutations(l):
    """
    Get all permutations of n
    """
    if len(l)<=1:
        return [l]
    else:
        perms = permutations(l[1:])
        out = []
        for perm in perms:
            for i in range(len(l)):
                out.append(perm[:i] + [l[0]] + perm[i:])
        return out

def distance(p1: tuple[float, float], p2: tuple[float, float]):
    return np.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def clamp(x, a, b):
    return x if x>=a and x<=b else (a if x<a else b)

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


def newtonSolve(f, df, x0, epsilon):
    its = 0
    while abs(f(x0)) > epsilon:
        x0 = x0 - f(x0) / df(x0)
        its+=1
    print("Used newton, solved in {} iterations".format(its))
    return x0