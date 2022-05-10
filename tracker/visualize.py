import cv2

import tracker.common as cmn
from . import utils

def visualize(cap, data: cmn.TrackedData):
    frame = 0
    deltaDelayMs = int(1000/float(60))
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255), (255, 0, 255)]
    paused = False
    tracks = data.tracks

    dx = cap.get(cv2.CAP_PROP_FRAME_WIDTH)/(2*data.input_width)
    dy = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)/(2*data.input_height)
    if len(tracks)==0:
        utils.log("No track found")
        return
    while cap.isOpened():
        ret, pic = cap.read()
        if ret:
            sized = cv2.resize(pic, (0, 0), fx=0.5, fy=0.5)
            withTrack = sized.copy()
            j=0
            for track in tracks:
                frames = track.frames
                idx = frame
                while idx>=0 and len(frames)>idx and frames[idx]:
                    if frames[idx].frame_number == frame and not frames[idx].empty:
                        loc = frames[idx].points[0].location
                        # print(frames[idx].points)
                        cv2.circle(withTrack, (int(dx*loc[0]), int(dy*loc[1])), 5, colors[j], -1)
                        cv2.putText(withTrack, str(j), (int(dx*loc[0])+5, int(dy*loc[1])+5), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 1)
                        j+=1
                        break
                    idx-=1

            cv2.putText(withTrack, "Frame " + str(frame), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 1)
            cv2.putText(withTrack, "Tracks : " + str(j), (sized.shape[1]-200, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 1)
            cv2.putText(sized, "Frame " + str(frame), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 1)
            cv2.imshow("Original", sized)
            cv2.imshow("Tracked", withTrack)
            key = cv2.waitKey(deltaDelayMs)
            if key == ord('q'):
                break
            elif key == ord('p'):
                paused = True
            if paused:
                key = cv2.waitKey()
                if key == ord('p'):
                    paused = False
                elif key == ord('l'):
                    frame += 1
                    cap.set(1, frame)
                    continue
                elif key == ord('j'):
                    frame -= 1
                    cap.set(1, frame)
                    continue
                elif key == ord('q'):
                    break
            frame += 1
        else:
            break