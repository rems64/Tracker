import numpy as np

def constructIntrinsicMatrix(frameResolution, sensorHeight, focalLength):
    """
    @param frameResolution: (width, height) in pixels
    @param sensorWidth: width of the sensor in mm
    @param sensorHeight: height of the sensor in mm
    @param focalLength: focal length of the lens in mm
    """
    aspectRatio = frameResolution[0] / frameResolution[1]
    fx = focalLength * frameResolution[0] / (sensorHeight * aspectRatio)
    fy = focalLength * frameResolution[1] / sensorHeight
    cx = frameResolution[0] / 2
    cy = frameResolution[1] / 2
    return np.matrix([[fx, 0, cx], [0, fy, cy], [0, 0, 1]])


def constructInverseIntrinsicMatrix(frameResolution, sensorHeight, focalLength):
    """
    @param frameResolution: (width, height) in pixels
    @param sensorWidth: width of the sensor in mm
    @param sensorHeight: height of the sensor in mm
    @param focalLength: focal length of the lens in mm
    """
    aspectRatio = frameResolution[0] / frameResolution[1]
    fx = focalLength * frameResolution[0] / (sensorHeight * aspectRatio)
    fy = focalLength * frameResolution[1] / sensorHeight
    cx = frameResolution[0] / 2
    cy = frameResolution[1] / 2
    return np.matrix([[1/fx, 0, -cx/fx], [0, 1/fy, -cy/fy], [0, 0, 1]])