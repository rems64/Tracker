import numpy as np
import cv2

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

def computeProjectionMatrix(camera, worldObject):
    """
    @param camera: Camera object
    @param worldObject: WorldObject object
    """
    # Get the rotation matrix
    rotation = np.matrix([[np.cos(worldObject.rotation[0]), -np.sin(worldObject.rotation[0]), 0],
                            [np.sin(worldObject.rotation[0]), np.cos(worldObject.rotation[0]), 0],
                            [0, 0, 1]])
    # Get the translation matrix
    translation = np.matrix([[1, 0, 0, -worldObject.location[0]],
                            [0, 1, 0, -worldObject.location[1]],
                            [0, 0, 1, -worldObject.location[2]],
                            [0, 0, 0, 1]])
    # Get the extrinsic matrix
    extrinsic = rotation * translation
    # Get the intrinsic matrix
    intrinsic = constructIntrinsicMatrix(camera.resolution, camera.sensorHeight, camera.focalLength)
    # Get the projection matrix
    projection = intrinsic * extrinsic
    return projection



cv2.createCameraMatrix(27)