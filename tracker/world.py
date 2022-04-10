from . import utils

class World:
    def __init__(self):
        self.cameras = []
    
    def appendCamera(self, cam):
        self.cameras.append(cam)
    
    def __str__(self) -> str:
        return "There are " + str(len(self.cameras)) + " cameras in this world"


class WorldObject:
    def __init__(self, location=(0, 0, 0), rotation=(0, 0, 0)):
        self.location = location
        self.rotation = rotation
    
    def getLocation(self):
        return self.location
    
    def __str__(self) -> str:
        return "Location (" + str(self.location[0]) + ", " + str(self.location[1]) + ", " + str(self.location[2]) + ")"

class Camera(WorldObject):
    def __init__(self, position=(0, 0, 0), rotation=(0, 0, 0), fov=45, near=0, far=0, id=0):
        WorldObject.__init__(self, position, rotation)
        self.id = id
        self.fov = fov
        self.near = near
        self.far = far
        self.tracks = []
    
    def getFOV(self):
        return self.fov
    
    def addTrack(self, track):
        self.tracks.append(track)
    
    def setTracks(self, tracks):
        self.tracks = tracks
    
    def __str__(self) -> str:
        return "Camera with id (" + str(self.id) + "). " + super().__str__()



def createWorld(data):
    cameras = data["cameras"]
    # world = {"cameras": [], "points": []}
    world = World()
    maxTracks = []
    for camera in cameras:
        fp = camera["filepath"]
        utils.log("Loading camera " + str(camera["id"]) + " from " + fp, utils.logTypes.trace)
        cam = utils.open_bson(fp)

        maxTracks.append(cam["infos"]["max_tracks"])
        print(camera)


        ongoingCamera = Camera(camera["position"], camera["rotation"], camera["fov"], camera["near"], camera["far"], camera["id"])

        # ongoingCamera = {
        #     "id": camera["id"],
        #     "position": (camera["position"][0], camera["position"][1], camera["position"][2]),
        #     "rotation": (camera["rotation"][0], camera["rotation"][1], camera["rotation"][2]),
        #     "fov": camera["fov"],
        #     "resolution": camera["resolution"],
        #     "near": camera["near"],
        #     "far": camera["far"],
        #     "tracks": []
        #     }
        
        for track in cam["tracks"]:
            stableId = 0
            for id in camera["tracksMap"]:
                if id["source"] == track["trackId"]:
                    stableId = id["destination"]
                    break
            ongoingCamera.addTrack({
                "id": stableId,
                "frames": track["frames"]
            })
        
        # world["cameras"].append(ongoingCamera)
        world.appendCamera(ongoingCamera)
    # world["points"] = [{"id": i, "frames": []} for i in range(max(maxTracks))]
    
    if min(maxTracks) != max(maxTracks):
        utils.log("Some track are missing from one camera to another", utils.logTypes.error)
        return None
    
    utils.log("Creating world with " + str(len(cameras)) + " cameras and " + str(min(maxTracks)) + " tracks", utils.logTypes.info)

    return world