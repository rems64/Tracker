# -*- coding: utf-8 -*-
# !/usr/bin/python3
# Path: Tracker\tracker\common.py


class Frame():
    def __init__(self, frame_number: int, points: list):
        self.frame_number = frame_number
        self.points = points
    
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
    
    def __str__(self) -> str:
        return "(" + str(self.x) + ", " + str(self.y) + ")"


class Track():
    def __init__(self, id, name="defaultTrack", mapping=0):
        self.id = id
        self.name = name
        self.frames = []
        self.mapping = mapping
    
    def appendFrame(self, frame: Frame):
        self.frames.append(frame)
    
    def __str__(self) -> str:
        return "Track containing " + str(len(self.frames)) + " frames with mapping to index " + str(self.mapping)


class TrackedData:
    def __init__(self):
        self.tracks = []
        self.frame_count = 0