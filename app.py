import os
import streamlit as st
import requests

# ------------------------------
# Streamlit UI
# ------------------------------
st.set_page_config(page_title="Seedream 4.0 REST Demo", layout="centered")
st.title("🎨 BytePlus Seedream 4.0 Demo (REST API)")

st.write("Generate images using Seedream 4.0 by uploading reference images and writing a prompt.")

# User inputs
prompt = st.text_area("Prompt", "Replace the clothing in image 1 with the outfit from image 2.")

image1_url = st.text_input(
    "Image 1 URL",
    "https://ark-doc.tos-ap-southeast-1.bytepluses.com/doc_image/seedream4_imagesToimage_1.png",
)
image2_url = st.text_input(
    "Image 2 URL",
    "https://ark-doc.tos-ap-southeast-1.bytepluses.com/doc_image/seedream4_imagesToimage_2.png",
)

size_option = st.selectbox("Image Size", ["1K", "2K", "4K"])
watermark = st.checkbox("Add Watermark", value=True)

# Generate button
# ark_api_key = os.environ.get("ARK_API_KEY")
if st.button("Generate Image"):
    ark_api_key = st.secrets["ARK_API_KEY"]
    if not ark_api_key:
        st.error("API Key not found. Please set ARK_API_KEY environment variable.")
    else:
        with st.spinner("Generating image..."):
            url = "https://ark.ap-southeast.bytepluses.com/api/v3/images/generate"
            headers = {
                "Authorization": f"Bearer {ark_api_key}",
                "Content-Type": "application/json",
            }
            payload = {
                "model": "seedream-4-0-250828",
                "prompt": prompt,
                "image": [image1_url, image2_url],
                "size": size_option,
                "sequential_image_generation": "disabled",
                "response_format": "url",
                "watermark": watermark,
            }
            try:
                response = requests.post(url, json=payload, headers=headers)
                response.raise_for_status()
                data = response.json()

                if "data" in data and len(data["data"]) > 0:
                    st.success("✅ Image generated successfully!")
                    for idx, img in enumerate(data["data"]):
                        st.image(img["url"], caption=f"Generated Image {idx+1}", use_column_width=True)
                else:
                    st.error("❌ No image returned from API.")
            except Exception as e:
                st.error(f"Error: {e}")
