from inspect import currentframe
import cv2

import tracker.common as cmn
from . import utils

def visualize(source: cmn.TrackingSource, data: cmn.TrackedData):
    frame = 0
    deltaDelayMs = int(1000/float(60))
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255), (255, 0, 255)]
    paused = False
    tracks = data.tracks

    dx = source.resolution[0]/(2*data.input_width)
    dy = source.resolution[1]/(2*data.input_height)
    if len(tracks)==0:
        utils.log("No track found")
        return
    shouldExit = False
    shouldPause = True
    source.setFrame(source.begin_frame)
    while not shouldExit:
        ret, pic = source.readFrame()
        if not ret or frame > source.frame_count:
            shouldExit = True
            break
        if ret:
            sized = cv2.resize(pic, (0, 0), fx=0.5, fy=0.5)
            withTrack = sized.copy()
            displayedTracksIndex=0
            displayedTracksCount=0
            for track in range(len(tracks)):
                frames = tracks[track].frames
                idx = frame+1
                while idx>=0:
                    if  idx>=len(frames) or not frames[idx]:
                        idx-=1
                        continue
                    if frames[idx].frame_number == frame and not frames[idx].empty:
                        loc = frames[idx].points[0].location
                        cv2.circle(withTrack, (int(dx*loc[0]), int(dy*loc[1])), 5, colors[displayedTracksIndex], -1)
                        cv2.putText(withTrack, str(displayedTracksIndex), (int(dx*loc[0])+5, int(dy*loc[1])+5), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 1)
                        displayedTracksCount+=1
                        break
                    idx-=1
                displayedTracksIndex+=1

            cv2.putText(withTrack, "Frame " + str(frame), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 1)
            cv2.putText(withTrack, "Tracks : " + str(displayedTracksCount), (sized.shape[1]-200, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 1)
            cv2.putText(sized, "Frame " + str(frame), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 1)
            cv2.imshow("Original", sized)
            cv2.imshow("Tracked", withTrack)
            key = cv2.waitKey(deltaDelayMs)
            if key == ord('q'):
                break
            elif key == ord('p') or shouldPause:
                shouldPause = False
                paused = True
            if paused:
                key = cv2.waitKey()
                if key == ord('p'):
                    paused = False
                elif key == ord('l'):
                    frame += 1
                    source.setFrame(frame)
                    continue
                elif key == ord('j'):
                    frame -= 1
                    source.setFrame(frame)
                    continue
                elif key == ord('q'):
                    break
            frame += 1
        else:
            break