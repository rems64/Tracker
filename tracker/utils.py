import cv2
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


class QuadTree:
    def __init__(self, points, bounds, depth=0):
        self.points = points
        self.bounds = bounds
        self.subdivisions = []
        self.depth = depth
        self.build()

    def build(self):
        if len(self.points) <= 1:
            return
        x_min = min(p[0] for p in self.points)
        x_max = max(p[0] for p in self.points)
        y_min = min(p[1] for p in self.points)
        y_max = max(p[1] for p in self.points)
        x_mid = (x_min + x_max) / 2
        y_mid = (y_min + y_max) / 2
        self.subdivisions.append(QuadTree([p for p in self.points if p[0] < x_mid and p[1] < y_mid], self.side/2, self.depth+1))
        self.subdivisions.append(QuadTree([p for p in self.points if p[0] >= x_mid and p[1] < y_mid], self.side/2, self.depth+1))
        self.subdivisions.append(QuadTree([p for p in self.points if p[0] < x_mid and p[1] >= y_mid], self.side/2, self.depth+1))
        self.subdivisions.append(QuadTree([p for p in self.points if p[0] >= x_mid and p[1] >= y_mid], self.side/2, self.depth+1))

    def getPoints(self):
        return self.points

    def getSubdivisions(self):
        return self.subdivisions

    def getSubdivision(self, x, y):
        if len(self.subdivisions) == 0:
            return self
        if x < self.side/2:
            if y < self.side/2:
                return self.subdivisions[0]
            else:
                return self.subdivisions[1]
        else:
            if y < self.side/2:
                return self.subdivisions[2]
            else:
                return self.subdivisions[3]
    
    def getPoints(self):
        return self.points
    
    def getDepth(self):
        return self.depth