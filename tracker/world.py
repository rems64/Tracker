from sympy import re
import numpy as np
from . import utils
import tracker.cameraProjection as cproj
import pathlib

class World:
    def __init__(self):
        self.cameras = []
    
    def appendCamera(self, cam):
        self.cameras.append(cam)
    
    def __str__(self) -> str:
        return "World with " + str(len(self.cameras)) + " cameras"


class WorldObject:
    def __init__(self, location=(0, 0, 0), rotation=(0, 0, 0)):
        self.location = location
        self.rotation = rotation
    
    def getLocation(self):
        return self.location
    
    def __str__(self) -> str:
        return "Location (" + str(self.location[0]) + ", " + str(self.location[1]) + ", " + str(self.location[2]) + ")"


class Camera(WorldObject):
    def __init__(self, position=(0, 0, 0), rotation=(0, 0, 0), focalLength=50, sensorWidth=27, sensorHeight=27, id=0, resolution=[1920, 1080]):
        WorldObject.__init__(self, position, rotation)
        self.id = id
        self.focalLength = focalLength
        self.sensorWidth = sensorWidth
        self.sensorHeight = sensorHeight
        self.tracks = []
        self.resolution = resolution
    
    def getFocalLength(self):
        return self.focalLength
    
    def addTrack(self, track):
        self.tracks.append(track)
    
    def setTracks(self, tracks):
        self.tracks = tracks
    
    def __str__(self) -> str:
        return "Camera with id (" + str(self.id) + "). There are " + str(len(self.tracks)) + " tracks. " + super().__str__()


class Track():
    def __init__(self, name="defaultTrack", mapping=0):
        self.frames = []
        self.mapping = mapping

class Frame():
    def __init__(self, frame_number, point):
        self.frame_number = frame_number
        self.point = point
        self.direction = []


def getMapping(cam, i):
    for map in cam["tracksMap"]:
        if int(map["source"])==i:
            return map["destination"]
    return -1

def createWorld(data, rootPath):
    print(rootPath)
    print(data)
    utils.log("Loading world, version " + str(data["version"]), utils.logTypes.info)
    world = World()
    for cam in data["cameras"]:
        cameraObj = Camera(cam["position"], cam["rotation"], cam["focalLength"], cam["sensorWidth"], cam["sensorHeight"], cam["id"], cam["resolution"])
        world.appendCamera(cameraObj)
        p2 = pathlib.Path(rootPath).joinpath(cam["filepath"])
        camData = utils.open_bson(p2)
        tracks = []
        i=0
        for track in range(camData["infos"]["max_tracks"]):
            tracks.append(Track("Track number " + str(track), getMapping(cam, i+1)))
            i+=1
        
        for frame in camData["frames"]:
            for i in range(len(frame["points"])):
                tracks[i].frames.append(Frame(frame["frame_number"], frame["points"][i]))
        
        cameraObj.setTracks(tracks)
        # print(cameraObj.tracks[0].mapping)
    
    return world



def generateDirections(world):
    for cam in world.cameras:
        invMat = cproj.constructInverseIntrinsicMatrix(cam.resolution, cam.sensorHeight, cam.focalLength)
        for track in cam.tracks:
            if track.mapping != -1:
                for frame in track.frames:
                    coords = np.matrix([[frame.point[0]], [frame.point[1]], [1]])
                    direction = invMat * coords
                    direction /= np.linalg.norm(direction)
                    frame.direction = [a[0] for a in direction.tolist()]