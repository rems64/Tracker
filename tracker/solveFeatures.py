import numpy as np
import uuid
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

def getHighDensityAreas(points, side):
    while currentSubdivision


def solveByAccelerationOnSubset(tracks, data):
    