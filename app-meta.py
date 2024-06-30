import streamlit as st
from PIL import Image

def main():
    st.title("Image Uploader")

    st.write("Upload an image or click one from the sidebar.")

    # Sidebar for uploading or clicking an image
    st.sidebar.title("Upload or Click Image")
    uploaded_file = st.sidebar.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

    if uploaded_file is not None:
        # Display uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

    # Click to capture an image (not implemented in Streamlit natively, would require custom implementation)

if __name__ == "__main__":
    main()
