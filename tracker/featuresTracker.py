from . import utils
import tracker.common as cmn
import numpy as np
import cv2
import uuid



class TrackingSource:
    def __init__(self, path: str):
        self.type = "video" if path!="" else "live"    # Could be either video or live
        self.uuid = str(uuid.uuid4().int)
        self.video_path = path
        self.video = None
        self.fps = 0
        self.frame_count = 0
        self.resolution = (0, 0)
        self.ratio = 1
    
    def loadVideo(self, video_path: str = "") -> bool:
        if self.type != "video":
            raise Exception("This source is not a video")
        if video_path != "":
            self.video_path = video_path
        self.video = cv2.VideoCapture(self.video_path)
        self.fps = self.video.get(cv2.CAP_PROP_FPS)
        self.frame_count = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))
        self.resolution = (int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        utils.log("Video loaded with resolution " + str(self.resolution) + " and " + str(self.frame_count) + " frames")
        self.ratio = self.resolution[0] / self.resolution[1]
        return True
    
    def readFrame(self) -> tuple[bool, np.ndarray]:
        return self.video.read()


class RawTrackedData(cmn.TrackedData):
    """
    Raw tracked data
    """
    def __init__(self, video_file: str):
        cmn.TrackedData.__init__(self)
        self.video_file = video_file
        self._currentFrame = 0
        self._trackInsertCounter = 0
    
    def newFrame(self):
        self._currentFrame += 1
        self._trackInsertCounter = 0
    
    def addTrackedPoint(self, point: cmn.Point):
        if self._trackInsertCounter >= len(self.tracks):
            while self._trackInsertCounter >= len(self.tracks):
                self.tracks.append(cmn.Track(len(self.tracks)))
        self.tracks[self._trackInsertCounter].appendFrame(cmn.Frame(self._currentFrame, [point]))
        self._trackInsertCounter += 1

        

def add_noise(frame, noise_level: float):
    """
    Add noise to the frame
    """
    noise = np.random.randint(0, 255*noise_level, (frame.shape[0], frame.shape[1], frame.shape (2)))
    frame = np.uint8(np.clip(frame + noise, 0, 255))
    return frame



def trackFeatures(source, noise_level=0, frame_limit=0, show=False):
    """
    Track features in the video
    @param source: TrackingSource object
    @param noise_level: Noise level (0-1)
    @param frame_limit: Number of frames to process
    @param show: Show the ongoing result
    """

    shouldExit = False
    tracked = RawTrackedData(source.video_path)

    while not shouldExit:
        ret, frame = source.readFrame()
        if not ret or (frame_limit != 0 and (source.frame_count >= frame_limit)):
            shouldExit = True
            break

        if noise_level:
            frame = add_noise(frame, noise_level)

        ret, thresh = cv2.threshold(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), 127, 255, 0) # Ugly, needs more refactoring
        contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        detected = []
        for contour in contours:
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                if show:
                    cv2.polylines(frame, contour, True, (0, 255, 0), 2)
                    detected.append((cx, cy))
                tracked.addTrackedPoint(cmn.Point(cx, cy))
        if show:
            for c in detected:
                cv2.circle(frame, c, 10, (0, 0, 255), 2)
            cv2.imshow("Tracking...", frame)
            key = cv2.waitKey(1)
            if key==ord('q'):
                show = False

        tracked.newFrame()
    utils.log("Tracking finished", utils.logTypes.trace)
    utils.log("Tracked " + str(len(tracked.tracks)) + " tracks", utils.logTypes.info)