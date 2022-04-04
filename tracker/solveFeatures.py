import math
import numpy as np
import uuid

from sympy import true
from . import utils



def solveRawPaste(data):
    frames = data['frames']
    tracks = [{'trackId': uuid.uuid4(), 'frames': []} for _ in range(int(data["infos"]["max_tracks"]))]
    frame_count = len(frames)
    for i in range(frame_count):
        frame = frames[i]
        length = len(frame["points"])
        if frame['infos']['empty']:
            continue
        for j in range(len(tracks)):
            if j < length:
                tracks[j]["frames"].append({"location": frame["points"][j]})
            else:
                tracks[j]["frames"].append({"location": (0, 0)})
    data['tracks'] = tracks
    return data

def getBestCandidateByPosition(candidate, tracks, assigned):
    best_track = None
    best_distance = None
    i=0
    for track in tracks:
        if i in assigned:
            i+=1
            continue
        if len(track["frames"]) <= 0:
            best_track = i
            continue
        distance = np.linalg.norm(np.array(track["frames"][-1]["location"]) - np.array(candidate))
        if best_track is None or distance < best_distance:
            best_track = i
            best_distance = distance
        i+=1
    return best_track


def solveByPosition(data):
    frames = data["frames"]
    tracks = [{'trackId': uuid.uuid4(), 'frames': []} for _ in range(int(data["infos"]["max_tracks"]))]
    frame_count = len(frames)
    for i in range(frame_count):
        frame = frames[i]
        candidates = [c for c in frame["points"]]
        assigned = []
        for candidate in candidates:
            bc = getBestCandidateByPosition(candidate, tracks, assigned)
            assigned.append(bc)
            tracks[bc]["frames"].append({"location": candidate})
        if len(tracks)-len(candidates) != 0:
            for track in range(len(tracks)):
                if track in assigned:
                    continue
                utils.log("Found an empty track", utils.logTypes.warning)
                tracks[track]["frames"].append({"location": (10, 10)})
    data["tracks"] = tracks
    return data




def getBestCandidateBySpeed(candidate, tracks, assigned):
    best_track = None
    best_distance = None
    i=0
    for track in tracks:
        if i in assigned:
            i+=1
            continue
        if len(track["frames"]) <= 1:
            best_track = i
            continue
        speed = (np.array(track["frames"][-1]["location"]) - np.array(track["frames"][-2]["location"]))
        predictedSpeed = (np.array(candidate) - np.array(track["frames"][-1]["location"]))
        distance = np.linalg.norm(speed - predictedSpeed)
        if best_track is None or best_distance is None or distance < best_distance:
            best_track = i
            best_distance = distance
        i+=1
    return best_track


def solveBySpeed(data):
    frames = data["frames"]
    tracks = [{'trackId': uuid.uuid4(), 'frames': []} for _ in range(int(data["infos"]["max_tracks"]))]
    frame_count = len(frames)
    for i in range(frame_count):
        frame = frames[i]
        candidates = [c for c in frame["points"]]
        assigned = []
        if len(tracks)-len(candidates) != 0:
            utils.log("Delta "+str(len(tracks)-len(candidates)), utils.logTypes.warning)
        for candidate in candidates:
            bc = getBestCandidateBySpeed(candidate, tracks, assigned)
            assigned.append(bc)
            tracks[bc]["frames"].append({"location": candidate})
        if len(tracks)-len(candidates) != 0:
            for track in range(len(tracks)):
                if track in assigned:
                    continue
                utils.log("Found an empty track", utils.logTypes.warning)
                if len(tracks[track]["frames"]) > 0:
                    tracks[track]["frames"].append({"location": tracks[track]["frames"][-1]["location"]})
                else:
                    tracks[track]["frames"].append({"location": (0, 0)})
    data["tracks"] = tracks
    return data


def getBestCandidateByAcceleration(candidate, tracks, assigned):
    best_track = None
    best_distance = None
    i=0
    for track in tracks:
        if i in assigned:
            i+=1
            continue
        if len(track["frames"]) <= 2:
            best_track = i
            continue
        acceleration = (np.array(track["frames"][-1]["location"]) - 2*np.array(track["frames"][-2]["location"])) + (np.array(track["frames"][-3]["location"]))
        possibleAcceleration = (np.array(candidate) - 2*np.array(track["frames"][-1]["location"])) + (np.array(track["frames"][-2]["location"]))
        distance = np.linalg.norm(acceleration - possibleAcceleration)
        if best_track is None or best_distance is None or distance < best_distance:
            best_track = i
            best_distance = distance
        i+=1
    return best_track


def solveByAcceleration(data):
    frames = data["frames"]
    tracks = [{'trackId': uuid.uuid4(), 'frames': []} for _ in range(int(data["infos"]["max_tracks"]))]
    frame_count = len(frames)
    for i in range(frame_count):
        frame = frames[i]
        candidates = [c for c in frame["points"]]
        assigned = []
        if len(tracks)-len(candidates) != 0:
            utils.log("Delta "+str(len(tracks)-len(candidates)), utils.logTypes.warning)
        for candidate in candidates:
            bc = getBestCandidateByAcceleration(candidate, tracks, assigned)
            assigned.append(bc)
            tracks[bc]["frames"].append({"location": candidate})
        if len(tracks)-len(candidates) != 0:
            for track in range(len(tracks)):
                if track in assigned:
                    continue
                utils.log("Found an empty track", utils.logTypes.warning)
                tracks[track]["frames"].append({"location": (10, 10)})
    data["tracks"] = tracks
    return data



def maxSpeed(tracks):
    max_speed = 0
    for track in tracks:
        if len(track["frames"]) <= 1:
            continue
        speed = np.linalg.norm(np.array(track["frames"][-1]["location"]) - np.array(track["frames"][-2]["location"]))
        if speed > max_speed:
            max_speed = speed
    return max_speed

# def getHighDensityAreas(points, side):
#     xS = [p[0] for p in points]
#     yS = [p[1] for p in points]
#     dx = np.max(xS)-np.min(xS)
#     dy = np.max(yS)-np.min(yS)
#     quadtree = utils.QuadTreeMedian(points, (np.min(xS), np.min(yS)), (np.max(xS), np.max(yS)))
#     utils.getSubAfterN(quadtree, 5)


def getHighDensityAreas(points, side, width, height):
    # Subcells, to consider 3x3 chunk when high density is detected
    hiddenSide = side/3
    xS = [p[0] for p in points]
    yS = [p[1] for p in points]
    # begin = (np.min(xS), np.min(yS))
    # end = (np.max(xS), np.max(yS)) 
    begin = (0, 0)
    end = (width, height)
    dX = end[0]-begin[0]
    dY = end[1]-begin[1]
    cx = math.ceil(dX/hiddenSide)
    cy = math.ceil(dY/hiddenSide)
    areas = [[[] for _ in range(cy)] for _ in range(cx)]
    for point in points:
        i = math.floor(utils.clamp((point[0]-begin[0])/dX, 0, 0.99999)*(cx-1))
        j = math.floor(utils.clamp((point[1]-begin[1])/dY, 0, 0.99999)*(cy-1))
        # print(utils.clamp((point[0]-begin[0])/dX, 0, 0.99999))
        # print(i, j)
        areas[i][j].append(point)
    areaSizes = []
    for i in range(1, len(areas)-1):
        for j in range(1, len(areas[i])-1):
            total = []
            for x in range(-1, 2):
                for y in range(-1, 2):
                    total+=areas[i+x][j+y]
            if len(total)>=4:
                areaSizes.append([[((i-1)*hiddenSide+begin[0], (j-1)*hiddenSide+begin[1]), ((i+2)*hiddenSide+begin[0], (j+2)*hiddenSide+begin[1])], len(areas[i][j]), total])

    areaSizesSorted = sorted(areaSizes, key=lambda x : x[1], reverse=True)
    concernedAreas = [(i[0], i[2]) for i in areaSizesSorted]
    # utils.log("Most dense area : " + str(areaSizesSorted[0][1]), utils.logTypes.info)
    return concernedAreas


def smartSolve(data):
    frames = data["frames"]
    # tracks = [{'trackId': uuid.uuid4(), 'frames': []} for _ in range(int(data["infos"]["max_tracks"]))]
    # tracks = [{'trackId': uuid.uuid4(), 'frames': []}]
    width = int(data["infos"]["width"])
    height = int(data["infos"]["height"])
    tracks = [{'trackId': uuid.uuid4(), 'frames': []} for _ in range(4)]
    frame_count = len(frames)
    for i in range(frame_count):
        frame = frames[i]
        candidates = [c for c in frame["points"]]
        hdas = getHighDensityAreas(candidates, 150, width, height)
        if len(hdas)>0:
            # if len(hdas)>1:
                # utils.log("There are " + str(len(hdas)) + " conflict areas", utils.logTypes.warning)
            hda = hdas[0][0]
            # utils.log("Permutations for " + str(len(hdas[0][1])) + " points", utils.logTypes.warning)
            permuts = utils.permutations(len(hdas[0][1]))
            # utils.log(hda)
            tracks[0]["frames"].append({"location": (hda[0][0], hda[0][1])})
            tracks[1]["frames"].append({"location": (hda[1][0], hda[0][1])})
            tracks[2]["frames"].append({"location": (hda[0][0], hda[1][1])})
            tracks[3]["frames"].append({"location": (hda[1][0], hda[1][1])})
        else:
            tracks[0]["frames"].append({"location": (0, 0)})
            tracks[1]["frames"].append({"location": (0, 0)})
            tracks[2]["frames"].append({"location": (0, 0)})
            tracks[3]["frames"].append({"location": (0, 0)})

    data["tracks"] = tracks
    return data
