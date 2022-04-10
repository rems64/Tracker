#!/usr/bin/env python3
import argparse
import time

description = "Run world reconstruction on input data"
argparser = argparse.ArgumentParser(description=description)
argparser.add_argument("-i", "--input", help="Path to the input data file", required=True)
argparser.add_argument("-c", "--usecache", help="Use cached result", required=False, default=False)
args = argparser.parse_args()



if __name__ == "__main__":
    import tracker.utils as utils
    import tracker.naivePerspectiveSolver as nps
    import tracker.world as wd
    import tracker.visualize as vz

    utils.log("Starting pipeline...", utils.logTypes.info)
    begin = time.time()

    utils.log("Loading data from "+args.input, utils.logTypes.info)
    inputData = utils.open_json(args.input)
    world = wd.createWorld(inputData)

    utils.log(world, utils.logTypes.warning)
    utils.log(world.cameras[0], utils.logTypes.error)

    end = time.time()
    utils.log("Pipeline finished in {:.2f} seconds".format(end - begin), utils.logTypes.timer)
    utils.log("Shutting down pipeline", utils.logTypes.info)