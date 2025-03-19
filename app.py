import streamlit as st
import cv2 as cv
import numpy as np
from functions import *
from PIL import Image
from streamlit_lottie import st_lottie
import json

st.set_page_config(page_title="DaVinci", page_icon="🎨", layout="wide")
st.markdown(
    """
    <style>
        .block-container {
            padding-left: 8rem;
            padding-right: 8rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Load Lottie file from local JSON
def load_lottie_file(filepath):
    with open(filepath, "r") as f:
        return json.load(f)

lottie_animation = load_lottie_file("Animation - 1742391387884.json")

col1, col2 = st.columns([1, 2])

with col1:
    st_lottie(lottie_animation, speed=1, width=250, height=250, loop=True)

with col2:
    st.title("🖌️ DaVinci")
    st.subheader("Your personal painter!")
    st.write("🎨 Go to the sidebar and upload an image to get your piece of art!")

with st.sidebar:
    st.header("⚙️ Settings")
    st.write("Customize your image processing options below:")
    
    st.divider()

    uploaded_file = st.file_uploader("📂 Upload an image", type=["jpg", "png", "jpeg"])

    st.subheader("🖼️ Select an Effect:")
    effect = st.radio("", ("Sketch", "Color Sketch", "Watercolor"), horizontal=True)

    st.subheader("🗑️ Additional Options:")
    remove_bg = st.checkbox("Remove Background")

    st.markdown("---")
    st.info("✨ Tip: Try different effects to see what works best!")

# File Upload
if uploaded_file:

    image = Image.open(uploaded_file)
    image = np.array(image)  # Convert PIL to NumPy array
    image = cv.resize(image, (800, 500))

    if remove_bg:
        image = remove_background(image)

    if effect == "Sketch":
        output_image = apply_sketch_effect(image)
    elif effect == "Watercolor":
        # Add sliders for sigma_s and sigma_r
        sigma_s = st.slider("Smoothness", min_value=0, max_value=200, value=100, step=1)
        sigma_r = st.slider("Edge Preservation", min_value=0.0, max_value=1.0, value=0.45, step=0.01)

        with st.expander("How to Adjust Settings? 🎨"):
            st.markdown("""
            - **Increase Smoothness** for smoother edges. Higher values create a more refined sketch.  
            - **Decrease Edge Preservation ** for more details. Lower values enhance fine details.  
            """)

        output_image = apply_watercolor_effect(image, sigma_s, sigma_r)  

    else:
        sigma_s = st.slider("Smoothness", min_value=0, max_value=200, value=100, step=1)
        sigma_r = st.slider("Edge Preservation", min_value=0.0, max_value=1.0, value=0.07, step=0.01)
        shade_factor=st.slider("Shading", min_value=0.0, max_value=1.0, value=0.09, step=0.01)
        with st.expander("How to Adjust Settings? 🎨"):
            st.markdown("""
            - **Increase Smoothness** for smoother edges. Higher values create a more refined sketch.  
            - **Decrease Edge Preservation** for more details. Lower values enhance fine details.  
            - **Adjust Shading** to control contrast. Lower values produce lighter sketches, while higher values make the shadows darker.  
            """)
        output_image=apply_color_sketch_effect(image,sigma_s, sigma_r,shade_factor)

    # Create two equal columns
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🖼️ Original Image")  # Section title
        st.image(image, caption="Original Image", use_container_width=True)

    with col2:
        st.markdown(f"### 🎨 {effect} Effect")  # Section title
        st.image(output_image, caption=f"{effect} Effect", use_container_width=True)

    # Add spacing between sections
    st.markdown("<br>", unsafe_allow_html=True)

    # Download button
    result = cv.imencode(".png", output_image)[1].tobytes()
    st.markdown("### 📥 Download Your Processed Image")
    st.download_button("Download Processed Image", result, file_name="processed_image.png", mime="image/png")
