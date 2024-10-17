import streamlit as st
from PIL import Image


st.set_page_config(
    layout='wide',
    initial_sidebar_state = 'expanded'
)

profile,data = st.columns([0.2,0.8])
LO = profile.button("Log out")
if LO:
    st.session_state['st_name'] = ""
    st.session_state['Student_login'] =False
    st.session_state['ad_name'] = ""
    st.session_state['Admin_login'] =False
    st.switch_page("Home.py")
    st.empty()
if "Student_login" and "st_name" in st.session_state and st.session_state["Student_login"]==True:
    st.write("Welcome "+st.session_state['st_name']+'😄')
    photo = Image.open('C:/Users/KOTA SRI SURYA TEJA/Desktop/Wastage/desktop/photo.jpeg').resize(size=(300,300))

    profile.image(photo,caption=st.session_state['st_name'])
    data.success("Hi dear")
elif "Admin_login" and "ad_name" in st.session_state and st.session_state["Admin_login"]==True:
    st.write("Welcome Admin "+st.session_state['ad_name']+'😊')
    photo = Image.open('C:/Users/KOTA SRI SURYA TEJA/Desktop/Wastage/desktop/photo.jpeg').resize(size=(300,300))
    profile.image(photo,caption=st.session_state['st_name'])
    data.success("Hi munda")
else:
    profile.warning("Please show yourself🧐")