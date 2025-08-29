
import streamlit as st
from rembg import remove
from PIL import Image, ImageOps
import io
from streamlit_drawable_canvas import st_canvas
#from streamlit import image_to_url

def center_crop(image, size):
    # Center crop to square size (size x size)
    return ImageOps.fit(image, (size, size), method=Image.LANCZOS, centering=(0.5, 0.5))

st.title("Profile Photo Background Remover")

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
    img_width, img_height = output_image.size
    canvas_result = st_canvas(
        fill_color="",
        stroke_width=3,
        stroke_color="#FF0000",
        background_image=output_image,
        height=img_height if img_height<600 else 600,
        width=img_width if img_width<800 else 800,
        drawing_mode="rect",
        key="canvas",
    )
    if canvas_result.json_data and "shapes" in canvas_result.json_data:
        shapes = canvas_result.json_data["shapes"]
        if shapes:
            rect = shapes[-1]["geometry"]
            x, y = int(rect["x"]), int(rect["y"])
            w, h = int(rect["width"]), int(rect["height"])

            # Crop the rectangle area from output_image
            cropped = output_image.crop((x, y, x + w, y + h))

            st.image(cropped, caption="Cropped Selection", use_column_width=True)

            # Save cropped to bytes
            buf = io.BytesIO()
            cropped.save(buf, format="PNG")
            byte_im = buf.getvalue()

            st.download_button(
                label="Download Cropped Image",
                data=byte_im,
                file_name="cropped_no_bg.png",
                mime="image/png"
            )
