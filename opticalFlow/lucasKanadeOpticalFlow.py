"""Adapted from the OpenCV optical flow documentation code: https://docs.opencv.org/4.5.3/d4/dee/tutorial_optical_flow.html"""

""" ABOUT-----------------------------------------------------------------------
Lucas Kanade Optical Flow calculates the optical flow (motion) of specific features in a video clip.
The Shi-Tomasi corner detection is used to pick points in the video that are easy for to track.
The optical flow algorithm will track where those features move.
The visualization will draw a point over the tracked features and a trail of where the feature has been.
The program currently outputs the result video to the same location as your input video, with the name <input_vid_filename>_LK_FLOW.mp4

The idea is that perhaps the data about how certain pixels/features are moving across the screen could be used to figure out how the player camera / aim was changing.
"""

import cv2 as cv
import numpy as np
import os, sys

# PARAMETERS------------------------------------------------------------------

#Canny Threshholds
th1 = 300
th2 = 300

# path to input videofile
vidpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bf_clip.mp4")

# do you want to save the video?
savevid = False

# do you want to preview the output?
previewWindow = True

# output video params
fps = 30 # fps of output video, should match input video

# visualization parameters
numPts = 3 # max number of points to track
trailLength = 600 # how many frames to keep a fading trail behind a tracked point to show motion
trailThickness = 8 # thickness of the trail to draw behind the target
trailFade = 0 # the intensity at which the trail fades
pointSize = 10 # pixel radius of the circle to draw over tracked points

# params for Shi-Tomasi corner detection
shitomasi_params = {
    "qualityLevel": 0.3,
    "minDistance": 7,
    "blockSize": 7
}

# params for Lucas-Kanade optical flow
LK_params = {
    "winSize": (15,15),
    "maxLevel": 2,
    "criteria": (cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03)
}


# SETUP -----------------------------------------------------------------------

# generate random colors
color = np.random.randint(0,255,(100,3))

# read the video file into memory
cap = cv.VideoCapture(vidpath)

# get the first frame
_, old_frame = cap.read()
old_gray = cv.cvtColor(old_frame, cv.COLOR_BGR2GRAY)
old_gray = cv.Canny(old_gray, th1, th2)

# get resolution of video
res_x = len(old_frame[0])
res_y = len(old_frame)

# create crosshair mask
crosshair_bottom = int(0.7*res_y)
crosshair_top = int(0.3*res_y)
crosshair_left = int(0.3*res_x)
crosshair_right = int(0.7*res_x)
crosshairmask = np.zeros(old_frame.shape[:2], dtype="uint8")
cv.rectangle(crosshairmask, (crosshair_left, crosshair_top), (crosshair_right, crosshair_bottom), 255, -1)

# create masks for drawing purposes
trail_history = [[[(0,0), (0,0)] for i in range(trailLength)] for i in range(numPts)]

# get features from first frame
print(f"\nRunning Optical Flow on: {vidpath}")
old_points = cv.goodFeaturesToTrack(old_gray, maxCorners=numPts, mask=crosshairmask, **shitomasi_params)

# if saving video
if savevid:
    # path to save output video
    pathparts = vidpath.split('.')
    savepath = vidpath.split('.')[-2] + '_LK_FLOW' + '.mp4'
    print(f"Saving Output video to: {savepath}")

    # get shape of video frames
    height, width, channels = old_frame.shape

    # setup videowriter object
    fourcc = cv.VideoWriter_fourcc(*'mp4v')
    videoOut = cv.VideoWriter(savepath, fourcc, fps, (width, height))

# PROCESS VIDEO ---------------------------------------------------------------
while(True):
    # get next frame and convert to grayscale
    stillGoing, new_frame = cap.read()

    # if video is over, quit
    if not stillGoing:
        break

    # convert to grayscale edge map using canny
    new_frame_gray = cv.Canny(new_frame, th1, th2)
    imgCanny = new_frame_gray

     #convert single channel Canny image to three channel image
    imgCanny = cv.merge((imgCanny,imgCanny,imgCanny))

    # calculate optical flow
    new_points, st, err = cv.calcOpticalFlowPyrLK(old_gray, new_frame_gray, old_points, None, **LK_params)

    # select good points
    if old_points is not None:
        good_new = new_points[st==1]
        good_old = old_points[st==1]

    # create trail mask to add to image
    trailMask = np.zeros_like(old_frame)

    # calculate motion lines and points
    for i,(new,old) in enumerate(zip(good_new, good_old)):
        # flatten coords
        a,b = new.ravel()
        c,d = old.ravel()

        # list of the prev and current points converted to int
        linepts = [(int(a),int(b)), (int(c),int(d))]

        # add points to the trail history
        trail_history[i].insert(0, linepts)

        # get color for this point
        pointColor = color[i].tolist()

        # add trail lines
        for j in range(len(trail_history[i])):
            trailColor = [int( pointColor[0] - (trailFade*j) ), int( pointColor[1] - (trailFade*j) ), int( pointColor[2] - (trailFade*j) )] # fading colors
            trailMask = cv.line(trailMask, trail_history[i][j][0], trail_history[i][j][1], trailColor, thickness=trailThickness, lineType=cv.LINE_AA)
        
        # get rid of the trail segment
        trail_history[i].pop()

        # add circle over the point
        new_frame = cv.circle(new_frame, trail_history[i][0][0], pointSize, color[i].tolist(), -1)
        imgCanny = cv.circle(imgCanny, trail_history[i][0][0], pointSize, color[i].tolist(), -1)
    
   
    # add trail to frame
    img = cv.add(new_frame, trailMask)
    imgCanny = cv.add(imgCanny, trailMask)

    # show the frames
    if previewWindow:
        cv.imshow('trailMask', trailMask)
        cv.imshow('optical flow', img)
        cv.imshow('canny', imgCanny)

    # write frames to new output video
    if savevid:
        videoOut.write(img)
    
    #Save a jpg to see how the canny img looks like
    #cv.imwrite(vidpath.split('.')[0] + 'test' + str(th1) + "-" + str(th2) + '.jpg', new_frame_gray)

    # kill window if ESC is pressed
    k = cv.waitKey(30) & 0xff
    if k == 27:
        break

    # update previous frame and previous points
    old_gray = new_frame_gray.copy()
    old_points = good_new.reshape(-1,1,2)

    # if old_points < numPts, get new points
    if (numPts - len(old_points)) > 0:
        old_points = cv.goodFeaturesToTrack(old_gray, maxCorners=numPts, mask=crosshairmask, **shitomasi_params)

# after video is finished
print('\nComplete!\n')