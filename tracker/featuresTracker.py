"""
Usage :
    python3 featuresTracker.py --video=<video_file>
"""

from . import utils
import numpy as np
import cv2
import uuid


"""
Storage:
{
    "infos": {
        "video_file": "video_file",
        "noise_level": 0.1,
        "frames_count": n
    },
    "frames": [
        {
            "frame_number": 1-n,
            "points": [
                (x, y),
                (x, y),
                (x, y),
                ...
            ],
            "infos": {
                "empty": True/False
            }
        },
        ...
    ],
    "tracks": [
        0: {
            "trackId": 1-s,
            "frames": [
                0: {location: (x, y)},
                1: {location: (x, y)},
                ...
            ]
        },
        ...
    ]
}
"""


def add_noise(frame, noise_level):
    """
    Add noise to the frame
    """
    noise = np.random.randint(0, 255*noise_level, (frame.shape[0], frame.shape[1], frame.shape (2)))
    frame = np.uint8(np.clip(frame + noise, 0, 255))
    return frame

def trackFeatures(cap, noise_level=0, frame_limit=0, show=False, filename=""):
    """
    Track features on the video
    @param cap: VideoCapture object
    @param noise_level: Noise level (0-1)
    @param frame_limit: Number of frames to process
    @param show: Show the ongoing result
    """
    currentFrame = 0
    tracked = {
        "infos": {
            "video_file": "live" if filename == "" else filename,
            "uuid": str(uuid.uuid4().int),
            "noise_level": noise_level,
            "frames_count": cap.get(cv2.CAP_PROP_FRAME_COUNT),
            "width": int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            "height": int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            "ratio": float(cap.get(cv2.CAP_PROP_FRAME_WIDTH) / cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            "fps": cap.get(cv2.CAP_PROP_FPS),
            "max_tracks": 0
        },
        "frames": [],
        "tracks": []
    }
    maxDetected = 0
    while True:
        ret, frame = cap.read()
        if (ret == False) or (frame_limit != 0 and currentFrame >= frame_limit):
            break

        if noise_level:
            frame = add_noise(frame, noise_level)
        
        ret, thresh = cv2.threshold(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), 127, 255, 0)
        contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        detected = []
        for cnt in contours:
            if show:
                cv2.polylines(frame, cnt, True, (0, 255, 0), 2)
            M = cv2.moments(cnt)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                detected.append((cX, cY))
        
        maxDetected = max(maxDetected, len(detected))

        tracked["frames"].append(
            {
                "frame_number": currentFrame,
                "points": detected,
                "infos": {
                    "empty": len(detected) == 0
                }
            }
        )
        if show:
            for c in detected:
                cv2.circle(frame, c, 10, (0, 0, 255), 2)
            cv2.imshow("Tracking...", frame)
            key = cv2.waitKey(1)
            if key==ord('q'):
                show = False
        currentFrame += 1
    
    tracked["infos"]["max_tracks"] = maxDetected
    return tracked
    """
    frame+=1
    ret, pic = cap.read()
    if ret:
        sized = cv2.resize(pic, (0, 0), fx=0.5, fy=0.5)
        if noiseLvl>0:
            noise = np.random.randint(0, noiseLvl, (sized.shape[0], sized.shape[1], 3))

            sized = np.uint8(np.clip(sized + noise, 0, 255))
        # To replace with a more elaborate processing
        ret, thresh = cv2.threshold(cv2.cvtColor(sized, cv2.COLOR_BGR2GRAY), 127, 255, 0)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        detected = []
        for cnt in contours:
            if args.show:
                cv2.polylines(sized, cnt, True, (0, 255, 0), 2)
            M = cv2.moments(cnt)
            # print(M)
            # exit()
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                detected.append((cX, cY))
        tracks.append((frame, detected))
        if args.show:
            for c in detected:
                cv2.circle(sized, c, 10, (0, 0, 255), 2)
            cv2.imshow("Tracking...", sized)
            key = cv2.waitKey(1)
            if key==ord('q'):
                args.show = False
    else:
        break
    """
