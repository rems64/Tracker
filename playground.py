#!/usr/bin/env python3
import argparse
import time

description = "Run the pipeline on a video file"
argparser = argparse.ArgumentParser(description=description)
argparser.add_argument("-i", "--input", help="Path to the video file", required=True)
argparser.add_argument("-o", "--output", help="Path to the output file", required=False)
argparser.add_argument("-n", "--noise", help="Noise level (0-1)", required=False, default=0)
argparser.add_argument("-f", "--frame-limit", help="Number of frames to process", required=False, default=0)
argparser.add_argument("-c", "--usecache", help="Use cached result", required=False, default=False)
argparser.add_argument("-p", "--permutations", help="Use permutations", required=False, default=True)
argparser.add_argument("-v", "--vizu", help="Use permutations", required=False, default="curves")
args = argparser.parse_args()

# 150 à 180

if __name__ == "__main__":
    import tracker.featuresTracker as ft
    import tracker.solveFeatures as sf
    import tracker.visualize as vz
    import tracker.utils as utils
    import tracker.common as cmn
    import cv2
    import pathlib
    import matplotlib.pyplot as plt

    utils.log("Starting {}".format(pathlib.Path(__file__).name), utils.logTypes.info)

    begin = time.time()
    source = cmn.TrackingSource(args.input)
    source.loadVideo(frame_limit=int(args.frame_limit))

    read, frame = source.readFrame()
    if not read: utils.log("No frame to read", utils.logTypes.error)
    mean = cv2.mean(frame)
    grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    histogram = cv2.calcHist([grey], [0], None, [256], [0, 256])
    utils.log("Mean: {}".format(mean))
    plt.plot(histogram)
    plt.show()
    
    end = time.time()
    utils.log("Pipeline finished in {:.2f} seconds".format(end - begin), utils.logTypes.timer)
    
    # utils.save_bson(tracked, args.output)
    # utils.log("Saved to {}".format(args.output))