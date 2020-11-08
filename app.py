import streamlit as st
import SessionState
from functions import Camera, Mask, Magic

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

    dict2 = {'Front': 0, 'Back': 1}
    x = st.selectbox('Choose an option for your input camera', ('Front', 'Back'))
    x = dict2[x]

    cap, background = Camera(x)
    session_state.background = background
    session_state.cap = cap
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
