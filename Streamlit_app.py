import cv2
import numpy as np
import time
import streamlit as st
import SessionState


def Camera(cap):
    frames1 = st.empty()
    button1 = st.button('DONE', key=0)
    while cap.isOpened() and not button1:
        frames1.image(cap.read()[1], channels="BGR")
    if button1:
        time.sleep(2)
        return cap.read()[1]
    cap.release()
    st.write("Failed to load camera")
    return None


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


st.markdown('''# Invisible Cloak''')

st.sidebar.header('Choose the option: ')
option = st.sidebar.radio('Choose the option', ['Choose Camera and Background', 'Mask', 'Magic'])
dict1 = {'Choose Camera and Background': 0, 'Mask': 1, 'Magic': 2}
option = dict1[option]
st.sidebar.write(option)
session_state = SessionState.get(name='', background=None, cap=None, lower_bound=None, upper_bound=None)

if option == 0:
    st.markdown('''        
            ## **1. Choose camera and Background**
            ### Adjust your camera according to the needs, when done press DONE. The
            background image will be captured after 2 seconds.
            ''')

    dict2 = {'Front': -1, 'Back': 0}
    x = st.selectbox('Choose an option for your input camera', ('Front', 'Back'))
    x = dict2[x]
    cap = cv2.VideoCapture(x)
    
    background = Camera(cap)
    session_state.background = background
    session_state.cap = cap
    if background:
        st.image(background, channels="BGR")
        st.write('This is the background image')


if option == 1:
    st.markdown('''
            ## **2. Choose the HSV**
            ### Choose the mask by setting the slider.
            ''')
    cap = session_state.cap
    lower_bound, upper_bound = Mask(cap)
    session_state.lower_bound, session_state.upper_bound = lower_bound, upper_bound


if option == 2:
    st.markdown('''
            ## **2. It's Magic Time**
            ### Move the object around and see the magic.
            ''')
    cap, background, lower_bound, upper_bound = session_state.cap,session_state.background, session_state.lower_bound, session_state.upper_bound
    Magic(cap, lower_bound, upper_bound, background)
    cap.release()
