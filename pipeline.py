#!/usr/bin/env python3
import argparse
import time

description = "Run the pipeline on a video file"
argparser = argparse.ArgumentParser(description=description)
argparser.add_argument("-i", "--input", help="Path to the video file", required=True)
argparser.add_argument("-o", "--output", help="Path to the output file", required=True)
argparser.add_argument("-n", "--noise", help="Noise level (0-1)", required=False, default=0)
argparser.add_argument("-f", "--frame-limit", help="Number of frames to process", required=False, default=0)
argparser.add_argument("-c", "--usecache", help="Use cached result", required=False, default=False)
argparser.add_argument("-p", "--permutations", help="Use permutations", required=False, default=True)
args = argparser.parse_args()

# 150 à 180

if __name__ == "__main__":
    import tracker.featuresTracker as ft
    import tracker.solveFeatures as sf
    import tracker.visualize as vz
    import tracker.utils as utils
    import tracker.common as cmn

    utils.log("Starting pipeline")

    begin = time.time()
    source = cmn.TrackingSource(args.input)
    source.loadVideo(frame_limit=int(args.frame_limit))

    utils.log_newline()
    utils.log("Processing video")
    b = time.time()
    tracked = ft.trackFeatures(source, float(args.noise), False)
    utils.log("Tracking features took {:.2f} seconds".format(time.time() - b), utils.logTypes.timer)
    
    utils.log_newline()
    utils.log("Processed successfully, solving features")
    b = time.time()
    # solved = sf.solveByNearestNeighbour(tracked)
    solved = sf.multipleSolve(tracked, int(args.permutations))
    utils.log("Solving features took {:.2f} seconds".format(time.time() - b), utils.logTypes.timer)
    
    end = time.time()

    utils.log_newline()
    utils.log("Features solved, visualizing")
    vz.visualize(source, solved)
    # vz.drawCurves(solved)

    utils.log_newline()
    utils.log("Pipeline finished in {:.2f} seconds".format(end - begin), utils.logTypes.timer)
    
    # utils.save_bson(tracked, args.output)
    # utils.log("Saved to {}".format(args.output))