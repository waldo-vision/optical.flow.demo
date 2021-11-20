"""Adapted from the OpenCV optical flow documentation code: https://docs.opencv.org/4.5.3/d4/dee/tutorial_optical_flow.html"""

""" ABOUT-----------------------------------------------------------------------
Farneback Optical Flow calculates the optical flow (motion) of every pixel in a video clip.
Right now, in the result visualization, the intensity of a pixel's motion will change both it's color and magnitude.
Brighter pixels have more motion.
The output visualization is stored in the same location as the input video with the name <input_vid_filename>_FB_FLOW.mp4
The idea is that perhaps the data about how certain pixels/features are moving across the screen could be used to figure out how the player camera / aim was changing.
"""

import numpy as np
import cv2 as cv

# PARAMETERS--------------------------------

# path to input video file
vidpath = r""

# do you want to save the output video?
savevid = True

# fps of input/output video
fps = 30

# farneback parameters (currently set to default)
pyr_scale = 0.5  # default 0.5
levels = 5  # default 3
winsize = 15  # default 15
iterations = 3  # default 3
poly_n = 2  # default 5
poly_sigma = 1.2  # default 1.2
flags = cv.OPTFLOW_FARNEBACK_GAUSSIAN

# SETUP ------------------------------------

# load video into memory and assign it to variable cap
cap = cv.VideoCapture(vidpath)

# read first frame using variable cap
_, old_frame = cap.read()
old_frame_gray = cv.cvtColor(
    old_frame, cv.COLOR_BGR2GRAY
)

# create black result image
hsv_img = np.zeros_like(old_frame)
hsv_img[..., 1] = 255

# if saving video
if savevid:
    # path to save output video
    savepath = (
        vidpath.split(".")[0]
        + "_FB_FLOW"
        + ".mp4"
    )

    # get shape of video frames
    height, width, channels = old_frame.shape

    # setup videowriter object
    fourcc = cv.VideoWriter_fourcc(*"mp4v")
    videoOut = cv.VideoWriter(
        savepath,
        fourcc,
        fps,
        (width, height),
    )
# PROCESS VIDEO ---------------------------
while True:
    # get frame and convert to grayscale
    _, new_frame = cap.read()
    new_frame_gray = cv.cvtColor(
        new_frame, cv.COLOR_BGR2GRAY
    )

    # do Farneback optical flow
    flow = cv.calcOpticalFlowFarneback(
        old_frame_gray,
        new_frame_gray,
        None,
        pyr_scale,
        levels,
        winsize,
        iterations,
        poly_n,
        poly_sigma,
        flags,
    )

    # conversion
    mag, ang = cv.cartToPolar(
        flow[..., 0], flow[..., 1]
    )

    # draw onto the result image - color is determined by direction, brightness is by magnitude of motion
    # hsv_img[...,0] = ang*180/np.pi/2
    # hsv_img[...,2] = cv.normalize(mag, None, 0, 255, cv.NORM_MINMAX)

    # color and brightness by magnitude
    hsv_img[..., 0] = cv.normalize(
        mag, None, 0, 255, cv.NORM_MINMAX
    )
    hsv_img[..., 1] = cv.normalize(
        mag, None, 0, 255, cv.NORM_MINMAX
    )
    hsv_img[..., 2] = cv.normalize(
        mag, None, 0, 255, cv.NORM_MINMAX
    )

    bgr_img = cv.cvtColor(
        hsv_img, cv.COLOR_HSV2BGR
    )

    #  show the image and break out if ESC pressed
    cv.imshow(
        "Farneback Optical Flow", bgr_img
    )
    k = cv.waitKey(30) & 0xFF
    if k == 27:
        break
    # write frames to new output video
    if savevid:
        videoOut.write(bgr_img)
    # set old frame to new
    old_frame_gray = new_frame_gray
# cleanup
videoOut.release()
cv.destroyAllWindows()
