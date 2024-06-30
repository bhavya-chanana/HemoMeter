import streamlit as st
import tempfile
import os
from process_vid import videoDetails, extract_ppg_from_video, convert_csv, pyppgFeatures, FeaturesDict
from predict import predict_hb

def main():
    st.title("HemoMeter")

    # Input fields for age and gender
    age = st.number_input("Enter your age:", min_value=0, max_value=120, step=1)
    gender = st.selectbox("Select your gender:", ["M", "F"])

    # File uploader for video on the main page
    uploaded_file = st.file_uploader("Choose a video...", type=["mp4", "mov"])

    if uploaded_file is not None:
        # Display uploaded video
        # st.video(uploaded_file)

        # Save the uploaded file to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as temp_file:
            temp_file.write(uploaded_file.getbuffer())
            temp_video_path = temp_file.name

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

        # st.write(features_dict)
        
        Hb_predicted = predict_hb(features_dict)
        # Display uploaded video
        st.pyplot(ppgplot)
        st.write(f"Haemoglobin level: {Hb_predicted:.2f}")

        # Clean up temporary file
        os.remove(temp_video_path)

if __name__ == "__main__":
    main()
