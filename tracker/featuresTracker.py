from . import utils
import tracker.common as cmn
import numpy as np
import cv2
import uuid

        

def add_noise(frame, noise_level: float):
    """
    Add noise to the frame
    """
    noise = np.random.randint(0, 255*noise_level, (frame.shape[0], frame.shape[1], frame.shape (2)))
    frame = np.uint8(np.clip(frame + noise, 0, 255))
    return frame



def trackFeatures(source, noise_level=0, show=False):
    """
    Track features in the video
    @param source: TrackingSource object
    @param noise_level: Noise level (0-1)
    @param frame_limit: Number of frames to process
    @param show: Show the ongoing result
    """

    shouldExit = False
    tracked = cmn.RawTrackedData(source.video_path)
    tracked.input_width = source.resolution[0]
    tracked.input_height = source.resolution[1]

    source.setFrame(source.begin_frame)
    tracked._currentFrame = source.begin_frame
    bar = utils.ProgressBar("Tracking....", max=source.frame_count-source.begin_frame)
    while not shouldExit:
        ret, frame = source.readFrame()
        if not ret or tracked.currentFrame >= source.frame_count:
            shouldExit = True
            break
        bar.next()

        # if noise_level:
        #     frame = add_noise(frame, noise_level)

        ret, thresh = cv2.threshold(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), 127, 255, 0) # Ugly, needs more refactoring
        contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        detected = []
        for contour in contours:
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                # if show:
                #     cv2.polylines(frame, contour, True, (0, 255, 0), 2)
                #     detected.append((cx, cy))
                tracked.addTrackedPoint(cmn.Point(cx, cy))
        # if show:
        #     for c in detected:
        #         cv2.circle(frame, c, 10, (0, 0, 255), 2)
        #     cv2.imshow("Tracking...", frame)
        #     key = cv2.waitKey(1)
        #     if key==ord('q'):
        #         show = False

        tracked.newFrame()
    bar.finish()
    utils.log("Tracked up to " + str(len(tracked.tracks)) + " tracks", utils.logTypes.info)
    return tracked