# -*- coding: utf-8 -*-
# !/usr/bin/python3
# Path: Tracker\tracker\common.py

import cv2
import numpy as np
import tracker.utils as utils
import uuid


class Frame():
    def __init__(self, frame_number: int, points: list):
        self.frame_number = frame_number
        self.points = points
    
    @property
    def empty(self):
        return len(self.points) == 0
    
    def __str__(self) -> str:
        return "Frame number " + str(self.frame_number) + " with " + str(len(self.points)) + " points"


class Point():
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y
        
    @classmethod
    def fromCouple(self, coords: tuple[float, float]) -> None:
        self.x = coords[0]
        self.y = coords[1]
    
    @property
    def location(self):
        return (self.x, self.y)
    
    @property
    def array(self):
        return [self.x, self.y]
    
    def __str__(self) -> str:
        return "(" + str(self.x) + ", " + str(self.y) + ")"
    
    def distance(self, other) -> float:
        return ((self.x-other.x)**2 + (self.y-other.y)**2)**0.5


class Track():
    def __init__(self, id, name="defaultTrack", mapping=0):
        self.id = id
        self.name = name
        self.frames = []
        self.mapping = mapping
    
    def appendFrame(self, frame: Frame) -> None:
        self.frames.append(frame)
    
    @property
    def frames_count(self) -> int:
        return len(self.frames)
    
    @property
    def empty(self) -> bool:
        return len(self.frames) == 0
    
    def containsFrame(self, frame_number: int) -> bool:
        return frame_number in [frame.frame_number for frame in self.frames]
    
    def __str__(self) -> str:
        return "Track containing " + str(len(self.frames)) + " frames with mapping to index " + str(self.mapping)


class TrackedData:
    def __init__(self):
        self.tracks = []
        self.input_width = 0
        self.input_height = 0
        self._frames_count = 0
    
    @property
    def frames_count(self) -> int:
        if self._frames_count != 0:
            return self._frames_count
        else:
            for track in self.tracks:
                if track.frames_count > self._frames_count:
                    self._frames_count = track.frames_count
            return self._frames_count
    
    @property
    def tracks_count(self) -> int:
        return len(self.tracks)


class TrackingSource:
    def __init__(self, path: str):
        self.type = "video" if path!="" else "live"    # Could be either video or live
        self.uuid = str(uuid.uuid4().int)
        self.video_path = path
        self.video = None
        self.fps = 0
        self.begin_frame = 0
        self.frame_count = 0
        self.resolution = (0, 0)
        self.ratio = 1
    
    def loadVideo(self, video_path: str = "", frame_limit: int=0) -> bool:
        if self.type != "video":
            raise Exception("This source is not a video")
        if video_path != "":
            self.video_path = video_path
        self.video = cv2.VideoCapture(self.video_path)
        self.fps = self.video.get(cv2.CAP_PROP_FPS)
        self.frame_count = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT)) if not frame_limit else frame_limit
        self.resolution = (int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        utils.log("Video loaded with resolution " + str(self.resolution) + " and " + str(self.frame_count) + " frames")
        self.ratio = self.resolution[0] / self.resolution[1]
        return True
    
    def readFrame(self) -> tuple[bool, np.ndarray]:
        return self.video.read()
    
    def setFrame(self, frame: int) -> None:
        self.video.set(1, frame)


class RawTrackedData(TrackedData):
    """
    Raw tracked data
    """
    def __init__(self, video_file: str):
        TrackedData.__init__(self)
        self.video_file = video_file
        self._currentFrame = 0
        self._trackInsertCounter = 0
    
    def newFrame(self):
        self._currentFrame += 1
        self._trackInsertCounter = 0
    
    @property
    def currentFrame(self) -> int:
        return self._currentFrame
    
    def addTrackedPoint(self, point: Point):
        if self._trackInsertCounter >= len(self.tracks):
            while self._trackInsertCounter >= len(self.tracks):
                self.tracks.append(Track(len(self.tracks)))
        self.tracks[self._trackInsertCounter].appendFrame(Frame(self._currentFrame, [point]))
        self._trackInsertCounter += 1
    
    def setFrame(self, frame: int) -> None:
        TrackedData.setFrame(self, frame)
        self._currentFrame = frame