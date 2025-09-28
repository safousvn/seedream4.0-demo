import streamlit as st
import requests

# ------------------------------
# Streamlit Page Config
# ------------------------------
st.set_page_config(page_title="Seedream 4.0 Demo", layout="centered")
st.title("🎨 Seedream 4.0 Demo (REST API)")

st.write(
    "Upload two reference images, write a prompt, and generate new images using Seedream 4.0."
)

# ------------------------------
# Upload Images
# ------------------------------
st.subheader("Upload Images")
image1_file = st.file_uploader("Image 1", type=["png", "jpg", "jpeg"])
image2_file = st.file_uploader("Image 2", type=["png", "jpg", "jpeg"])

# Preview uploaded images
if image1_file:
    st.image(image1_file, caption="Uploaded Image 1", use_column_width=True)
if image2_file:
    st.image(image2_file, caption="Uploaded Image 2", use_column_width=True)

st.write(
    "⚠️ Note: Ark API requires public URLs for images. Upload your images to a public hosting service "
    "(e.g., Imgur, Postimages) and paste the URLs below."
)

# ------------------------------
# Image URLs for API
# ------------------------------
image1_url = st.text_input("Image 1 Public URL (for API)")
image2_url = st.text_input("Image 2 Public URL (for API)")

# ------------------------------
# Prompt and options
# ------------------------------
prompt = st.text_area("Prompt", "Replace the clothing in image 1 with the outfit from image 2.")
size_option = st.selectbox("Image Size", ["1K", "2K", "4K"])
watermark = st.checkbox("Add Watermark", value=True)

# ------------------------------
# Generate Image
# ------------------------------
if st.button("Generate Image"):
    if not image1_url or not image2_url:
        st.error("Please provide public URLs for both images.")
    else:
        try:
            ark_api_key = st.secrets["ARK_API_KEY"]
        except KeyError:
            st.error("API Key not found. Add ARK_API_KEY in Streamlit Secrets.")
        else:
            url = "https://ark.ap-southeast.bytepluses.com/api/v3/images/generations"
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
                "watermark": watermark
            }

            with st.spinner("Generating image..."):
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
                except requests.exceptions.HTTPError as http_err:
                    st.error(f"HTTP error: {http_err}")
                except Exception as e:
                    st.error(f"Error: {e}")
