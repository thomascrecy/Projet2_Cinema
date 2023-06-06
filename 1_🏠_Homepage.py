import streamlit as st 

st.set_page_config(
    page_title='Accueil',
    page_icon='🎥'
)
#st.sidebar.error('20th Century Pandas', icon='🎥')

# import base64
# def add_bg_from_local(image_file):
#     with open(image_file, "rb") as image_file:
#         encoded_string = base64.b64encode(image_file.read())
#     st.markdown(
#     f"""
#     <style>
#     .stApp {{
#         background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
#         background-size: cover
#     }}
#     </style>
#     """,
#     unsafe_allow_html=True
#     )
# add_bg_from_local('Popcorn.png')

import streamlit as st
from PIL import Image

image = Image.open('logo.png')
st.image(image)
