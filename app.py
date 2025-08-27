
import streamlit as st
from rembg import remove
from PIL import Image, ImageOps
import io

def center_crop(image, size):
    # Center crop to square size (size x size)
    return ImageOps.fit(image, (size, size), method=Image.LANCZOS, centering=(0.5, 0.5))

st.title("Profile Photo Background Remover & Center Crop")

uploaded_file = st.file_uploader("Upload a JPEG photo", type=["jpg", "jpeg"])
if uploaded_file:
    input_image = Image.open(uploaded_file).convert("RGBA")

    # Remove background
    output_image = remove(input_image)

    # Center crop to square based on shortest side
    #min_side = min(output_image.size)
    #cropped = center_crop(output_image, min_side)
    
    cropped = output_image
    st.image(cropped, caption="Processed Image", use_column_width=True)

    # Save to bytes
    buf = io.BytesIO()
    cropped.save(buf, format="PNG")
    byte_im = buf.getvalue()

    st.download_button(
        label="Download Edited Image",
        data=byte_im,
        file_name="profile_no_bg.png",
        mime="image/png"
    )
