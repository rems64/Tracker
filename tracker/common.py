# -*- coding: utf-8 -*-
# !/usr/bin/python3
# Path: Tracker\tracker\common.py


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