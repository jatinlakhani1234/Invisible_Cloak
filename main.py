import cv2
import numpy as np
import time

def nothing(x):
    pass


# Capturing the video
cap = cv2.VideoCapture(0)
time.sleep(1)  # Give time for camera to warm up

while cv2.waitKey(10) != ord(' ') and cap.isOpened():
    ret, frame = cap.read()
    cv2.imshow('Video', frame)

# Getting the background
for i in range(35):
    if cap.isOpened():
        ret, background = cap.read()  # Reading frames one by one from the video

cv2.imshow('Background', background)
cv2.waitKey(0)

# Sliders for getting the HSV
cv2.namedWindow('Slider')
cv2.createTrackbar('LH', 'Slider', 0, 179, nothing)
cv2.createTrackbar('LS', 'Slider', 0, 255, nothing)
cv2.createTrackbar('LV', 'Slider', 0, 255, nothing)
cv2.createTrackbar('UH', 'Slider', 179, 179, nothing)
cv2.createTrackbar('US', 'Slider', 255, 255, nothing)
cv2.createTrackbar('UV', 'Slider', 255, 255, nothing)

while cv2.waitKey(10) != ord(' ') and cap.isOpened():
    ret, frame = cap.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lh = cv2.getTrackbarPos('LH', 'Slider')
    ls = cv2.getTrackbarPos('LS', 'Slider')
    lv = cv2.getTrackbarPos('LV', 'Slider')
    uh = cv2.getTrackbarPos('UH', 'Slider')
    us = cv2.getTrackbarPos('US', 'Slider')
    uv = cv2.getTrackbarPos('UV', 'Slider')

    lower_bound = np.array([lh, ls, lv])
    upper_bound = np.array([uh, us, uv])

    mask = cv2.inRange(hsv, lower_bound, upper_bound)
    # mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), dtype=np.uint8), iterations=3)
    mask = cv2.erode(mask, np.ones((5, 5), dtype=np.uint8), iterations=3)
    mask = cv2.dilate(mask, np.ones((5, 5), dtype=np.uint8), iterations=5)
    res = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow('Frame', frame)
    cv2.imshow('Mask', mask)
    cv2.imshow('Result', res)

cv2.destroyAllWindows()

while cv2.waitKey(10) != ord(' ') and cap.isOpened():
    ret, frame = cap.read()
    # cv2.imshow('Original_Video', frame)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, lower_bound, upper_bound)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), dtype=np.uint8), iterations=3)
    mask = cv2.dilate(mask, np.ones((3, 3), dtype=np.uint8))
    mask_inverted = cv2.bitwise_not(mask)

    foreground = cv2.bitwise_and(frame, frame, mask=mask_inverted)
    background_new = cv2.bitwise_and(background, background, mask=mask)

    # result = cv2.addWeighted(foreground, 1, background, 1, gamma=0)
    result = cv2.add(foreground, background_new)


    cv2.imshow("Invisible_cloak", result)


cap.release()
cv2.destroyAllWindows()