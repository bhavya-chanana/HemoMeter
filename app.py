import streamlit as st
import tempfile
import os
from process_vid import videoDetails, extract_ppg_from_video, convert_csv, pyppgFeatures, FeaturesDict
from predict import predict_hb

def main():
    # Inject custom CSS
    st.markdown(
        """
        <style>
        .stButton button {
            margin-top: 10px;
            margin-bottom: 10px;
        }
        .stNumberInput, .stSelectbox {
            margin-top: 10px;
            margin-bottom: 10px;
        }
        .stFileUploader {
            margin-top: 10px;
            margin-bottom: 10px;
        }
        .stExpander {
            margin-top: 20px;
            margin-bottom: 20px;
        }
        .stMarkdown h2 {
            margin-top: 20px;
            margin-bottom: 20px;
        }
        </style>
        """, 
        unsafe_allow_html=True
    )

    st.title("HemoMeter")
    st.write('Calculating Hemoglobin is now as easy as placing your finger on the camera, literally.')

    # Input fields for age and gender
    age = st.number_input("Enter your age:", min_value=0, max_value=120, step=1, value=21)
    gender = st.selectbox("Select your gender:", ["M", "F"])

    # Expander for instructions
    with st.expander("""**How to Take a Good Recording for Accurate Hemoglobin Prediction**"""):
        st.write("""
        - **Clean and Clear Equipment**: Make sure your finger, camera lens, and flash are clean and unobstructed.
        - **Cover the Camera and Flash**: Cover the main(wide lens) camera and flash with your finger, ensure no external light is detected by the camera.
        - **Keep the Camera Stable**: Avoid any movement or shaking during the recording.
        - **Record for at Least 25 Seconds**: Ensure the recording duration is sufficient for a stable reading.
        - **Prevent Flash Overheating**: Ensure the flash does not overheat during the recording.
        """)
        st.image("images/ppg_example.png", caption="Sample PPG Reading")

    # File uploader for video on the main page
    uploaded_file = st.file_uploader("Choose a video...", type=["mp4", "mov"])

    if uploaded_file is not None:
        # Display uploaded video
        # st.video(uploaded_file)

        # Save the uploaded file to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as temp_file:
            temp_file.write(uploaded_file.getbuffer())
            temp_video_path = temp_file.name

        if st.button("Calculate Hb"):
            video_file = os.path.basename(temp_video_path)
            video_name = os.path.splitext(video_file)[0]
            video_extension = os.path.splitext(video_file)[1]

            videoDetailsDict = videoDetails(video_name, age, gender)

            red_ppg, green_ppg, fps = extract_ppg_from_video(temp_video_path, start_time=0, duration=20)
            
            if video_extension == ".mov":
                convert_csv(red_ppg, video_name)
            else:
                convert_csv(green_ppg, video_name)

            ppgplot = pyppgFeatures(video_name)  # gets features and plots them

            features_dict = FeaturesDict(videoDetailsDict)

            Hb_predicted = predict_hb(features_dict)
            # Display uploaded video
            st.pyplot(ppgplot)
            # Display the predicted Hb value using Streamlit's built-in functions
            st.subheader(f"Predicted Hb: {Hb_predicted:.2f}")

            # Clean up temporary file
            os.remove(temp_video_path)



    # Place buttons in columns for inline display
    col1, col2, col3, col4 = st.columns(4)


if __name__ == "__main__":
    main()
