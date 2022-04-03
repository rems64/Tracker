#!/usr/bin/env python3
import argparse
import time

description = "Run the pipeline on a video file"
argparser = argparse.ArgumentParser(description=description)
argparser.add_argument("-i", "--input", help="Path to the video file", required=True)
argparser.add_argument("-o", "--output", help="Path to the output file", required=True)
argparser.add_argument("-n", "--noise", help="Noise level (0-1)", required=False, default=0)
argparser.add_argument("-f", "--frame-limit", help="Number of frames to process", required=False, default=0)
args = argparser.parse_args()



if __name__ == "__main__":
    import tracker.featuresTracker as ft
    import tracker.solveFeatures as sf
    import tracker.visualize as vz
    import tracker.utils as utils

    utils.log("Starting pipeline")
    begin = time.time()
    cap = utils.open_video(args.input)

    utils.log("Processing video")
    b = time.time()
    tracked = ft.trackFeatures(cap, float(args.noise), int(args.frame_limit), False, filename=args.input)
    utils.log("Tracking features took {} seconds".format(time.time() - b), utils.logTypes.timer)

    utils.log("Processed successfully, solving features")
    b = time.time()
    solved = sf.solveByAcceleration(tracked)
    utils.log("Solving features took {} seconds".format(time.time() - b), utils.logTypes.timer)

    end = time.time()
    utils.log("Features solved, visualizing")

    vz.visualize(utils.open_video(args.input), tracked)

    utils.log("Pipeline finished in {} seconds".format(end - begin), utils.logTypes.timer)
    
    utils.save_json(tracked, args.output)
    utils.log("Saved to {}".format(args.output))