import cv2
import numpy as np
import time
import streamlit as st


def Camera(x):
    cap = cv2.VideoCapture(x)
    frames1 = st.empty()
    button1 = st.button('DONE', key=0)
    while cap.isOpened() and not button1:
        frames1.image(cap.read()[1], channels="BGR")
    if button1:
        time.sleep(2)
        background = cap.read()[1]
    return cap, background


def Mask(cap):
    frames2 = st.empty()
    frames3 = st.empty()
    frames4 = st.empty()
    lh = st.slider('Lower Hue', 0, 179, 37)
    ls = st.slider('Lower Saturation', 0, 255, 0)
    lv = st.slider('Lower Value', 0, 255, 0)
    uh = st.slider('Upper Hue', 0, 179, 88)
    us = st.slider('Upper Saturation', 0, 255, 255)
    uv = st.slider('Upper Value', 0, 255, 255)
    button2 = st.button('DONE', key=1)

    while cap.isOpened() and not button2:
        ret, frame = cap.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        lower_bound = np.array([lh, ls, lv])
        upper_bound = np.array([uh, us, uv])

        mask = cv2.inRange(hsv, lower_bound, upper_bound)
        # mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), dtype=np.uint8), iterations=3)
        mask = cv2.erode(mask, np.ones((5, 5), dtype=np.uint8), iterations=3)
        mask = cv2.dilate(mask, np.ones((5, 5), dtype=np.uint8), iterations=5)
        res = cv2.bitwise_and(frame, frame, mask=mask)

        frames2.image(frame, channels="BGR", caption='This is Frame')
        frames3.image(mask, caption='This is Mask')
        frames4.image(res, channels="BGR", caption='This is Result')

    return np.array([lh, ls, lv]), np.array([uh, us, uv])


def Magic(cap, lower_bound, upper_bound, background):
    frames5 = st.empty()
    button3 = st.button('DONE', key=2)
    while cap.isOpened() and not button3:
        ret, frame = cap.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, lower_bound, upper_bound)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), dtype=np.uint8), iterations=3)
        mask = cv2.dilate(mask, np.ones((3, 3), dtype=np.uint8))
        mask_inverted = cv2.bitwise_not(mask)

        foreground = cv2.bitwise_and(frame, frame, mask=mask_inverted)
        background_new = cv2.bitwise_and(background, background, mask=mask)

        # result = cv2.addWeighted(foreground, 1, background, 1, gamma=0)
        result = cv2.add(foreground, background_new)
        frames5.image(result, channels="BGR")
