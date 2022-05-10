import tracker.utils as utils
import tracker.common as cmn

def naiveAssignment(tracked: cmn.TrackedData) -> cmn.TrackedData:
    """
    Naive assignment of trackers to tracks
    """
    # Nothing to do with the new method
    return None

def solveByNearestNeighbour(tracked: cmn.TrackedData, permuts: bool=True) -> cmn.TrackedData:
    """
    Solve by nearest neighbour
    """
    output = cmn.TrackedData()
    output.input_width = tracked.input_width
    output.input_height = tracked.input_height

    # Early exit if tracked is empty
    if not tracked:
        utils.log("Tracked data is None", utils.logTypes.error)
        return output
    
    # Store each frame as a list of points
    frames_count = tracked.frames_count
    frames = [[] for _ in range(frames_count)]
    for track in tracked.tracks:
        for frame in track.frames:
            for point in frame.points:
                frames[frame.frame_number].append(point)
    
    # Early exit if frames is empty
    if len(frames[0]) == 0:
        return output
    
    # Assign the first points to tracks
    utils.log("Initializing " + str(tracked.tracks_count) + " tracks for " + str(len(frames[0]))+ " init points", utils.logTypes.trace)
    output.tracks = [cmn.Track(i) for i in range(tracked.tracks_count)]
    for i in range(len(frames[0])):
        if i>=len(output.tracks):
            utils.log("Not enough tracks to deal with initial points", utils.logTypes.warning)
            utils.log("Skipping points from point " + str(i), utils.logTypes.trace)
            break
        point = frames[0][i]
        output.tracks[i].appendFrame(cmn.Frame(0, [point]))
    
    # Precompute permutations
    if permuts:
        if tracked.tracks_count > 8:
            utils.log("High number of points, permutations will take a huge amount of time", utils.logTypes.warning)
        permutations_nbr = {n: utils.permutations([i for i in range(n)]) for n in range(0, tracked.tracks_count+1)}
    # Assign the rest of the points to tracks
    for frame_number in range(1, frames_count):
        frmsCount = 0
        points = frames[frame_number]
        # utils.log("Assigning " + str(len(points)) + " points to tracks", utils.logTypes.trace)
        # permutations = utils.permutations(points) if permuts else [points]
        scores = []
        for permutation in (permutations_nbr[len(points)] if permuts else [[i for i in range(len(points))]]):
            score = 0
            # For the point indexed i, stores the index of the best matching track
            ordered_tracks = []
            for i in permutation:
                point = points[i]
                # Find the closest track
                closest_track = None
                closest_distance = float("inf")
                for track in range(len(output.tracks)):
                    if track in ordered_tracks:
                        continue
                    if len(output.tracks[track].frames)<=0:
                        distance = 10000
                    else:
                        distance = point.distance(output.tracks[track].frames[-1].points[0])
                    if distance < closest_distance:
                        closest_track = track
                        closest_distance = distance
                # Add the point to the closest track
                if closest_track is not None:
                    ordered_tracks.append(closest_track)
                else:
                    utils.log("No closest track found for point " + str(point), utils.logTypes.warning)
                    utils.log("Skipping point " + str(point), utils.logTypes.trace)
                    continue
                # Add the distance to the score
                score += closest_distance
            # Add the score to the list
            scores.append(score)
        # Find the best permutation
        best_permutation = None
        best_score = float("inf")
        for i in range(len(scores)):
            if scores[i] < best_score:
                best_permutation = i
                best_score = scores[i]
        
        # Compute the best permutation
        if best_permutation is not None:
            ordered_tracks = []
            for i in permutations_nbr[len(points)][best_permutation]:
                point = points[i]
                # Find the closest track
                closest_track = None
                closest_distance = float("inf")
                for track in range(len(output.tracks)):
                    if track in ordered_tracks:
                        continue
                    if len(output.tracks[track].frames)<=0:
                        distance = 1000
                    else:
                        distance = point.distance(output.tracks[track].frames[-1].points[0])
                    if distance < closest_distance:
                        closest_track = track
                        closest_distance = distance
                # Add the point to the closest track
                if closest_track is not None:
                    ordered_tracks.append(closest_track)
                    output.tracks[closest_track].appendFrame(cmn.Frame(frame_number, [point]))
                    frmsCount += 1
                else:
                    utils.log("No closest track found for point " + str(point), utils.logTypes.warning)
                    utils.log("Skipping point " + str(point), utils.logTypes.trace)
                    continue
    return output