import os
import streamlit as st
from byteplussdkarkruntime import Ark
from byteplussdkarkruntime.types.images.images import SequentialImageGenerationOptions

# ------------------------------
# Initialize Ark client
# ------------------------------
client = Ark(
    base_url="https://ark.ap-southeast.bytepluses.com/api/v3",
    api_key=os.environ.get("ARK_API_KEY"),
)

# ------------------------------
# Streamlit UI
# ------------------------------
st.set_page_config(page_title="Seedream 4.0 Image Generator", layout="centered")
st.title("🎨 BytePlus Seedream 4.0 Demo")

st.write("Generate images using Seedream 4.0 by uploading reference images and writing a prompt.")

# User inputs
prompt = st.text_area("Prompt", "Replace the clothing in image 1 with the outfit from image 2.")

image1_url = st.text_input("Image 1 URL", "https://ark-doc.tos-ap-southeast-1.bytepluses.com/doc_image/seedream4_imagesToimage_1.png")
image2_url = st.text_input("Image 2 URL", "https://ark-doc.tos-ap-southeast-1.bytepluses.com/doc_image/seedream4_imagesToimage_2.png")

size_option = st.selectbox("Image Size", ["1K", "2K", "4K"])
watermark = st.checkbox("Add Watermark", value=True)

# Button to generate
if st.button("Generate Image"):
    with st.spinner("Generating image..."):
        try:
            response = client.images.generate(
                model="seedream-4-0-250828",
                prompt=prompt,
                image=[image1_url, image2_url],
                size=size_option,
                sequential_image_generation=SequentialImageGenerationOptions.DISABLED,
                response_format="url",
                watermark=watermark
            )

            # Display result
            if response.data and len(response.data) > 0:
                st.success("✅ Image generated successfully!")
                for idx, img in enumerate(response.data):
                    st.image(img.url, caption=f"Generated Image {idx+1}", use_column_width=True)
            else:
                st.error("No image returned from API.")

        except Exception as e:
            st.error(f"Error generating image: {e}")
